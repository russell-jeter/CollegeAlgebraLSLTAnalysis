import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import os

from utils import commonly_used_functions, interval_masking_method

code_name = 'convert_quadratic_equation_to_graph'

def put_dicts_in_order(list_of_dicts):
    correct_order = ['A', 'B', 'C', 'D', 'E']
    ordered_dicts = []
    for ordered_letter in correct_order:
        for temp_dict in list_of_dicts:
            if temp_dict['letter'] == ordered_letter:
                ordered_dicts.append(temp_dict)
                break
    return ordered_dicts

def generate_display_problem(aCoeffFtG, vertexFtG):
    if aCoeffFtG < 0:
        if vertexFtG[0] < 0:
            if vertexFtG[1] < 0:
                displayProblem = 'f(x) = -(x+%s)^2 - %s' %(-vertexFtG[0], -vertexFtG[1])
            else:
                displayProblem = 'f(x) = -(x+%s)^2 + %s' %(-vertexFtG[0], vertexFtG[1])
        else:
            if vertexFtG[1] < 0:
                displayProblem = 'f(x) = -(x-%s)^2 - %s' %(vertexFtG[0], -vertexFtG[1])
            else:
                displayProblem = 'f(x) = -(x-%s)^2 + %s' %(vertexFtG[0], vertexFtG[1])
    else:
        if vertexFtG[0] < 0:
            if vertexFtG[1] < 0:
                displayProblem = 'f(x) = (x+%s)^2 - %s' %(-vertexFtG[0], -vertexFtG[1])
            else:
                displayProblem = 'f(x) = (x+%s)^2 + %s' %(-vertexFtG[0], vertexFtG[1])
        else:
            if vertexFtG[1] < 0:
                displayProblem = 'f(x) = (x-%s)^2 - %s' %(vertexFtG[0], -vertexFtG[1])
            else:
                displayProblem = 'f(x) = (x-%s)^2 + %s' %(vertexFtG[0], vertexFtG[1])
    return displayProblem

def generate_graphs_and_option_dicts(aCoeffFtG, vertexFtG, version):
    base_dir = os.getcwd()

    figure_letter_list = ['A', 'B', 'C', 'D']
    random.shuffle(figure_letter_list)

    xPlot = np.arange(-5, 5, 0.01)
    graphX = np.arange(-5, 5, 0.01)

    solutionGraph = aCoeffFtG* (xPlot-vertexFtG[0])**2 + vertexFtG[1]
    SMALL_SIZE = 24
    MEDIUM_SIZE = 28
    BIGGER_SIZE = 32

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    showPlot = plt.plot(graphX, solutionGraph, linewidth = 5, color = 	'#02325f')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    figure_path_0 = os.path.join(base_dir, 'temp_files', 'build_exams', 'figures', f'{code_name}_{figure_letter_list[0]}_{version}.png')
    plt.savefig(figure_path_0, bbox_inches='tight')
    plt.close()

    display_solution = generate_display_problem(aCoeffFtG, vertexFtG)
    solution_feedback = "* Correct option."
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'solution',
        'Expected solution',
        display_solution, 
        f'Graph of {display_solution}',
        solution_feedback,
        1
    )
    solution_dict['letter'] = figure_letter_list[0]
    solution_dict['choice_presentation'] = f'{code_name}_{figure_letter_list[0]}_{version}.png'

    # a(x+h)^2+k
    postiveHdistractor = aCoeffFtG* (xPlot+vertexFtG[0])**2 + vertexFtG[1]
    showPlot = plt.plot(graphX, postiveHdistractor, linewidth = 5, color = 	'#02325f')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    figure_path_1 = os.path.join(base_dir, 'temp_files', 'build_exams', 'figures', f'{code_name}_{figure_letter_list[1]}_{version}.png')
    plt.savefig(figure_path_1, bbox_inches='tight')
    plt.close()

    display_option_1 = generate_display_problem(aCoeffFtG, [-vertexFtG[0], vertexFtG[1]])
    option_1_feedback = " Used the incorrect general form $f(x) = a(x+h)^2 + k$"
    option_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_1',
        'Misconception - general form $f(x) = a(x+h)^2 + k$',
        display_option_1, 
        f'Graph of {display_option_1}',
        option_1_feedback,
        0
    )
    option_1_dict['letter'] = figure_letter_list[1]
    option_1_dict['choice_presentation'] = f'{code_name}_{figure_letter_list[1]}_{version}.png'

    # -a(x-h)^2+k
    negativeAdistractor = -aCoeffFtG* (xPlot-vertexFtG[0])**2 + vertexFtG[1]
    showPlot = plt.plot(graphX, negativeAdistractor, linewidth = 5, color = '#02325f')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    figure_path_2 = os.path.join(base_dir, 'temp_files', 'build_exams', 'figures', f'{code_name}_{figure_letter_list[2]}_{version}.png')
    plt.savefig(figure_path_2, bbox_inches='tight')
    plt.close()

    display_option_2 = generate_display_problem(-aCoeffFtG, vertexFtG)
    option_2_feedback = " Used the incorrect general form $f(x) = -a(x-h)^2 + k$"
    option_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2',
        'Misconception - general form $f(x) = -a(x-h)^2 + k$',
        display_option_2, 
        f'Graph of {display_option_2}',
        option_2_feedback,
        0
    )
    option_2_dict['letter'] = figure_letter_list[2]
    option_2_dict['choice_presentation'] = f'{code_name}_{figure_letter_list[2]}_{version}.png'

    #-a(x+h)^2+k
    negativeApositiveHdistractor = -aCoeffFtG* (xPlot+vertexFtG[0])**2 + vertexFtG[1]
    showPlot = plt.plot(graphX, negativeApositiveHdistractor, linewidth = 5, color = 	'#02325f')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    figure_path_3 = os.path.join(base_dir, 'temp_files', 'build_exams', 'figures', f'{code_name}_{figure_letter_list[3]}_{version}.png')
    plt.savefig(figure_path_3, bbox_inches='tight')
    plt.close()

    display_option_3 = generate_display_problem(-aCoeffFtG, vertexFtG)
    option_3_feedback = " Used the incorrect general form $f(x) = -a(x+h)^2 + k$"
    option_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        'Misconception - general form $f(x) = -a(x-h)^2 + k$',
        display_option_3, 
        f'Graph of {display_option_2}',
        option_3_feedback,
        0
    )
    option_3_dict['letter'] = figure_letter_list[3]
    option_3_dict['choice_presentation'] = f'{code_name}_{figure_letter_list[3]}_{version}.png'

    option_4_feedback = " You likely thought the vertex did not correspond to the equation."
    option_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_4', 
        'Catch all - Unexpected vertex placement?',
        'None of the above', 
        'None of the above',
        option_4_feedback,
        0
    )
    option_4_dict['letter'] = 'E'
    option_4_dict['choice_presentation'] = 'None of the above'

    option_dicts = [solution_dict, option_1_dict, option_2_dict, option_3_dict, option_4_dict]
    return option_dicts

def convert_quadratic_equation_to_graph_function(response_type, version):
    aCoeffFtG = commonly_used_functions.maybeMakeNegative(random.randint(1, 4))
    vertexFtG = [0, 0]
    vertexFtG[0] = commonly_used_functions.maybeMakeNegative(random.randint(1, 4))
    vertexFtG[1] = commonly_used_functions.maybeMakeNegative(random.randint(10, 20))

    option_dicts = generate_graphs_and_option_dicts(aCoeffFtG, vertexFtG, version)
    solution_dict = option_dicts[0]

    ordered_option_dicts = put_dicts_in_order(option_dicts)

    presentation_order = []
    for temp_dict in ordered_option_dicts:
        presentation_order.append(temp_dict['name'])

    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(ordered_option_dicts)

    if response_type=="Multiple-Choice":
        display_stem = 'Choose the graph of the equation below.'
    else:
        display_stem = 'Graph the equation below.'

    display_problem = generate_display_problem(aCoeffFtG, vertexFtG)
    general_comment = "Remember that Vertex Form is $y = a(x-h)^2+k$, where the vertex is $(h, k)$."

    display_stem_type="String"
    display_problem_type="Math Mode"
    display_options_type="Graph"

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