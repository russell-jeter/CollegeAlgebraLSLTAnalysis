import utils
import pandas as pd

def show_question_counts(student_responses_with_details):
    number_of_distractors_chosen = len(student_responses_with_details[student_responses_with_details['is_distractor'] > .5])
    number_of_correct_answers_chosen = len(student_responses_with_details[student_responses_with_details['is_distractor'] < .5])
    number_of_questions = len(student_responses_with_details)

    print(f"Number of questions: {number_of_questions}.\nNumber of correct answers chosen: {number_of_correct_answers_chosen}.\nNumber of distractors chosen: {number_of_distractors_chosen}")


if __name__ == "__main__":
    student_responses_with_details = utils.get_student_responses_with_details()
    show_question_counts(student_responses_with_details)