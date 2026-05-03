import numpy as np
import pandas as pd
import random

from utils import commonly_used_functions, interval_masking_method

code_name = 'solve_compound_or'

def createAllCoefficients():
    c0 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
    c1 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
    c2 = abs(c1) + random.randint(1, 3)
    c3 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
    c4 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
    c5 = abs(c4) + random.randint(1, 3)
    coefficients = [c0, c1, c2, c3, c4, c5]
    smallerEndpoint = float(-c0/(c1-c2))
    largerEndpoint = float(-c3/(c4-c5))
    while (largerEndpoint <= smallerEndpoint):
        c0 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        c1 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        c2 = abs(c1) + random.randint(1, 3)
        c3 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        c4 = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
        c5 = abs(c4) + random.randint(1, 3)
        coefficients = [c0, c1, c2, c3, c4, c5]
        smallerEndpoint = float(-c0/(c1-c2))
        largerEndpoint = float(-c3/(c4-c5))
    return coefficients

def createIntervalFromGreaterThanInequality(coefficients):
    a, b, c = coefficients
    left = np.poly1d([b, a])
    right = np.poly1d([c, 0])
    diff_of_left_right= left-right
    endpoint = diff_of_left_right.r
    return [0, endpoint[0]]

def createIntervalFromLessThanInequality(coefficients):
    a, b, c = coefficients
    left = np.poly1d([b, a])
    right = np.poly1d([c, 0])
    diff_of_left_right= left-right
    endpoint = diff_of_left_right.r
    return [endpoint[0], 0]

def distractorNegateAndInverseDomain(intervalPresentation):
    a, b = intervalPresentation
    return [-b, -a]

def intervalCupInclusive(solutionInterval):
    a, b = solutionInterval
    return "(-\\infty, a] \\cup [b, \\infty)"

def intervalCupExclusive(solutionInterval):
    a, b = solutionInterval
    return "(-\\infty, a) \\cup (b, \\infty)"

def extractValue(solutionInterval):
    a, b = solutionInterval
    if(a == 0):
        return b
    else:
        return a

def generate_all_option_dicts(solution_endpoints):
    a, b = solution_endpoints
    display_solution = "(-\\infty, %s) \\text{ or } (%s, \\infty)" %(round(a, 3), round(b, 3))
    solution_feedback = "* $%s$, which is the correct option." %display_solution
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'solution', 
        'Expected solution', 
        solution_endpoints, 
        display_solution, 
        solution_feedback, 
        1
    )
    
    distractor_1_endpoints = [-b, -a]
    display_distractor_1 = "(-\\infty, %s) \\text{ or } (%s, \\infty)" %(round(-b, 3), round(-a, 3))
    distractor_1_feedback = " $%s$, which corresponds to inverting the inequality and negating the solution." %display_distractor_1
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_1',
        'Arithmetic error - negative of true solution',
        distractor_1_endpoints, 
        display_distractor_1, 
        distractor_1_feedback,
        0
    )

    distractor_2_endpoints = [a, b]
    display_distractor_2 = "(-\\infty, %s] \\text{ or } [%s, \\infty)" %(round(a, 3), round(b, 3))
    distractor_2_feedback = " $%s$, which corresponds to including the endpoints (when they should be excluded)." %display_distractor_2
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2', 
        'Misconception - including endpoints when they should be excluded',
        distractor_2_endpoints,
        display_distractor_2,
        distractor_2_feedback, 
        0
    )

    distractor_3_endpoints = [-b, -a]
    display_distractor_3 = "(-\\infty, %s] \\text{ or } [%s, \\infty)" %(round(-b, 3), round(-a, 3))
    distractor_3_feedback = " $%s$, which corresponds to including the endpoints (when they should be excluded) and inverting the inequality and negating the solution." %display_distractor_3
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        'Misconception and Arithmetic - including endpoints when they should be excluded and negative of true solution',
        distractor_3_endpoints, 
        display_distractor_3, 
        distractor_3_feedback,
        0
    )

    display_distractor_4 = "(-\\infty, \\infty)"
    distractor_4_feedback = " $%s$, which corresponds to the variable canceling and does not happen in this instance." %display_distractor_4
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_4', 
        'Catch all distractor - all real numbers',
        display_distractor_4, 
        display_distractor_4,
        distractor_4_feedback,
        0
    )

    return [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]

def solve_compound_or_function(response_type):
    run_without_error = 0
    while run_without_error == 0:
        try:
            # block[0] + block[1]*x > block[2]*x "or" block[3] + block[4]*x < block[5]*x
            solution_endpoints = [0,0]
            while (abs(solution_endpoints[0])==abs(solution_endpoints[1]) or abs(solution_endpoints[0])<1 or abs(solution_endpoints[1])<1 or abs(abs(solution_endpoints[0])-abs(solution_endpoints[1])) < 1 ):
                allCoefficients = createAllCoefficients()
                factor1Coefficients = [allCoefficients[0], allCoefficients[1], allCoefficients[2]]
                factor2Coefficients = [allCoefficients[3], allCoefficients[4], allCoefficients[5]]
                intervalLeft = createIntervalFromGreaterThanInequality(factor1Coefficients)
                intervalRight = createIntervalFromLessThanInequality(factor2Coefficients)
                endpointLeft = extractValue(intervalLeft)
                endpointRight = extractValue(intervalRight)
                solution_endpoints = [float(endpointLeft), float(endpointRight)]
            solution_dict, option_1_dict, option_2_dict, option_3_dict, option_4_dict = generate_all_option_dicts(solution_endpoints)

            a, b = solution_endpoints

            # Four intervals for options 0 (solution) and 1
            interval_options_0_1 = interval_masking_method.createIntervalOptions([ [a,b], [-b,a] ], 1, 0.5)
            solution_interval_0 = commonly_used_functions.display_interval(interval_options_0_1[0][0])
            solution_interval_1 = commonly_used_functions.display_interval(interval_options_0_1[0][1])
            option_1_interval_0 = commonly_used_functions.display_interval(interval_options_0_1[1][0])
            option_1_interval_1 = commonly_used_functions.display_interval(interval_options_0_1[1][1])

            # Four intervals for options 2 and 3
            interval_options_2_3 = interval_masking_method.createIntervalOptions([ [a,b], [-b,a] ], 1, 0.5)
            option_2_interval_0 = commonly_used_functions.display_interval(interval_options_2_3[0][0])
            option_2_interval_1 = commonly_used_functions.display_interval(interval_options_2_3[0][1])
            option_3_interval_0 = commonly_used_functions.display_interval(interval_options_2_3[1][0])
            option_3_interval_1 = commonly_used_functions.display_interval(interval_options_2_3[1][1])

            run_without_error = 1
        except Exception as e:
            print(e)
            pass

    solution_format = '(-\\infty, a) \\text{ or } (b, \\infty)'
    solution_dict['choice_presentation'] = "%s, \\text{ where } a \\in %s \\text{ and } b \\in %s" %(solution_format, solution_interval_0, solution_interval_1)

    option_1_format = solution_format
    option_1_dict['choice_presentation'] = "%s, \\text{ where } a \\in %s \\text{ and } b \\in %s" %(option_1_format, option_1_interval_0, option_1_interval_1)

    option_2_format = '(-\\infty, a] \\text{ or } [b, \\infty)'
    option_2_dict['choice_presentation'] = "%s, \\text{ where } a \\in %s \\text{ and } b \\in %s" %(option_2_format, option_2_interval_0, option_2_interval_1)

    option_3_format = option_2_format
    option_3_dict['choice_presentation'] = "%s, \\text{ where } a \\in %s \\text{ and } b \\in %s" %(option_3_format, option_3_interval_0, option_3_interval_1)

    option_4_dict['choice_presentation'] = option_4_dict['value']

    presentation_order = ['solution', 'distractor_1', 'distractor_2', 'distractor_3', 'distractor_4']
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame([solution_dict, option_1_dict, option_2_dict, option_3_dict, option_4_dict])
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)

    if factor1Coefficients[1] < 0:
        displayLeftFactor = "%s - %s x > %s x" %(factor1Coefficients[0], -factor1Coefficients[1], factor1Coefficients[2])
    else:
        displayLeftFactor = "%s + %s x > %s x" %(factor1Coefficients[0], factor1Coefficients[1], factor1Coefficients[2])

    if factor2Coefficients[1] < 0:
        displayRightFactor = "%s - %s x < %s x" %(factor2Coefficients[0], -factor2Coefficients[1], factor2Coefficients[2])
    else:
        displayRightFactor = "%s + %s x < %s x" %(factor2Coefficients[0], factor2Coefficients[1], factor2Coefficients[2])

    if response_type=="Multiple-Choice":
        display_stem = 'Solve the linear inequality below. Then, choose the constant and interval combination that describes the solution set.'
    else:
        display_stem = 'Solve the linear inequality below.'
    display_problem = '%s \\text{ or } %s' %(displayLeftFactor, displayRightFactor)
    general_comment = "When multiplying or dividing by a negative, flip the sign."

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