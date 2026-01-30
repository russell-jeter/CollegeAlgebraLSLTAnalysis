try:
    from analyses import database_utils
except ImportError:
    import database_utils

import numpy as np
import pandas as pd


def get_kr_20_frame(student_responses_with_details=None, exam_scores=None):
    """
    Calculate the Kuder-Richardson Formula 20 (KR-20) reliability coefficient for exams.

    Args:
        student_responses_with_details (pd.DataFrame, optional): DataFrame of student responses.
            If None, fetches from database.
        exam_scores (pd.DataFrame, optional): DataFrame of exam scores.
            If None, fetches from database.

    Returns:
        pd.DataFrame: DataFrame containing KR-20 statistics (K, r, variance, exam_id).
    """
    if student_responses_with_details is None:
        student_responses_with_details = (
            database_utils.get_student_responses_with_details()
        )

    if exam_scores is None:
        # Maintaining API compatibility.
        exam_scores = database_utils.get_exam_scores(student_responses_with_details)

    # Prepare student score frame (0 for correct, 1 for distractor -> converted to score)
    # The database says 'is_distractor' == 0 is correct.
    student_score_frame = student_responses_with_details[
        ["question_id", "student_id", "is_distractor"]
    ].copy()
    student_score_frame["exam_id"] = student_score_frame["question_id"].str[:2]

    # Calculate score: 1 if correct (is_distractor == 0), else 0
    student_score_frame["question_score"] = (
        student_score_frame["is_distractor"] == 0
    ).astype(int)
    student_score_frame = student_score_frame.drop(columns=["is_distractor"])

    # Calculate p (proportion correct) and q (proportion incorrect) for each question
    # Group by exam_id and question_id
    question_stats = (
        student_score_frame.groupby(["exam_id", "question_id"])["question_score"]
        .agg(["sum", "count"])
        .reset_index()
    )
    question_stats["p"] = question_stats["sum"] / question_stats["count"]
    question_stats["q"] = 1.0 - question_stats["p"]

    # Calculate pq for each question
    question_stats["pq"] = question_stats["p"] * question_stats["q"]

    # Sum pq per exam
    sum_pq_per_exam = question_stats.groupby("exam_id")["pq"].sum()

    # Calculate K (number of questions) per exam
    k_per_exam = question_stats.groupby("exam_id")["question_id"].count()

    # Calculate exam score variance
    # We can use the pre-calculated exam_scores dataframe
    variance_per_exam = exam_scores.groupby("exam_id")["exam_score"].var()

    # Combine into KR frame
    # We need shared index to compute
    kr_data = pd.DataFrame(
        {"K": k_per_exam, "sum_pq": sum_pq_per_exam, "variance": variance_per_exam}
    )

    # Calculate r (KR-20)
    # formula: (K / (K - 1)) * (1 - (sum(p*q) / variance))
    # Handle division by zero or K=1 if necessary, though typical exams have K > 1

    kr_data["r"] = (kr_data["K"] / (kr_data["K"] - 1)) * (
        1 - (kr_data["sum_pq"] / kr_data["variance"])
    )

    # Format output
    kr_frame = kr_data.reset_index()[["K", "r", "variance", "exam_id"]]

    return kr_frame


if __name__ == "__main__":
    print(get_kr_20_frame())
