import numpy as np
import pandas as pd
import random 

from utils import commonly_used_functions, interval_masking_method

code_name = 'solve_compound_and'

def create_coefficients_and_endpoints():
    c0, c1, c2, c3, c4, c5, c6 = [0, 0, 0, 0, 0, 0, 0]
    smaller_endpoint = 0
    larger_endpoint = 0

    while  (larger_endpoint <= smaller_endpoint):
        c0 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        c1 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        c3 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        c4 = random.randint(3, 9)
        c5 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        c6 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        # Need 1, 4, and 6 set before 2
        c2 = (max(c1, c6)*c4) + random.randint(2, 5) # This flips the inequalities

        smaller_endpoint = float((-c0*c4-c3) / (c1*c4-c2))
        larger_endpoint = float((c4*c5+c3) / (c2-c4*c6))
       
    coefficients = [c0, c1, c2, c3, c4, c5, c6]
    endpoints = [smaller_endpoint, larger_endpoint]
    return [coefficients, endpoints]

def present_choice_intervals(string_presentation, interval_options):
    option_interval_a = f'[{interval_options[0][0]}, {interval_options[0][1]}]'
    option_interval_b = f'[{interval_options[1][0]}, {interval_options[1][1]}]'
    choice_presentation = '%s, \\text{ where } a \\in %s \\text{ and } b \\in %s' %(string_presentation, option_interval_a, option_interval_b)
    return choice_presentation

def solve_compound_and_function(response_type, interval_type):
    coefficients = [0, 0, 0, 0, 0, 0, 0]
    endpoints = [0, 0]
    while (
        abs(endpoints[0]) == abs(endpoints[1]) or
        abs(endpoints[0]) < 1 or 
        abs(endpoints[1]) < 1 or
        abs(abs(endpoints[0]) - abs(endpoints[1])) < 1 
    ):
        coefficients, endpoints = create_coefficients_and_endpoints()

    c0, c1, c2, c3, c4, c5, c6 = coefficients
    if c1 < 0:
        AndInequalityLeft = "%s - %s x" %(c0, -c1)
    else:
        AndInequalityLeft = "%s + %s x" %(c0, c1)

    if c3 < 0:
        AndInequalityMiddle = "\\frac{%s x + %s}{%s}" %(c2, -c3, c4)
    else:
        AndInequalityMiddle = "\\frac{%s x - %s}{%s}" %(c2, c3, c4)

    if c6 < 0:
        AndInequalityRight = "%s - %s x" %(c5, -c6)
    else:
        AndInequalityRight = "%s + %s x" %(c5, c6)

    problem_type = random.randint(0,3) # 0-1 uses correct values, 2-3 uses negative values

    # Intervals are created for each option since the display of the options are all different
    modified_endpoints = [endpoint*(-1)**problem_type for endpoint in endpoints]
    interval_options_1 = interval_masking_method.createIntervalOptions(modified_endpoints, 4, 0.75)
    interval_options_2 = interval_masking_method.createIntervalOptions(modified_endpoints, 4, 0.75)
    interval_options_3 = interval_masking_method.createIntervalOptions(modified_endpoints, 4, 0.75)
    interval_options_4 = interval_masking_method.createIntervalOptions(modified_endpoints, 4, 0.75)

    option_1_string_presentation = '(a, b]'
    option_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'option_1',
        'Placeholder distractor short_description', # short_description
        modified_endpoints, 
        f'({round(modified_endpoints[0], 3)}, {round(modified_endpoints[1], 3)}]',
        'Placeholder student feedback', # feedback
        0
    )
    option_1_dict['choice_presentation'] = present_choice_intervals(option_1_string_presentation, interval_options_1)

    option_2_string_presentation = '[a, b)'
    option_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'option_2',
        'Placeholder distractor short_description', # short_description
        modified_endpoints, 
        f'[{round(modified_endpoints[0], 3)}, {round(modified_endpoints[1], 3)})',
        'Placeholder student feedback', # feedback
        0
    )
    option_2_dict['choice_presentation'] = present_choice_intervals(option_2_string_presentation, interval_options_2)

    option_3_string_presentation = '(-\\infty, a) \\cup [b, \\infty)'
    option_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'option_3',
        'Placeholder distractor short_description', # short_description
        modified_endpoints, 
        f'(-\\infty, {round(modified_endpoints[0], 3)}) \\cup [{round(modified_endpoints[1], 3)}, \\infty)',
        'Placeholder student feedback', # feedback
        0
    )
    option_3_dict['choice_presentation'] = present_choice_intervals(option_3_string_presentation, interval_options_3)

    option_4_string_presentation = '(-\\infty, a] \\cup (b, \\infty)'
    option_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'option_4',
        'Placeholder distractor short_description', # short_description
        modified_endpoints, 
        f'(-\\infty, {round(modified_endpoints[0], 3)}] \\cup ({round(modified_endpoints[1], 3)}, \\infty)',
        'Placeholder student feedback', # feedback
        0
    )
    option_4_dict['choice_presentation'] = present_choice_intervals(option_4_string_presentation, interval_options_4)

    option_5_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'option_5',
        'Placeholder distractor short_description', # short_description
        'None of the above.', 
        '\\text{None of the above.}', 
        'Placeholder student feedback', # feedback
        0
    )
    option_5_dict['choice_presentation'] = '\\text{None of the above.}'


    if problem_type == 0: # left < middle \leq right
        display_problem = '%s < %s \\leq %s' %(AndInequalityLeft, AndInequalityMiddle, AndInequalityRight)
        option_1_dict['name'] = 'solution'
        option_1_dict['short_description'] = 'Expected solution'
        option_1_dict['feedback'] = '* This is the correct option!'
        option_1_dict['solution'] = 1
        solution_dict = option_1_dict

        option_2_dict['short_description'] = "Misconception - flipping final inequality"
        option_2_dict['feedback'] = f" ${option_2_dict['value']}$, which corresponds to flipping the inequality."

        option_3_dict['short_description'] = "Misconception - and-inequality displayed as or-inequality"
        option_3_dict['feedback'] = f" ${option_3_dict['value']}$, which corresponds to displaying the and-inequality as an or-inequality."

        option_4_dict['short_description'] = "Misconception - and-inequality displayed as or-inequality AND flipping the inequality"
        option_4_dict['feedback'] = f" ${option_4_dict['value']}$, which corresponds to displaying the and-inequality as an or-inequality AND flipping the inequality."

        option_5_dict['short_description'] = "Catch-all none of the above response"
        option_5_dict['feedback'] = "This corresponds to thinking that the values were not correct."

    elif problem_type == 1: # left < middle \leq right with negatives of correct endpoints 
        display_problem = '%s < %s \\leq %s' %(AndInequalityLeft, AndInequalityMiddle, AndInequalityRight)
        option_5_dict['name'] = 'solution'
        option_5_dict['short_description'] = 'Expected solution'
        option_5_dict['feedback'] = '* This is the correct option!'
        option_5_dict['solution'] = 1
        solution_dict = option_5_dict

        option_1_dict['short_description'] = "Arithmetic - Values are negative of what they should be"
        option_1_dict['feedback'] = f" ${option_1_dict['value']}$, which is the correct interval but negatives of the actual endpoints."

        option_2_dict['short_description'] = "Misconception - flipping final inequality and negatives"
        option_2_dict['feedback'] = f" ${option_2_dict['value']}$, which corresponds to flipping the inequality and getting negatives of the actual endpoints."

        option_3_dict['short_description'] = "Misconception - and-inequality displayed as or-inequality and negatives"
        option_3_dict['feedback'] = f" ${option_3_dict['value']}$, which corresponds to displaying the and-inequality as an or-inequality and getting negatives of the actual endpoints."

        option_4_dict['short_description'] = "Misconception - and-inequality displayed as or-inequality AND flipping the inequality AND negatives"
        option_4_dict['feedback'] = f" ${option_4_dict['value']}$, which corresponds to displaying the and-inequality as an or-inequality AND flipping the inequality AND getting negatives of the actual endpoints."

    elif problem_type == 2: # left \leq middle < right
        display_problem = '%s \\leq %s < %s'%(AndInequalityLeft, AndInequalityMiddle, AndInequalityRight)
        option_2_dict['name'] = 'solution'
        option_2_dict['short_description'] = 'Expected solution'
        option_2_dict['feedback'] = '* This is the correct option!'
        option_2_dict['solution'] = 1
        solution_dict = option_2_dict

        option_1_dict['short_description'] = "Misconception - flipping final inequality"
        option_1_dict['feedback'] = f" ${option_1_dict['value']}$, which corresponds to flipping the inequality."

        option_3_dict['short_description'] = "Misconception - and-inequality displayed as or-inequality AND flipping the inequality"
        option_3_dict['feedback'] = f" ${option_3_dict['value']}$, which corresponds to displaying the and-inequality as an or-inequality AND flipping the inequality."

        option_4_dict['short_description'] = "Misconception - and-inequality displayed as or-inequality"
        option_4_dict['feedback'] = f" ${option_4_dict['value']}$, which corresponds to displaying the and-inequality as an or-inequality."

        option_5_dict['short_description'] = "Catch-all none of the above response"
        option_5_dict['feedback'] = "This corresponds to thinking that the values were not correct."

    elif problem_type == 3: # left \leq middle < right with negatives of correct endpoints
        display_problem = '%s \\leq %s < %s' %(AndInequalityLeft, AndInequalityMiddle, AndInequalityRight)
        option_5_dict['name'] = 'solution'
        option_5_dict['short_description'] = 'Expected solution'
        option_5_dict['feedback'] = '* This is the correct option!'
        option_5_dict['solution'] = 1
        solution_dict = option_5_dict

        option_1_dict['short_description'] = "Misconception - flipping final inequality and negatives"
        option_1_dict['feedback'] = f" ${option_1_dict['value']}$, which corresponds to flipping the inequality and getting negatives of the actual endpoints."

        option_2_dict['short_description'] = "Arithmetic - Values are negative of what they should be"
        option_2_dict['feedback'] = f" ${option_2_dict['value']}$, which is the correct interval but negatives of the actual endpoints."

        option_3_dict['short_description'] = "Misconception - and-inequality displayed as or-inequality AND flipping the inequality AND negatives"
        option_3_dict['feedback'] = f" ${option_3_dict['value']}$, which corresponds to displaying the and-inequality as an or-inequality AND flipping the inequality AND getting negatives of the actual endpoints."

        option_4_dict['short_description'] = "Misconception - and-inequality displayed as or-inequality and negatives"
        option_4_dict['feedback'] = f" ${option_4_dict['value']}$, which corresponds to displaying the and-inequality as an or-inequality and getting negatives of the actual endpoints."

    solution_dicts_list = [option_1_dict, option_2_dict, option_3_dict, option_4_dict, option_5_dict]
    presentation_order = []
    for temp_dict in solution_dicts_list:
        presentation_order.append(temp_dict['name'])
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(solution_dicts_list)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)   

    if (response_type=="Multiple-Choice") and (int(interval_type) == 1):
        display_stem = 'Solve the linear inequality below. Then, choose the constant and interval combination that describes the solution set.'
    else:
        display_stem = 'Solve the linear inequality below.'
    general_comment = "To solve, you will need to break up the compound inequality into two inequalities. Be sure to keep track of the inequality! It may be best to draw a number line and graph your solution."

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

