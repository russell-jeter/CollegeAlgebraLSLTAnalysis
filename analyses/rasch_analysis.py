import numpy as np
import pandas as pd
import math
import statistics # Used for statistics.fmean()
import os # Used to define file location at end of ipynb

# Definitions to form 0/1 dataframe with each row being a student and each column being a single exam/version question

# Returns dataframe df with just rows with 'question_id' == num_and_ver
def exam_num_ver_df(num_and_ver, df):
    exam_mask = df.apply(lambda x: x['question_id'].startswith(num_and_ver), axis=1) # Applies lambda function searching for rows (axis=1) with 'question_id' = num_and_ver
    exam_df = df[exam_mask]
    return exam_df

# Reorganizes student responses to a single exam into columns by question_id
def questions_to_columns(df):
    list_of_unique_id_dicts=[] # initalize empty list for future df
    for unique_id in df['student_id'].unique(): # for each student 
        unique_id_df = df[df['student_id'] == unique_id] # reduce df to just the student responses on the exam
        temp_dict={'id': unique_id} # initalize future row as a dict by student id

        question_list = unique_id_df['question_id'].tolist() # list of question_ids for columns
        selection_list = unique_id_df['selected_option'].tolist() # list of student responses by question_id
        
        for index in range(0, len(question_list)):
            temp_dict[question_list[index]]=selection_list[index] # assign student response to each question_id for future row as a dict
        
        list_of_unique_id_dicts.append(temp_dict) # add future row as dict to list for future df

    restructured_df=pd.DataFrame(list_of_unique_id_dicts) # create dataframe based on list of dicts as rows
    restructured_df=restructured_df.set_index('id', drop=True) # set the student ids as the index and drop the old index
    bad_question=['4A01', '4B01', '4C01'] # Exam 4 question 1 is "what version exam do you have" and is omitted from analysis
    for bad_q_label in bad_question: # Removes bad questions from df
        if bad_q_label in restructured_df.keys():
            restructured_df.drop(bad_q_label, axis=1, inplace=True)
    return restructured_df

# Creates a key for the num_and_ver exam to be used for the correct/incorrect matrix
def create_num_ver_key_dict(num_and_ver, key_df):
    exam_key_df = exam_num_ver_df(num_and_ver, key_df) # Takes full key_df and reduces to key_df for just this num_and_ver
    question_ids = exam_key_df['question_id'].tolist() # Creates list of question_ids 

    answer_series=exam_key_df['option_id'].replace({'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5'}) # avoids downcast warning
    answer_series=answer_series.astype(int) # manually forces downcasting
    answers = answer_series.tolist() # list of answers

    key_dict = {} # initalize key dict
    for index in range(0, len(question_ids)):
        key_dict[question_ids[index]] = answers[index] # assign an answer to each question_id
    return key_dict

# Function for df.apply to compare whether a row is the same as another on some subset of the df 
# Used to compare key_dict to a student row
def compare_row_to_dict(row, dict_to_compare):
    return row.eq(pd.Series(dict_to_compare))

# Creates 0/1 df by matching key_dict to each student's response
def true_false_df(df, key_dict):
    tf_df = df.apply(compare_row_to_dict, axis=1, args=(key_dict,)) # axis=1 for row matching, additional args for the key
    return tf_df

# Remove students & questions with 100% scores and 0% scores as these cause issues with ability and difficulty estimates
def remove_issue_scores(df):
    temp_df = df.copy()
    len_of_key = len(df.keys()) # Used to check for total number of questions for exam
    temp_df['score']=temp_df.sum(axis=1) # Column with student's total number of correct responses

    if len_of_key in temp_df['score'].unique(): # If any students got every single question correct
        drop_list_100s=temp_df[temp_df['score'] == len_of_key].index.to_list() # List of indicies for students who scored 100%
        temp_df.drop(drop_list_100s, inplace=True) # Drop rows by indicies
        #print(f'{len(drop_list_100s)} 100% scores were dropped.') 
    if 0 in temp_df['score'].unique(): # If any students got no question correct
        drop_list_0s=temp_df[temp_df['score'] == 0].index.to_list() 
        temp_df.drop(drop_list_0s, inplace=True) # List of indicies for students who scored 0%
        #print(f'{len(drop_list_0s)} 0% scores were dropped.')
    temp_df.drop(['score'], axis=1, inplace=True) # Drop rows by indicies

    question_score_series=temp_df.mean(axis=0) # Series to check for 100% and 0% scores by question (axis=0 for columns)
    
    question_0_score_series=question_score_series.where(question_score_series == 0).dropna() # Returns reduced series where average response to question was 0 (which implies all students got it wrong or omitted)
    if len(question_0_score_series) > 0:
        q0_index_list=question_0_score_series.index.to_list() # List of indicies for questions with scores 0%
        temp_df.drop(q0_index_list, axis=1, inplace=True) # Drop columns by indicies, but column names are now rows of the Series

    question_100_score_series=question_score_series.where(question_score_series == 1).dropna() # Returns reduced series where average response to question was 1 (which implies all students got it right or omitted)
    if len(question_100_score_series) > 0:
        q100_index_list=question_100_score_series.index.to_list() # List of indicies for questions with scores 100%
        temp_df.drop(q100_index_list, axis=1, inplace=True) # Drop columns by indicies, but column names are now rows of the Series

    return temp_df

# Defines list of all exam numbers [character 1] and exam forms [character 2]
def collect_all_exam_numbers_and_forms(df):
    all_question_ids=df['question_id'].tolist()
    all_exam_numbers_and_forms=list(set([x[0:2] for x in all_question_ids])) # list comprehension for first two characters of question_id list, then cast to set for uniqueness, then returned to list
    return all_exam_numbers_and_forms

def create_true_false_for_all_exams(full_df, key_df, all_exam_numbers_and_forms):
    list_of_tf_dfs=[] # initialize future list of true/false dfs for Rasch model
    for exam_num_and_form in all_exam_numbers_and_forms:
        temp_exam_df=exam_num_ver_df(exam_num_and_form, full_df) # temp df based on exam number and form
        temp_exam_responses_df=questions_to_columns(temp_exam_df) # convert to students by row with question_ids as columns
        temp_exam_answer_key=create_num_ver_key_dict(exam_num_and_form, key_df) # create answer key for scoring student responses
        temp_exam_tf_df=true_false_df(temp_exam_responses_df, temp_exam_answer_key).astype(int) # score student responses with answer key
        list_of_tf_dfs.append({'exam_num_and_form': exam_num_and_form, 'true_false_df': temp_exam_tf_df}) # return 0/1 df by name
    return list_of_tf_dfs

# Function for df.apply() to create ability estimate by row
def ability_estimate(row):
    return math.log(row['avg_student_score'] / (1 - row['avg_student_score']))

# Function for df.apply() to create difficulty estimate by column
def difficulty_estimate(col):
    return math.log((1 - col['avg_question_score'] ) / col['avg_question_score'])

# Calculuate ability and difficulty estimates based on 0/1 df
def approximate_ability_and_difficulty(df):
    temp_df=df.copy() # creates a copy just in case 
    temp_df['avg_student_score']=temp_df.mean(axis=1) # mean by row, where mean of 0/1s is overall score on exam
    theta_s=temp_df.apply(ability_estimate, axis=1).tolist() # df.apply returns a single value based on the row, which would be a Series that we convert to list
    temp_df.drop(['avg_student_score'], axis=1, inplace=True) # drop the 'avg_student_score' so a difficulty estimate is not made based on the column

    temp_df.loc['avg_question_score']=temp_df.mean(axis=0) # mean by column, where mean of 0/1s is overall score on question
    beta_i_non_normal=temp_df.apply(difficulty_estimate, axis=0) # df.apply returns a single value based on the column, returns as Series
    # temp_df.drop(['avg_question_score'], inplace=True) # depreciated since df no longer returned
    avg_beta_i=beta_i_non_normal.mean() # calculates average beta_i (difficulty estimate for item i) to normalize
    beta_i=beta_i_non_normal - avg_beta_i # normalizes difficulty estimates
    beta_i_keys=beta_i.keys().tolist() # Question names for dict keys, needed for calc_expected_values function
    return {'beta_i_keys': beta_i_keys, 'beta_i': beta_i, 'theta_s': theta_s} # returns ability and difficulty estimate with question_id keys for future columns

# If error is too large, adjust beta_i and theta_s by sum of error / sum of variance 
def iterate_variable_estimates(variable_estimates_dict, variance_df, residuals_df):
    beta_i=list(variable_estimates_dict['beta_i'])
    theta_s=list(variable_estimates_dict['theta_s'])
    beta_i_keys=list(variable_estimates_dict['beta_i_keys']) # Not used in this function but is returned for new variable_estimates_dict

    new_beta_i=[]
    for beta_index in range(0, len(beta_i)):
        col_names=variance_df.columns.tolist() # Track column names by variance_df (which matches residuals_df) in case questions were thrown out due to 100% or 0%
        temp_key=col_names[beta_index] # question_i associated to beta_i
        residual_col_sum=residuals_df[temp_key].sum() # sum of residuals by column (i)
        variance_col_sum=variance_df[temp_key].sum() # sum of variance by column (i)
        temp_new_beta = beta_i[beta_index] - (residual_col_sum / variance_col_sum) # new estimate is old beta_i - sum of error by column / variance by column
        new_beta_i.append(temp_new_beta) 

    new_theta_s=[]
    for theta_index in range(0, len(theta_s)):
        index_names=variance_df.index.values.tolist() # Uses variance_df indicies in case students were thrown out due to 100% or 0%
        temp_index=index_names[theta_index] # student_s associated with theta_s
        residual_row_sum=residuals_df.loc[temp_index].sum() # sum of residuals by student (s)
        variance_row_sum=variance_df.loc[temp_index].sum() # sum of variance by student (s)
        new_theta = theta_s[theta_index] + (residual_row_sum / variance_row_sum) # new estimate is old theta_s - sum of error by row / variance by row
        new_theta_s.append(new_theta)

    beta_mean=statistics.fmean(new_beta_i) # convert all values to float-type then compute mean, faster than .mean
    new_beta_i=[x-beta_mean for x in new_beta_i] # normalizes difficulty estimates, as before

    return {'beta_i': new_beta_i, 'theta_s': new_theta_s, 'beta_i_keys': beta_i_keys}

# Expected values are the probability of student s answering question i correctly given a student's ability score theta_i and the item's difficulty beta_i
# Matched against student responses (1/0) on exam
def calc_expected_values(variable_estimates_dict):
    beta_i_keys=list(variable_estimates_dict['beta_i_keys'])
    beta_i=list(variable_estimates_dict['beta_i'])
    theta_s=list(variable_estimates_dict['theta_s'])

    list_of_ev_dicts=[]
    # Iterrate by rows, then by columns to create each entry
    for theta_index in range(0, len(theta_s)):
        temp_ev_dict={} # initalize new row for theta_index
        for beta_index in range(0, len(beta_i)): # iterate by column to create row dict
            exp_vars=math.exp(theta_s[theta_index] - beta_i[beta_index]) # Rasch model of 1PL with alpha=1
            temp_ev_dict[beta_i_keys[beta_index]] = exp_vars / (1 + exp_vars) # probability of student s answering question i correctly given a student's ability score theta_i and the item's difficulty beta_i
        list_of_ev_dicts.append(temp_ev_dict) 

    ev_df=pd.DataFrame(list_of_ev_dicts)
    return ev_df

# Calculates variance dataframe for itereate_variable_estimates function
def calc_est_var(df):
    return df.apply(lambda x: x*(1-x)) # variance of binomial distribution is n*p*(1-p), where n=1 for variance of a single (_i)(_s) entry

# function to find sum of squares by row (equal to sum of squares by column)
def calc_sum_sqr_residuals(df):
    temp_series_sum = df.sum(axis=1) # sum by row (axis=1)
    temp_series_sum = temp_series_sum.pow(2) # .pow(n) raises each Series entry to the nth power
    sum_of_sqrs = temp_series_sum.sum() # sum the squares of each Series entry
    return sum_of_sqrs

def build_rasch_model(base_df):
    student_ids=base_df.index.tolist() # Save student_ids to apply at end
    first_iteration=1 # first iteration will approximate ability and difficulty, all others will iterate the variables
    sum_sqr_res=1 # forces while to fail on first iteration and is calculated later
    iteration_num=0 # only used for testing
    while sum_sqr_res > 0.0001: # while sum of errors is "large"
        if first_iteration==1:
            iteration_num=1 # only used for testing
            first_iteration=0 # forces future iterations to iterate on future ability and difficulty estimates
            variable_estimates_dict=approximate_ability_and_difficulty(base_df) # initial ability estimates by student and difficulty estimates by item
        else:
            iteration_num+=1
            variable_estimates_dict=iterate_variable_estimates(variable_estimates_dict, est_var_ex_vals_df, residuals_df) # modifies ability and difficulty estimates by giving more weight to ability and less to difficulty
        expected_values_df=calc_expected_values(variable_estimates_dict) # probability a student s answers question i correctly
        est_var_ex_vals_df=calc_est_var(expected_values_df) # variance of expected values as 1*p*(1-p)
        base_df.index=expected_values_df.index # ensure indicies between base_df and expected_values_df are equal for subtraction of dfs
        residuals_df=base_df-expected_values_df # difference between actual response scores and probability based on student ability and item difficulty
        sum_sqr_res=calc_sum_sqr_residuals(residuals_df) # sum of errors between actual response scores and probability

    fit_df=residuals_df.pow(2)/est_var_ex_vals_df # final normalized error for each expected value
    fit_df.index=student_ids # applies original index of base_df

    var_estimates_students=pd.Series(variable_estimates_dict['theta_s'], index=student_ids) # variance for ability estimates by student
    var_estimates_students.name='var_estimates_students'
    var_estimates_items=pd.Series(variable_estimates_dict['beta_i'], index=variable_estimates_dict['beta_i_keys']) # variance for difficulty estimates by item
    var_estimates_items.name='var_estimates_items'

    # Outfit (Outlier-Sensitivity fit) Unweighted Fit Mean Square
    # Sensitive to "outer" outliers (difficulty and ability far apart)
    outfit_students=fit_df.mean(axis=1) 
    outfit_students.index=student_ids
    outfit_students.name='outfit_students'

    outfit_items=fit_df.mean(axis=0)
    outfit_items.name='outfit_items'

    # Infit (Inlier-Sensitivity fit) Weighted Fit Mean Square
    # Sensitive to "inner" outliers (unexpected performance on items at student difficulty level)
    infit_students=residuals_df.pow(2).sum(axis=1)/est_var_ex_vals_df.sum(axis=1) # Weighted by variance
    infit_students.index=student_ids
    infit_students.name='infit_students'

    infit_items=residuals_df.pow(2).sum(axis=0)/est_var_ex_vals_df.sum(axis=0) # Weighted by variance
    infit_items.name='infit_items'

    rasch_dict={'fit_df': fit_df, 
            'var_estimates_students': var_estimates_students, # returns as Series
            'var_estimates_items': var_estimates_items, # returns as Series
            'outfit_students': outfit_students, # returns as Series
            'outfit_items': outfit_items, # returns as Series
            'infit_students': infit_students, # returns as Series
            'infit_items': infit_items # returns as Series
            }
    return rasch_dict

# Joins list of Series on their index to create DataFrame
def join_series_from_list_on_index(list_of_series):
    list_of_dfs=[pd.DataFrame(series, columns=[series.name]) for series in list_of_series] # convert Series to DataFrame to use df.join()
    if len(list_of_dfs) == 0:
        joined_dfs=pd.DataFrame() # This shouldn't happen but it put just in case
    elif len(list_of_dfs) == 1:
        joined_dfs=list_of_dfs[0] # Single Series was already converted to DataFrame, returning that DataFrame
    else:
        first_df=list_of_dfs.pop(0) # Remove the first df from the list as the base df to join on
        joined_dfs=first_df.join(list_of_dfs, how='inner') # join the rest of the dfs to the first on the shared indicies 
    return joined_dfs

# Create a student and item df based on rasch statistics by column
def build_rasch_dfs(list_of_rasch_dicts):
    list_of_student_dfs=[] # initalize list to be converted to df
    list_of_item_dfs=[] # initalize list to be converted to df
    for rasch_dict in list_of_rasch_dicts:
        student_statistics=['var_estimates_students', 'outfit_students', 'infit_students']
        student_partial_series_list=[rasch_dict[s_key] for s_key in student_statistics] # list of rasch Series statistics on students
        #Append student scores
        student_score_series = rasch_dict['true_false_df'].mean(axis=1)
        student_score_series.name = 'student_exam_score'
        student_partial_series_list.append(student_score_series) 
        temp_student_df=join_series_from_list_on_index(student_partial_series_list) # Joins Series into single df joined on shared indicies

        temp_standard_error=math.sqrt(2/len(temp_student_df)) # standard error to determine outliers as 2 more than fit value of 1

        temp_student_df['is_outfit_outlier']=(temp_student_df['outfit_students'] > 1+2*temp_standard_error) # create 0/1 column to easily sort in Excel
        temp_student_df['is_infit_outlier']=(temp_student_df['infit_students'] > 1+2*temp_standard_error) # create 0/1 column to easily sort in Excel
        temp_student_df=temp_student_df.astype({'is_outfit_outlier': 'int', 'is_infit_outlier': 'int'}) # cast from True/False to 1/0

        list_of_student_dfs.append(temp_student_df) # Add student statistics for specific exam and version to list to be concat later

        item_statistics=['var_estimates_items', 'outfit_items', 'infit_items'] 
        item_partial_series_list=[rasch_dict[i_key] for i_key in item_statistics] # list of rasch Series statistics on items
        temp_item_df=join_series_from_list_on_index(item_partial_series_list) # Joins Series into single df joined on shared indicies


        temp_item_df['is_outfit_outlier']=(temp_item_df['outfit_items'] > 1+2*temp_standard_error) # create 0/1 column to easily sort in Excel
        temp_item_df['is_infit_outlier']=(temp_item_df['infit_items'] > 1+2*temp_standard_error) # create 0/1 column to easily sort in Excel
        temp_item_df=temp_item_df.astype({'is_outfit_outlier': 'int', 'is_infit_outlier': 'int'}) # cast from True/False to 1/0

        list_of_item_dfs.append(temp_item_df) # Add item statistics for specific exam and version to list to be concat later

    rasch_students_df=pd.concat(list_of_student_dfs) # Create single students df for all exams analyzed
    rasch_students_df.index.name='student_id'

    rasch_items_df=pd.concat(list_of_item_dfs) # Create single items df for all exams analyzed
    rasch_items_df.index.name='question_id'
    
    return [rasch_students_df, rasch_items_df]

def get_rasch_students_and_items_frames_as_dict():
    database_filename = "./data/question_database_schema.xlsx"
    try:
        raw_df = pd.read_excel(database_filename, sheet_name="student_question_responses")
        key_df = pd.read_excel(database_filename, sheet_name="answer_choices")
    except FileNotFoundError:
        database_filename = "." + database_filename
        raw_df = pd.read_excel(database_filename, sheet_name="student_question_responses")
        key_df = pd.read_excel(database_filename, sheet_name="answer_choices")
    key_df = key_df[key_df['is_distractor'] == 0] 

    all_exam_numbers_and_forms=collect_all_exam_numbers_and_forms(raw_df) # creates list of exam numbers and forms from df
    list_of_tf_dfs=create_true_false_for_all_exams(raw_df, key_df, all_exam_numbers_and_forms) # creates list of dicts with true/false dataframes based on key_df provided and the exam number+form

    list_of_rasch_dicts=[]
    for exam_dict in list_of_tf_dfs:
        no_error_exam_df=remove_issue_scores(exam_dict['true_false_df']) # removes 0% and 100% from student rows and question columns
        rasch_dict=build_rasch_model(no_error_exam_df) # iterates through until error is effectively 0
        rasch_dict['exam_num_and_form']=exam_dict['exam_num_and_form'] # extract exam number and form from 
        rasch_dict['true_false_df']=exam_dict['true_false_df'] # save originally graded dataframe based on student responses
        list_of_rasch_dicts.append(rasch_dict)

    rasch_students_df, rasch_items_df = build_rasch_dfs(list_of_rasch_dicts)
    return {'rasch_student_df': rasch_students_df, 'rasch_items_df': rasch_items_df}

