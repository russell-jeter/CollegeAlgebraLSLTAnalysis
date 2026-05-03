from sympy import primerange
import numpy as np
import pandas as pd
import random
from math import gcd

from utils import commonly_used_functions, interval_masking_method

code_name = 'solve_quadratic_with_factoring'

def generate_factors(minimumPrime, maximumPrime, numberOfFactors):
    listPrimes = list(primerange(minimumPrime, maximumPrime))
    bFactors = [random.sample(listPrimes, 1) for i in range(numberOfFactors)]
    dFactors = [random.sample(listPrimes, 1) for i in range(numberOfFactors)]
    return [bFactors, dFactors]

def generate_solution_factor_coefficients(minimum, maximum, factors):
    # This makes sure the middle coefficient does not cancel out and allow the student to solve without the quadratic formula or factoring.
    a, b, c, d = [0, 0, 0, 0]
    while (a*d+b*c==0) or (gcd(a, b) > 1) or (gcd(c, d) > 1):
        bFactors = factors[0]
        dFactors = factors[1]
        b = commonly_used_functions.maybeMakeNegative(np.prod(bFactors))
        d = commonly_used_functions.maybeMakeNegative(np.prod(dFactors))
        a = random.randint(minimum, maximum)
        c = random.randint(minimum, maximum)
    #This will guarantee that we always generate solutions with b < d
    if(b < d):
        return [a, b, c, d]
    else:
        return[c, d, a, b]

def generate_quadratic_coefficients(solution):
    a, b, c, d = solution
    return [a*c, a*d + b*c, b*d]

def generate_solution_values(solution):
    s0 = float(solution[0])
    s1 = float(solution[1])
    s2 = float(solution[2])
    s3 = float(solution[3])
    z0 = float(-s1/s0)
    z1 = float(-s3/s2)
    if (z0 < z1):
        factoredPolynomial = "(%s)(%s)" %(commonly_used_functions.generatePolynomialDisplay([solution[0], solution[1]]), commonly_used_functions.generatePolynomialDisplay([solution[2], solution[3]]))
        answer = [z0, z1, factoredPolynomial]
    else:
        factoredPolynomial = "(%s)(%s)" %(commonly_used_functions.generatePolynomialDisplay([solution[2], solution[3]]), commonly_used_functions.generatePolynomialDisplay([solution[0], solution[1]]))
        answer = [z1, z0, factoredPolynomial]
    return answer

def generate_distractor_1_values(solution):
    a, b, c, d = solution
    if -a*d < -b*c:
        factoredPolynomial = "(%s)(%s)" %(commonly_used_functions.generatePolynomialDisplay([1, a*d]), commonly_used_functions.generatePolynomialDisplay([1, b*c]))
        return [-a*d, -b*c, factoredPolynomial]
    else:
        factoredPolynomial = "(%s)(%s)" %(commonly_used_functions.generatePolynomialDisplay([1, b*c]), commonly_used_functions.generatePolynomialDisplay([1, a*d]))
        return [-b*c, -a*d, factoredPolynomial]

def generate_distractor_2_values(solution):
    a = float(solution[0])
    b = float(solution[1])
    c = float(solution[2])
    d = float(solution[3])
    z0 = float(-b/(a*c))
    z1 = -d
    if (z0<=z1):
        factoredPolynomial = "(%s)(%s)" %(commonly_used_functions.generatePolynomialDisplay([solution[0]*solution[2], solution[1]]), commonly_used_functions.generatePolynomialDisplay([1, solution[3]]))
        return [z0, z1, factoredPolynomial]
    else:
        factoredPolynomial = "(%s)(%s)" %(commonly_used_functions.generatePolynomialDisplay([1, solution[3]]), commonly_used_functions.generatePolynomialDisplay([solution[0]*solution[2], solution[1]]))
        return [z1, z0, factoredPolynomial]

def generate_distractor_3_values(solution, factors):
    bFactors = factors[0]
    #dFactors = factors[1]
    a = float(solution[0])
    b = float(solution[1])
    c = float(solution[2])
    d = float(solution[3])
    index = random.randint(0,len(bFactors)-1)
    b = float(b/(bFactors[index][0]))
    d = d*bFactors[index][0]
    z0 = float(-b/a)
    z1 = float(-d/c)
    intA = int(a)
    intB = int(b)
    intC = int(c)
    intD = int(d)
    if (z0<=z1):
        factoredPolynomial = "(%s)(%s)" %(commonly_used_functions.generatePolynomialDisplay([intA, intB]), commonly_used_functions.generatePolynomialDisplay([intC, intD]))
        return [z0, z1, factoredPolynomial]
    else:
        factoredPolynomial = "(%s)(%s)" %(commonly_used_functions.generatePolynomialDisplay([intC, intD]), commonly_used_functions.generatePolynomialDisplay([intA, intB]))
        return [z1, z0, factoredPolynomial]

def generate_distractor_4_values(solution, factors):
    #bFactors = factors[0]
    dFactors = factors[1]
    a = float(solution[0])
    b = float(solution[1])
    c = float(solution[2])
    d = float(solution[3])
    index = random.randint(0,len(dFactors)-1)
    d = float(d/(dFactors[index][0]))
    b = b*dFactors[index][0]
    z0 = float(-b/a)
    z1 = float(-d/c)
    intA = int(a)
    intB = int(b)
    intC = int(c)
    intD = int(d)
    if (z0<=z1):
        factoredPolynomial = "(%s)(%s)" %(commonly_used_functions.generatePolynomialDisplay([intA, intB]), commonly_used_functions.generatePolynomialDisplay([intC, intD]))
        return [z0, z1, factoredPolynomial]
    else:
        factoredPolynomial = "(%s)(%s)" %(commonly_used_functions.generatePolynomialDisplay([intC, intD]), commonly_used_functions.generatePolynomialDisplay([intA, intB]))
        return [z1, z0, factoredPolynomial]

def generate_all_option_dicts(solution_coefficients, factors):
    solution_s1, solution_s2, solution_polynomial_factored = generate_solution_values(solution_coefficients)
    display_solution = "x_1 = %.3f \\text{ and } x_2 = %.3f" %(solution_s1, solution_s2)
    solution_feedback = "* $%s$, which is the correct option. Obtained by solving the factored version $%s$." %(display_solution, solution_polynomial_factored)
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'solution',
        'Expected solution',
        [solution_s1, solution_s2], 
        display_solution,
        solution_feedback,
        1
    )

    distractor_1_s1, distractor_1_s2, distractor_1_polynomial_factored = generate_distractor_1_values(solution_coefficients)
    display_distractor_1 = "x_1 = %.3f \\text{ and } x_2 = %.3f" %(distractor_1_s1, distractor_1_s2)
    distractor_1_feedback = " $%s$, which corresponds to solving the factored version $%s$." %(display_distractor_1, distractor_1_polynomial_factored)
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_1',
        f'Misconception - Factored as if a=1 and c = a*c',
        [distractor_1_s1, distractor_1_s2],
        display_distractor_1,
        distractor_1_feedback,
        0
    )

    distractor_2_s1, distractor_2_s2, distractor_2_polynomial_factored = generate_distractor_2_values(solution_coefficients)
    display_distractor_2 = "x_1 = %.3f \\text{ and } x_2 = %.3f" %(distractor_2_s1, distractor_2_s2)
    distractor_2_feedback = " $%s$, which corresponds to solving the factored version $%s$." %(display_distractor_2, distractor_2_polynomial_factored)
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2',
        f'Misconception [unexpected] - Factored as if c=1 and a = a*c',
        [distractor_2_s1, distractor_2_s2],
        display_distractor_2,
        distractor_2_feedback,
        0
    )

    distractor_3_s1, distractor_3_s2, distractor_3_polynomial_factored = generate_distractor_3_values(solution_coefficients, factors)
    display_distractor_3 = "x_1 = %.3f \\text{ and } x_2 = %.3f" %(distractor_3_s1, distractor_3_s2)
    distractor_3_feedback = " $%s$, which corresponds to solving the factored version $%s$." %(display_distractor_3, distractor_3_polynomial_factored)
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        f'Arithmetic - product correct but sum for middle term not',
        [distractor_3_s1, distractor_3_s2],
        display_distractor_3,
        distractor_3_feedback,
        0
    )

    distractor_4_s1, distractor_4_s2, distractor_4_polynomial_factored = generate_distractor_4_values(solution_coefficients, factors)
    display_distractor_4 = "x_1 = %.3f \\text{ and } x_2 = %.3f" %(distractor_4_s1, distractor_4_s2)
    distractor_4_feedback = " $%s$, which corresponds to solving the factored version $%s$." %(display_distractor_4, distractor_4_polynomial_factored)
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_4',
        f'Arithmetic - product correct but sum for middle term not',
        [distractor_4_s1, distractor_4_s2],
        display_distractor_4,
        distractor_4_feedback,
        0
    )

    return [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]

def solve_quadratic_with_factoring_function(response_type):
    run_without_error = 0
    while run_without_error == 0:
        try:
            list_of_first_distractor_values = [0, 0, 0, 0]
            while len(list_of_first_distractor_values) != len(list(set(list_of_first_distractor_values))):
                minimum = 2
                maximum = 5
                numberOfFactors = 2
                factors = generate_factors(minimum, maximum, numberOfFactors)
                solution_coefficients = generate_solution_factor_coefficients(minimum, maximum, factors)

                all_dicts_list = generate_all_option_dicts(solution_coefficients, factors)
                list_of_first_distractor_values = []
                list_of_both_distractor_values = []
                for temp_dict in all_dicts_list:
                    temp_list_values = temp_dict['values_for_interval_generation']
                    list_of_first_distractor_values.append(temp_list_values[0])
                    list_of_both_distractor_values.append(temp_list_values)
                
                interval_options = interval_masking_method.createIntervalOptions(list_of_both_distractor_values, 5, 1)

                run_without_error = 1
        except Exception as e:
            print(e)
            pass

    index_counter = 0

    solution_dict = all_dicts_list[0]
    for temp_dict in all_dicts_list:
        temp_choice_interval_pairs = interval_options[index_counter]
        temp_interval_1 = commonly_used_functions.display_interval(temp_choice_interval_pairs[0])
        temp_interval_2 = commonly_used_functions.display_interval(temp_choice_interval_pairs[1])
        temp_dict[f'choice_presentation'] = "x_1 \\text{ in } %s \\text{ and } x_2 \\text{ in } %s" %(temp_interval_1, temp_interval_2)
        index_counter += 1

    presentation_order = ['solution', 'distractor_1', 'distractor_2', 'distractor_3', 'distractor_4']
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(all_dicts_list)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)

    ### DEFINE STEM, PROBLEM, AND GENERAL COMMENT ###
    if response_type=="Multiple-Choice":
        display_stem = 'Solve the quadratic equation below. Then, choose the intervals that the solutions $x_1$ and $x_2$ belong to, with $x_1 \\leq x_2$.'
    else:
        display_stem = 'Solve the quadratic equation below.'
    display_problem = commonly_used_functions.generatePolynomialDisplay(generate_quadratic_coefficients(solution_coefficients))
    general_comment = "This question can be factored, but it may be faster to find the solutions via the Quadratic Equation."

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
