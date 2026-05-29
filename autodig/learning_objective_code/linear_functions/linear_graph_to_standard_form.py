import random
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import os

from utils import commonly_used_functions, interval_masking_method

code_name = 'linear_graph_to_standard_form'

### DEFINITIONS ###
def simplifySolution(A, B, C):
    if(A < 0):
        A = -A; B = -B; C = -C # math.gcd does not like negative values
    GCD_A_B = math.gcd(A, B)
    GCD_B_C = math.gcd(B, C)
    mixed_GCD = math.gcd(GCD_A_B, GCD_B_C)
    while(mixed_GCD > 1):
        A = int(A/mixed_GCD)
        B = int(B/mixed_GCD)
        C = int(C/mixed_GCD)
        GCD_A_B = math.gcd(A, B)
        GCD_B_C = math.gcd(B, C)
        mixed_GCD = math.gcd(GCD_A_B, GCD_B_C)
    return [A, B, C]

def generateProblemAndSolution(numeratorMax, interceptMax):
    numeratorSlope = commonly_used_functions.maybeMakeNegative(random.randint(2, numeratorMax))
    denominatorSlope = random.randint(2, numeratorMax)
    # Makes sure slope is rational
    while math.gcd(numeratorSlope, denominatorSlope) > 1:
        numeratorSlope = commonly_used_functions.maybeMakeNegative(random.randint(2, numeratorMax))
        denominatorSlope = random.randint(2, numeratorMax)
    slopeGraph = float(numeratorSlope)/float(denominatorSlope)
    yInt = random.randint(-interceptMax, interceptMax)
    point2 = [denominatorSlope, slopeGraph*denominatorSlope + yInt]
    point3 = [-denominatorSlope, -slopeGraph*denominatorSlope + yInt]
    # Converts to Stadard Form
    if slopeGraph > 0:
        aOfGraph = -numeratorSlope
        bOfGraph = denominatorSlope
        cOfGraph = denominatorSlope*yInt
    else:
        aOfGraph = numeratorSlope
        bOfGraph = -denominatorSlope
        cOfGraph = -denominatorSlope*yInt
    return [simplifySolution(aOfGraph, bOfGraph, cOfGraph), [slopeGraph, yInt], point2, point3]

def clean_display_of_equation(coefficients):
    A, B, C = coefficients
    if B < 0:
        standardForm = "%sx - %sy = %s" %(A, -B, C)
    else:
        standardForm = "%sx + %sy = %s" %(A, B, C)
    return standardForm

def generate_all_option_dicts(solution):
    A, B, C = solution

    display_solution = clean_display_of_equation(solution)
    solution_feedback = f"* ${display_solution}$, which is the correct option."
    solution_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'solution',
        'Expected solution',
        solution, 
        display_solution,
        solution_feedback,
        1
    )

    distractor_1 = [-A, -B, -C]
    display_distractor_1 = clean_display_of_equation(distractor_1)
    distractor_1_feedback = f" ${display_distractor_1}$, which corresponds to not making $A$ positive (by multiplying the equation by $-1$)."
    distractor_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_1',
        'Mechanical - A is not made positive',
        distractor_1,
        display_distractor_1,
        distractor_1_feedback,
        0
    )

    distractor_2 = [A, -B, -C]
    display_distractor_2 = clean_display_of_equation(distractor_2)
    distractor_2_feedback = f" ${display_distractor_2}$, which corresponds to using the opposite (negative) slope of the graph, but did everything else correctly."
    distractor_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_2', 
        'Arithmetic error - Negative slope',
        distractor_2,
        display_distractor_2,
        distractor_2_feedback, 
        0
    ) 

    distractor_3 = [round(float(A/B), 3), 1, round(float(C)/float(B), 3)]
    display_distractor_3 = clean_display_of_equation(distractor_3)
    distractor_3_feedback = f" ${display_distractor_3}$, which corresponds to not removing rational values for Standard Form."
    distractor_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_3',
        'Conceptual error - does not remove rational values for Standard Form',
        distractor_3, 
        display_distractor_3, 
        distractor_3_feedback,
        0
    )

    distractor_4 =  [round(float(A/B), 3), -1, round(-float(C)/float(B), 3)]
    display_distractor_4 = clean_display_of_equation(distractor_4)
    distractor_4_feedback = f" ${display_distractor_4}$, which corresponds to using the opposite (negative) slope of the graph and not removing rational values."
    distractor_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        code_name, 
        'distractor_4', 
        'Arithmetic error - Negative slope; Conceptual error - does not remove rational values for Standard Form',
        distractor_4, 
        display_distractor_4,
        distractor_4_feedback,
        0
    )

    list_of_dicts = [solution_dict, distractor_1_dict, distractor_2_dict, distractor_3_dict, distractor_4_dict]
    return list_of_dicts

#########################
def plotGraph(slopeGraph, yInt, point2, point3, version):
    graphX = np.arange(-5.0, 5.0, 0.01)
    graphY = slopeGraph*graphX + yInt
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
    plt.plot(graphX, graphY, linewidth = 5, color = '#02325f')
    plt.plot([point2[0]], [point2[1]], 'bo', markersize=20)
    plt.plot([point3[0]], [point3[1]], 'bo', markersize=20)
    #
    if slopeGraph > 0:
        #plt.text(0, yInt, "[0, %s]" %yInt, fontsize=28, horizontalalignment='right')
        plt.text(point2[0], point2[1], "[%d, %d]" %(point2[0], point2[1]), fontsize=28, horizontalalignment='right')
        plt.text(point3[0], point3[1], "[%d, %d]" %(point3[0], point3[1]), fontsize=28, horizontalalignment='right')
    else:
        #plt.text(0, yInt, "[0, %s]" %yInt, fontsize=28)
        plt.text(point2[0], point2[1], "[%d, %d]" %(point2[0], point2[1]), fontsize=28)
        plt.text(point3[0], point3[1], "[%d, %d]" %(point3[0], point3[1]), fontsize=28)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)

    base_dir = os.getcwd()
    figure_path = os.path.join(base_dir, 'temp_files', 'build_exams', 'figures', f'{code_name}_{version}.png')
    plt.savefig(figure_path, bbox_inches='tight')
    plt.close()
    return

def linear_graph_to_standard_form_function(response_type, interval_type, version):
    run_without_error = 0
    while run_without_error == 0:
        try:
            numeratorMax = 5
            interceptMax = 5
            solution, slopeInt, point2, point3 = generateProblemAndSolution(numeratorMax, interceptMax)
            plotGraph(slopeInt[0], slopeInt[1], point2, point3, version)

            distractor_dicts = generate_all_option_dicts(solution)

            option_value_list = []
            for temp_dict in distractor_dicts:
                option_value_list.append(temp_dict['values_for_interval_generation'])

            interval_options = interval_masking_method.createIntervalOptions(option_value_list, 1, 0.5)
            # interval_options returns 5 groups of 2 pairs of interval endings

            run_without_error = 1
        except:
            pass

    index_counter = 0
    solution_dict = distractor_dicts[0]
    for temp_dict in distractor_dicts:
        temp_choice_interval_pairs = interval_options[index_counter]
        temp_interval_1 = commonly_used_functions.display_interval(temp_choice_interval_pairs[0])
        temp_interval_2 = commonly_used_functions.display_interval(temp_choice_interval_pairs[1])
        temp_interval_3 = commonly_used_functions.display_interval(temp_choice_interval_pairs[2])
        temp_dict[f'choice_presentation'] = "A \\in %s, \\hspace{3mm} B \\in %s, \\text{ and } \\hspace{3mm} C \\in %s" %(temp_interval_1, temp_interval_2, temp_interval_3)
        index_counter += 1

    presentation_order = ['solution', 'distractor_1', 'distractor_2', 'distractor_3', 'distractor_4']
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(distractor_dicts)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)

    ### DEFINE STEM, PROBLEM, AND GENERAL COMMENT ###
    if (response_type=="Multiple-Choice") and (int(interval_type) == 1):
        display_stem = 'Write the equation of the line in the graph below in Standard Form $Ax+By=C$. Then, choose the intervals that contain $A, B, \\text{ and } C$.'
    else:
        display_stem = "Write the equation of the line in the graph below in Standard Form $Ax+By=C$."
    display_problem = "\\text{Equation that was graphed:} f(x)= %s" %commonly_used_functions.generatePolynomialDisplay(slopeInt)
    general_comment = "Standard form is supposed to have $A > 0$ and all fractions removed."

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