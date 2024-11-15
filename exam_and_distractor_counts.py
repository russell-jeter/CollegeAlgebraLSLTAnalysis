import utils
import pandas as pd

def show_question_counts(student_responses_with_details = None):
    if type(student_responses_with_details) == type(None):
        student_responses_with_details = utils.get_student_responses_with_details()
    number_of_distractors_chosen = len(student_responses_with_details[student_responses_with_details['is_distractor'] > .5])
    number_of_correct_answers_chosen = len(student_responses_with_details[student_responses_with_details['is_distractor'] < .5])
    number_of_questions = len(student_responses_with_details)

    print(f"Number of questions: {number_of_questions}.\nNumber of correct answers chosen: {number_of_correct_answers_chosen}.\nNumber of distractors chosen: {number_of_distractors_chosen}")

def show_exam_question_distractor_counts(dict_of_dfs = None):
    if type(dict_of_dfs) == type(None):
        dict_of_dfs = utils.load_database_to_dict_of_dfs()
    
    completed_answer_choices = utils.get_completed_answer_choices(dict_of_dfs)

    exam_question_distractor_count_frame = completed_answer_choices.groupby(by = 'distractor_type').count()["question_id"].reset_index().rename(columns = {"question_id": "count", "distractor_type": "distractor_id"})

    exam_question_distractor_count_frame = pd.merge(
        left=exam_question_distractor_count_frame, 
        right=dict_of_dfs['distractor_type'],
        how='left',
        left_on=['distractor_id'],
        right_on=['distractor_id'],
    )
    exam_question_distractor_count_frame["percent"] = exam_question_distractor_count_frame["count"] / exam_question_distractor_count_frame["count"].sum() 

    print(exam_question_distractor_count_frame)

if __name__ == "__main__":
    student_responses_with_details = utils.get_student_responses_with_details()
    show_question_counts(student_responses_with_details)
    show_exam_question_distractor_counts()