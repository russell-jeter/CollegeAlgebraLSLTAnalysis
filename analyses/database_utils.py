import pandas as pd
import numpy as np


def load_database_to_dict_of_dfs(df_filename=None):
    """
    Load a dictionary of dataframes from an xlsx file.

    Args:
        df_filename (str, optional): File name of the xlsx file that contains the database.
            Defaults to None, which loads "./data/question_database_schema.xlsx".

    Returns:
        dict[str, pd.DataFrame]: Dictionary where keys are sheet names and values are dataframes.

    Raises:
        ValueError: If the filename does not end with '.xlsx'.
    """
    if df_filename is None:
        df_filename = "./data/question_database_schema.xlsx"

    if ".xlsx" not in df_filename:
        raise ValueError(
            f"The filename {df_filename} was not valid. Please input an xlsx file."
        )

    try:
        dict_of_dfs = pd.read_excel(df_filename, sheet_name=None)
    except FileNotFoundError:
        # Fallback for when running from a different directory (e.g., tests)
        if not df_filename.startswith("."):
            df_filename = "." + df_filename
        dict_of_dfs = pd.read_excel(df_filename, sheet_name=None)

    return dict_of_dfs


def load_all_sheets(df_filename=None):
    """
    Loads specific sheets from the database extended for analyses.

    Args:
        df_filename (str, optional): Path to database file.

    Returns:
        tuple: (raw_df, key_df, options_df, questions_df)
    """
    dict_dfs = load_database_to_dict_of_dfs(df_filename)

    raw_df = dict_dfs.get("student_question_responses", pd.DataFrame())
    key_df = dict_dfs.get("answer_choices", pd.DataFrame())
    options_df = key_df.copy()  # Options usually same as key table structure
    questions_df = dict_dfs.get("questions", pd.DataFrame())

    return raw_df, key_df, options_df, questions_df


def get_completed_answer_choices(dict_of_dfs=None):
    """
    Get a dataframe that details each answer choice for each question.

    Args:
        dict_of_dfs (dict, optional): Dictionary of dataframes. If None, loads from default file.

    Returns:
        pd.DataFrame: DataFrame of answer choices.
    """
    if dict_of_dfs is None:
        dict_of_dfs = load_database_to_dict_of_dfs()

    if "answer_choices" not in dict_of_dfs:
        dict_of_dfs = load_database_to_dict_of_dfs()

    completed_answer_choices = dict_of_dfs["answer_choices"]

    # Convert option_id to a number with index starting at 1.
    if "A" in pd.unique(completed_answer_choices["option_id"]):
        completed_answer_choices = completed_answer_choices.copy()
        completed_answer_choices["option_id"] = [
            ord(letter) - 64 for letter in completed_answer_choices["option_id"]
        ]

    # Omit the first answer choice from the final exam version check questions
    # Exam 4 questions start with 4A01, 4B01, 4C01 which are version checks
    completed_answer_choices = completed_answer_choices[
        ~completed_answer_choices["question_id"].isin(["4A01", "4B01", "4C01"])
    ]

    return completed_answer_choices


def get_student_responses(dict_of_dfs=None):
    """
    Get a dataframe of student responses for all valid exam questions.

    Args:
        dict_of_dfs (dict, optional): Dictionary of dataframes. If None, loads from default file.

    Returns:
        pd.DataFrame: Dataframe of student responses to exams.
    """
    if dict_of_dfs is None:
        dict_of_dfs = load_database_to_dict_of_dfs()

    if "student_question_responses" not in dict_of_dfs:
        dict_of_dfs = load_database_to_dict_of_dfs()

    completed_answer_choices = get_completed_answer_choices(dict_of_dfs)
    student_responses = dict_of_dfs["student_question_responses"]

    # Filter for valid questions only
    student_responses = student_responses[
        student_responses["question_id"].isin(
            pd.unique(completed_answer_choices["question_id"])
        )
    ]

    return student_responses


def get_student_responses_with_details(dict_of_dfs=None):
    """
    Get a dataframe of student responses with details about the distractors.

    Args:
        dict_of_dfs (dict, optional): Dictionary of dataframes. If None, loads from default file.

    Returns:
        pd.DataFrame: Student responses joined with answer choice details.
    """
    completed_answer_choices = get_completed_answer_choices(dict_of_dfs)
    student_responses = get_student_responses(dict_of_dfs)

    student_responses_with_details = pd.merge(
        left=student_responses,
        right=completed_answer_choices,
        how="left",
        left_on=["question_id", "selected_option"],
        right_on=["question_id", "option_id"],
    )
    return student_responses_with_details


def get_questions_per_exam(completed_answer_choices=None):
    """
    Get the count of questions per exam.

    Args:
        completed_answer_choices (pd.DataFrame, optional): Dataframe of answer choices.

    Returns:
        pd.DataFrame: with "exam_id" and "number_of_questions".
    """
    if completed_answer_choices is None:
        completed_answer_choices = get_completed_answer_choices()

    question_list = pd.unique(completed_answer_choices["question_id"])
    question_frame = pd.DataFrame(data=question_list, columns=["question_id"])
    question_frame["exam_id"] = question_frame["question_id"].str[0:2]

    question_counts = (
        question_frame.groupby(by=["exam_id"])["question_id"].count().reset_index()
    )
    question_counts = question_counts.rename(
        columns={"question_id": "number_of_questions"}
    )
    return question_counts


def get_exam_scores(student_responses_with_details=None):
    """
    Calculate exam scores for each student.

    Args:
        student_responses_with_details (pd.DataFrame, optional): DataFrame with student responses.

    Returns:
        pd.DataFrame: DataFrame with "exam_id", "student_id", "exam_score", "exam_score_percent".
    """
    if student_responses_with_details is None:
        student_responses_with_details = get_student_responses_with_details()

    questions_per_exam = get_questions_per_exam()

    # Work on a copy to avoid SettingWithCopyWarning
    student_score_frame = student_responses_with_details[
        ["question_id", "student_id", "is_distractor"]
    ].copy()
    student_score_frame["exam_id"] = student_score_frame["question_id"].str[:2]

    # 1 point if not a distractor (is_distractor == 0)
    student_score_frame["question_score"] = (
        student_score_frame["is_distractor"] == 0
    ).astype(int)
    student_score_frame = student_score_frame.drop(columns=["is_distractor"])

    # Get total score per student per exam
    grouped_scores = (
        student_score_frame.groupby(["student_id", "exam_id"])["question_score"]
        .sum()
        .reset_index()
    )
    grouped_scores = grouped_scores.rename(columns={"question_score": "exam_score"})

    # Merge with questions_per_exam to calculate percentage
    exam_scores = pd.merge(grouped_scores, questions_per_exam, on="exam_id", how="left")
    exam_scores["exam_score_percent"] = (
        exam_scores["exam_score"] / exam_scores["number_of_questions"]
    )

    return exam_scores[["exam_id", "student_id", "exam_score", "exam_score_percent"]]


if __name__ == "__main__":
    print(load_database_to_dict_of_dfs().keys())
