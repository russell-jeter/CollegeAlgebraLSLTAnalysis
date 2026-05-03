import numpy as np
import pandas as pd
import random

from utils import commonly_used_functions, interval_masking_method

code_name = 'solve_inequality_integer_coefficients'

def switch_direction(direction):
    if direction == "left":
        new_direction = "right"
    elif direction == "right":
        new_direction = "left"
    return new_direction

def createCoefficients():
    coefficients = [0, 0, 0, 0]
    while (coefficients[1] >= coefficients[2] or coefficients[0] == coefficients[3]):
        coefficients[0] = commonly_used_functions.maybeMakeNegative(random.randint(3, 10))
        coefficients[1] = commonly_used_functions.maybeMakeNegative(random.randint(3, 10))
        coefficients[2] = commonly_used_functions.maybeMakeNegative(random.randint(3, 10))
        coefficients[3] = commonly_used_functions.maybeMakeNegative(random.randint(3, 10))
    return coefficients

def createIntervalToDisplay(solution_display_directions):
    direction, inclusion, value = solution_display_directions
    if direction == "left" and inclusion == "yes":
        intervalToDisplay = "(-\\infty, %s]" %value
    elif direction == "left" and inclusion == "no":
        intervalToDisplay = "(-\\infty, %s)" %value
    elif direction == "right" and inclusion == "yes":
        intervalToDisplay = "[%s, \\infty)" %value
    elif direction == "right" and inclusion == "no":
        intervalToDisplay = "(%s, \\infty)" %value
    else:
        intervalToDisplay = "\\text{An error occured when creating this interval look.}"
    return intervalToDisplay

def solve_inequality_integer_coefficients_function(response_type):
    run_without_error = 0
    while run_without_error == 0:
        try:
            coefficients = createCoefficients()
            a, b, c, d = coefficients
            left=np.poly1d([b, a])
            right=np.poly1d([c, d])
            diff_of_left_right=left-right
            endpoint=diff_of_left_right.r
            endpointCleaned = round(float(endpoint[0]), 3)

            interval_options_0_2 = interval_masking_method.createIntervalOptions([endpointCleaned, -endpointCleaned], 5, 1)
            solution_interval = commonly_used_functions.display_interval(interval_options_0_2[0])
            option_2_interval = commonly_used_functions.display_interval(interval_options_0_2[1])

            interval_options_1_3 = interval_masking_method.createIntervalOptions([endpointCleaned, -endpointCleaned], 5, 1)
            option_1_interval = commonly_used_functions.display_interval(interval_options_1_3[0])
            option_3_interval = commonly_used_functions.display_interval(interval_options_1_3[1])

            run_without_error = 1
        except Exception as e:
            print(e)
            pass

    allProblemTypes = ["less", "leq", "greater", "geq"]
    random.shuffle(allProblemTypes)
    problemType = allProblemTypes[0]

    left_block_display = commonly_used_functions.generatePolynomialDisplay([b, a])
    right_block_display = commonly_used_functions.generatePolynomialDisplay([c, d])

    if problemType == "less":
        display_problem = "%s < %s" %(left_block_display, right_block_display)
        if (b-c > 0):
            solution_display_directions = ["left", "no", endpointCleaned]
        else:
            solution_display_directions = ["right", "no", endpointCleaned]

    elif problemType == "leq":
        display_problem = "%s \\leq %s" %(left_block_display, right_block_display)
        if (b-c > 0):
            solution_display_directions = ["left", "yes", endpointCleaned]
        else:
            solution_display_directions = ["right", "yes", endpointCleaned]

    elif problemType == "greater":
        display_problem = "%s > %s" %(left_block_display, right_block_display)
        if (b-c < 0):
            solution_display_directions = ["left", "no", endpointCleaned]
        else:
            solution_display_directions = ["right", "no", endpointCleaned]

    else: # "geq"
        display_problem = "%s \\geq %s" %(left_block_display, right_block_display)
        if (b-c < 0):
            solution_display_directions = ["left", "yes", endpointCleaned]
        else:
            solution_display_directions = ["right", "no", endpointCleaned]

    display_solution = createIntervalToDisplay(solution_display_directions)
    solution_feedback = "* $%s$, which is the correct option." %display_solution
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'solution', 
        'Expected solution', 
        endpointCleaned, 
        display_solution, 
        solution_feedback, 
        1
    )
    solution_format = createIntervalToDisplay([solution_display_directions[0], solution_display_directions[1], "a"])
    solution_dict['choice_presentation'] = "%s, \\text{ where } a \\in %s" %(solution_format, solution_interval)

    ### Distractor 1 is the inverse of the solution ###
    display_option_1 = createIntervalToDisplay([switch_direction(solution_display_directions[0]), solution_display_directions[1], solution_display_directions[2]])
    option_1_feedback = " $%s$, which corresponds to switching the direction of the interval. You likely did this if you did not flip the inequality when dividing by a negative!" %display_option_1
    option_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_1',
        'Misconception - flip inequality when dividing by negative',
        endpointCleaned, 
        display_option_1, 
        option_1_feedback,
        0
    )
    option_1_format = createIntervalToDisplay([switch_direction(solution_display_directions[0]), solution_display_directions[1], "a"])
    option_1_dict['choice_presentation'] = "%s, \\text{ where } a \\in %s" %(option_1_format, option_1_interval)

    ### Distractor 2 is the negation of the solution endpoint ###
    display_option_2 = createIntervalToDisplay([solution_display_directions[0], solution_display_directions[1], -solution_display_directions[2]])
    option_2_feedback = " $%s$, which corresponds to negating the endpoint of the solution." %display_option_2
    option_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2',
        'Artimetic - Negative of true solution',
        -endpointCleaned, 
        display_option_2, 
        option_2_feedback,
        0
    )
    option_2_format = solution_format
    option_2_dict['choice_presentation'] = "%s, \\text{ where } a \\in %s" %(option_2_format, option_2_interval)

    ### Distractor 3 is the negation AND inverse of the solution ###
    display_option_3 = createIntervalToDisplay([switch_direction(solution_display_directions[0]), solution_display_directions[1], -solution_display_directions[2]])
    option_3_feedback = " $%s$, which corresponds to switching the direction of the interval AND negating the endpoint. You likely did this if you did not flip the inequality when dividing by a negative as well as not moving values over to a side properly." %display_option_3
    option_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        'Misconception and Arithmetic - flip inequality when dividing by negative and negative of true solution',
        -endpointCleaned, 
        display_option_3, 
        option_3_feedback,
        0
    )
    option_3_format = option_1_format
    option_3_dict['choice_presentation'] = "%s, \\text{ where } a \\in %s" %(option_3_format, option_3_interval)

    ### Distractor 4 is None of the above ###
    option_4_feedback = "None of the above. You may have chosen this if you thought the inequality did not match the ends of the intervals."
    option_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_4',
        'Catch all - none of the above',
        'None of the above', 
        '\\text{None of the above}', 
        option_4_feedback,
        0
    )
    option_4_dict['choice_presentation'] = "\\text{None of the above}"

    solution_dicts_list = [solution_dict, option_1_dict, option_2_dict, option_3_dict, option_4_dict]
    presentation_order = []
    for temp_dict in solution_dicts_list:
        presentation_order.append(temp_dict['name'])
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(solution_dicts_list)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)   

    if response_type=="Multiple-Choice":
        display_stem = 'Solve the linear inequality below. Then, choose the constant and interval combination that describes the solution set.'
    else:
        display_stem = 'Solve the linear inequality below.'
    general_comment = "Remember that less/greater than or equal to includes the endpoint, while less/greater do not. Also, remember that you need to flip the inequality when you multiply or divide by a negative."

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