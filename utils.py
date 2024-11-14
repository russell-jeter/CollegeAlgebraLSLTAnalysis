import pandas as pd

def load_database_to_dict_of_dfs(df_filename = None):
    """
    TODO: UPDATE THIS DOCSTRING
    """
    if df_filename == None:
        df_filename = "./data/question_database_schema.xlsx"
    dict_of_dfs = pd.read_excel(df_filename, sheet_name = None)
    return dict_of_dfs

def get_completed_answer_choices(dict_of_dfs = None):
    """
    TODO: UPDATE THIS DOCSTRING
    """
    # Load completed answer choices table from database file.
    if dict_of_dfs == None:
        dict_of_dfs = load_database_to_dict_of_dfs()
    if "answer_choices" not in dict_of_dfs.keys():
        dict_of_dfs = load_database_to_dict_of_dfs()

    completed_answer_choices = dict_of_dfs['answer_choices']

    # Convert option_id to a number with index starting at 1.
    if 'A' in pd.unique(completed_answer_choices['option_id']):
        completed_answer_choices['option_id'] = completed_answer_choices['option_id'] = [ ord(letter) - 64 for letter in completed_answer_choices['option_id'] ]
    
    # Omit the first answer choice from the final exam. It is not a real question
    completed_answer_choices = completed_answer_choices[~completed_answer_choices["question_id"].isin(["4A01", "4B01", "4C01"])]
    
    # Return processed dataframe.
    return completed_answer_choices

def get_student_responses(dict_of_dfs = None):
    """
    Get a dataframe of student responses for all valid exam questions.
    Parameters
    ----------
    dict_of_dfs : Dictionary of dataframes that has the existing frames you want 
        to manipulated, optional
        
        Default: None. If no dictionary is given, the function will load the dictionary
            using the excel database file in the ./data/ directory.

    Returns
    -------
    student_responses : Pandas dataframe of student responses to exams.
        The dataframe has the following fields: 
        question_id, option_id, is_distractor, distractor_type, distractor_learning_objective_understanding, notes.
        TODO: Add description of fields
    """

    # Load completed answer choices table from database file.
    if dict_of_dfs == None:
        dict_of_dfs = load_database_to_dict_of_dfs()
    if "student_responses" not in dict_of_dfs.keys():
        dict_of_dfs = load_database_to_dict_of_dfs()

    completed_answer_choices = get_completed_answer_choices(dict_of_dfs)

    student_responses = dict_of_dfs['answer_choices']

    # Only grab the student responses that are for the questions in the completed answer choices dataframe
    student_responses = student_responses[student_responses['question_id'].isin(pd.unique(completed_answer_choices['question_id']))]
    
    # Return processed dataframe.
    return student_responses

def get_student_responses_with_details(dict_of_dfs = None):
    """
    TODO: UPDATE THIS DOCSTRING
    """
    completed_answer_choices = get_completed_answer_choices(dict_of_dfs)
    student_responses        = get_student_responses(dict_of_dfs)

    student_responses_with_details = pd.merge(
        left=student_responses, 
        right=completed_answer_choices,
        how='left',
        left_on=['question_id', 'selected_option'],
        right_on=['question_id', 'option_id'],
    )
    return student_responses_with_details

if __name__ == "__main__":
    print(get_student_responses())