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

def export_plot_data(filename="plot_data.xlsx"):
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
    # Bins from item_difficulty.py: [-.5, -.25, 0, 0.25, 0.5, 0.75, 1]
    pbc_bins = [-0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]
    pbc_hist_df = get_histogram_df(pbc_df, "pbc", pbc_bins, group_col="exam_id")

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

    # Create writer
    print(f"Writing to {filename}...")
    with pd.ExcelWriter(filename) as writer:
        os_hist_df.to_excel(writer, sheet_name="Observed Scores", index=False)
        id_hist_df.to_excel(writer, sheet_name="Item Difficulty", index=False)
        pbc_hist_df.to_excel(writer, sheet_name="PBC", index=False)
        effective_distractors_df.to_excel(writer, sheet_name="Effective Distractors", index=False)
        distractors_chosen_export.to_excel(writer, sheet_name="Distractors Chosen", index=False)
        
        rasch_items_1pl_hist.to_excel(writer, sheet_name="Rasch Items 1PL", index=False)
        rasch_students_1pl_hist.to_excel(writer, sheet_name="Rasch Students 1PL", index=False)
        rasch_items_3pl_hist.to_excel(writer, sheet_name="Rasch Items 3PL", index=False)
        rasch_students_3pl_hist.to_excel(writer, sheet_name="Rasch Students 3PL", index=False)

    print("Done.")

if __name__ == "__main__":
    export_plot_data()
