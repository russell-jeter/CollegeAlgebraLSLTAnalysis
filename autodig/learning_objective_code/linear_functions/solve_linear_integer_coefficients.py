import random
import numpy as np
import pandas as pd

from utils import commonly_used_functions, interval_masking_method

code_name = "solve_linear_integer_coefficients"

### DEFINITIONS ###
def generate_coefficients():    # Create an array of 6 distinct naturals, then make some integers
    coefficients = [0,0,0,0,0,0]
    OneSolutionCheck = 0
    while (OneSolutionCheck == 0):    # Makes sure there is exactly one solution
        coefficients = random.sample(range(2, 20), 6) # ensures all coefficients are distinct
        coefficients[0] = -coefficients[0] # to ensure a distractor for distribution of negative incorrectly
        coefficients[1] = commonly_used_functions.maybeMakeNegative(coefficients[1])
        coefficients[2] = commonly_used_functions.maybeMakeNegative(coefficients[2])
        coefficients[3] = -coefficients[3] # to ensure a distractor for distribution of negative incorrectly
        coefficients[4] = commonly_used_functions.maybeMakeNegative(coefficients[4])
        coefficients[5] = commonly_used_functions.maybeMakeNegative(coefficients[5])
        OneSolutionCheck = coefficients[0]*coefficients[2] - coefficients[3]*coefficients[4] # checks that the coefficient for resulting linear equation is nonzero
    return coefficients

def generate_solution(coefficients):
    a, b, c, d, e, f = coefficients
    eq1 = np.poly1d([a*b, a*c])
    eq2 = np.poly1d([d*e, d*f])
    basicLinearEquation = eq1 - eq2
    solve_equation = basicLinearEquation.r

    if len(solve_equation) == 0:
        solution = [0]
    else:
        solution = solve_equation[0]
    
    return solution

def generate_all_option_dicts(coefficients):
    a, b, c, d, e, f = coefficients

    solution = generate_solution(coefficients)
    display_solution = round(solution, 3)
    solution_feedback = f"* $x = {display_solution}$, which is the correct option."
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'solution', 
        'Expected solution', 
        solution, 
        display_solution, 
        solution_feedback, 
        1
    )

    distractor_1 = generate_solution([a, b, -c, d, e, f])    
    display_distractor_1 = round(distractor_1, 3)
    distractor_1_feedback = f" $x = {display_distractor_1}$, which corresponds to not distributing the negative in front of the first parentheses correctly."
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_1',
        'Arithmetic error - distribution negative in front of parentheses',
        distractor_1, 
        display_distractor_1, 
        distractor_1_feedback,
        0
    )

    distractor_2 = generate_solution([a, b, c, d, e, -f])
    display_distractor_2 = round(distractor_2, 3)
    distractor_2_feedback = f" $x = {display_distractor_2}$, which corresponds to not distributing the negative in front of the second parentheses correctly." 
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2', 
        'Arithmetic error - distribution negative in front of parentheses',
        distractor_2,
        display_distractor_2,
        distractor_2_feedback, 
        0
    )

    distractor_3 = generate_solution([-a, b, c, d, e, f]) 
    display_distractor_3 = round(distractor_3, 3)
    distractor_3_feedback = f" $x = {display_distractor_3}$, which corresponds to getting the negative of the actual solution."
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        'Artificial distractor - negative of solution',
        distractor_3, 
        display_distractor_3, 
        distractor_3_feedback,
        0
    )

    distractor_4 = "There are no Real solutions."
    display_distractor_4 = "\\text{%s}" %distractor_4
    distractor_4_feedback = f" ${display_distractor_4}$, which corresponds to students thinking a fraction means there is no solution to the equation."
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_4', 
        'Misconception - Fractions means no Real solution',
        distractor_4, 
        display_distractor_4,
        distractor_4_feedback,
        0
    )

    return [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]

def solve_linear_integer_coefficients_function(response_type):
    run_without_error = 0
    while run_without_error == 0:
        try:
            coefficients = generate_coefficients()
            distractor_dicts = generate_all_option_dicts(coefficients)

            option_value_list = []
            for temp_dict in distractor_dicts:
                if type(temp_dict['values_for_interval_generation']) == type(str()):
                    pass
                else:
                    option_value_list.append(temp_dict['values_for_interval_generation'])
            interval_options = interval_masking_method.createIntervalOptions(option_value_list, 1, 0.5)
            run_without_error = 1
        except Exception as e:
            print(e)
            pass

    index_counter = 0
    solution_dict = distractor_dicts[0]
    for temp_dict in distractor_dicts:
        if index_counter < 4:
            temp_choice_interval_pairs = interval_options[index_counter]
            temp_interval_1 = commonly_used_functions.display_interval(temp_choice_interval_pairs)
            temp_dict['choice_presentation'] = "x \\in %s" %temp_interval_1
            index_counter += 1
        else: 
            temp_dict['choice_presentation'] = temp_dict['value'] # this should be display_distractor_4 from generate_all_option_dicts

    presentation_order = ['solution', 'distractor_1', 'distractor_2', 'distractor_3', 'distractor_4']
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(distractor_dicts)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)

    ### DEFINE STEM, PROBLEM, AND GENERAL COMMENT ###
    if response_type=="Multiple-Choice":
        display_stem = 'Solve the equation below. Then, choose the interval that contains the solution.'
    else:
        display_stem = 'Solve the equation below.'
    display_problem = "%d(%s) = %d(%s)" %(coefficients[0], commonly_used_functions.generatePolynomialDisplay([coefficients[1], coefficients[2]]), coefficients[3], commonly_used_functions.generatePolynomialDisplay([coefficients[4], coefficients[5]]))
    general_comment = "The most common mistake on this question is to not distribute the negative in front of the second fraction correctly. The best way to avoid this is putting the numerator in parentheses, which will help you remember to distribute the negative correctly."

    display_stem_type="String"
    display_problem_type="Math Mode"
    display_options_type="Math Mode"

    question_dict = {
        'code_name': code_name,
        'Response Type': response_type, # Included as argument in function
        'Display Stem Type': display_stem_type, # Options: String, Math Mode, Graph
        'Display Stem': display_stem,
        'Display Problem Type': display_problem_type, # Options: String, Math Mode, Graph, Table
        'Display Problem': display_problem,
        'Display Options Type': display_options_type, # Options: String, Math Mode, Graph
        'Solution': solution_dict['value'],
        'Answer Letter': answer_letter,
        'General Comment': general_comment
    }

    # return 1 dictionary (for the question) and dataframe by options for the question

    return [question_dict, options_df]
