import random
import pandas as pd

from utils import commonly_used_functions, interval_masking_method

### DEFINITIONS ###
def display_complex_float(list_coefficients):
    a = list_coefficients[0]
    b = list_coefficients[1]
    
    if b < 0:
        if b == -1:
            display = "%.2f  - i" %a
        else:
            display = "%.2f  - %.2f i" %(a, -b)
    else:
        if b == 1:
            display = "%.2f + i" %a
        else:
            display = "%.2f  + %.2f i" %(a, b)
    return display

def generateProblemCoefficients():
    listIntegers = range(2, 11)
    constants = random.sample(listIntegers, 4)
    constants = [commonly_used_functions.maybeMakeNegative(i) for i in constants]
    a1, b1, a2, b2 = constants
    while (a1*b2 + b1*a2) == 0:
        constants = random.sample(listIntegers, 4)
        constants = [commonly_used_functions.maybeMakeNegative(i) for i in constants]
        a1, b1, a2, b2 = constants
    return constants

def generateSolutionAndDistractors(coefficients):
    a1, b1, a2, b2 = coefficients
    complex1 = complex(a1, b1)
    complex2 = complex(a2, b2)
    product = complex1*complex2

    solution = [int(product.real), int(product.imag)]
    solution_feedback = f'${display_complex_float(solution)}$, which is the correct option.'
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        'multiply_complex_numbers',
        'solution', 
        'Expected solution', 
        solution,
        display_complex_float(solution), 
        solution_feedback,
        1
    )

    distractor1Product = complex(a1, -b1)*complex(a2, b2)
    distractor_1 = [int(distractor1Product.real), int(distractor1Product.imag)]
    distractor_1_feedback = f'${display_complex_float(distractor_1)}$, which corresponds to adding a minus sign in the first term.'
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        'multiply_complex_numbers',
        'distractor_1', 
        'Adding a minus sign in the first term', 
        distractor_1,
        display_complex_float(distractor_1), 
        distractor_1_feedback,
        0
    )

    distractor2Product = complex(a1, b1)*complex(a2, -b2)
    distractor_2 = [int(distractor2Product.real), int(distractor2Product.imag)]
    distractor_2_feedback = f'${display_complex_float(distractor_2)}$, which corresponds to adding a minus sign in the second term.'
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        'multiply_complex_numbers',
        'distractor_2', 
        'Adding a minus sign in the second term', 
        distractor_2,
        display_complex_float(distractor_2), 
        distractor_2_feedback,
        0
    )

    distractor3Product = complex(a1, -b1)*complex(a2, -b2)
    distractor_3 = [int(distractor3Product.real), int(distractor3Product.imag)]
    distractor_3_feedback = f'${display_complex_float(distractor_3)}$, which corresponds to adding a minus sign to both term.'
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        'multiply_complex_numbers',
        'distractor_3', 
        'Adding a minus sign in both terms', 
        distractor_3,
        display_complex_float(distractor_3), 
        distractor_3_feedback,
        0
    )

    distractor4Product = complex(a1*a2, b1*b2)
    distractor_4 = [int(distractor4Product.real), int(distractor4Product.imag)]
    distractor_4_feedback = f'${display_complex_float(distractor_4)}$, which corresponds to just multiplying the real terms to get the real part of the solution and the coefficients in the complex terms to get the complex part.'
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        'multiply_complex_numbers',
        'distractor_4', 
        'Multiplying like coefficient terms only', 
        distractor_4,
        display_complex_float(distractor_4), 
        distractor_4_feedback,
        0
    )

    return [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]


def multiply_complex_numbers_function(response_type):
    run_without_error = 0
    while run_without_error == 0:
        try:
            problemCoefficients = generateProblemCoefficients()
            solution_dicts_list = generateSolutionAndDistractors(problemCoefficients)
            solution_dict = solution_dicts_list[0]

            ### CREATE INTERVAL OPTIONS ###
            option_value_list = []
            for temp_dict in solution_dicts_list:
                option_value_list.append(temp_dict['values_for_interval_generation'])

            interval_options = interval_masking_method.createIntervalOptions(option_value_list, 5, 1)
            run_without_error = 1
        except:
            pass
    
    index_counter = 0
    for dict in solution_dicts_list:
        temp_choice_interval_pairs = interval_options[index_counter]
        temp_interval_1 = commonly_used_functions.display_interval(temp_choice_interval_pairs[0])
        temp_interval_2 = commonly_used_functions.display_interval(temp_choice_interval_pairs[1])
        dict[f'choice_presentation'] = "a \\in %s \\text{ and } b \\in %s" %(temp_interval_1, temp_interval_2)
        index_counter += 1

    presentation_order = ['solution', 'distractor_1', 'distractor_2', 'distractor_3', 'distractor_4']
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(solution_dicts_list)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)

    ### DEFINE STEM, PROBLEM, AND GENERAL COMMENT ###
    if response_type=="Multiple-Choice":
        display_stem = 'Simplify the expression below into the form $a+bi$. Then, choose the intervals that $a$ and $b$ belong to.'
    else:
        display_stem = 'Simplify the expression below into the form $a+bi$.'
    display_problem = "(%s)(%s)" %(display_complex_float([problemCoefficients[0], problemCoefficients[1]]), display_complex_float([problemCoefficients[2], problemCoefficients[3]]))
    general_comment = "You can treat $i$ as a variable and distribute. Just remember that $i^2=-1$, so you can continue to reduce after you distribute."


    display_stem_type="String"
    display_problem_type="Math Mode"
    display_options_type="Math Mode"

    question_dict = {
        'code_name': 'multiply_complex_numbers',
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