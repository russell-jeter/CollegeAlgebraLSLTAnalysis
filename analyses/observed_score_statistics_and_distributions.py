try:
    from analyses import database_utils  # Absolute import (for direct execution)
except ImportError:
    import database_utils  # Relative import (for package context)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Color palette for plots
CUSTOM_PALETTE = ['#cf4456', '#f29566', '#831c64', '#2f0f3e', '#feedb0']
plt.rcParams['axes.prop_cycle'] = plt.cycler('color', CUSTOM_PALETTE)


def get_student_exam_taken_count(exam_scores=None):
    """
    Print the count of exams taken by exam_id.

    Args:
        exam_scores (pd.DataFrame, optional): DataFrame of exam scores. 
            If None, fetches from database.
    """
    if exam_scores is None:
        exam_scores = database_utils.get_exam_scores()
    
    exam_counts = exam_scores.groupby(by=["exam_id"])["exam_score"].count()
    print(exam_counts)


def export_observed_score_statistics(exam_scores=None):
    """
    Export observed score statistics (mean, median, std, etc.) to an Excel file.

    Args:
        exam_scores (pd.DataFrame, optional): DataFrame of exam scores.
            If None, fetches from database.
    """
    if exam_scores is None:
        exam_scores = database_utils.get_exam_scores()

    questions_per_exam = database_utils.get_questions_per_exam()
    
    # Calculate statistics
    mean_series = exam_scores.groupby(by=["exam_id"])["exam_score"].mean()
    summary_frame = mean_series.to_frame(name="mean")
    
    summary_frame["median"] = exam_scores.groupby(by=["exam_id"])["exam_score"].median()
    summary_frame["std"] = exam_scores.groupby(by=["exam_id"])["exam_score"].std()
    summary_frame["skewness"] = exam_scores.groupby(by=["exam_id"])["exam_score"].skew()
    summary_frame["kurtosis"] = exam_scores.groupby(by=["exam_id"])["exam_score"].apply(pd.Series.kurtosis)
    
    summary_frame = summary_frame.reset_index()
    
    # Merge with questions count
    summary_frame = pd.merge(
        left=summary_frame,
        right=questions_per_exam,
        how="left",
        left_on=["exam_id"],
        right_on=["exam_id"],
    )
    
    summary_frame.to_excel("observed_score_statistics.xlsx", index=False)


def add_os_subplot(exam_scores, axis, bins, exam_keys, title):
    """
    Helper function to add a histogram subplot of exam scores.

    Args:
        exam_scores (pd.DataFrame): DataFrame of exam scores.
        axis (matplotlib.axes.Axes): The axis to plot on.
        bins (list): List of bin edges.
        exam_keys (list): List of exam IDs (strings) to include in this plot.
        title (str): Title of the subplot.
    """
    data_list = []
    for key in exam_keys:
        # data_list expects array-like
        subset = exam_scores[exam_scores["exam_id"].isin([key])]["exam_score_percent"]
        data_list.append(subset.values)

    # stacked=True creates a stacked histogram
    # returns (n, bins, patches)
    # n is a list of arrays (one for each dataset) representing heights
    # patches is a list of lists of Patch objects (Rectangle)
    counts, _, patches = axis.hist(data_list, bins, histtype='bar', stacked=True, label=exam_keys)
    
    # Text annotation logic
    # We need to calculate the cumulative height to place text correctly in stacked bars
    
    # Flatten counts if single dataset, but here data_list is list of lists, so counts is list of arrays
    # counts structure: [array(bin1_count, bin2_count...), array(...)] corresponding to layers
    
    # Initialize bottom accumulator
    bottoms = np.zeros(len(bins)-1)
    
    text_color = ["black", "black", "white"]

    # Iterate through layers (exams)
    for i, layer_counts in enumerate(counts):
        # Iterate through bins
        for j, count in enumerate(layer_counts):
            height = count
            if height >= 20: # Threshold for showing label
                # Calculate center position
                # bin_edges are bins[j] and bins[j+1]
                x_center = (bins[j] + bins[j+1]) / 2
                y_center = bottoms[j] + height / 2
                
                # Dynamic text color logic
                # Simplification: if bar is tall enough, use contrast color from palette
                
                color = text_color[i % len(text_color)]
                axis.text(x_center, y_center, f"{height:.0f}", ha='center', va='center', color=color)
            
            bottoms[j] += height # Stack up

    axis.legend(prop={'size': 10})
    axis.set_xlabel("Exam Score")
    axis.set_ylabel("Number of Students")
    axis.set_title(title)


def save_os_distribution_plots(exam_scores=None, filename=None):
    """
    Generate and save distribution plots of observed scores.

    Args:
        exam_scores (pd.DataFrame, optional): DataFrame of exam scores.
            If None, fetches from database.
        filename (str, optional): Output filename. 
            Defaults to "./figures/observed_scores_distributions.png".
    """
    if exam_scores is None:
        exam_scores = database_utils.get_exam_scores()
    
    if filename is None:
        filename = "./figures/observed_scores_distributions.png"
        
    bins = [0, 0.2, 0.4, 0.6, .8, 1]
    
    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(10,6))

    add_os_subplot(exam_scores, ax0, bins, ["1A", "1B"], "Exam 1")
    add_os_subplot(exam_scores, ax1, bins, ["2A", "2B", "2C"], "Exam 2")
    add_os_subplot(exam_scores, ax2, bins, ["3A", "3B", "3C"], "Exam 3")
    add_os_subplot(exam_scores, ax3, bins, ["4A", "4B", "4C"], "Exam 4")

    fig.tight_layout()
    
    try:
        plt.savefig(filename)
    except FileNotFoundError:
        # Fallback if directory doesn't exist or running from wrong cwd
        if not filename.startswith("."):
            filename = "." + filename
        plt.savefig(filename)
    
    plt.close(fig)


if __name__ == "__main__":
    # print(database_utils.get_exam_scores())
    # get_student_exam_taken_count()
    # export_observed_score_statistics()
    save_os_distribution_plots()