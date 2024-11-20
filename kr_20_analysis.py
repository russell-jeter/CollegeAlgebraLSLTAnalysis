import numpy as np
import pandas as pd
import database_utils

def get_kr_20_frame(student_responses_with_details = None):
    if type(student_responses_with_details) == type(None):
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
            student_score_frame.loc[student_score_frame_for_one_exam.index.values, "exam_score"] = student_score_frame_for_one_exam["question_score"].sum()
    
    exam_scores = student_score_frame[["exam_id", "student_id", "exam_score"]].copy()
    exam_scores = exam_scores.groupby(by = ["exam_id", "student_id"]).mean().reset_index()

    question_id_list = np.unique(student_score_frame["question_id"].values)

    kr_frame = pd.DataFrame(columns=["K", "r", "variance", "exam_id"])
    kr_frame["exam_id"] = np.unique(exam_scores["exam_id"].values)

    for index, row in kr_frame.iterrows():
        exam_id = row["exam_id"]
        exam_score_variance = 0
        exam_score_frame = exam_scores[exam_scores["exam_id"].isin([exam_id])]
        exam_score_variance = exam_score_frame["exam_score"].var()
        number_of_questions = sum(exam_id in string for string in question_id_list)
        kr_frame.loc[index, "variance"] = exam_score_variance
        kr_frame.loc[index, "K"] = number_of_questions

    return kr_frame

if __name__ == "__main__":
    print(get_kr_20_frame())