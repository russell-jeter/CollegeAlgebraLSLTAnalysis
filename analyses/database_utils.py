import pandas as pd
import numpy as np

def load_database_to_dict_of_dfs(df_filename = None):
    """
    Load a dictionary of dataframe from an xlsx file.

    Parameters
    ----------
    df_filename : File name of the xlsx file that contains the database you 
        want to load,optional
        
        Default: None. If no filename is given is given, the function will load
            excel database file in the ./data/ directory.

    Returns
    -------
    list of dictionaries
        TODO: Add description of fields
    """
    try: 
        if df_filename == None:
            df_filename = "./data/question_database_schema.xlsx"

        if ".xlsx" not in df_filename:
            raise(f"The filename {df_filename} was not valid. Please input an xlsx file.")
    
        dict_of_dfs = pd.read_excel(df_filename, sheet_name = None)
        
    except FileNotFoundError:
        df_filename = "." + df_filename
        dict_of_dfs = pd.read_excel(df_filename, sheet_name = None)
    
    return dict_of_dfs


def get_completed_answer_choices(dict_of_dfs = None):
    """
    Get a dataframe that details each answer choice for each question.

    Parameters
    ----------
    dict_of_dfs : Dictionary of dataframes that has the existing frames you want 
        to manipulated, optional
        
        Default: None. If no dictionary is given, the function will load the dictionary
            using the excel database file in the ./data/ directory.

    Returns
    -------
    completed_answer_choices : Pandas dataframe of answer choices to each exam question.
        The dataframe has the following fields: 
        question_id, option_id, is_distractor, distractor_type, distractor_learning_objective_understanding, notes.
        TODO: Add description of fields
    """
    # Load completed answer choices table from database file.
    if dict_of_dfs == None:
        dict_of_dfs = load_database_to_dict_of_dfs()
    if "answer_choices" not in dict_of_dfs.keys():
        dict_of_dfs = load_database_to_dict_of_dfs()

    completed_answer_choices = dict_of_dfs["answer_choices"]

    # Convert option_id to a number with index starting at 1.
    if "A" in pd.unique(completed_answer_choices["option_id"]):
        completed_answer_choices["option_id"] = completed_answer_choices["option_id"] = [ ord(letter) - 64 for letter in completed_answer_choices["option_id"] ]
    
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
    if "student_question_responses" not in dict_of_dfs.keys():
        dict_of_dfs = load_database_to_dict_of_dfs()

    completed_answer_choices = get_completed_answer_choices(dict_of_dfs)

    student_responses = dict_of_dfs["student_question_responses"]

    # Only grab the student responses that are for the questions in the completed answer choices dataframe
    student_responses = student_responses[student_responses["question_id"].isin(pd.unique(completed_answer_choices["question_id"]))]
    
    # Return processed dataframe.
    return student_responses

def get_student_responses_with_details(dict_of_dfs = None):
    """
    Get a dataframe of student responses with details about the distractors
      for all valid exam questions.

    Parameters
    ----------
    dict_of_dfs : Dictionary of dataframes that has the existing frames you want 
        to manipulated, optional
        
        Default: None. If no dictionary is given, the function will load the dictionary
            using the excel database file in the ./data/ directory.

    Returns
    -------
    student_responses_with_details : Pandas dataframe of student responses to exams with details
        about the distractors to the question.

        The dataframe has the following fields:

        question_id, student_id, selected_option, option_id, is_distractor, distractor_type, distractor_learning_objective_understanding, notes.
        TODO: Add description of fields
        TODO: Update columns that are floats to ints.
    """
    completed_answer_choices = get_completed_answer_choices(dict_of_dfs)
    student_responses        = get_student_responses(dict_of_dfs)
    student_responses_with_details = pd.merge(
        left=student_responses, 
        right=completed_answer_choices,
        how="left",
        left_on=["question_id", "selected_option"],
        right_on=["question_id", "option_id"],
    )
    return student_responses_with_details

def get_questions_per_exam(completed_answer_choices = None):
    if type(completed_answer_choices) == type(None):
        completed_answer_choices = get_completed_answer_choices()
    question_list = pd.unique(completed_answer_choices["question_id"])
    question_frame = pd.DataFrame(data = question_list, columns=["question_id"])
    question_frame["exam_id"] = question_frame["question_id"].str[0:2]
    question_counts = question_frame.groupby(by = ["exam_id"]).count().reset_index()
    question_counts = question_counts.rename(columns={"question_id": "number_of_questions"})
    return question_counts

def get_exam_scores(student_responses_with_details = None):
    if type(student_responses_with_details) == type(None):
        student_responses_with_details = get_student_responses_with_details()

    questions_per_exam = get_questions_per_exam()
    student_score_frame = student_responses_with_details[["question_id", "student_id", "is_distractor"]].copy()
    student_score_frame["exam_id"] = student_score_frame["question_id"].str[:2]
    student_score_frame.loc[:, "question_score"] = (student_score_frame.loc[:, "is_distractor"] == 0).astype(int)

    student_score_frame = student_score_frame.drop(columns=["is_distractor"])

    student_score_frame["exam_score"] = student_score_frame.loc[:, "question_score"]
    student_score_frame["exam_score_percent"] = student_score_frame.loc[:, "question_score"].astype(float)

    student_id_list = np.unique(student_score_frame["student_id"].values)

    for student_id in student_id_list:
        student_exam_frame = student_score_frame[student_score_frame["student_id"].isin([student_id])]
        exam_id_list = np.unique(student_exam_frame["exam_id"].values) 
        for exam_id in exam_id_list:
            student_score_frame_for_one_exam =  student_exam_frame[student_exam_frame["exam_id"].isin([exam_id])]
            number_of_questions =  questions_per_exam[questions_per_exam["exam_id"].isin([exam_id])]["number_of_questions"].values[0]
            student_score_frame.loc[student_score_frame_for_one_exam.index.values, "exam_score"] = student_score_frame_for_one_exam["question_score"].sum()
            student_score_frame.loc[student_score_frame_for_one_exam.index.values, "exam_score_percent"] = student_score_frame_for_one_exam["question_score"].sum()/number_of_questions
    
    exam_scores = student_score_frame[["exam_id", "student_id", "exam_score", "exam_score_percent"]].copy()
    exam_scores = exam_scores.groupby(by = ["exam_id", "student_id"]).mean().reset_index()
    return exam_scores

if __name__ == "__main__":
    print(get_exam_scores())