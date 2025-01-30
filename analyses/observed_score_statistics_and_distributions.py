try:
    from analyses import database_utils  # Absolute import (for direct execution)
except ImportError:
    import database_utils  # Relative import (for package context)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

custom_palette = ['#cf4456', '#f29566', '#831c64', '#2f0f3e', '#feedb0']

plt.rcParams['axes.prop_cycle'] = plt.cycler('color', custom_palette)

def get_student_exam_taken_count(exam_scores = None):
    if type(exam_scores) == type(None):
        exam_scores = database_utils.get_exam_scores()
    exam_counts = exam_scores.groupby(by = ["exam_id"])["exam_score"].count()
    print(exam_counts)

def export_observed_score_statistics(exam_scores = None):
    if type(exam_scores) == type(None):
        exam_scores = database_utils.get_exam_scores()

    questions_per_exam = database_utils.get_questions_per_exam()
    mean_series = exam_scores.groupby(by = ["exam_id"])["exam_score"].mean()
    summary_frame = mean_series.to_frame()
    summary_frame = summary_frame.rename(columns={"item_difficulty": "mean"})
    summary_frame["median"] = exam_scores.groupby(by = ["exam_id"])["exam_score"].median()
    summary_frame["std"] = exam_scores.groupby(by = ["exam_id"])["exam_score"].std()
    summary_frame["skewness"] = exam_scores.groupby(by = ["exam_id"])["exam_score"].skew()
    summary_frame["kurtosis"] = exam_scores.groupby(by = ["exam_id"])["exam_score"].apply(pd.Series.kurtosis)
    summary_frame = summary_frame.reset_index()
    summary_frame = summary_frame.rename(columns={"exam_score": "mean"})

    summary_frame = pd.merge(
        left=summary_frame,
        right = questions_per_exam,
        how="left",
        left_on=["exam_id"],
        right_on=["exam_id"],
    )
    summary_frame.to_excel("observed_score_statistics.xlsx", index = False)

def add_os_subplot(exam_scores, axis, bins, exam_keys, title):
    data_list = []
    for key in exam_keys:
        data_list.append(exam_scores[exam_scores["exam_id"].isin([key])]["exam_score_percent"].values)

    # Calculate histogram values for annotations
    hist_values = []
    for data in data_list:
        counts, _ = np.histogram(data, bins=bins)
        hist_values.append(counts)

    # The actual plotting
    n_bins = len(bins) - 1  # Number of bins
    cumulative_counts = np.zeros(n_bins)  # Keep track of where the last bar ended

    bars = axis.hist(data_list, bins, histtype='bar', stacked=True, label=exam_keys)
    text_color = ["black", "black", "white"]
    for i, key in enumerate(exam_keys):  # Iterate through each exam type
        for j, rect in enumerate(bars[2][i]):  # Iterate through each bar in a given exam type
            height = rect.get_height()
            if height >= 20:  # Only add label if bar is visible
                x_center = rect.get_x() + rect.get_width() / 2
                y_center = cumulative_counts[j] + height / 2  # Stack bars
                text_label = f"{height:.2f}"  # Convert count to int for cleaner label
                
                axis.text(x_center, y_center, text_label, ha='center', va='center', 
                          color=text_color[i] if height > np.max(hist_values)/3 else 'black')  # Adjust color
            cumulative_counts[j] += height  # Update cumulative height for next bar

    axis.legend(prop={'size': 10})
    axis.set_xlabel("Exam Score")
    axis.set_ylabel("Number of Students")
    axis.set_title(title)


def save_os_distribution_plots(exam_scores = None, filename = None):
    if type(exam_scores) == type(None):
        exam_scores = database_utils.get_exam_scores()
    if type(filename) == type(None):
        filename = "./figures/observed_scores_distributions.png"
    bins = [0, 0.2, 0.4, 0.6, .8, 1]
    print(exam_scores)
    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(10,6))

    add_os_subplot(exam_scores, ax0, bins, ["1A", "1B"], "Exam 1")
    add_os_subplot(exam_scores, ax1, bins, ["2A", "2B", "2C"], "Exam 2")
    add_os_subplot(exam_scores, ax2, bins, ["3A", "3B", "3C"], "Exam 3")
    add_os_subplot(exam_scores, ax3, bins, ["4A", "4B", "4C"], "Exam 4")

    fig.tight_layout()
    
    try:
        plt.savefig(filename)
    except FileNotFoundError:
        filename = "." + filename
        plt.savefig(filename)
    
    plt.close(fig)

if __name__ == "__main__":
    get_student_exam_taken_count()
    export_observed_score_statistics()
    save_os_distribution_plots()