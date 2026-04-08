import random
import pandas as pd

from utils import commonly_used_functions, interval_masking_method

def generateDistinctCoefficients():
    listIntegers = [i for i in range(1, 9)]
    constants = random.sample(listIntegers, 4)
    constants = [commonly_used_functions.maybeMakeNegative(i) for i in constants]
    return constants

def round_set_of_floats(pairs_of_floats, round_to):
    return [[round(value[0], round_to), round(value[1], round_to)] for value in pairs_of_floats]

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

def generate_distractors_and_feedback(coefficients):
    a1, b1, a2, b2 = coefficients

    # Divide like terms
    distractor_1 = [float(a1/a2), float(b1/b2)]
    distractor_1_feedback = f" ${display_complex_float(distractor_1)}$, which corresponds to just dividing the first term by the first term and the second by the second."
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        'divide_complex_numbers',
        'distractor_1', 
        'Divide like terms', 
        distractor_1,
        display_complex_float(distractor_1), 
        distractor_1_feedback,
        0
    )

    # Multiply by non-conjugate and treat like conjugate in denominator
    quotientD2 = ( complex(a1, b1) * complex(a2, b2) ) / ( complex(a2, b2) * complex(a2, -b2) )
    distractor_2 = [quotientD2.real, quotientD2.imag]
    distractor_2_feedback = f" ${display_complex_float(distractor_2)}$, which corresponds to forgetting to multiply the conjugate by the numerator and not computing the conjugate correctly."
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        'divide_complex_numbers',
        'distractor_2', 
        'Multiply by non-conjugate and treat like conjugate in denominator',
        distractor_2,
        display_complex_float(distractor_2), 
        distractor_2_feedback,
        0
    )

    # Multiply by conjugate, only divide first term
    numeratorD3 = complex(a1, b1) * complex(a2, -b2)
    denominatorD3 = complex(a2, b2) * complex(a2, -b2)
    realTermD3 = float(numeratorD3.real / denominatorD3.real)
    imagTermD3 = float(numeratorD3.imag)
    distractor_3 = [realTermD3, imagTermD3]
    distractor_3_feedback = f" ${display_complex_float(distractor_3)}$, which corresponds to forgetting to multiply the conjugate by the numerator."
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        'divide_complex_numbers',
        'distractor_3',
        'Multiply by conjugate, only divide first term',
        distractor_3,
        display_complex_float(distractor_3),
        distractor_3_feedback,
        0
    )

    # Multiply by conjugate, only divide second term
    numeratorD4 = complex(a1, b1) * complex(a2, -b2)
    denominatorD4 = complex(a2, b2) * complex(a2, -b2)
    realTermD4 = float(numeratorD4.real)
    imagTermD4 = float(numeratorD4.imag / denominatorD4.real)
    distractor_4 = [realTermD4, imagTermD4]
    distractor_4_feedback = f" ${display_complex_float(distractor_4)}$, which corresponds to forgetting to multiply the conjugate by the numerator and using a plus instead of a minus in the denominator."
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        'divide_complex_numbers',
        'distractor_4',
        'Multiply by conjugate, only divide second term',
        distractor_4,
        display_complex_float(distractor_4),
        distractor_4_feedback,
        0
    )

    return [distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]

def generateProblemCoefficientsAndSolution():
    complex1 = complex(0,0)
    complex2 = complex(0,0)
    while complex1==complex2:
        initialCoefficients = generateDistinctCoefficients()
        a1, b1, a2, b2 = initialCoefficients
        a1 = 9 * a1
        b1 = 11 * b1
        complex1=complex(a1, b1)
        complex2=complex(a2, b2)
        coefficients=[a1, b1, a2, b2]
        quotient=complex1/complex2
        solution = [quotient.real, quotient.imag]
        solution_feedback = f' ${display_complex_float(solution)}$, which is the correct option.'
        solution_dict = commonly_used_functions.value_and_feedback_to_dict(
            'divide_complex_numbers',
            'solution',
            'Expected solution',
            solution,
            display_complex_float(solution),
            solution_feedback,
            1
        )
    return [coefficients, solution_dict]

def divide_complex_numbers_function(response_type):
    coefficients, solution_dict = generateProblemCoefficientsAndSolution()
    distractor_dicts = generate_distractors_and_feedback(coefficients)
    # In the future, I need to do something to check if the distractors are far enough apart.

    ### CREATE INTERVAL OPTIONS ###
    option_value_list = [solution_dict['values_for_interval_generation']]
    for temp_dict in distractor_dicts:
        option_value_list.append(temp_dict['values_for_interval_generation'])

    interval_options = interval_masking_method.createIntervalOptions(option_value_list, 1, 0.5)
    # interval_options returns 5 groups of 2 pairs of interval endings

    list_of_dicts = [solution_dict] + distractor_dicts
    index_counter = 0
    for dict in list_of_dicts:
        temp_choice_interval_pairs = interval_options[index_counter]
        temp_interval_1 = commonly_used_functions.display_interval(temp_choice_interval_pairs[0])
        temp_interval_2 = commonly_used_functions.display_interval(temp_choice_interval_pairs[0])
        dict[f'choice_presentation'] = "a \\in %s \\text{ and } b \\in %s", (temp_interval_1, temp_interval_2)
        index_counter+=1

    presentation_order = ['solution', 'distractor_1', 'distractor_2', 'distractor_3', 'distractor_4']
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(list_of_dicts)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)

    ### DEFINE STEM, PROBLEM, AND GENERAL COMMENT ###
    if response_type=="Multiple-Choice":
        display_stem = 'Simplify the expression below into the form $a+bi$. Then, choose the intervals that $a$ and $b$ belong to.'
    else:
        display_stem = 'Simplify the expression below into the form $a+bi$.'
    display_problem = "\\frac{%s}{%s}" %(display_complex_float([coefficients[0], coefficients[1]]), display_complex_float([coefficients[2], coefficients[3]]))
    general_comment = "Multiply the numerator and denominator by the *conjugate* of the denominator, then simplify. For example, if we have $2+3i$, the conjugate is $2-3i$."

    display_stem_type="String"
    display_problem_type="Math Mode"
    display_options_type="Math Mode"

    question_dict = {
        'code_name': 'divide_complex_numbers',
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