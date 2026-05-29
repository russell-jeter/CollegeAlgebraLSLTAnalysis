import math
import random
import numpy as np
import pandas as pd

from utils import commonly_used_functions, interval_masking_method

code_name = "solve_linear_rational_coefficients"

def createThreeRandomIntegers():
    a = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
    b = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
    c = commonly_used_functions.maybeMakeNegative(random.randint(3, 9))
    return [a, b, c]

def createThreeDistinctRandomNaturals():
    possibleNaturals= range(2,9)
    naturals = random.sample(possibleNaturals, 3)
    return naturals

def createThreeDistinctRandomIntegers():
    a, b, c = random.sample(range(3, 9), 3)
    return [commonly_used_functions.maybeMakeNegative(a), commonly_used_functions.maybeMakeNegative(b), commonly_used_functions.maybeMakeNegative(c)]

def checkDivisibility(set, divisors):
    if math.gcd(set[0], divisors[0]) > 1 or math.gcd(set[1], divisors[1]) > 1 or math.gcd(set[2], divisors[2]) > 1:
        setDivisible = 1
    else:
        setDivisible = 0
    return setDivisible

def createViableConstants():
    OneSolutionCheck = 0
    firstDivisible = 0
    secondDivisible = 0
    firstOrSecondDivisible = random.randint(0, 1)
    if firstOrSecondDivisible == 0:
        while (OneSolutionCheck == 0) or (firstDivisible == 0) or (secondDivisible==1):
            a, b, c = createThreeRandomIntegers() #in numerator factor, coefficient for x
            d, e, f = createThreeRandomIntegers() #in numerator factor, coefficient for x^0
            g, h, i = createThreeDistinctRandomNaturals() # denominators
            OneSolutionCheck = float(a/g) - float(b/h) - float(c/i) # checks that coefficients for x do not cancel to 0 and lead to infinitely many solutions
            firstDivisible = checkDivisibility([a,b,c], [g,h,i])
            secondDivisible = checkDivisibility([d,e,f], [g,h,i])
    else:
        while (OneSolutionCheck == 0) or (firstDivisible == 1) or (secondDivisible==0):
            a, b, c = createThreeRandomIntegers() #in numerator factor, coefficient for x
            d, e, f = createThreeRandomIntegers() #in numerator factor, coefficient for x^0
            g, h, i = createThreeDistinctRandomNaturals() # denominators
            OneSolutionCheck = float(a/g) - float(b/h) - float(c/i) # checks that coefficients for x do not cancel to 0 and lead to infinitely many solutions
            firstDivisible = checkDivisibility([a,b,c], [g,h,i])
            secondDivisible = checkDivisibility([d,e,f], [g,h,i])
    return [a, b, c, d, e, f, g, h, i]

def generate_solution(constants):
    a, b, c, d, e, f, g, h, i = constants
    eq1 = np.poly1d([a/g, d/g])
    eq2 = np.poly1d([b/h, e/h])
    eq3 = np.poly1d([c/i, f/i])
    toSolve = eq1 - eq2 - eq3
    solution = toSolve.r
    if len(solution)==0:
        solution = [0]
    return solution[0]

def generate_all_option_dicts(constants):
    a, b, c, d, e, f, g, h, i = constants

    solution = generate_solution(constants)
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

    distractor_1 = generate_solution([a, b, c, d, -e, f, g, h, i])    
    display_distractor_1 = round(distractor_1, 3)
    distractor_1_feedback = f" $x = {display_distractor_1}$, which corresponds to not distributing the negative in front of the second fraction."
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_1',
        'Arithmetic error - distribution negative in front of fraction',
        distractor_1, 
        display_distractor_1, 
        distractor_1_feedback,
        0
    )

    distractor_2 = generate_solution([a, b, c, g*d, h*e, i*f, g, h, i]) 
    display_distractor_2 = round(distractor_2, 3)
    distractor_2_feedback = f" $x = {display_distractor_2}$, which corresponds to dividing the coefficients in front of x by the denominator rather than dividing BOTH parts of the numerator by the denominator (or removing the fractions through multiplication)." 
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2', 
        'Misconception - division by first coefficient (a) only of ax+b',
        distractor_2,
        display_distractor_2,
        distractor_2_feedback, 
        0
    )

    distractor_3 = generate_solution([g*a, h*b, i*c, d, e, f, g, h, i])   
    display_distractor_3 = round(distractor_3, 3)
    distractor_3_feedback = f" $x = {display_distractor_3}$, which corresponds to dividing the second number in the numerator by the denominator rather than dividing BOTH parts of the numerator by the denominator (or removing the fractions through multiplication)."
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        'Misconception - division by second coefficient (b) only of ax+b',
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

def solve_linear_rational_coefficients_function(response_type, interval_type):
    option_value_list = [0, 0, 0, 0]
    while commonly_used_functions.findMinDiff(option_value_list) < 1 or np.prod(option_value_list) == 0: # ensures solution/distractors are large enough so intervals are easier to read AND that all distractors lead to a solution
        try:
            constants = createViableConstants()
            distractor_dicts = generate_all_option_dicts(constants)
            option_value_list = []
            for temp_dict in distractor_dicts:
                if type(temp_dict['values_for_interval_generation']) == type(str()):
                    pass
                else:
                    option_value_list.append(temp_dict['values_for_interval_generation'])
            interval_options = interval_masking_method.createIntervalOptions(option_value_list, 1, 0.5)
        except:
            option_value_list = [0, 0, 0, 0]

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
    if (response_type=="Multiple-Choice") and (int(interval_type) == 1):
        display_stem = 'Solve the linear equation below. Then, choose the interval that contains the solution.'
    else:
        display_stem = 'Solve the linear equation below.'
    display_problem = "\\frac{%s}{%s} - \\frac{%s}{%s} = \\frac{%s}{%s}" %(commonly_used_functions.generatePolynomialDisplay(  [constants[0], constants[3]]  ), constants[6], commonly_used_functions.generatePolynomialDisplay(  [constants[1], constants[4]]  ), constants[7], commonly_used_functions.generatePolynomialDisplay(  [constants[2], constants[5]]  ), constants[8]    )
    general_comment = "If you are having trouble with this problem, try to remove a fraction at a time by multiplying each term by the denominator."


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