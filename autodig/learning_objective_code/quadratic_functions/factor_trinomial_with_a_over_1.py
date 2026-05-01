import numpy as np
import pandas as pd
import random
import math
from sympy import primerange

from utils import commonly_used_functions, interval_masking_method

code_name = 'factor_trinomial_with_a_over_1'

def generate_factors(minimumPrime, maximumPrime, numberOfFactors):
    listPrimes = list(primerange(minimumPrime, maximumPrime))
    aFactors = [random.sample(listPrimes, 1) for i in range(numberOfFactors)]
    cFactors = [random.sample(listPrimes, 1) for i in range(numberOfFactors)]
    return [aFactors, cFactors]

def display_factored_form(solution):
    f1, f2, f3, f4 = solution
    first_factor = commonly_used_functions.generatePolynomialDisplay([f1, f2])
    second_factor = commonly_used_functions.generatePolynomialDisplay([f3, f4])
    factored_form = "(%s)(%s)" %(first_factor, second_factor)
    return factored_form 

def generate_solution(minimum, maximum, factors):
    a, b, c, d = [1, 1, 1, -1]
    # This makes sure we can't factor out a constant and the middle coefficient doesn't cancel.
    while ((math.gcd(a, abs(b))*math.gcd(c, abs(d))>1) or (a==c and b==-d) or (a*d+b*c==0)):
        aFactors, cFactors = factors
        a = np.prod(aFactors)
        c = np.prod(cFactors)
        b = commonly_used_functions.maybeMakeNegative(random.randint(minimum, maximum))
        d = commonly_used_functions.maybeMakeNegative(random.randint(minimum, maximum))

    #This will guarantee that we always generate solutions with b <= d
    if(b <= d):
        return [a, b, c, d]
    else:
        return[c, d, a, b]

def generate_quadratic_coefficients(solution):
    a, b, c, d = solution
    return [a*c, a*d + b*c, b*d]

def generate_distractor_1_coefficients(solution):
    a, b, c, d = solution
    if a*d < b*c:
        distractor_1_coeffs = [1, a*d, 1, b*c]
    else:
        distractor_1_coeffs = [1, b*c, 1, a*d]
    return distractor_1_coeffs

def generate_distractor_2_coefficients(solution, factors):
    aFactors = factors[0]
    cFactors = factors[1]
    a, b, c, d = solution
    index = random.randint(0,len(aFactors)-1)

    a = int(a/(aFactors[index][0]))
    c = c*aFactors[index][0]
    if(b <= d):
        return [a, b, c, d]
    else:
        return [c, d, a, b]

def generate_distractor_3_coefficients(solution, factors):
    aFactors = factors[0]
    cFactors = factors[1]
    a, b, c, d = solution
    index = random.randint(0,len(aFactors)-1)
    c = int(c/(cFactors[index][0]))
    a = a*cFactors[index][0]
    if(b <= d):
        return [a, b, c, d]
    else:
        return [c, d, a, b]

def generate_all_option_dicts(solution, factors):
    a, b, c, d = solution
    c0, c1, c2 = generate_quadratic_coefficients(solution)

    display_solution = display_factored_form(solution)
    solution_feedback = "* $%s$, which is the correct option." %display_solution
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'solution',
        'Expected solution',
        solution, 
        display_solution,
        solution_feedback,
        1
    )

    distractor_1_coeffs = generate_distractor_1_coefficients(solution)
    display_distractor_1 = display_factored_form(distractor_1_coeffs)
    distractor_1_quadratic = commonly_used_functions.generatePolynomialDisplay(generate_quadratic_coefficients(distractor_1_coeffs))
    distractor_1_feedback = " $%s$, which corresponds to factoring $%s$." %(display_distractor_1, distractor_1_quadratic)
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_1',
        f'Misconception - Made a=1 and factored $f(x) = {distractor_1_quadratic}$',
        distractor_1_coeffs,
        display_distractor_1,
        distractor_1_feedback,
        0
    )

    distractor_2_coeffs = generate_distractor_2_coefficients(solution, factors)
    display_distractor_2 = display_factored_form(distractor_2_coeffs)
    distractor_2_quadratic = commonly_used_functions.generatePolynomialDisplay(generate_quadratic_coefficients(distractor_2_coeffs))
    distractor_2_feedback = " $%s$, which corresponds to associating some factor of c to a." %display_distractor_2
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2',
        f'Misconception - Associated some factors of c to a and factored $f(x) = {distractor_2_quadratic}$',
        distractor_2_coeffs,
        display_distractor_2,
        distractor_2_feedback,
        0
    )

    distractor_3_coeffs = generate_distractor_3_coefficients(solution, factors)
    display_distractor_3 = display_factored_form(distractor_3_coeffs)
    distractor_3_quadratic = commonly_used_functions.generatePolynomialDisplay(generate_quadratic_coefficients(distractor_3_coeffs))
    distractor_3_feedback = " $%s$, which corresponds to associating some factor of a to c." %display_distractor_3
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        f'Misconception - Associated some factors of a to c and factored $f(x) = {distractor_3_quadratic}$',
        distractor_3_coeffs,
        display_distractor_3,
        distractor_3_feedback,
        0
    )   

    distractor_4_feedback = " None of the above, which corresponds to a different factoring than any of the predicted options. If you get this, please let the coordinator know so they can work with you to figure out what went wrong with your factoring."
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_4',
        f'Catch all - None of the above',
        'None of the above',
        '\\text{None of the above.}',
        distractor_4_feedback,
        0
    ) 
    distractor_4_dict['choice_presentation'] = '\\text{None of the above.}'

    return [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]

def factor_trinomial_with_a_over_1_function(response_type):
    run_without_error = 0
    while run_without_error == 0:
        try:
            option_value_list = [0, 0, 0, 0]
            while (
                option_value_list[0]==option_value_list[1] or 
                option_value_list[0]==option_value_list[2] or 
                option_value_list[0]==option_value_list[3] or 
                option_value_list[1]==option_value_list[2] or 
                option_value_list[1]==option_value_list[3] or 
                option_value_list[2]==option_value_list[3]
            ):
                minimum = 2
                maximum = 7
                numberOfFactors = 2

                factors = generate_factors(minimum, maximum, numberOfFactors)
                solution = generate_solution(minimum, maximum, factors)
                list_of_dicts = generate_all_option_dicts(solution, factors)

                option_value_list = []
                for temp_dict in list_of_dicts:
                    if type(temp_dict['values_for_interval_generation']) == type(str()):
                        pass
                    else:
                        option_value_list.append(temp_dict['values_for_interval_generation'])

            interval_options = interval_masking_method.createIntervalOptions(option_value_list, 5, 1)

            run_without_error = 1
        except Exception as e:
            print(e)
            pass
   
    index_counter = 0
    solution_dict = list_of_dicts[0]
    while index_counter < len(list_of_dicts)-1:
        temp_dict = list_of_dicts[index_counter]
        temp_choice_interval_pairs = interval_options[index_counter]
        temp_interval_1 = commonly_used_functions.display_interval(temp_choice_interval_pairs[0])
        temp_interval_2 = commonly_used_functions.display_interval(temp_choice_interval_pairs[1])
        temp_interval_3 = commonly_used_functions.display_interval(temp_choice_interval_pairs[2])
        temp_interval_4 = commonly_used_functions.display_interval(temp_choice_interval_pairs[3])
        temp_dict[f'choice_presentation'] = "a \\in %s, \\hspace*{5mm} b \\in %s, \\hspace*{5mm} c \\in %s, \\text{ and } \\hspace*{5mm} d \\in %s" %(temp_interval_1, temp_interval_2, temp_interval_3, temp_interval_4)
        index_counter += 1

    presentation_order = ['solution', 'distractor_1', 'distractor_2', 'distractor_3', 'distractor_4']
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(list_of_dicts)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)

    ### DEFINE STEM, PROBLEM, AND GENERAL COMMENT ###
    if response_type=="Multiple-Choice":
        display_stem = 'Factor the quadratic below. Then, choose the intervals that contain the constants in the form $(ax+b)(cx+d); b \\leq d.$'
    else:
        display_stem = 'Factor the quadratic below into the form $(ax+b)(cx+d)$.'
    display_problem = commonly_used_functions.generatePolynomialDisplay(generate_quadratic_coefficients(solution))
    general_comment = "$ac$ had many factors in this problem. It is best to list out the possible pairs in order to make sure you don't miss any."

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
