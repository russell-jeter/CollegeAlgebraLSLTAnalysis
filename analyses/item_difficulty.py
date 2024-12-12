import numpy as np
import pandas as pd

try:
    # Absolute import (for direct execution)
    from analyses import database_utils  
    from analyses.effective_distractors_analysis import get_distractor_counts_frame
except ImportError:
    # Relative import (for package context)
    import database_utils  
    from effective_distractors_analysis import get_distractor_counts_frame


import matplotlib.pyplot as plt

custom_palette = ['#cf4456', '#f29566', '#831c64', '#2f0f3e', '#feedb0']

plt.rcParams['axes.prop_cycle'] = plt.cycler('color', custom_palette)

def add_pbc_subplot(point_biserial_correlation_frame, axis, bins, exam_keys, title):
    data_list = []
    for key in exam_keys:
        data_list.append(point_biserial_correlation_frame[point_biserial_correlation_frame["exam_id"].isin([key])]["pbc"].values)
    axis.hist(data_list, bins, histtype='bar', stacked=True, label=exam_keys)
    axis.legend(prop={'size': 10})
    axis.set_xlabel("Point-Biserial Correlation")
    axis.set_ylabel("Number of Questions")
    axis.set_title(title)

def save_pbc_distribution_plots(point_biserial_correlation_frame = None, filename = None):
    if type(point_biserial_correlation_frame) == type(None):
        point_biserial_correlation_frame = get_point_biserial_coefficient_frame()
    if type(filename) == type(None):
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
        filename = "." + filename
        plt.savefig(filename)
    
    plt.close(fig)

def get_item_difficulty_frame():
    distractor_selection_counts = get_distractor_counts_frame()
    item_difficulty_frame = distractor_selection_counts[distractor_selection_counts["is_distractor"] == 0]

    item_difficulty_frame = item_difficulty_frame[["question_id", "exam_id", "count", "percent"]]
    item_difficulty_frame = item_difficulty_frame.rename(columns = {"percent": "item_difficulty"})

    return item_difficulty_frame

def show_item_difficulty_statistics(item_difficulty_frame = None):
    if type(item_difficulty_frame) == type(None):
        item_difficulty_frame = get_item_difficulty_frame()
    mean_series = item_difficulty_frame.groupby(by = ["exam_id"])["item_difficulty"].mean()
    summary_frame = mean_series.to_frame()
    summary_frame = summary_frame.rename(columns={"item_difficulty": "mean"})
    summary_frame["median"] = item_difficulty_frame.groupby(by = ["exam_id"])["item_difficulty"].median()
    summary_frame["std"] = item_difficulty_frame.groupby(by = ["exam_id"])["item_difficulty"].std()
    summary_frame["skewness"] = item_difficulty_frame.groupby(by = ["exam_id"])["item_difficulty"].skew()
    summary_frame["kurtosis"] = item_difficulty_frame.groupby(by = ["exam_id"])["item_difficulty"].apply(pd.Series.kurtosis)
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

def save_item_difficulty_distributions(item_difficulty_frame = None, filename = None):
    if type(item_difficulty_frame) == type(None):
        item_difficulty_frame = get_item_difficulty_frame()
    if type(filename) == type(None):
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
        filename = "." + filename
        plt.savefig(filename)
        
    plt.close(fig)

def get_student_score_frame(student_responses_with_details = None):
    if type(student_responses_with_details) == type(None):
        student_responses_with_details = database_utils.get_student_responses_with_details()

    student_responses_with_details = database_utils.get_student_responses_with_details()
    student_score_frame = student_responses_with_details[["question_id", "student_id", "is_distractor"]].copy()
    student_score_frame["exam_id"] = student_score_frame["question_id"].str[:2]
    student_score_frame.loc[:, "question_score"] = (student_score_frame.loc[:, "is_distractor"] == 0).astype(int)

    student_score_frame = student_score_frame.drop(columns=["is_distractor"])

    student_score_frame["exam_score"] = student_score_frame.loc[:, "question_score"]

    student_id_list = np.unique(student_score_frame["student_id"].values)

    for student_id in student_id_list:
        student_exam_frame = student_score_frame[student_score_frame["student_id"].isin([student_id])]
        exam_id_list = np.unique(student_exam_frame["exam_id"].values) 
        for exam_id in exam_id_list:
            student_score_frame_for_one_exam =  student_exam_frame[student_exam_frame["exam_id"].isin([exam_id])]
            student_score_frame.loc[student_score_frame_for_one_exam.index.values, "exam_score"] = student_score_frame_for_one_exam["question_score"].sum() - student_score_frame_for_one_exam["question_score"]
    
    return student_score_frame

def get_point_biserial_coefficient_frame(student_score_frame = None):
    if type(student_score_frame) == type(None):
        student_score_frame = get_student_score_frame()

    point_biserial_correlation_frame = student_score_frame.groupby(by = ["question_id"])[["question_score", "exam_score"]].corr()

    point_biserial_correlation_frame = point_biserial_correlation_frame["question_score"].reset_index()
    point_biserial_correlation_frame = point_biserial_correlation_frame[point_biserial_correlation_frame["level_1"] == "exam_score"].drop(columns="level_1")
    point_biserial_correlation_frame = point_biserial_correlation_frame.rename(columns={"question_score": "pbc"})
    point_biserial_correlation_frame["p_value"] = point_biserial_correlation_frame["pbc"]

    for index, row in point_biserial_correlation_frame.iterrows():
        question_id = row["question_id"]
        student_question_response_frame = student_score_frame[student_score_frame["question_id"].isin([question_id])]
        p_value = student_question_response_frame["question_score"].sum()/len(student_question_response_frame)
        point_biserial_correlation_frame.loc[index, "p_value"] = p_value

    point_biserial_correlation_frame["exam_id"] = point_biserial_correlation_frame["question_id"].str[0:2]

    return point_biserial_correlation_frame

def show_pbc_ranges(point_biserial_correlation_frame = None):
    if type(point_biserial_correlation_frame) == type(None):
        point_biserial_correlation_frame = get_point_biserial_coefficient_frame()

    pbc_bins = [0, 0.15, 0.25, 1]
    exam_ids = np.unique(point_biserial_correlation_frame["exam_id"])
    dict_list = []

    for i in range(len(pbc_bins) + 1):
        new_dict = dict()
        for exam_id in exam_ids:
            new_dict[exam_id] = 0
        dict_list.append(new_dict)

    for exam_id in exam_ids:
        
        pbc_bin_assignment = np.digitize(point_biserial_correlation_frame[point_biserial_correlation_frame["exam_id"].isin([exam_id])]["pbc"], pbc_bins, right = False)
        unique, counts = np.unique(pbc_bin_assignment, return_counts=True)
        
        for i in range(len(unique)):
            dict_list[unique[i]][exam_id] = float(counts[i])/sum(counts)
    
    print(pd.DataFrame(dict_list))

    pd.DataFrame(dict_list).to_excel("pbc_ranges.xlsx")

if __name__ == "__main__":
    #print(get_item_difficulty_frame())
    #save_item_difficulty_distributions()
    #print(get_student_score_frame())
    #print(get_point_biserial_coefficient_frame())
    #save_pbc_distribution_plots()
    show_pbc_ranges()