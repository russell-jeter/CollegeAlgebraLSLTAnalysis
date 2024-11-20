try:
    from analyses import database_utils  # Absolute import (for direct execution)
except ImportError:
    import database_utils  # Relative import (for package context)

import pandas as pd

def show_question_counts(student_responses_with_details = None):
    """
    This function prints a summary of the question counts and students' overall performance.

    Parameters
    ----------
    student_responses_with_details : Pandas dataframe of student responses to exams with details
        about the distractors to the question.

        The dataframe has the following fields:

        question_id, student_id, selected_option, option_id, is_distractor, distractor_type, distractor_learning_objective_understanding, notes.
        
        Default: None. If no dataframe is given, it will be loaded using database_utils.get_student_responses_with_details()

    Returns
    -------
    None. This function prints a summary of the question counts and students' overall performance.
    """
    if type(student_responses_with_details) == type(None):
        student_responses_with_details = database_utils.get_student_responses_with_details()
    number_of_distractors_chosen = len(student_responses_with_details[student_responses_with_details['is_distractor'] > .5])
    number_of_correct_answers_chosen = len(student_responses_with_details[student_responses_with_details['is_distractor'] < .5])
    number_of_questions = len(student_responses_with_details)

    print(f"Number of questions: {number_of_questions}.\nNumber of correct answers chosen: {number_of_correct_answers_chosen}.\nNumber of distractors chosen: {number_of_distractors_chosen}")

def show_exam_question_distractor_counts(dict_of_dfs = None):
    """
    This function prints a summary of the distractor selection counts by question_id.

    Parameters
    ----------
    dict_of_dfs : Dictionary of dataframes that has the existing frames you want 
        to manipulated, optional
        
        Default: None. If no dictionary is given, the function will load the dictionary
            using the excel database file in the ./data/ directory.

    Returns
    -------
    None. This function prints a summary of the distractor selection counts by question_id.
    """
    if type(dict_of_dfs) == type(None):
        dict_of_dfs = database_utils.load_database_to_dict_of_dfs()
    
    completed_answer_choices = database_utils.get_completed_answer_choices(dict_of_dfs)

    exam_question_distractor_count_frame = completed_answer_choices.groupby(by = 'distractor_type').count()["question_id"].reset_index().rename(columns = {"question_id": "count", "distractor_type": "distractor_id"})

    exam_question_distractor_count_frame = pd.merge(
        left=exam_question_distractor_count_frame, 
        right=dict_of_dfs['distractor_type'],
        how='left',
        left_on=['distractor_id'],
        right_on=['distractor_id'],
    )
    exam_question_distractor_count_frame["percent"] = exam_question_distractor_count_frame["count"] / exam_question_distractor_count_frame["count"].sum() 

    print("-----------------------------------------")
    print("Exam question distractor counts frame:")
    print(exam_question_distractor_count_frame)

def show_student_distractor_selection_counts(dict_of_dfs = None):
    """
    This function prints a summary of the distractor selection counts by student_id.

    Parameters
    ----------
    dict_of_dfs : Dictionary of dataframes that has the existing frames you want 
        to manipulated, optional
        
        Default: None. If no dictionary is given, the function will load the dictionary
            using the excel database file in the ./data/ directory.

    Returns
    -------
    None. This function prints a summary of the distractor selection counts by student_id
    """
    if type(dict_of_dfs) == type(None):
        dict_of_dfs = database_utils.load_database_to_dict_of_dfs()
    
    student_responses_with_details = database_utils.get_student_responses_with_details(dict_of_dfs)
    
    student_responses_distractor_selection_counts = student_responses_with_details.groupby(by = 'distractor_type').count()["question_id"].reset_index().rename(columns = {"question_id": "count", "distractor_type": "distractor_id"})
    student_responses_distractor_selection_counts = pd.merge(
        left=student_responses_distractor_selection_counts, 
        right=dict_of_dfs['distractor_type'],
        how='left',
        left_on=['distractor_id'],
        right_on=['distractor_id'],
    )
    student_responses_distractor_selection_counts["percent"] = student_responses_distractor_selection_counts["count"] / student_responses_distractor_selection_counts["count"].sum() 
    print("-----------------------------------------")
    print("Student responses distractor counts frame:")
    print(student_responses_distractor_selection_counts)

if __name__ == "__main__":
    student_responses_with_details = database_utils.get_student_responses_with_details()
    show_question_counts(student_responses_with_details)
    dict_of_dfs = database_utils.load_database_to_dict_of_dfs()
    show_exam_question_distractor_counts(dict_of_dfs)
    show_student_distractor_selection_counts(dict_of_dfs)