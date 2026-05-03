import numpy as np
import pandas as pd
import math
import random

from utils import commonly_used_functions, interval_masking_method

code_name = 'solve_using_quadratic_formula'

def generate_solutions(coefficients):
    a, b, c = coefficients
    polynomial = np.poly1d([a, b, c])
    solution = polynomial.r
    return [min(solution[0], solution[1]), max(solution[0], solution[1])]

def find_discriminant(coefficients):
    a, b, c = coefficients
    return b**2 - 4*a*c

def is_square(integer):
    root = math.sqrt(integer)
    if int(root + 0.5) ** 2 == integer:
        return True
    else:
        return False

def generate_all_option_dicts(coefficients):
    a, b, c = coefficients
    solution_values = generate_solutions(coefficients)
    display_solution = "x_1 = %.3f \\text{ and } x_2 = %.3f" %(solution_values[0], solution_values[1])
    solution_feedback = "* $%s$, which is the correct option." %display_solution
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'solution',
        'Expected solution',
        solution_values, 
        display_solution,
        solution_feedback,
        1
    ) 

    distractor_1_values = generate_solutions([1, b, c])
    display_distractor_1 = "x_1 = %.3f \\text{ and } x_2 = %.3f" %(distractor_1_values[0], distractor_1_values[1])
    distractor_1_feedback = " $%s$, which corresponds to using the Quadratic Formula with $a=1$." %display_distractor_1
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_1',
        'Mechanical - Quadratic formula with a=1',
        distractor_1_values,
        display_distractor_1,
        distractor_1_feedback,
        0
    )

    distractor_2_values = generate_solutions([a, -b, c])
    display_distractor_2 = "x_1 = %.3f \\text{ and } x_2 = %.3f" %(distractor_2_values[0], distractor_2_values[1])
    distractor_2_feedback = " $%s$, which corresponds to using the Quadratic Formula as $\\frac{b \\pm \\sqrt{b^2 - 4ac}}{2a}$" %display_distractor_2
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2',
        'Mechanical - Quadratic formula with b in numerator',
        distractor_2_values,
        display_distractor_2,
        distractor_2_feedback,
        0
    )

    fA = float(a)
    fB = float(b)
    fC = float(c)
    distractor_3_values = [float(-fB/(2*fA) - math.sqrt(fB**2-4*fA*fC)), float(-fB/(2*fA) + math.sqrt(fB**2-4*fA*fC))]
    display_distractor_3 = "x_1 = %.3f \\text{ and } x_2 = %.3f" %(distractor_3_values[0], distractor_3_values[1])
    distractor_3_feedback = " $%s$, which corresponds to using the Quadratic Formula as $-\\frac{b}{2a} \\pm \\sqrt{b^2 - 4ac}$." %display_distractor_3
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        'Mechanical - Quadratic formula with a=1',
        distractor_3_values,
        display_distractor_3,
        distractor_3_feedback,
        0
    )

    distractor_4_feedback = " Corresponds to getting a negative under the radical or believing that since the quadratic cannot be factored, it has no Real solutions."
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_4',
        'Misconception or Mechanical - Cannot be factored means no solutions or negative under radical due to mechanical error',
        "There are no Real solutions",
        "\\text{There are no Real solutions}",
        distractor_4_feedback,
        0
    )
    distractor_4_dict['choice_presentation'] = '\\text{There are no Real solutions.}'

    return [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]

def solve_using_quadratic_formula_function(response_type):
    run_without_error = 0
    while run_without_error == 0:
        try:
            list_of_first_distractor_values = [0, 0, 0, 0]
            while len(list_of_first_distractor_values) != len(list(set(list_of_first_distractor_values))):
                discrim = 0
                while (discrim <= 0 or is_square(discrim)==True):
                    solution_coefficients = [
                        commonly_used_functions.maybeMakeNegative(random.randint(10, 20)), 
                        commonly_used_functions.maybeMakeNegative(random.randint(7, 15)), 
                        commonly_used_functions.maybeMakeNegative(random.randint(2, 9))
                        ]
                    discrim = find_discriminant(solution_coefficients)

                all_dicts_list = generate_all_option_dicts(solution_coefficients)
                list_of_first_distractor_values = []
                list_of_both_distractor_values = []
                for temp_dict in all_dicts_list:
                    if type(temp_dict['values_for_interval_generation']) == type(str()):
                        pass
                    else:
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
        if type(temp_dict['values_for_interval_generation']) == type(str()):
            pass
        else:
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
        display_stem = 'Solve the quadratic equation below. Then, choose the intervals that the solutions belong to, with $x_1 \\leq x_2$ (if they exist).'
    else:
        display_stem = 'Solve the quadratic equation below.'
    display_problem = commonly_used_functions.generatePolynomialDisplay(solution_coefficients)
    general_comment = "This requires Quadratic Formula. Just be sure to use the correct formula and watch your signs."

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