import random
from math import gcd
import pandas as pd

from utils import commonly_used_functions, interval_masking_method

code_name = 'subgroup_complex_numbers'

### DEFINITIONS ###
def generateRationalFromSubgroupReal():
    numerator = random.randint(5, 25)
    denominator = random.randint(5, 25)
    while (gcd(numerator, denominator) > 1): # Checks to make sure we get a non-Whole, Rational number
        denominator = random.randint(5, 25)
    return [numerator**2, denominator**2]

def generateIrrationalFromSubgroupReal():
    discriminantbase = random.randint(9, 18)
    irrationalmaker = random.choice([5, 7, 11, 13]) #The number we will use to make sure we get an irrational number
    maskirrational = random.randint(5, 15) # Makes sure the product is not a perfect square
    while gcd(discriminantbase, irrationalmaker) > 1:
        irrationalmaker = random.randint(9, 18)
    numerator = discriminantbase * irrationalmaker * maskirrational
    denominator = maskirrational
    return [numerator, denominator]

def generateNonRealFromSubgroupReal():
    numerator = random.randint(5, 25)
    denominator = 0
    return [numerator, denominator]

def generateComplexFromSubgroupReal():
    discrim = random.randint(9, 18)
    irrationalmaker = random.choice([5, 7, 11, 13]) #The number we will use to make sure we get an irrational number
    maskirrational = random.randint(5, 15)
    while gcd(discrim, irrationalmaker) > 1:
        irrationalmaker = random.randint(9, 18)
    numerator = - discrim * irrationalmaker * maskirrational
    denominator = maskirrational
    return [numerator, denominator]

# Generate different display_problem types
def generateRationalNumber(): # Question Type 1 generates Rational number with possible i^2 term
    numerator = random.randint(2, 20)*(-1)**random.randint(0, 1)
    denominator = random.randint(2, 20)*(-1)**random.randint(0, 1)
    b = random.randint(2, 10)**2
    randomChoice=random.randint(0, 2)
    if randomChoice==0:
        displayProblem = '\\frac{%d}{%d}+\\sqrt{-%d}i' %(numerator, denominator, b)
    elif randomChoice==1:
        displayProblem = '\\frac{%d}{%d}+%di^2' %(numerator, denominator, b)
    else:
        numerator, denominator = generateRationalFromSubgroupReal()
        randomNeg = (-1)**random.randint(0, 1)
        if randomNeg == -1:
            displayProblem =  '-\\sqrt{\\frac{%d}{%d}} + %di^2' %(numerator, denominator, b)
        else:
            displayProblem =  '\\sqrt{\\frac{%d}{%d}} + %di^2' %(numerator, denominator, b)
    return displayProblem

def generateIrrationalNumber(): #Question Type 2 generates Irrational numbers of the form a + 0i
    discriminantbase = random.randint(9, 18) # Base of the number under the square root
    irrationalmaker = random.choice([5, 7, 11, 13]) #The number we will use to make sure we get an irrational number
    while gcd(discriminantbase, irrationalmaker) > 1: # Makes sure the product is not a perfect square
        irrationalmaker = random.randint(9, 18)
    numerator = discriminantbase * irrationalmaker
    denominator = random.randint(5, 20)
    b = random.randint(2, 10)
    randomChoice=random.randint(0, 2)
    if randomChoice == 0:
        displayProblem = '\\frac{\\sqrt{%d}}{%d}+\\sqrt{-%d}i' %(numerator, denominator, b)
    elif randomChoice == 1:
        displayProblem = '\\frac{\\sqrt{%d}}{%d}+%di^2' %(numerator, denominator, b)
    else:
        numerator, denominator = generateIrrationalFromSubgroupReal()
        randomNeg = (-1)**random.randint(0, 1)
        if randomNeg == -1:
            displayProblem =  '-\\sqrt{\\frac{%d}{%d}}+%di^2' %(numerator, denominator, b)
        else:
            displayProblem =  '\\sqrt{\\frac{%d}{%d}}+%di^2' %(numerator, denominator, b)
    return displayProblem

def generateNonRealComplexNumber(): #Question Type 3 generates Nonreal Complex numbers of the form a + bi
    numerator = random.randint(5, 25)*(-1)**random.randint(0, 1)
    denominator = random.randint(5, 25)
    while gcd(numerator, denominator) == denominator:
        denominator = random.randint(5, 25)
    discriminantbase = random.randint(9, 18) # Base of the number under the square root
    irrationalmaker = random.choice([5, 7, 11, 13]) #The number we will use to make sure we get an irrational number
    while gcd(discriminantbase, irrationalmaker) > 1: # Makes sure the product is not a perfect square
        irrationalmaker = random.randint(9, 18)
    inside = discriminantbase*irrationalmaker
    b = "\\sqrt{%d} i" %inside
    randomChoice=random.randint(0, 4)
    if randomChoice==0:
        displayProblem = '\\frac{%d}{%d}+%s' %(numerator, denominator, b)
    elif randomChoice==1:
        numerator, denominator = generateRationalFromSubgroupReal()
        displayProblem = '\\sqrt{\\frac{%d}{%d}}+%s' %(numerator, denominator, b)
    elif randomChoice==2:
        numerator, denominator = generateIrrationalFromSubgroupReal()
        displayProblem = '\\sqrt{\\frac{%d}{%d}}+%s' %(numerator, denominator, b)
    elif randomChoice==3:
        numerator, denominator = generateComplexFromSubgroupReal()
        displayProblem = '\\sqrt{\\frac{%d}{%d}}+\\sqrt{%d}' %(numerator, denominator, inside)
    else:
        numerator, denominator = generateComplexFromSubgroupReal()
        displayProblem = '\\sqrt{\\frac{%d}{%d}} i+\\sqrt{%d}i' %(numerator, denominator, inside)
    return displayProblem

def generatePureImaginaryNumber(): #Question Type 4 generates Pure Imaginary numbers of the form 0 + bi
    denominator = random.randint(2, 20)*(-1)**random.randint(0, 1)
    b = int(random.randint(2, 10))
    randomChoice=random.randint(0, 3)
    if randomChoice==0:
        displayProblem = '\\frac{0}{%d \\pi}+\\sqrt{%s}i' %(denominator, b)
    elif randomChoice==1:
        numerator, denominator = generateRationalFromSubgroupReal()
        displayProblem = '\\sqrt{\\frac{0}{%d}}+\\sqrt{%s}i' %(denominator, b)
    elif randomChoice==2:
        numerator, denominator = generateIrrationalFromSubgroupReal()
        displayProblem = '\\sqrt{\\frac{0}{%d}}+\\sqrt{%s}i' %(denominator, b)
    else:
        numerator, denominator = generateComplexFromSubgroupReal()
        displayProblem = '\\sqrt{\\frac{%d}{%d}}+\\sqrt{0}i' %(numerator, denominator)
    return displayProblem

def generateNonNumber(): #Question Type 5 generates Non-Complex numbers (dividing by 0)
    numerator = random.randint(5, 25)*(-1)**random.randint(0, 1)
    denominator = random.randint(5, 25)
    while gcd(numerator, denominator) == denominator:
        denominator = random.randint(5, 25)
    # Base of the number under the square root
    discriminantbase = random.randint(9, 18)
    # The number we will use to make sure we get an irrational number
    irrationalmaker = random.choice([5, 7, 11, 13]) #The number we will use to make sure we get an irrational number
    # Makes sure the product is not a perfect square
    while gcd(discriminantbase, irrationalmaker) > 1:
        irrationalmaker = random.randint(9, 18)
    inside = discriminantbase*irrationalmaker
    b = "\\sqrt{%d} i" %inside
    randomChoice=random.randint(0, 4)
    if randomChoice==0:
        displayProblem = '\\frac{%d}{0}+%s' %(numerator, b)
    elif randomChoice==1:
        numerator, denominator = generateRationalFromSubgroupReal()
        displayProblem = '\\sqrt{\\frac{%d}{0}}+%s' %(numerator, b)
    elif randomChoice==2:
        numerator, denominator = generateIrrationalFromSubgroupReal()
        displayProblem = '\\sqrt{\\frac{%d}{0}}+%s' %(numerator, b)
    elif randomChoice==3:
        numerator, denominator = generateComplexFromSubgroupReal()
        displayProblem = '\\sqrt{\\frac{%d}{0}}+\\sqrt{%d}' %(numerator, inside)
    else:
        numerator, denominator = generateComplexFromSubgroupReal()
        displayProblem = '\\sqrt{\\frac{%d}{0}} i+\\sqrt{%d}i' %(numerator, inside)
    return displayProblem

def subgroup_complex_numbers_function(response_type, interval_type):
    option_0_feedback = " These are numbers that can be written as fraction of Integers (e.g., -2/3 + 5)"
    option_0_dict = commonly_used_functions.value_and_feedback_to_dict(
        'subgroup_complex_numbers',
        'option_0', # to be replaced later
        'distractor_0 description', # to be replaced later
        'Rational', 
        'Rational',
        option_0_feedback, 
        0 # may be assigned as answer later
    )
    option_0_dict['choice_presentation'] = 'Rational'

    option_1_feedback = " These cannot be written as a fraction of Integers. Remember: $\\pi$ is not an Integer!"
    option_1_dict = commonly_used_functions.value_and_feedback_to_dict(
        'subgroup_complex_numbers',
        'option_1', # to be replaced later
        'distractor_1 description', # to be replaced later
        'Irrational', 
        'Irrational',
        option_1_feedback, 
        0 # may be assigned as answer later
    )
    option_1_dict['choice_presentation'] = 'Irrational'

    option_2_feedback = " This is a Complex number $(a+bi)$ that is not Real (has $i$ as part of the number)."
    option_2_dict = commonly_used_functions.value_and_feedback_to_dict(
        'subgroup_complex_numbers',
        'option_2', # to be replaced later
        'distractor_2 description', # to be replaced later
        'Nonreal Complex', 
        'Nonreal Complex',
        option_2_feedback, 
        0 # may be assigned as answer later
    )
    option_2_dict['choice_presentation'] = 'Nonreal Compelx'

    option_3_feedback = " This is a Complex number $(a+bi)$ that \\textbf{only} has an imaginary part like $2i$."
    option_3_dict = commonly_used_functions.value_and_feedback_to_dict(
        'subgroup_complex_numbers',
        'option_3', # to be replaced later
        'distractor_3 description', # to be replaced later
        'Pure Imaginary', 
        'Pure Imaginary',
        option_3_feedback, 
        0 # may be assigned as answer later
    )
    option_3_dict['choice_presentation'] = 'Pure Imaginary'

    option_4_feedback = " This is not a number. The only non-Complex number we know is dividing by 0 as this is not a number!"
    option_4_dict = commonly_used_functions.value_and_feedback_to_dict(
        'subgroup_complex_numbers',
        'option_4', # to be replaced later
        'distractor_4 description', # to be replaced later
        'Not a Complex Number', 
        'Not a Complex Number',
        option_4_feedback, 
        0 # may be assigned as answer later
    )
    option_4_dict['choice_presentation'] = 'Not a Complex Number'

    types = ["Rational", "Irrational", "NonrealComplex", "PureImaginary", "NotComplex"]
    questionType = random.choice(types)

    if questionType == "Rational":
        display_problem = generateRationalNumber()

        option_0_dict['name'] = 'solution'
        option_0_dict['short_description'] = 'Expected solution'
        option_0_dict['feedback'] = "* This is the correct option!"
        option_0_dict['solution'] = 1
        solution_dict = option_0_dict

        option_1_dict['short_description'] = 'Chose irrational when rational, maybe due to seeing square root of a number?'
        option_2_dict['short_description'] = 'Chose Nonreal Complex when rational, likely due to seeing i'
        option_3_dict['short_description'] = 'Chose Pure Imaginary when rational, likely due to seeing i'
        option_4_dict['short_description'] = 'Chose Not a Complex when rational, maybe due to seeing i or square root of a number?'

    elif questionType == "Irrational":
        display_problem = generateIrrationalNumber()

        option_1_dict['name'] = 'solution'
        option_1_dict['short_description'] = 'Expected solution'
        option_1_dict['feedback'] = "* This is the correct option!"
        option_1_dict['solution'] = 1
        solution_dict = option_1_dict

        option_0_dict['short_description'] = 'Chose rational when irrational, maybe due to seeing a rational solution and assuming structure to answer?'
        option_2_dict['short_description'] = 'Chose Nonreal Complex when irrational, likely due to seeing i'
        option_3_dict['short_description'] = 'Chose Pure Imaginary when irrational, likely due to seeing i'
        option_4_dict['short_description'] = 'Chose Not a Complex when irrational, maybe due to seeing i or square root of a number?'

    elif questionType == "NonrealComplex":
        display_problem = generateNonRealComplexNumber()

        option_2_dict['name'] = 'solution'
        option_2_dict['short_description'] = 'Expected solution'
        option_2_dict['feedback'] = "* This is the correct option!"
        option_2_dict['solution'] = 1
        solution_dict = option_2_dict

        option_0_dict['short_description'] = 'Chose Rational when Nonreal Complex, unclear why'
        option_1_dict['short_description'] = 'Chose Irrational when Nonreal Complex, likely due conceptualizing irrational as not rational'
        option_3_dict['short_description'] = 'Chose Pure Imaginary when Nonreal Complex, likely due to seeing i'
        option_4_dict['short_description'] = 'Chose Not a Complex when Nonreal Complex, unclear why'

    elif questionType == "PureImaginary":
        display_problem = generatePureImaginaryNumber()

        option_3_dict['name'] = 'solution'
        option_3_dict['short_description'] = 'Expected solution'
        option_3_dict['feedback'] = "* This is the correct option!"
        option_3_dict['solution'] = 1
        solution_dict = option_3_dict

        option_0_dict['short_description'] = 'Chose Rational when Pure Imaginary, unclear why'
        option_1_dict['short_description'] = 'Chose Irrational when Pure Imaginary, unclear why'
        option_2_dict['short_description'] = 'Chose Nonreal Complex when Pure Imaginary, unclear why'
        option_4_dict['short_description'] = 'Chose Not a Complex when Pure Imaginary, unclear why'

    else:
        display_problem = generateNonNumber()

        option_4_dict['name'] = 'solution'
        option_4_dict['short_description'] = 'Expected solution'
        option_4_dict['feedback'] = "* This is the correct option!"
        option_4_dict['solution'] = 1
        solution_dict = option_4_dict

        option_0_dict['short_description'] = 'Chose Rational when Not a Complex, unclear why'
        option_1_dict['short_description'] = 'Chose Irrational when Not a Complex, unclear why'
        option_2_dict['short_description'] = 'Chose Nonreal Complex Not a Complex, unclear why'
        option_3_dict['short_description'] = 'Chose Pure Imaginary when Not a Complex, unclear why'

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
        display_stem = 'Choose the \\textbf{smallest} set of Complex numbers that the number below belongs to.'
    else:
        display_stem = 'What is the \\textbf{smallest} set of Complex numbers that the number below belongs to?'
    # displayProblem was already defined
    general_comment =  "Be sure to simplify $i^2 = -1$. This may remove the imaginary portion for your number. If you are having trouble, you may want to look at the \\textit{Subgroups of the Real Numbers} section."

    display_stem_type="String"
    display_problem_type="Math Mode"
    display_options_type="String"

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