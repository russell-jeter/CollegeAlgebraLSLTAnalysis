import random
import pandas as pd
from math import gcd
from utils import commonly_used_functions, interval_masking_method

### DEFINITIONS ###
def generateWhole():
    denominatorbase = random.randint(5, 25)
    numeratorbase = denominatorbase * random.randint(5, 25)
    denominator = denominatorbase * denominatorbase
    numerator = numeratorbase * numeratorbase
    displayProblem =  '\\sqrt{\\frac{%d}{%d}}' %(numerator, denominator)
    simplifiedNumber = numeratorbase
    return [displayProblem, simplifiedNumber]

def generateInteger():
    denominatorbase = random.randint(5, 25)
    numeratorbase = denominatorbase * random.randint(5, 25) # Makes sure we return a natural number
    denominator = denominatorbase * denominatorbase # Makes perfect squares
    numerator = numeratorbase * numeratorbase
    displayProblem =  '-\\sqrt{\\frac{%d}{%d}}' %(numerator, denominator)
    simplifiedNumber = -numeratorbase
    return [displayProblem, simplifiedNumber]

def generateRational():
    numerator = random.randint(5, 25)
    denominator = random.randint(5, 25)
    while (gcd(numerator, denominator) > 1): # Checks to make sure we get a non-Whole, Rational number
        denominator = random.randint(5, 25)
    randomNeg = (-1)**random.randint(0, 1)
    if randomNeg == -1:
        displayProblem =  '-\\sqrt{\\frac{%d}{%d}}' %(numerator**2, denominator**2)
        simplifiedNumber = '-\\frac{%d}{%d}' %(numerator, denominator)
    else:
        displayProblem =  '\\sqrt{\\frac{%d}{%d}}' %(numerator**2, denominator**2)
        simplifiedNumber = '\\frac{%d}{%d}' %(numerator, denominator)
    return [displayProblem, simplifiedNumber]

def generateIrrational():
    discriminantbase = random.randint(9, 18) #Base of the number under the square root
    irrationalmaker = random.choice([5, 7, 11, 13]) #The number we will use to make sure we get an irrational number
    maskirrational = random.randint(5, 15) # Masks that the fraction is not a perfect square
    while gcd(discriminantbase, irrationalmaker) > 1: # Makes sure the product is not a perfect square
        irrationalmaker = random.randint(9, 18)
    numerator = discriminantbase * irrationalmaker * maskirrational
    denominator = maskirrational
    randomNeg = commonly_used_functions.maybeMakeNegative(1)
    if randomNeg == -1:
        displayProblem =  '-\\sqrt{\\frac{%d}{%d}}' %(numerator, denominator)
        simplifiedNumber = '-\\sqrt{%d}' %(discriminantbase*irrationalmaker)
    else:
        displayProblem =  '\\sqrt{\\frac{%d}{%d}}' %(numerator, denominator)
        simplifiedNumber = '\\sqrt{%d}' %(discriminantbase*irrationalmaker)
    return [displayProblem, simplifiedNumber]

def generateNonReal():
    chooseDivideByZeroOrComplex = random.randint(0, 1)
    if chooseDivideByZeroOrComplex == 0:
        # Divides by zero
        numerator = random.randint(5, 25)
        denominator = 0
        randomNeg = commonly_used_functions.maybeMakeNegative(1)
        if randomNeg == -1:
            displayProblem =  '-\\sqrt{\\frac{%d}{%d}}' %(numerator, denominator)
        else:
            displayProblem =  '\\sqrt{\\frac{%d}{%d}}' %(numerator, denominator)
        simplifiedNumber = displayProblem
    else:
        # Complex number
        discrim = random.randint(9, 18)
        irrationalmaker = random.choice([5, 7, 11, 13])
        maskirrational = random.randint(5, 15)
        while gcd(discrim, irrationalmaker) > 1:
            irrationalmaker = random.randint(9, 18)
        numerator = - discrim * irrationalmaker * maskirrational
        denominator = maskirrational
        randomNeg = (-1)**random.randint(0, 1)
        if randomNeg == -1:
            displayProblem =  '-\\sqrt{\\frac{%d}{%d}}' %(numerator, denominator)
            simplifiedNumber = '-\\sqrt{%d} i' %(discrim * irrationalmaker)
        else:
            displayProblem =  '\\sqrt{\\frac{%d}{%d}}' %(numerator, denominator)
            simplifiedNumber = '\\sqrt{%d} i' %(discrim * irrationalmaker)
    return [displayProblem, simplifiedNumber]

def subgroup_real_numbers_function(response_type, interval_type):
    option_0_feedback = " These are the counting numbers with 0 (0, 1, 2, 3, ...)"
    option_0_dict = commonly_used_functions.value_and_feedback_to_dict(
        'subgroup_real_numbers',
        'option_0',  # to be replaced later
        'distractor_0 description',  # to be replaced later
        'Whole',
        'Whole',
        option_0_feedback,
        0 # may be assigned as answer later
    )
    option_0_dict['choice_presentation'] = 'Whole'

    option_1_feedback = " These are the negative and positive counting numbers (..., -3, -2, -1, 0, 1, 2, 3, ...)"
    option_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        'subgroup_real_numbers',
        'option_1', # to be replaced later
        'distractor_1 description', # to be replaced later
        'Integer', 
        'Integer',
        option_1_feedback, 
        0 # may be assigned as answer later
    )
    option_1_dict['choice_presentation'] = 'Integer'

    option_2_feedback = " These are numbers that can be written as fraction of Integers (e.g., -2/3)"
    option_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        'subgroup_real_numbers',
        'option_2', # to be replaced later
        'distractor_2 description', # to be replaced later
        'Rational', 
        'Rational',
        option_2_feedback, 
        0 # may be assigned as answer later
    )
    option_2_dict['choice_presentation'] = 'Rational'

    option_3_feedback = " These cannot be written as a fraction of Integers."
    option_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        'subgroup_real_numbers',
        'option_3', # to be replaced later
        'distractor_3 description', # to be replaced later
        'Irrational', 
        'Irrational',
        option_3_feedback, 
        0 # may be assigned as answer later
    )
    option_3_dict['choice_presentation'] = 'Irrational'

    option_4_feedback = "These are Nonreal Complex numbers \\textbf{OR} things that are not numbers (e.g., dividing by 0)."
    option_4_dict = commonly_used_functions.value_and_feedback_to_dict(    
        'subgroup_real_numbers',
        'option_4', # to be replaced later
        'distractor_4 description', # to be replaced later
        'Not a Real Number', 
        'Not a Real Number',
        option_4_feedback, 
        0 # may be assigned as answer later
    )
    option_4_dict['choice_presentation'] = 'Not a Real Number'

    ### VARIABLE DECLARATIONS ###
    types = ["Whole", "Integer", "Rational", "Irrational", "Nonreal"]
    questionType = random.choice(types)

    if questionType == "Whole":
        display_problem, simplifiedNumber = generateWhole()

        option_0_dict['name'] = 'solution'
        option_0_dict['short_description'] = 'Expected solution'
        option_0_dict['feedback'] = "* This is the correct option!"
        option_0_dict['solution'] = 1
        solution_dict = option_0_dict

        option_1_dict['short_description'] = 'Chose Integer when Whole, unclear why'
        option_2_dict['short_description'] = 'Chose Rational when Whole, likely due to seeing a fraction'
        option_3_dict['short_description'] = 'Chose Irrational when Whole, likely due to seeing a square root'
        option_4_dict['short_description'] = 'Chose Not a Real when Whole, unclear why'

    elif questionType == "Integer":
        display_problem, simplifiedNumber = generateInteger()

        option_1_dict['name'] = 'solution'
        option_1_dict['short_description'] = 'Expected solution'
        option_1_dict['feedback'] = "* This is the correct option!"
        option_1_dict['solution'] = 1
        solution_dict = option_1_dict

        option_0_dict['short_description'] = 'Chose Whole when Integer, unclear why'
        option_2_dict['short_description'] = 'Chose Rational when Integer, likely due to seeing a fraction'
        option_3_dict['short_description'] = 'Chose Irrational when Integer, likely due to seeing a square root'
        option_4_dict['short_description'] = 'Chose Not a Real when Integer, unclear why'

    elif questionType == "Rational":
        display_problem, simplifiedNumber = generateRational()

        option_2_dict['name'] = 'solution'
        option_2_dict['short_description'] = 'Expected solution'
        option_2_dict['feedback'] = "* This is the correct option!"
        option_2_dict['solution'] = 1
        solution_dict = option_2_dict

        option_0_dict['short_description'] = 'Chose Whole when Rational, unclear why'
        option_1_dict['short_description'] = 'Chose Integer when Rational, unclear why'
        option_3_dict['short_description'] = 'Chose Irrational when Rational, likely due to seeing square root'
        option_4_dict['short_description'] = 'Chose Not a Real when Rational, unclear why'

    elif questionType == "Irrational":
        display_problem, simplifiedNumber = generateIrrational()

        option_3_dict['name'] = 'solution'
        option_3_dict['short_description'] = 'Expected solution'
        option_3_dict['feedback'] = "* This is the correct option!"
        option_3_dict['solution'] = 1
        solution_dict = option_3_dict

        option_0_dict['short_description'] = 'Chose Whole when Irrational, unclear why'
        option_1_dict['short_description'] = 'Chose Integer when Irrational, unclear why'
        option_2_dict['short_description'] = 'Chose Rational when Irrational, unclear why'
        option_4_dict['short_description'] = 'Chose Not a Real when Irrational, unclear why'

    else:
        display_problem, simplifiedNumber = generateNonReal()

        option_4_dict['name'] = 'solution'
        option_4_dict['short_description'] = 'Expected solution'
        option_4_dict['feedback'] = "* This is the correct option!"
        option_4_dict['solution'] = 1
        solution_dict = option_4_dict

        option_0_dict['short_description'] = 'Chose Whole when Not a Real, unclear why'
        option_1_dict['short_description'] = 'Chose Integer when Not a Real, unclear why'
        option_2_dict['short_description'] = 'Chose Rational Not a Real, unclear why'
        option_3_dict['short_description'] = 'Chose Irrational when Not a Real, unclear why'

    solution_dicts_list = [option_0_dict, option_1_dict, option_2_dict, option_3_dict, option_4_dict]
    presentation_order = []
    for temp_dict in solution_dicts_list:
        presentation_order.append(temp_dict['name'])
    random.shuffle(presentation_order)
    answer_letter = commonly_used_functions.identify_answer_letter(presentation_order)

    options_df = pd.DataFrame(solution_dicts_list)
    options_df = commonly_used_functions.assign_option_letters(presentation_order, options_df)   

    ### DEFINE STEM, PROBLEM, GENERAL COMMENT ###
    if response_type=="Multiple-Choice":
        display_stem = 'Choose the \\textbf{smallest} set of Real numbers that the number below belongs to.'
    else:
        display_stem = 'What is the \\textbf{smallest} set of Real numbers that the number below belongs to?'
    # displayProblem was already defined
    general_comment =  "First, you \\textbf{NEED} to simplify the expression. This question simplifies to $%s$. " \
    "\n \n Be sure you look at the simplified fraction and not just the decimal expansion. Numbers such as 13, 17, and 19 provide " \
    "\\textbf{long but repeating/terminating decimal expansions!} \n \n The only ways to *not* be a Real number are: " \
    "dividing by 0 or taking the square root of a negative number. \n \n Irrational numbers are more than just square root of 3: " \
    "adding or subtracting values from square root of 3 is also irrational." %simplifiedNumber

    display_stem_type="String"
    display_problem_type="Math Mode"
    display_options_type="String"

    question_dict = {
        'code_name': 'subgroup_real_numbers',
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