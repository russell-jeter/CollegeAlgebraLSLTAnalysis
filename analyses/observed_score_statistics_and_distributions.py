try:
    from analyses import database_utils  # Absolute import (for direct execution)
except ImportError:
    import database_utils  # Relative import (for package context)

import pandas as pd

def get_observed_score_frame():
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

if __name__ == "__main__":
    student_responses_with_details = database_utils.get_student_responses_with_details()
    show_question_counts(student_responses_with_details)
    dict_of_dfs = database_utils.load_database_to_dict_of_dfs()
    show_exam_question_distractor_counts(dict_of_dfs)
    show_student_distractor_selection_counts(dict_of_dfs)