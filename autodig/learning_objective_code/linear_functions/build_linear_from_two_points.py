import sys
import random
import numpy as np
import pandas as pd

from utils import commonly_used_functions, interval_masking_method

code_name = 'build_linear_from_two_points'

### DEFINITIONS ###
def generateProblem():
    numerator = 0
    denominator = 0
    slope = 1
    while (numerator==0 or denominator==0 or slope==1):
        pointOne = [commonly_used_functions.maybeMakeNegative(random.randint(2, 11)), commonly_used_functions.maybeMakeNegative(random.randint(2, 11))]
        pointTwo = [commonly_used_functions.maybeMakeNegative(random.randint(2, 11)), commonly_used_functions.maybeMakeNegative(random.randint(2, 11))]
        numerator = float(pointTwo[1]-pointOne[1])
        denominator = float(pointTwo[0]-pointOne[0])
        slope = numerator/denominator
    return [pointOne, pointTwo]

def clean_display_of_equation(coefficients):
    displayCleanEquation = "y = %s" %commonly_used_functions.generatePolynomialDisplay([round(coefficients[0], 2), round(coefficients[1], 2)])
    return displayCleanEquation

def generateSolutionAndDistractors(problem):
    pointOne, pointTwo = problem
    slope = float(pointTwo[1]-pointOne[1])/float(pointTwo[0]-pointOne[0])
    yInt = float(pointTwo[1]-slope*pointTwo[0])

    solution = [slope, yInt]
    display_solution = clean_display_of_equation(solution)
    solution_feedback = f"* ${display_solution}$, which is the correct option."
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'solution',
        'Expected solution',
        solution, 
        display_solution,
        solution_feedback,
        1
    )

    distractor_1 = [-slope, float(pointTwo[1]+slope*pointTwo[0])]
    display_distractor_1 = clean_display_of_equation(distractor_1)
    distractor_1_feedback = f" ${display_distractor_1}$, which corresponds to using the negative slope and the correct equation."
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_1',
        'Arithmetic error of negative slope',
        distractor_1,
        display_distractor_1,
        distractor_1_feedback,
        0
    )

    distractor_2 = [slope, -yInt]
    display_distractor_2 = clean_display_of_equation(distractor_2)
    distractor_2_feedback = f" ${display_distractor_2}$, which corresponds to using the correct slope and getting the negative y-intercept."
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2', 
        'Arithmetic error of negative y-value',
        distractor_2,
        display_distractor_2,
        distractor_2_feedback, 
        0
    ) 

    distractor_3 = [slope, -pointOne[0] + pointOne[1]]
    display_distractor_3 = clean_display_of_equation(distractor_3)
    distractor_3_feedback = f" ${display_distractor_3}$, which corresponds to using the correct slope/equation but not distributing correctly using the first point."
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        'Arithmetic error - distribution with first point',
        distractor_3, 
        display_distractor_3, 
        distractor_3_feedback,
        0
    )

    distractor_4 = [slope, -pointTwo[0] + pointTwo[1]]
    display_distractor_4 = clean_display_of_equation(distractor_4)
    distractor_4_feedback = f" ${display_distractor_4}$, which corresponds to using the correct slope/equation but not distributing correctly using the second point."
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_4', 
        'Arithmetic error - distribution with second point',
        distractor_4, 
        display_distractor_4,
        distractor_4_feedback,
        0
    )

    list_of_dicts = [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]

    return list_of_dicts

def build_linear_from_two_points_function(response_type, interval_type):
    run_without_error = 0
    while run_without_error == 0:
        try:
            problem = generateProblem()
            distractor_dicts = generateSolutionAndDistractors(problem)

            option_value_list = []
            for temp_dict in distractor_dicts:
                option_value_list.append(temp_dict['values_for_interval_generation'])

            interval_options = interval_masking_method.createIntervalOptions(option_value_list, 1, 0.5)
            # interval_options returns 5 groups of 2 pairs of interval endings
            run_without_error = 1
        except:
            pass
    
    index_counter = 0
    solution_dict = distractor_dicts[0]
    for temp_dict in distractor_dicts:
        temp_choice_interval_pairs = interval_options[index_counter]
        temp_interval_1 = commonly_used_functions.display_interval(temp_choice_interval_pairs[0])
        temp_interval_2 = commonly_used_functions.display_interval(temp_choice_interval_pairs[1])
        temp_dict[f'choice_presentation'] = "a \\in %s \\text{ and } b \\in %s" %(temp_interval_1, temp_interval_2)
        index_counter += 1

    presentation_order = ['solution', 'distractor_1', 'distractor_2', 'distractor_3', 'distractor_4']
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(distractor_dicts)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)

    ### DEFINE STEM, PROBLEM, AND GENERAL COMMENT ###
    if (response_type=="Multiple-Choice") and (int(interval_type) == 1):
        display_stem = 'First, find the equation of the line containing the two points below. Then, write the equation in the form $ y=mx+b $ and choose the intervals that contain $m$ and $b$.'
    else:
        display_stem = 'First, find the equation of the line containing the two points below. Then, write the equation in the form $ y=mx+b $.'
    pointOne, pointTwo = problem
    display_problem = "(%s, %s) \\text{ and } (%s, %s)" %(pointOne[0], pointOne[1], pointTwo[0], pointTwo[1])
    general_comment = "Remember to keep your points in order when plugging in to the slope formula."

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