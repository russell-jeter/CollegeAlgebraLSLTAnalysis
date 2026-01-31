try:
    from analyses import database_utils  # Absolute import (for direct execution)
except ImportError:
    import database_utils  # Relative import (for package context)
    
import numpy as np
import pandas as pd


def get_kr_20_frame(student_responses_with_details = None, exam_scores = None):
    if type(student_responses_with_details) == type(None):
        student_responses_with_details = database_utils.get_student_responses_with_details()

    if type(exam_scores) == type(None):
        exam_scores = database_utils.get_exam_scores(student_responses_with_details)

    question_id_list = np.unique(student_responses_with_details["question_id"].values)

    # student_score_frame for calculating p and q
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
            student_score_frame.loc[student_score_frame_for_one_exam.index.values, "exam_score"] = student_score_frame_for_one_exam["question_score"].sum()

    # question_scores frame for calculating KR-20    
    question_scores = student_score_frame[["exam_id", "question_id"]].copy()
    question_scores = question_scores.groupby(by = ["exam_id", "question_id"]).count().reset_index()
    question_scores["p"] = np.zeros(len(question_scores))
    question_scores["q"] = np.zeros(len(question_scores))
    for index, row in question_scores.iterrows():
        question_id = row["question_id"]
        exam_id = row["exam_id"]
        question_scores_frame = student_score_frame[student_score_frame["question_id"].isin([question_id])]
        p = question_scores_frame["question_score"].sum() / question_scores_frame["question_score"].count()
        q = 1 - p
        question_scores.loc[index, "p"] = p
        question_scores.loc[index, "q"] = q
    
    # Create KR frame
    kr_frame = pd.DataFrame(columns=["K", "r", "variance", "exam_id"])
    kr_frame["exam_id"] = np.unique(exam_scores["exam_id"].values)

    for index, row in kr_frame.iterrows():
        exam_id = row["exam_id"]
        exam_score_variance = 0
        exam_score_frame = exam_scores[exam_scores["exam_id"].isin([exam_id])]
        question_scores_frame = question_scores[question_scores["exam_id"].isin([exam_id])]
        sum_term = (question_scores_frame["p"] * question_scores_frame["q"]).sum()
        
        exam_score_variance = exam_score_frame["exam_score"].var()
        number_of_questions = sum(exam_id in string for string in question_id_list)
        kr_frame.loc[index, "variance"] = exam_score_variance
        kr_frame.loc[index, "K"] = number_of_questions
        kr_frame.loc[index, "r"] = (number_of_questions/(number_of_questions - 1)) * (1 - sum_term/exam_score_variance)

    return kr_frame

if __name__ == "__main__":
    print(get_kr_20_frame())