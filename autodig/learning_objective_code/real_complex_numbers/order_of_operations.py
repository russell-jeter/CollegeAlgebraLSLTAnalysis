import random
import pandas as pd

from utils import commonly_used_functions, interval_masking_method

### DEFINITIONS ###
def createCoefficients():
    listNaturals=list(range(1, 21))
    constants = random.sample(listNaturals, 6)
    return constants

def generate_structure_0():
    c1, c2, c3, c4, c5, c6 = createCoefficients()
    solution = float((c1 - ( float(c2/c3) * c4 ) ) - ( c5 * c6 ))
    distractor_1 = float(c1 - float(c2 / (c3 * c4) ) - (c5 * c6))
    distractor_2 =  float(c1 - float(c2 / (c3 * c4)) + c5 * c6)
    distractor_3 =  float(((c1 - (float(c2/c3) * c4)) - c5) * c6)
    solutionList = [solution, distractor_1, distractor_2, distractor_3]
    while commonly_used_functions.checkUnique(solutionList)=="Copies":
        c1, c2, c3, c4, c5, c6 = createCoefficients()
        solution = float((c1 - (float(c2/c3) * c4)) - (c5 * c6))
        distractor_1 = float(c1 - float(c2 / (c3 * c4) ) - (c5 * c6))
        distractor_2 =  float(c1 - float(c2 / (c3 * c4)) + c5 * c6)
        distractor_3 =  float(((c1 - (float(c2/c3) * c4)) - c5) * c6)
        solutionList = [solution, distractor_1, distractor_2, distractor_3]

    display_problem = '%d - %d \\div %d * %d - (%d * %d)' %(c1, c2, c3, c4, c5, c6)

    solution_feedback = f'${round(solution, 3)}$, which is the correct option.'
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        'order_of_operations',
        'solution', 
        'Expected solution', 
        solution,
        round(solution, 3), 
        solution_feedback,
        1
    )

    distractor_1_feedback = f'${round(distractor_1, 3)}$, which corresponds to an Order of Operations error: not reading left-to-right for multiplication/division.'
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        'order_of_operations',
        'distractor_1', 
        'PEMDAS: Not reading left-to-right for MD', 
        distractor_1,
        round(distractor_1, 3), 
        distractor_1_feedback,
        0
    )

    distractor_2_feedback = f'${round(distractor_2, 3)}$, which corresponds to not distributing addition and subtraction correctly.'
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        'order_of_operations',
        'distractor_2', 
        'Not distributing addition/subtraction correctly', 
        distractor_2,
        round(distractor_2, 3), 
        distractor_2_feedback,
        0
    )

    distractor_3_feedback = f'${round(distractor_3, 3)}$, which corresponds to not distributing a negative correctly.'
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        'order_of_operations',
        'distractor_3', 
        'Not distributing addition/subtraction correctly', 
        distractor_3,
        round(distractor_3, 3), 
        distractor_3_feedback,
        0
    )

    distractor_4_feedback = " You may have gotten this by making an unanticipated error. If you got a value that is not any of the others, please let the coordinator know so they can help you figure out what happened."
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        'order_of_operations',
        'distractor_4', 
        'Catch-all none of the above, unknown thinking', 
        'None of the above',
        '\\text{None of the above}', 
        distractor_4_feedback,
        0
    )

    solution_dicts_list = [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]

    return [solution_dicts_list, display_problem]

def generate_structure_1():
    c1, c2, c3, c4, c5, c6 = createCoefficients()
    solution = float( c1 - c2**2 + float(c3/c4) * float(c5/c6) )
    distractor_1 = float( c1 + c2**2 + float(c3/c4) * float(c5/c6) )
    distractor_2 =  float( c1 - c2**2 + float(c3 / float(c4*c5))/c6 )
    distractor_3 =  float( c1 + c2**2 + float(c3 / float(c4*c5))/c6 )
    solutionList = [solution, distractor_1, distractor_2, distractor_3]

    while commonly_used_functions.checkUnique(solutionList)=="Copies":
        c1, c2, c3, c4, c5, c6 = createCoefficients()
        solution = float( c1 - c2**2 + float(c3/c4) * float(c5/c6) )
        distractor_1 = float( c1 + c2**2 + float(c3/c4) * float(c5/c6) )
        distractor_2 =  float( c1 - c2**2 + float(c3 / float(c4*c5))/c6 )
        distractor_3 =  float( c1 + c2**2 + float(c3 / float(c4*c5))/c6 )
        solutionList = [solution, distractor_1, distractor_2, distractor_3]

    display_problem = '%d - %d^2 + %d \\div %d * %d \\div %d' %(c1, c2, c3, c4, c5, c6)

    solution_feedback = f'${round(solution, 3)}$, which is the correct option.'
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        'order_of_operations',
        'solution', 
        'Expected solution', 
        solution,
        round(solution, 3), 
        solution_feedback,
        1
    )

    distractor_1_feedback = f'${round(distractor_1, 3)}$, which corresponds to an Order of Operations error: multiplying by negative before squaring. For example: $(-3)^2 \\neq -3^2$'
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        'order_of_operations',
        'distractor_1', 
        'PEMDAS: Multiplying by negative before squaring. For example: $(-3)^2 \\neq -3^2$', 
        distractor_1,
        round(distractor_1, 3), 
        distractor_1_feedback,
        0
    )

    distractor_2_feedback = f'${round(distractor_2, 3)}$, which corresponds to an Order of Operations error: not reading left-to-right for multiplication/division.'
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        'order_of_operations',
        'distractor_2', 
        'PEMDAS: Not reading left-to-right for MD', 
        distractor_2,
        round(distractor_2, 3), 
        distractor_2_feedback,
        0
    )

    distractor_3_feedback = f'${round(distractor_3, 3)}$, which corresponds to two Order of Operations errors: multiplying by negative before squaring and not reading left-to-right for multiplication/division.'
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        'order_of_operations',
        'distractor_3', 
        'PEMDAS: Multiplying by negative before squaring AND not reading left-to-right for MD', 
        distractor_3,
        round(distractor_3, 3), 
        distractor_3_feedback,
        0
    )

    distractor_4_feedback = " You may have gotten this by making an unanticipated error. If you got a value that is not any of the others, please let the coordinator know so they can help you figure out what happened."
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        'order_of_operations',
        'distractor_4', 
        'Catch-all none of the above, unknown thinking', 
        'None of the above',
        'None of the above', 
        distractor_4_feedback,
        0
    )

    solution_dicts_list = [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]

    return [solution_dicts_list, display_problem]

def order_of_operations_function(response_type):
    run_without_error = 0
    while run_without_error == 0:
        try:
            chooseStructureType = random.randint(0, 1)
            if chooseStructureType == 0:
                solution_dicts_list, display_problem = generate_structure_0()
            else:
                solution_dicts_list, display_problem = generate_structure_1()

            ### CREATE INTERVAL OPTIONS ###
            option_value_list = []
            for temp_dict in solution_dicts_list:
                if temp_dict['name'] == 'distractor_4':
                    # Do not pass "None of the above" for interval generation
                    pass
                else:
                    option_value_list.append(temp_dict['values_for_interval_generation'])

            interval_options = interval_masking_method.createIntervalOptions(option_value_list, 5, 1)
            run_without_error = 1
        except Exception as e: 
            print(e)
            pass

    ### DEFINE ANSWERLIST AND DISPLAYSOLUTION ###
    solution_dict = solution_dicts_list[0]
    index_counter = 0
    for dict in solution_dicts_list:
        if index_counter == len(solution_dicts_list) - 1:
            dict[f'choice_presentation'] = '\\text{None of the above}'
        else:
            temp_choice_interval_pairs = interval_options[index_counter]
            temp_interval_1 = commonly_used_functions.display_interval(temp_choice_interval_pairs)
            dict[f'choice_presentation'] = f'{temp_interval_1}'
            index_counter += 1

    presentation_order = ['solution', 'distractor_1', 'distractor_2', 'distractor_3', 'distractor_4']
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(solution_dicts_list)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)       

    ### DEFINE STEM, PROBLEM, GENERAL COMMENT ###
    if response_type=="Multiple-Choice":
        display_stem = 'Simplify the expression below and choose the interval the simplification is contained within.'
    else:
        display_stem = 'Simplify the expression below.'
    # displayProblem was already defined
    general_comment = "While you may remember (or were taught) PEMDAS is done in order, it is actually done as P/E/MD/AS. When we are at MD or AS, we read left to right."

    display_stem_type="String"
    display_problem_type="Math Mode"
    display_options_type="Math Mode"

    question_dict = {
        'code_name': 'order_of_operations',
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