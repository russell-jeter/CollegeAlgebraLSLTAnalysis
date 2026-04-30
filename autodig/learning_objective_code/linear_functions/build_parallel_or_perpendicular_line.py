import random
import math
import pandas as pd

from utils import commonly_used_functions, interval_masking_method

code_name = 'build_parallel_or_perpendicular_line'

def generateLineType():
    typeList = ['Parallel', 'Perpendicular']
    lineType = typeList[random.randint(0, len(typeList)-1)]
    return lineType

def generateProblemAndSolution(lineType):
    if lineType == 'Parallel':
        point = [commonly_used_functions.maybeMakeNegative(random.randint(2, 10)), commonly_used_functions.maybeMakeNegative(random.randint(2, 10))]
        A = random.randint(3, 9)
        B = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        while math.gcd(A, abs(B)) > 1:
            A = random.randint(3, 9)
            B = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        C = random.randint(3, 15)
        slope = float(-A)/float(B)
        yInt = float(point[1]-slope*point[0])
        return [[slope, yInt], point, [A,B,C]]
    else:
        point = [commonly_used_functions.maybeMakeNegative(random.randint(2, 10)), commonly_used_functions.maybeMakeNegative(random.randint(2, 10))]
        A = random.randint(3, 9)
        B = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        while math.gcd(A, abs(B)) > 1:
            A = random.randint(3, 9)
            B = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        C = float(random.randint(3, 15))
        slope = float(B)/float(A)
        yInt = float(point[1]-slope*point[0])
        return [[slope, yInt], point, [A,B,C]]

def clean_display_of_equation(coefficients):
    slope, yInt = coefficients
    if yInt < 0:
        equation = "y = %.2fx - %.2f" %(slope, -yInt)
    else:
        equation = "y = %.2fx + %.2f" %(slope, yInt)
    return equation

def generate_all_option_dicts(solution, point):
    slope, yInt = solution
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

    distractor_1 = [-slope, point[1] + slope*point[0]]
    display_distractor_1 = clean_display_of_equation(distractor_1)
    distractor_1_feedback = f" ${display_distractor_1}$, which corresponds to using the negative slope."
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
    distractor_2_feedback = f" ${display_distractor_2}$, which corresponds to using the correct slope and getting the negative $y$-intercept."
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2', 
        'Arithmetic error of negative y-value',
        distractor_2,
        display_distractor_2,
        distractor_2_feedback, 
        0
    ) 
    
    distractor_3 = [slope, -point[0] + point[1]]
    display_distractor_3 = clean_display_of_equation(distractor_3)
    distractor_3_feedback = f" ${display_distractor_3}$, which corresponds to correct slope and mis-distributing while simplifying to slope-intercept form."
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        'Arithmetic error - distribution with first point',
        distractor_3, 
        display_distractor_3, 
        distractor_3_feedback,
        0
    )

    distractor_4 = [1.0/slope, yInt]
    display_distractor_4 = clean_display_of_equation(distractor_4)
    distractor_4_feedback = f" ${display_distractor_4}$, which corresponds to using the reciprocal slope $(1/m)$."
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_4', 
        'Arithmetic error - Reciporacal slope 1/m',
        distractor_4, 
        display_distractor_4,
        distractor_4_feedback,
        0
    )

    return [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]

def build_parallel_or_perpendicular_line_function(response_type):
    run_without_error = 0
    while run_without_error == 0:
        try:
            lineType = generateLineType()
            solution, point, coefficients = generateProblemAndSolution(lineType)
            A, B, C = coefficients
            distractor_dicts = generate_all_option_dicts(solution, point)

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
        temp_dict['choice_presentation'] = "a \\in %s \\text{ and } b \\in %s" %(temp_interval_1, temp_interval_2)
        index_counter += 1

    presentation_order = ['solution', 'distractor_1', 'distractor_2', 'distractor_3', 'distractor_4']
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(distractor_dicts)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)

    ### DEFINE STEM, PROBLEM, AND GENERAL COMMENT ###
    if response_type=="Multiple-Choice":
        display_stem = 'Find the equation of the line described below. Write the linear equation in the form $ y=mx+b $ and choose the intervals that contain $m$ and $b$.'
    else:
        display_stem = 'Find the equation of the line described below. Write the linear equation in the form $y=mx+b$.'
    if B < 0:
        standardFormParOrPer = "%s x - %s y" %(A, -B)
    else:
        standardFormParOrPer = "%s x + %s y" %(A, B)
    display_problem = '\\text{%s to } %s = %d \\text{ and passing through the point } (%s, %s).' %(lineType, standardFormParOrPer, C, point[0], point[1])
    general_comment = "Parallel slope is the same and perpendicular slope is opposite reciprocal. Opposite reciprocal means flipping the fraction and changing the sign (positive to negative or negative to positive)."

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