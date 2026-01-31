try:
    from analyses import database_utils
except ImportError:
    import database_utils

import pandas as pd


def show_question_counts(student_responses_with_details=None):
    """
    Print a summary of question counts and student performance.

    Args:
        student_responses_with_details (pd.DataFrame, optional): DataFrame of student responses.
            If None, fetches from database.
    """
    if student_responses_with_details is None:
        student_responses_with_details = (
            database_utils.get_student_responses_with_details()
        )

    # Assuming 'is_distractor' is 0 or 1 (or 0.0 - 1.0), < 0.5 is correct, > 0.5 is distractor.
    distractor_mask = student_responses_with_details["is_distractor"] > 0.5
    correct_mask = student_responses_with_details["is_distractor"] < 0.5

    number_of_distractors_chosen = len(student_responses_with_details[distractor_mask])
    number_of_correct_answers_chosen = len(student_responses_with_details[correct_mask])
    number_of_questions = len(student_responses_with_details)

    print(
        f"Number of questions: {number_of_questions}.\n"
        f"Number of correct answers chosen: {number_of_correct_answers_chosen}.\n"
        f"Number of distractors chosen: {number_of_distractors_chosen}"
    )


def show_exam_question_distractor_counts(dict_of_dfs=None):
    """
    Print a summary of distractor selection counts by question_id (distractor type).

    Args:
        dict_of_dfs (dict, optional): Dictionary of dataframes. If None, loads from default file.
    """
    if dict_of_dfs is None:
        dict_of_dfs = database_utils.load_database_to_dict_of_dfs()

    completed_answer_choices = database_utils.get_completed_answer_choices(dict_of_dfs)

    # Group by distractor_type to count occurrences
    exam_question_distractor_count_frame = (
        completed_answer_choices.groupby(by="distractor_type")["question_id"]
        .count()
        .reset_index()
        .rename(columns={"question_id": "count", "distractor_type": "distractor_id"})
    )

    if "distractor_type" in dict_of_dfs:
        exam_question_distractor_count_frame = pd.merge(
            left=exam_question_distractor_count_frame,
            right=dict_of_dfs["distractor_type"],
            how="left",
            left_on=["distractor_id"],
            right_on=["distractor_id"],
        )

    total_count = exam_question_distractor_count_frame["count"].sum()
    if total_count > 0:
        exam_question_distractor_count_frame["percent"] = (
            exam_question_distractor_count_frame["count"] / total_count
        )
    else:
        exam_question_distractor_count_frame["percent"] = 0.0

    print("-----------------------------------------")
    print("Exam question distractor counts frame:")
    print(exam_question_distractor_count_frame)


def show_student_distractor_selection_counts(dict_of_dfs=None):
    """
    Print a summary of distractor selection counts by student selection.

    Args:
        dict_of_dfs (dict, optional): Dictionary of dataframes. If None, loads from default file.
    """
    if dict_of_dfs is None:
        dict_of_dfs = database_utils.load_database_to_dict_of_dfs()

    student_responses_with_details = database_utils.get_student_responses_with_details(
        dict_of_dfs
    )

    student_responses_distractor_selection_counts = (
        student_responses_with_details.groupby(by="distractor_type")["question_id"]
        .count()
        .reset_index()
        .rename(columns={"question_id": "count", "distractor_type": "distractor_id"})
    )

    if "distractor_type" in dict_of_dfs:
        student_responses_distractor_selection_counts = pd.merge(
            left=student_responses_distractor_selection_counts,
            right=dict_of_dfs["distractor_type"],
            how="left",
            left_on=["distractor_id"],
            right_on=["distractor_id"],
        )

    total_count = student_responses_distractor_selection_counts["count"].sum()
    if total_count > 0:
        student_responses_distractor_selection_counts["percent"] = (
            student_responses_distractor_selection_counts["count"] / total_count
        )
    else:
        student_responses_distractor_selection_counts["percent"] = 0.0

    print("-----------------------------------------")
    print("Student responses distractor counts frame:")
    print(student_responses_distractor_selection_counts)


if __name__ == "__main__":
    show_question_counts()
    show_exam_question_distractor_counts()
    show_student_distractor_selection_counts()
