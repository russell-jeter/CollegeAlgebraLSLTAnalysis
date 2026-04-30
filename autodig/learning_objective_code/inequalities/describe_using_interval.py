import numpy as np
import pandas as pd
import random

from utils import commonly_used_functions, interval_masking_method

code_name = 'describe_using_interval'

def generate_distance_and_from_number(minimum, maximum):
    distance = random.randint(minimum, maximum)
    fromNumber = random.randint(-maximum, maximum)
    while distance == fromNumber or fromNumber == 0:
        distance = random.randint(minimum, maximum)
        fromNumber = random.randint(-maximum, maximum)
    endValues = fromNumber - distance, fromNumber + distance
    return [distance, fromNumber, endValues]

def describe_using_interval_function(response_type):
    distance, from_number, end_values = generate_distance_and_from_number(2, 10)
    
    option_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'option_1',
        'Placeholder distractor description',
        "[%d, %d]" %(end_values[0], end_values[1]),
        "[%d, %d]" %(end_values[0], end_values[1]),
        " This describes the values no more than %d from %d" %(distance, from_number),
        0
    )
    option_1_dict['choice_presentation'] = "[%d, %d]" %(end_values[0], end_values[1])

    option_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'option_2',
        'Placeholder distractor description',
        "(%d, %d)" %(end_values[0], end_values[1]),
        "(%d, %d)" %(end_values[0], end_values[1]),
        " This describes the values less than %d from %d" %(distance, from_number),
        0
    )
    option_2_dict['choice_presentation'] = "(%d, %d)" %(end_values[0], end_values[1])

    option_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'option_3',
        'Placeholder distractor description',
        "(-\\infty, %d) \\cup (%d, \\infty)" %(end_values[0], end_values[1]),
        "(-\\infty, %d) \\cup (%d, \\infty)" %(end_values[0], end_values[1]),
        " This describes the values more than %d from %d" %(distance, from_number),
        0
    )
    option_3_dict['choice_presentation'] = "(-\\infty, %d) \\cup (%d, \\infty)" %(end_values[0], end_values[1])

    option_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'option_4',
        'Placeholder distractor description',
        "(-\\infty, %d] \\cup [%d, \\infty)" %(end_values[0], end_values[1]),
        "(-\\infty, %d] \\cup [%d, \\infty)" %(end_values[0], end_values[1]),
        " This describes the values no less than %d from %d" %(distance, from_number),
        0
    )
    option_4_dict['choice_presentation'] = "(-\\infty, %d] \\cup [%d, \\infty)" %(end_values[0], end_values[1])

    option_5_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'option_5',
        'Arithmetic error - student associates wording with structure of answer but does not check values',
        "None of the above",
        "\\text{None of the above}",
        " You likely thought the values in the interval were not correct.",
        0
    )
    option_5_dict['choice_presentation'] = "\\text{None of the above}"

    question_type = random.randint(1, 5)
    if question_type == 1: # No more than
        display_problem = "\\text{ No more than } %d \\text{ units from the number } %d." %(distance, from_number)

        option_1_dict['name'] = 'solution'
        option_1_dict['short_description'] = 'Expected solution'
        option_1_dict['feedback'] = "* This is the correct option!"
        option_1_dict['solution'] = 1
        solution_dict = option_1_dict
        
        option_2_dict['short_description'] = 'Misconception - confused "no more than" with "less than"'
        option_3_dict['short_description'] = 'Misconception - confused "no more than" with "more than"'
        option_4_dict['short_description'] = 'Misconception - confused "no more than" with "no less than"'

    elif question_type == 2: # less than
        display_problem = "\\text{ Less than } %d \\text{ units from the number } %d." %(distance, from_number)
        option_2_dict['name'] = 'solution'
        option_2_dict['short_description'] = 'Expected solution'
        option_2_dict['feedback'] = "* This is the correct option!"
        option_2_dict['solution'] = 1
        solution_dict = option_2_dict
        
        option_1_dict['short_description'] = 'Misconception - confused "less than" with "no more than"'
        option_3_dict['short_description'] = 'Misconception - confused "less than" with "more than"'
        option_4_dict['short_description'] = 'Misconception - confused "less than" with "no less than"'

    elif question_type == 3: # more than
        display_problem = "\\text{ More than } %d \\text{ units from the number } %d." %(distance, from_number)
        option_3_dict['name'] = 'solution'
        option_3_dict['short_description'] = 'Expected solution'
        option_3_dict['feedback'] = "* This is the correct option!"
        option_3_dict['solution'] = 1
        solution_dict = option_3_dict
        
        option_1_dict['short_description'] = 'Misconception - confused "more than" with "no more than"'
        option_2_dict['short_description'] = 'Misconception - confused "more than" with "less than"'
        option_4_dict['short_description'] = 'Misconception - confused "more than" with "no less than"'
    
    elif question_type == 4: # no less than
        display_problem = "\\text{ No less than } %d \\text{ units from the number } %d." %(distance, from_number)
        option_4_dict['name'] = 'solution'
        option_4_dict['short_description'] = 'Expected solution'
        option_4_dict['feedback'] = "* This is the correct option!"
        option_4_dict['solution'] = 1
        solution_dict = option_4_dict
        
        option_1_dict['short_description'] = 'Misconception - confused "no less than" with "no more than"'
        option_2_dict['short_description'] = 'Misconception - confused "no less than" with "less than"'
        option_3_dict['short_description'] = 'Misconception - confused "no less than" with "more than"'

    elif question_type == 5: # Reverses distance from number
        option_5_dict['name'] = 'solution'
        option_5_dict['short_description'] = 'Expected solution'
        option_5_dict['feedback'] = "* Options A-D described the values [more/less than] %d units from %d, which is the reverse of what the question asked." %(from_number, distance)
        option_5_dict['solution'] = 1
        solution_dict = option_5_dict

        random_display = random.randint(1, 4)
        random_display_problem_dict = {
            '1': ' No more than ',
            '2': ' Less than ',
            '3': ' More than ',
            '4': ' No less than '
        }
        display_phrase = random_display_problem_dict[str(random_display)]
        display_problem = "\\text{%s} %d \\text{ units from the number } %d." %(display_phrase, from_number, distance)

        if random_display == 1: # no more than reversed
            option_1_dict['short_description'] = 'Misconception - reversed interpretation of distance D from number N to N distance from D'
            option_2_dict['short_description'] = 'Misconception - reversed interpretation AND confused "no more than" with "less than"'
            option_3_dict['short_description'] = 'Misconception - reversed interpretation AND confused "no more than" with "more than"'
            option_4_dict['short_description'] = 'Misconception - reversed interpretation AND confused "no more than" with "no less than"'

        elif random_display == 2: # less than reversed
            option_1_dict['short_description'] = 'Misconception - reversed interpretation AND confused "less than" with "no more than"'
            option_2_dict['short_description'] = 'Misconception - reversed interpretation of distance D from number N to N distance from D'
            option_3_dict['short_description'] = 'Misconception - reversed interpretation AND confused "less than" with "more than"'
            option_4_dict['short_description'] = 'Misconception - reversed interpretation AND confused "less than" with "no less than"'

        elif random_display == 3: # more than reversed
            option_1_dict['short_description'] = 'Misconception - reversed interpretation AND confused "more than" with "no more than"'
            option_2_dict['short_description'] = 'Misconception - reversed interpretation AND confused "more than" with "less than"'
            option_3_dict['short_description'] = 'Misconception - reversed interpretation of distance D from number N to N distance from D'
            option_4_dict['short_description'] = 'Misconception - reversed interpretation AND confused "more than" with "no less than"'

        elif random_display == 4: # no less than reversed
            option_1_dict['short_description'] = 'Misconception - reversed interpretation AND confused "no less than" with "no more than"'
            option_2_dict['short_description'] = 'Misconception - reversed interpretation AND confused "no less than" with "less than"'
            option_3_dict['short_description'] = 'Misconception - reversed interpretation AND confused "no less than" with "more than"'
            option_4_dict['short_description'] = 'Misconception - reversed interpretation of distance D from number N to N distance from D'

    options_dict_list = [option_1_dict, option_2_dict, option_3_dict, option_4_dict, option_5_dict]
    presentation_order = []
    for temp_dict in options_dict_list:
        presentation_order.append(temp_dict['name'])
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(options_dict_list)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)   

    ### DEFINE STEM, PROBLEM, GENERAL COMMENT ###
    if response_type=="Multiple-Choice":
        display_stem = 'Using an interval or intervals, choose the option that describes all the $x$-values within or including a distance of the given values.'
    else:
        display_stem = 'Using an interval or intervals, describe all the $x$-values within or including a distance of the given values.'
    # displayProblem was already defined
    general_comment =  "When thinking about this language, it helps to draw a number line and try points."

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

