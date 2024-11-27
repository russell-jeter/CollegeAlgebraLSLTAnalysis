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