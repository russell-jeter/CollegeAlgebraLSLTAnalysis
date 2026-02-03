import pandas as pd
import numpy as np
from analyses import (
    database_utils,
    item_difficulty,
    effective_distractors_analysis,
    rasch_analysis,
)

def get_histogram_df(df, value_col, bins, group_col='exam_id', label_prefix=""):
    """
    Calculates histogram counts for each group in group_col.
    Returns a DataFrame with bins as rows and groups as columns.
    """
    # Create distinct labels for bins
    bin_labels = [f"{bins[i]} - {bins[i+1]}" for i in range(len(bins)-1)]
    
    # Initialize result dictionary with bin labels
    result_data = {"Bin Range": bin_labels}
    
    # Get all unique groups (exams), sorted
    if group_col in df.columns:
        groups = sorted(df[group_col].unique())
    else:
        groups = []

    for group in groups:
        # Filter data for this group
        subset = df[df[group_col] == group]
        data_values = subset[value_col].dropna().values
        
        # Calculate histogram
        counts, _ = np.histogram(data_values, bins=bins)
        
        # Add to result
        col_name = f"{label_prefix}{group}" if label_prefix else str(group)
        result_data[col_name] = counts
        
    return pd.DataFrame(result_data)

def get_pbc_category_df(df, group_col='exam_id'):
    """
    Calculates counts for Poor, Acceptable, Good categories based on dynamic thresholds.
    Matches logic in item_difficulty.py (add_pbc_subplot_with_dynamic_threshold).
    """
    # Categories
    categories = ["Poor", "Acceptable", "Good"]
    result_data = {"Category": categories}
    
    if group_col in df.columns:
        groups = sorted(df[group_col].unique())
    else:
        groups = []

    for group in groups:
        subset = df[df[group_col] == group]
        if subset.empty:
             result_data[group] = [0, 0, 0]
             continue
            
        # Thresholds are likely constant per exam, but safekeeping to row-wise if needed?
        # In item_difficulty.py, it assumes constant per exam key.
        # We can take the first row's thresholds for the group.
        if "poor_threshold" not in subset.columns or "good_threshold" not in subset.columns:
             # Fallback or error?
             # If thresholds missing, cant categorize.
             result_data[group] = [0, 0, 0]
             continue

        poor_thresh = subset["poor_threshold"].iloc[0]
        good_thresh = subset["good_threshold"].iloc[0]
        
        # Count
        count_poor = len(subset[subset["pbc"] <= poor_thresh])
        count_good = len(subset[subset["pbc"] >= good_thresh])
        count_acceptable = len(subset) - count_poor - count_good
        
        result_data[group] = [count_poor, count_acceptable, count_good]

    return pd.DataFrame(result_data)

def get_fit_category_df(df, col_name, group_col='exam_id'):
    """
    Calculates counts for Poor, Acceptable, Good categories for Fit Stats (Infit/Outfit).
    Uses columns like 'is_good_infit_items_1PL', 'is_acceptable_infit_items_1PL', 'is_poor_infit_items_1PL'.
    """
    # Categories
    categories = ["Poor", "Acceptable", "Good"]
    result_data = {"Category": categories}
    
    if group_col in df.columns:
        groups = sorted(df[group_col].unique())
    else:
        groups = []
        
    # Construct base column name for category flags
    # col_name is like 'infit_items_1PL'
    # Flag columns are: 'is_good_infit_items_1PL', etc.
    
    col_good = f"is_good_{col_name}"
    col_acceptable = f"is_acceptable_{col_name}"
    col_poor = f"is_poor_{col_name}"

    for group in groups:
        subset = df[df[group_col] == group]
        if subset.empty:
             result_data[group] = [0, 0, 0]
             continue
        
        # Check if helper columns exist
        if col_good not in subset.columns or col_acceptable not in subset.columns or col_poor not in subset.columns:
             # If flags missing, return zeros or maybe try to calculate? 
             # rasch_analysis.py should have added them.
             result_data[group] = [0, 0, 0]
             continue

        count_poor = subset[col_poor].sum()
        count_acceptable = subset[col_acceptable].sum()
        count_good = subset[col_good].sum()
        
        result_data[group] = [count_poor, count_acceptable, count_good]

    return pd.DataFrame(result_data)

def export_plot_data(filename="./results/plot_data.xlsx"):
    """
    Aggregates data used for all plots and exports it to a multi-sheet Excel file.
    Aggregates into histograms/counts to match the figures.
    """
    print("Gathering data for export...")
    
    # 1. Observed Scores
    print(" - Observed Scores (Histogram)")
    exam_scores = database_utils.get_exam_scores()
    os_bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
    
    os_hist_df = get_histogram_df(exam_scores, "exam_score_percent", os_bins, group_col="exam_id")

    # 2. Item Difficulty
    print(" - Item Difficulty (Histogram)")
    item_difficulty_df = item_difficulty.get_item_difficulty_frame()
    # Bins from item_difficulty.py: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    id_bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    id_hist_df = get_histogram_df(item_difficulty_df, "item_difficulty", id_bins, group_col="exam_id")
    
    # 3. Point-Biserial Correlation (PBC)
    print(" - PBC (Histogram)")
    pbc_df = item_difficulty.get_point_biserial_coefficient_frame()
    pbc_hist_df = get_pbc_category_df(pbc_df)

    # 4. Effective Distractors (Counts per Question & Form)
    print(" - Effective Distractors (Aggregated)")
    # This returns a dictionary of lists: {exam_id: [count_0, count_1, count_2, count_3, count_4]} (normalized percents)
    effective_distractor_counts_dict = effective_distractors_analysis.get_effective_distractors_by_form()
    
    # Convert dict to DataFrame: Rows = 0, 1, 2, 3, 4 effective distractors. Columns = Exams
    # Create empty DF with index
    ed_data = {"Num Effective Distractors": [0, 1, 2, 3, 4]}
    for exam_id, counts in sorted(effective_distractor_counts_dict.items()):
        # counts is list of percents
        ed_data[exam_id] = counts
    
    effective_distractors_df = pd.DataFrame(ed_data)

    # 5. Distractors Chosen (Never/Rarely/Sometimes)
    print(" - Distractors Chosen (Aggregated)")
    distractors_chosen_df = effective_distractors_analysis.get_percent_of_distractors_by_form()
    
    distractors_chosen_export = distractors_chosen_df[[
        "exam_id", "form", 
        "never_chosen_percent",
        "rarely_chosen_percent",
        "sometimes_chosen_percent"
    ]].copy()
    
    # 6. Rasch Analysis
    print(" - Rasch Analysis (Histograms)")
    rasch_dict = rasch_analysis.get_rasch_students_and_items_frames_as_dict()
    rasch_items_df = rasch_dict["rasch_items_df"]
    rasch_students_df = rasch_dict["rasch_student_df"]
    
    # Ensure exam_id exists
    if "exam_id" not in rasch_items_df.columns:
         if rasch_items_df.index.name == "question_id":
             rasch_items_df = rasch_items_df.reset_index()
         if "question_id" in rasch_items_df.columns:
             rasch_items_df["exam_id"] = rasch_items_df["question_id"].str[:2]

    if "exam_id" not in rasch_students_df.columns:
         pass

    # Bins from rasch_analysis.py: [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
    rasch_bins = [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
    
    # We need histograms for 1PL and 3PL, Items and Students
    # Columns in df: var_estimates_items_1PL, var_estimates_students_1PL, etc.
    
    # Items 1PL
    rasch_items_1pl_hist = get_histogram_df(rasch_items_df, "var_estimates_items_1PL", rasch_bins, group_col="exam_id")
    
    # Items 3PL
    rasch_items_3pl_hist = get_histogram_df(rasch_items_df, "var_estimates_items_3PL", rasch_bins, group_col="exam_id")

    # Students 1PL
    rasch_students_1pl_hist = get_histogram_df(rasch_students_df, "var_estimates_students_1PL", rasch_bins, group_col="exam_id")
    
    # Students 3PL
    rasch_students_3pl_hist = get_histogram_df(rasch_students_df, "var_estimates_students_3PL", rasch_bins, group_col="exam_id")

    # Fit Histograms (Infit/Outfit)
    print(" - Fit Statistics (Histograms)")
    fit_bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 3.0]
    
    fit_hist_dfs = {}
    for fit_type in ["infit", "outfit"]:
        for pl in ["1", "3"]:
            col_base = f"{fit_type}_items_{pl}PL"
            hist_df = get_histogram_df(rasch_items_df, col_base, fit_bins, group_col="exam_id")
            fit_hist_dfs[f"{fit_type}_{pl}PL"] = hist_df

    # 7. Item Difficulty Categories (Poor/Acceptable/Ideal)
    print(" - Item Difficulty (Categories)")
    id_cat_df = get_item_difficulty_category_df(item_difficulty_df)

    # 8. Effective Distractor Categories
    print(" - Effective Distractors (Categories)")
    ed_cat_df = effective_distractors_analysis.get_effective_distractor_categories_by_form()

    # 9. Integrated Methodology (Item Summary)
    print(" - Integrated Methodology (Item Summary)")
    import os
    pickle_path = "./results/item_summary.pkl"
    if os.path.exists(pickle_path):
        item_summary_df = pd.read_pickle(pickle_path)
    else:
        # Try to import and generate
        from analyses import item_summary
        item_summary.save_item_summary()
        item_summary_df = pd.read_pickle(pickle_path)

    # Create writer
    print(f"Writing to {filename}...")
    with pd.ExcelWriter(filename) as writer:
        os_hist_df.to_excel(writer, sheet_name="Observed Scores", index=False)
        id_hist_df.to_excel(writer, sheet_name="Item Difficulty", index=False)
        id_cat_df.to_excel(writer, sheet_name="Item Diff Categories", index=False)
        
        pbc_hist_df.to_excel(writer, sheet_name="PBC", index=False)
        effective_distractors_df.to_excel(writer, sheet_name="Effective Distractors", index=False)
        ed_cat_df.to_excel(writer, sheet_name="Eff Distractor Categories")
        
        distractors_chosen_export.to_excel(writer, sheet_name="Distractors Chosen", index=False)
        
        rasch_items_1pl_hist.to_excel(writer, sheet_name="Rasch Items 1PL", index=False)
        rasch_students_1pl_hist.to_excel(writer, sheet_name="Rasch Students 1PL", index=False)
        rasch_items_3pl_hist.to_excel(writer, sheet_name="Rasch Items 3PL", index=False)
        rasch_students_3pl_hist.to_excel(writer, sheet_name="Rasch Students 3PL", index=False)
        
        # Fit Histograms
        fit_hist_dfs["infit_1PL"].to_excel(writer, sheet_name="Hist Infit Items 1PL", index=False)
        fit_hist_dfs["outfit_1PL"].to_excel(writer, sheet_name="Hist Outfit Items 1PL", index=False)
        fit_hist_dfs["infit_3PL"].to_excel(writer, sheet_name="Hist Infit Items 3PL", index=False)
        fit_hist_dfs["outfit_3PL"].to_excel(writer, sheet_name="Hist Outfit Items 3PL", index=False)

        # Fit Stats Categories (Good, Acceptable, Poor)
        # Infit/Outfit Items 1PL
        get_fit_category_df(rasch_items_df, "infit_1PL", group_col="exam_id").to_excel(writer, sheet_name="Infit Items 1PL", index=False)
        get_fit_category_df(rasch_items_df, "outfit_1PL", group_col="exam_id").to_excel(writer, sheet_name="Outfit Items 1PL", index=False)
        
        # Infit/Outfit Items 3PL
        get_fit_category_df(rasch_items_df, "infit_3PL", group_col="exam_id").to_excel(writer, sheet_name="Infit Items 3PL", index=False)
        get_fit_category_df(rasch_items_df, "outfit_3PL", group_col="exam_id").to_excel(writer, sheet_name="Outfit Items 3PL", index=False)
        
        # Infit/Outfit Students 1PL
        get_fit_category_df(rasch_students_df, "infit_1PL", group_col="exam_id").to_excel(writer, sheet_name="Infit Students 1PL", index=False)
        get_fit_category_df(rasch_students_df, "outfit_1PL", group_col="exam_id").to_excel(writer, sheet_name="Outfit Students 1PL", index=False)

        # Infit/Outfit Students 3PL
        get_fit_category_df(rasch_students_df, "infit_3PL", group_col="exam_id").to_excel(writer, sheet_name="Infit Students 3PL", index=False)
        get_fit_category_df(rasch_students_df, "outfit_3PL", group_col="exam_id").to_excel(writer, sheet_name="Outfit Students 3PL", index=False)
        
        # Item Summary
        item_summary_df.to_excel(writer, sheet_name="Item Summary", index=False)

    print("Done.")


def get_item_difficulty_category_df(item_difficulty_frame, group_col='exam_id'):
    """
    Calculates counts for Poor, Acceptable, Ideal categories for Item Difficulty.
    Matches logic in item_difficulty.py (add_difficulty_category_subplot).
    """
    categories = ["Poor", "Acceptable", "Ideal"]
    result_data = {"Category": categories}
    
    if group_col in item_difficulty_frame.columns:
        groups = sorted(item_difficulty_frame[group_col].unique())
    else:
        groups = []
        
    for group in groups:
        subset = item_difficulty_frame[item_difficulty_frame[group_col] == group]
        if subset.empty:
            result_data[group] = [0, 0, 0]
            continue
            
        difficulties = subset["item_difficulty"]
        std_dev = difficulties.std()
        target = 0.74
        
        ideal_count = 0
        acceptable_count = 0
        poor_count = 0
        
        for diff in difficulties:
            deviation = abs(diff - target)
            if deviation <= std_dev:
                ideal_count += 1
            elif deviation <= 2 * std_dev:
                acceptable_count += 1
            else:
                poor_count += 1
                
        result_data[group] = [poor_count, acceptable_count, ideal_count]
        
    return pd.DataFrame(result_data)

if __name__ == "__main__":
    export_plot_data()
