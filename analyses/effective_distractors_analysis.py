try:
    from analyses import database_utils  # Absolute import (for direct execution)
except ImportError:
    import database_utils  # Relative import (for package context)

import pandas as pd

def get_distractor_counts_frame(dict_of_dfs = None):
    """
    Get a dataframe of counts for each distractor for each question.

    Parameters
    ----------
    dict_of_dfs : Dictionary of dataframes that has the existing frames you want 
        to manipulated, optional
        
        Default: None. If no dictionary is given, the function will load the dictionary
            using the excel database file in the ./data/ directory.

    Returns
    -------
    distractor_selection_counts : Pandas dataframe of counts for each distractor for each question.

        The dataframe has the following fields:

        question_id  option_id  is_distractor  count   percent exam_id
        TODO: Add description of fields
        TODO: Update columns that are floats to ints.
    """
    if type(dict_of_dfs) == type(None):
        dict_of_dfs = database_utils.load_database_to_dict_of_dfs()

    student_responses_with_details = database_utils.get_student_responses_with_details(dict_of_dfs = dict_of_dfs)
    completed_answer_choices       = database_utils.get_completed_answer_choices(dict_of_dfs=dict_of_dfs)
    
    distractor_selection_counts = student_responses_with_details.groupby(by = ['question_id', 'selected_option']).count()
    distractor_selection_counts = distractor_selection_counts.rename(columns = {"student_id": "count"})["count"].to_frame().reset_index()
    
    distractor_selection_counts = pd.merge(
        left=completed_answer_choices[["question_id", "option_id", "is_distractor"]],
        right = distractor_selection_counts,
        how='left',
        left_on=['question_id', 'option_id'],
        right_on=['question_id', 'selected_option'],
    )
    
    distractor_selection_counts = distractor_selection_counts.drop(columns = ["selected_option"])
    distractor_selection_counts = distractor_selection_counts.fillna(0)
    distractor_selection_counts["percent"] = distractor_selection_counts["count"] 
    distractor_selection_counts["exam_id"] = distractor_selection_counts["question_id"].str[:2]
    question_id_columns = pd.unique(distractor_selection_counts["question_id"].values)

    #Add percent of question answers that a given distractors got.
    for question_id in question_id_columns:
        question_selection_frame = distractor_selection_counts[distractor_selection_counts["question_id"].isin([question_id])]
        question_selection_frame.loc[:, "percent"] = question_selection_frame["count"]/question_selection_frame["count"].sum()
        distractor_selection_counts[distractor_selection_counts["question_id"].isin([question_id])] = question_selection_frame
    
    return distractor_selection_counts

def show_percent_of_distractors_by_form(distractor_selection_counts = None):
    """
    Print summary of distractor selection by exam, including distractor selection 
        counts and percentages for each exam. The categories are:
            never_chosen: selected 0% of the time
            rarely_chosen: selected 0-5% of the time
            sometimes_chosen: selected > 5% of the time
        
    Parameters
    ----------
    distractor_selection_counts: Pandas dataframe of counts for each distractor for each question.

        The dataframe has the following fields:

        question_id  option_id  is_distractor  count   percent exam_id
        
        Default: None. If no dictionary is given, the function will use the 
            function defined in this file to construct the frame.
        
    Returns
    -------
    None. This function prints a dataframe, it does not return a value.
    """
    
    if type(distractor_selection_counts) == type(None):
        distractor_selection_counts = get_distractor_counts_frame()
    
    exam_ids = pd.unique(distractor_selection_counts["exam_id"].values)
    distractors_chosen_list = []
    
    for exam_id in exam_ids:
        exam_distractors_chosen_dict = dict()
        exam_distractors_chosen_dict["exam_id"] = exam_id
        exam_selection_frame = distractor_selection_counts[distractor_selection_counts["exam_id"].isin([exam_id])]
        exam_selection_frame = exam_selection_frame[exam_selection_frame["is_distractor"] == 1]
        exam_distractors_chosen_dict["never_chosen"]      = len(exam_selection_frame[exam_selection_frame["percent"] == 0])
        exam_distractors_chosen_dict["rarely_chosen"]     = len(exam_selection_frame[(exam_selection_frame["percent"] > 0) & (exam_selection_frame["percent"] <= 0.05)])
        exam_distractors_chosen_dict["sometimes_chosen"]  = len(exam_selection_frame[exam_selection_frame["percent"] > 0.05])
        exam_distractors_chosen_dict["total_distractors"] = len(exam_selection_frame)
        distractors_chosen_list.append(exam_distractors_chosen_dict)
    
    exam_distractors_chosen_frame = pd.DataFrame(distractors_chosen_list)
    exam_distractors_chosen_frame["never_chosen_percent"]     = exam_distractors_chosen_frame["never_chosen"] / exam_distractors_chosen_frame["total_distractors"]
    exam_distractors_chosen_frame["rarely_chosen_percent"]    = exam_distractors_chosen_frame["rarely_chosen"] / exam_distractors_chosen_frame["total_distractors"]
    exam_distractors_chosen_frame["sometimes_chosen_percent"] = exam_distractors_chosen_frame["sometimes_chosen"] / exam_distractors_chosen_frame["total_distractors"]

    exam_distractors_chosen_frame["exam_form_id"] = exam_distractors_chosen_frame["exam_id"]
    exam_distractors_chosen_frame["form"] = exam_distractors_chosen_frame["exam_id"].str[1]
    exam_distractors_chosen_frame["exam_id"] = exam_distractors_chosen_frame["exam_id"].str[0]

    print(exam_distractors_chosen_frame)

def create_effective_distractor_counts_list():
    """
        Returns a blank array of zeros equal to the maximum number of answer choices for an item.
    """
    return [0, 0, 0, 0, 0]

def show_effective_distractors_by_form(distractor_selection_counts = None):
    """
    Print summary of the number of effective distractors (Selected > 5% of the time) by form  
        The output is read as follows:
            form_id [% of questions with 0 EDs chosen, % of questions with 1 ED chosen, % of questions with 2 EDs chosen, % of questions with 3 EDs chosen, % of questions with 4 EDs chosen]
        
    Parameters
    ----------
    distractor_selection_counts: Pandas dataframe of counts for each distractor for each question.

        The dataframe has the following fields:

        question_id  option_id  is_distractor  count   percent exam_id
        
        Default: None. If no dictionary is given, the function will use the 
            function defined in this file to construct the frame.

    Returns
    -------
    None. This function prints a dataframe, it does not return a value.
    """
    
    if type(distractor_selection_counts) == type(None):
        distractor_selection_counts = get_distractor_counts_frame()

    question_id_columns = pd.unique(distractor_selection_counts["question_id"].values)

    distractor_selection_counts["is_effective"] = distractor_selection_counts["percent"] > 0.05

    effective_distractor_count_dict = dict()

    for question_id in question_id_columns:
        question_selection_frame = distractor_selection_counts[distractor_selection_counts["question_id"].isin([question_id])]
        question_selection_frame = question_selection_frame[question_selection_frame["is_distractor"] == 1]
        exam_id = question_selection_frame["exam_id"].values[0]
        number_of_effective_distractors = question_selection_frame["is_effective"].sum()
        
        if exam_id not in effective_distractor_count_dict.keys():
            effective_distractor_count_dict[exam_id] = create_effective_distractor_counts_list()
        
        effective_distractor_count_dict[exam_id][number_of_effective_distractors] += 1

    for key in effective_distractor_count_dict.keys():
        list_sum = sum(effective_distractor_count_dict[key])
        
        for i in range(len(effective_distractor_count_dict[key])):
            effective_distractor_count_dict[key][i] = effective_distractor_count_dict[key][i] / list_sum
        
        print(key, effective_distractor_count_dict[key])

if __name__ == "__main__":

    dict_of_dfs = database_utils.load_database_to_dict_of_dfs()
    show_percent_of_distractors_by_form()
    print(get_distractor_counts_frame(dict_of_dfs))
    show_effective_distractors_by_form()
