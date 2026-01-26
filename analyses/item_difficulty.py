try:
    from analyses import database_utils  # Absolute import (for direct execution)
    from analyses.effective_distractors_analysis import get_distractor_counts_frame
except ImportError:
    import database_utils  # Relative import (for package context)
    from effective_distractors_analysis import get_distractor_counts_frame

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Color palette for plots
CUSTOM_PALETTE = ['#cf4456', '#f29566', '#831c64', '#2f0f3e', '#feedb0']
plt.rcParams['axes.prop_cycle'] = plt.cycler('color', CUSTOM_PALETTE)


def get_distractor_counts_frame_wrapper():
    """Wrapper to get distractor counts frame, handling import context."""
    return get_distractor_counts_frame()


def get_item_difficulty_frame():
    """
    Get a dataframe containing item difficulty statistics.
    Item difficulty is defined here as the percent of students who selected the correct answer (is_distractor == 0).
    """
    distractor_selection_counts = get_distractor_counts_frame_wrapper()
    
    # Filter for correct answers
    item_difficulty_frame = distractor_selection_counts[distractor_selection_counts["is_distractor"] == 0].copy()

    item_difficulty_frame = item_difficulty_frame[["question_id", "exam_id", "count", "percent"]]
    item_difficulty_frame = item_difficulty_frame.rename(columns={"percent": "item_difficulty"})

    return item_difficulty_frame


def get_student_score_frame(student_responses_with_details=None):
    """
    Get a dataframe of student scores (0 or 1) per question.
    """
    if student_responses_with_details is None:
        student_responses_with_details = database_utils.get_student_responses_with_details()

    student_score_frame = student_responses_with_details[["question_id", "student_id", "is_distractor"]].copy()
    student_score_frame["exam_id"] = student_score_frame["question_id"].str[:2]
    
    # 1 if correct (is_distractor == 0)
    student_score_frame["question_score"] = (student_score_frame["is_distractor"] == 0).astype(int)
    student_score_frame = student_score_frame.drop(columns=["is_distractor"])
    
    # Calculate exam totals for each student
    # Group by student_id and exam_id to sum scores
    exam_totals = student_score_frame.groupby(["student_id", "exam_id"])["question_score"].sum().reset_index()
    exam_totals = exam_totals.rename(columns={"question_score": "total_exam_score"})
    
    # Merge totals back to the main frame
    student_score_frame = pd.merge(student_score_frame, exam_totals, on=["student_id", "exam_id"], how="left")
    
    # Calculate exam score MINUS the current question score (part-whole correction often used in PBC)
    student_score_frame["exam_score"] = student_score_frame["total_exam_score"] - student_score_frame["question_score"]
    
    # Drop the temporary total column if not needed, or keep it. 
    # 'exam_score' is the adjusted score.
    student_score_frame = student_score_frame.drop(columns=["total_exam_score"])

    return student_score_frame


def get_point_biserial_coefficient_frame(student_score_frame=None):
    """
    Calculate Point-Biserial Correlation (PBC) for each question.
    Also calculates dynamic thresholds for 'poor' vs 'good' correlation based on exam size.
    """
    if student_score_frame is None:
        student_score_frame = get_student_score_frame()

    # Calculate correlation between question score (0/1) and adjusted exam score
    point_biserial_correlation_frame = student_score_frame.groupby("question_id")[["question_score", "exam_score"]].corr()
    
    # The corr() result has a multi-index. We extract the relevant correlation.
    # Structure is question_id -> (question_score, exam_score) x (question_score, exam_score)
    # We want corr(question_score, exam_score)
    
    point_biserial_correlation_frame = point_biserial_correlation_frame.reset_index()
    
    # Filter for the row where we correlate question_score with exam_score
    # We can select level_1 == 'exam_score' and look at 'question_score' column or vice versa.
    # Standardizing:
    point_biserial_correlation_frame = point_biserial_correlation_frame[
        point_biserial_correlation_frame["level_1"] == "exam_score"
    ].copy()
    
    point_biserial_correlation_frame = point_biserial_correlation_frame.rename(columns={"question_score": "pbc"})
    point_biserial_correlation_frame = point_biserial_correlation_frame[["question_id", "pbc"]]
    point_biserial_correlation_frame["exam_id"] = point_biserial_correlation_frame["question_id"].str[0:2]

    # Calculate p_value (mean score / difficulty) for each question
    question_stats = student_score_frame.groupby("question_id")["question_score"].mean().reset_index()
    question_stats = question_stats.rename(columns={"question_score": "p_value"})
    
    point_biserial_correlation_frame = pd.merge(point_biserial_correlation_frame, question_stats, on="question_id", how="left")

    # Calculate thresholds per exam
    # 3 bound scenarios logic preserved
        # A: poor_threshold = 1/sqrt(k), good_threshold = 2/sqrt(n-3) when 4k+3 >= n
        # B: poor_threshold = 2/sqrt(n-3), good_threshold = 1/sqrt(k) when 4k+3 < n < 9k+3
        # C: poor_threshold = 1/sqrt(k) - 1/sqrt(n-3), good_threshold = 1/sqrt(k) when n >= 9k+3
    
    # Get exam stats: number of questions (k) and number of students (n)
    exam_stats = student_score_frame.groupby("exam_id").agg(
        k=("question_id", "nunique"),
        n=("student_id", "nunique")
    ).reset_index()
    
    # Vectorized calculation of thresholds
    exam_stats["term_k"] = 1 / np.sqrt(exam_stats["k"])
    exam_stats["term_n"] = 2 / np.sqrt(exam_stats["n"] - 3)
    exam_stats["term_n_half"] = 1 / np.sqrt(exam_stats["n"] - 3) # used in scenario C
    
    exam_stats["scenario"] = "B" # Default
    
    # Scenario A: 4k + 3 >= n
    mask_A = (4 * exam_stats["k"] + 3) >= exam_stats["n"]
    exam_stats.loc[mask_A, "scenario"] = "A"
    exam_stats.loc[mask_A, "poor_threshold"] = exam_stats.loc[mask_A, "term_k"]
    exam_stats.loc[mask_A, "good_threshold"] = exam_stats.loc[mask_A, "term_n"]
    
    # Scenario C: 9k + 3 <= n
    mask_C = (9 * exam_stats["k"] + 3) <= exam_stats["n"]
    exam_stats.loc[mask_C, "scenario"] = "C"
    exam_stats.loc[mask_C, "poor_threshold"] = exam_stats.loc[mask_C, "term_k"] - exam_stats.loc[mask_C, "term_n_half"]
    exam_stats.loc[mask_C, "good_threshold"] = exam_stats.loc[mask_C, "term_k"]
    
    # Scenario B (remainder)
    mask_B = (~mask_A) & (~mask_C)
    exam_stats.loc[mask_B, "poor_threshold"] = exam_stats.loc[mask_B, "term_n"]
    exam_stats.loc[mask_B, "good_threshold"] = exam_stats.loc[mask_B, "term_k"]
    
    # Merge thresholds back to main frame
    point_biserial_correlation_frame = pd.merge(
        point_biserial_correlation_frame, 
        exam_stats[["exam_id", "poor_threshold", "good_threshold"]], 
        on="exam_id", 
        how="left"
    )

    return point_biserial_correlation_frame


def show_item_difficulty_statistics(item_difficulty_frame=None):
    """Print statistics about item difficulty."""
    if item_difficulty_frame is None:
        item_difficulty_frame = get_item_difficulty_frame()
        
    mean_series = item_difficulty_frame.groupby(by=["exam_id"])["item_difficulty"].mean()
    summary_frame = mean_series.to_frame()
    summary_frame = summary_frame.rename(columns={"item_difficulty": "mean"})
    summary_frame["median"] = item_difficulty_frame.groupby(by=["exam_id"])["item_difficulty"].median()
    summary_frame["std"] = item_difficulty_frame.groupby(by=["exam_id"])["item_difficulty"].std()
    summary_frame["skewness"] = item_difficulty_frame.groupby(by=["exam_id"])["item_difficulty"].skew()
    summary_frame["kurtosis"] = item_difficulty_frame.groupby(by=["exam_id"])["item_difficulty"].apply(pd.Series.kurtosis)
    print(summary_frame)


def add_item_difficulty_subplot(item_difficulty_frame, axis, bins, exam_keys, title):
    data_list = []
    for key in exam_keys:
        data_list.append(item_difficulty_frame[item_difficulty_frame["exam_id"].isin([key])]["item_difficulty"].values)
    axis.hist(data_list, bins, histtype='bar', stacked=True, label=exam_keys)
    axis.legend(prop={'size': 10})
    axis.set_xlabel("Item Difficulty")
    axis.set_ylabel("Number of Questions")
    axis.set_title(title)


def save_item_difficulty_distributions(item_difficulty_frame=None, filename=None):
    if item_difficulty_frame is None:
        item_difficulty_frame = get_item_difficulty_frame()
    if filename is None:
        filename = "./figures/item_difficulty_distributions.png"
    bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(10,6))

    add_item_difficulty_subplot(item_difficulty_frame, ax0, bins, ["1A", "1B"], "Exam 1")
    add_item_difficulty_subplot(item_difficulty_frame, ax1, bins, ["2A", "2B", "2C"], "Exam 2")
    add_item_difficulty_subplot(item_difficulty_frame, ax2, bins, ["3A", "3B", "3C"], "Exam 3")
    add_item_difficulty_subplot(item_difficulty_frame, ax3, bins, ["4A", "4B", "4C"], "Exam 4")

    fig.tight_layout()
    try:
        plt.savefig(filename)
    except FileNotFoundError:
        if not filename.startswith("."):
            filename = "." + filename
        plt.savefig(filename)
        
    plt.close(fig)


def add_pbc_subplot_with_dynamic_threshold(point_biserial_correlation_frame, axis, exam_keys, title):
    labels = ["Poor", "Acceptable", "Good"]
    text_color = ["black", "black", "white"]
    bar_bottoms = [0, 0, 0]
    bar_count = 0
    
    for key in exam_keys:
        exam_bar_data = []
        exam_pbc_values = point_biserial_correlation_frame[point_biserial_correlation_frame["exam_id"].isin([key])]
        
        # Count based on thresholds per row (though thresholds are constant per exam, so constant per key)
        # The loop `for key in exam_keys` creates separate layers in the stacked bar.
        # So `key` is a single exam_id (e.g. "1A").
        
        # Grab thresholds from the first row of this exam (since they are constant for the exam)
        if exam_pbc_values.empty:
             continue
             
        # Count categories
        count_poor = len(exam_pbc_values[exam_pbc_values["pbc"] <= exam_pbc_values["poor_threshold"]])
        count_good = len(exam_pbc_values[exam_pbc_values["pbc"] >= exam_pbc_values["good_threshold"]])
        count_acceptable = len(exam_pbc_values) - count_poor - count_good
        
        exam_bar_data = [count_poor, count_acceptable, count_good]
        
        total = np.sum(exam_bar_data)
        if total > 0:
            exam_bar_data = np.array(exam_bar_data) / total * 100
        else:
            exam_bar_data = np.array([0, 0, 0])
            
        axis.bar(labels, exam_bar_data, label=key, bottom=bar_bottoms)
        
        for i in range(len(bar_bottoms)):
            bar_bottoms[i] += exam_bar_data[i]
            
        for j in range(len(exam_bar_data)):
            y_position = (bar_bottoms[j] - exam_bar_data[j]/2)
            if exam_bar_data[j] >= 25:
                # Cycle text color if needed
                # bar_count increments per key (exam)
                color = text_color[bar_count % len(text_color)] 
                axis.text(labels[j], y_position, f"{exam_bar_data[j]:.2f}", 
                          color=color, ha='center', va='bottom', fontsize=10)
        bar_count += 1
    
    axis.legend(prop={'size': 10})
    axis.set_xlabel("Point-Biserial Correlation Category")
    axis.set_ylabel("Percent Questions")
    axis.set_title(title)


def save_pbc_distribution_plots_with_thresholds(point_biserial_correlation_frame=None, filename=None):
    if point_biserial_correlation_frame is None:
        point_biserial_correlation_frame = get_point_biserial_coefficient_frame()
    if filename is None:
        filename = "./figures/pbc_distributions_dynamic_thresholds.png"

    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(10,6))

    add_pbc_subplot_with_dynamic_threshold(point_biserial_correlation_frame, ax0, ["1A", "1B"], "Exam 1")
    add_pbc_subplot_with_dynamic_threshold(point_biserial_correlation_frame, ax1, ["2A", "2B", "2C"], "Exam 2")
    add_pbc_subplot_with_dynamic_threshold(point_biserial_correlation_frame, ax2, ["3A", "3B", "3C"], "Exam 3")
    add_pbc_subplot_with_dynamic_threshold(point_biserial_correlation_frame, ax3, ["4A", "4B", "4C"], "Exam 4")

    fig.tight_layout()
    
    try:
        plt.savefig(filename)
    except FileNotFoundError:
        if not filename.startswith("."):
            filename = "." + filename
        plt.savefig(filename)
    
    plt.close(fig)


def add_pbc_subplot(point_biserial_correlation_frame, axis, bins, exam_keys, title):
    data_list = []
    for key in exam_keys:
        val = point_biserial_correlation_frame[point_biserial_correlation_frame["exam_id"].isin([key])]["pbc"].values
        data_list.append(val)
    axis.hist(data_list, bins, histtype='bar', stacked=True, label=exam_keys)
    axis.legend(prop={'size': 10})
    axis.set_xlabel("Point-Biserial Correlation")
    axis.set_ylabel("Number of Questions")
    axis.set_title(title)


def save_pbc_distribution_plots(point_biserial_correlation_frame=None, filename=None):
    if point_biserial_correlation_frame is None:
        point_biserial_correlation_frame = get_point_biserial_coefficient_frame()
    if filename is None:
        filename = "./figures/pbc_distributions.png"
    bins = [-.5, -.25, 0, 0.25, 0.5, 0.75, 1]

    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(10,6))

    add_pbc_subplot(point_biserial_correlation_frame, ax0, bins, ["1A", "1B"], "Exam 1")
    add_pbc_subplot(point_biserial_correlation_frame, ax1, bins, ["2A", "2B", "2C"], "Exam 2")
    add_pbc_subplot(point_biserial_correlation_frame, ax2, bins, ["3A", "3B", "3C"], "Exam 3")
    add_pbc_subplot(point_biserial_correlation_frame, ax3, bins, ["4A", "4B", "4C"], "Exam 4")

    fig.tight_layout()
    try:
        plt.savefig(filename)
    except FileNotFoundError:
        if not filename.startswith("."):
            filename = "." + filename
        plt.savefig(filename)
    
    plt.close(fig)


def show_pbc_ranges(point_biserial_correlation_frame=None, use_arbitrary_binning=False):
    """
    Print PBC range distribution.
    """
    if point_biserial_correlation_frame is None:
        point_biserial_correlation_frame = get_point_biserial_coefficient_frame()

    if use_arbitrary_binning:
        pbc_bins = [0, 0.15, 0.25, 1]
        exam_ids = np.unique(point_biserial_correlation_frame["exam_id"])
        dict_list = []

        # Initialize list of dicts for bins
        for i in range(len(pbc_bins) + 1):
            new_dict = dict()
            for exam_id in exam_ids:
                new_dict[exam_id] = 0
            dict_list.append(new_dict)

        for exam_id in exam_ids:
            # digitize returns indices of bins
            pbc_bin_assignment = np.digitize(
                point_biserial_correlation_frame[point_biserial_correlation_frame["exam_id"].isin([exam_id])]["pbc"], 
                pbc_bins, 
                right=False
            )
            unique, counts = np.unique(pbc_bin_assignment, return_counts=True)
            
            for i in range(len(unique)):
                # unique[i] is the bin index
                if unique[i] < len(dict_list):
                     dict_list[unique[i]][exam_id] = float(counts[i])/sum(counts)
        
        df = pd.DataFrame(dict_list)
        print(df)
        df.to_excel("pbc_ranges.xlsx")


if __name__ == "__main__":
    #print(get_item_difficulty_frame())
    #save_item_difficulty_distributions()
    #print(get_student_score_frame())
    #print(get_point_biserial_coefficient_frame())
    #save_pbc_distribution_plots()
    #show_pbc_ranges(point_biserial_correlation_frame=None, use_arbitrary_binning=True)
    save_pbc_distribution_plots_with_thresholds()