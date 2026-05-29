import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import os

from utils import commonly_used_functions, interval_masking_method

code_name = 'convert_quadratic_graph_to_equation'

def generate_all_option_dicts(coefficients, vertex):
    a, b, c = coefficients

    display_solution = commonly_used_functions.generatePolynomialDisplay(coefficients)
    solution_feedback = f"* ${display_solution}$, which is the correct option."
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'solution',
        'Expected solution',
        coefficients, 
        display_solution,
        solution_feedback,
        1
    )

    distractor_1_coeffs = [a, -b, c]
    display_distractor_1 = commonly_used_functions.generatePolynomialDisplay(distractor_1_coeffs)
    distractor_1_feedback = " $f(x)=%s$, which corresponds to incorrectly using vertex form as $f(x) = a(x+h)^2+k$." %display_distractor_1
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_1',
        'Misconception - Used form $f(x) = a(x+h)^2+k$',
        distractor_1_coeffs,
        display_distractor_1,
        distractor_1_feedback,
        0
    )

    distractor_2_coeffs = [-a, b, -c+2*vertex[1]]
    display_distractor_2 = commonly_used_functions.generatePolynomialDisplay(distractor_2_coeffs)
    distractor_2_feedback = " $f(x)=%s$, which corresponds to incorrectly using vertex form as $f(x) = a(x+h)^2+k$ AND making $a$ the opposite sign than it should be." %display_distractor_2
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2',
        'Misconception - Used form $f(x) = -a(x+h)^2+k$',
        distractor_2_coeffs,
        display_distractor_2,
        distractor_2_feedback,
        0
    )

    distractor_3_coeffs = [a, -b, c-2*vertex[1]]
    display_distractor_3 = commonly_used_functions.generatePolynomialDisplay(distractor_3_coeffs)
    distractor_3_feedback = " $f(x)=%s$, which corresponds to incorrectly using vertex form as $f(x) = a(x+h)^2 - k$." %display_distractor_3
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        'Misconception - Used form $f(x) = a(x+h)^2-k$',
        distractor_3_coeffs,
        display_distractor_3,
        distractor_3_feedback,
        0
    )

    distractor_4_coeffs = [-a, -b, -c+2*vertex[1]]
    display_distractor_4 = commonly_used_functions.generatePolynomialDisplay(distractor_4_coeffs)
    distractor_4_feedback = " $f(x)=%s$, which corresponds to making $a$ the opposite sign than it should be." %display_distractor_4
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_4',
        'Misconception - Used form $f(x) = -a(x-h)^2+k$',
        distractor_4_coeffs,
        display_distractor_4,
        distractor_4_feedback,
        0
    )

    return [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]

def graph_function_return_coefficents(a, vertex, version):
    #a * (x-vertex[0])**2 + vertex[1]
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
    plt.figure(1)
    graphX = np.arange(vertex[0] - 3, vertex[0] + 3, 0.01)
    graphY = a * (graphX-vertex[0])**2 + vertex[1]
    plt.plot(graphX, graphY, linewidth = 5, color = 	'#02325f')
    plt.plot( [ vertex[0] ], [ vertex[1] ], 'bs')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    base_dir = os.getcwd()
    figure_path = os.path.join(base_dir, 'temp_files', 'build_exams', 'figures', f'{code_name}_{version}.png')
    plt.savefig(figure_path, bbox_inches='tight')
    plt.close()
    return [a, -2*vertex[0]*a, a*(vertex[0]**2) +vertex[1]]

def convert_quadratic_graph_to_equation_function(response_type, interval_type, version):
    run_without_error = 0
    while run_without_error == 0:
        try:
            a = commonly_used_functions.maybeMakeNegative(1)
            vertex = [commonly_used_functions.maybeMakeNegative(random.randint(1, 2))*2, commonly_used_functions.maybeMakeNegative(random.randint(1, 5))*2]
            coefficients = graph_function_return_coefficents(a, vertex, version)
            list_of_dicts = generate_all_option_dicts(coefficients, vertex)

            option_value_list = []
            for temp_dict in list_of_dicts:
                option_value_list.append(temp_dict['values_for_interval_generation'])

            interval_options = interval_masking_method.createIntervalOptions(option_value_list, 3, 1)

            run_without_error = 1
        except:
            pass
   
    index_counter = 0
    solution_dict = list_of_dicts[0]
    for temp_dict in list_of_dicts:
        temp_choice_interval_pairs = interval_options[index_counter]
        temp_interval_1 = commonly_used_functions.display_interval(temp_choice_interval_pairs[0])
        temp_interval_2 = commonly_used_functions.display_interval(temp_choice_interval_pairs[1])
        temp_interval_3 = commonly_used_functions.display_interval(temp_choice_interval_pairs[2])
        temp_dict[f'choice_presentation'] = "a \\in %s, \\hspace{3mm} b \\in %s, \\text{ and } \\hspace{3mm} c \\in %s" %(temp_interval_1, temp_interval_2, temp_interval_3)
        index_counter += 1

    presentation_order = ['solution', 'distractor_1', 'distractor_2', 'distractor_3', 'distractor_4']
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(list_of_dicts)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)

    ### DEFINE STEM, PROBLEM, AND GENERAL COMMENT ###
    if (response_type=="Multiple-Choice") and (int(interval_type) == 1):
        display_stem = 'Write the equation of the graph presented below in the form $f(x)=ax^2+bx+c$, assuming  $a=1$ or $a=-1$. Then, choose the intervals that $a, b,$ and $c$ belong to.'
    else:
        display_stem = 'Write the equation of the graph presented below in the form $f(x)=ax^2+bx+c$, assuming  $a=1$ or $a=-1$.'
    display_problem = "\\text{Equation that was graphed:} f(x)= %s" %commonly_used_functions.generatePolynomialDisplay(coefficients)
    general_comment = "When the graph is pointing up, $a=1$. When the graph is pointing down, $a=-1$. Be sure to use Vertex Form: $y = a(x-h)^2+k$."

    display_stem_type="String"
    display_problem_type="Graph"
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