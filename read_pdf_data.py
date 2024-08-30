from pypdf import PdfReader
import re

def get_is_student_response_report(text_array):
    for row in text_array:
            if "Student Response Report" in row:
                return True
            
    return False
    
def get_form_code(text_array):
    for row in text_array:
        if "Form Code" in row:
            form_code = row.split("Form Code = ")[1][0]
            return form_code
        
    return None

def get_number_of_questions(text_array):
    for row in text_array:
        if "Question" in row:
            question_split = row.split("Question")
            return len(row.split("Question")) - 1
    #There is no question row, use the previous count.
    return 0

def page_has_question_array(text_array):
    for row in text_array:
        if "Question" in row:
            return True
    return False

def get_question_array(text_array):
    for row in text_array:
        if "Question" in row:
            question_split = row.split("Question")
            question_split = question_split[1:]
            for i in range(len(question_split)):
                question_split[i] = re.sub("[^0-9]", "", question_split[i])
            return question_split                
    #There is no question row, use the previous count.
    #This probably shouldn't trigger anymore, because I first check if there is a question row in the page.
    return []

def get_first_student_row_index(text_array):
    for i in range(len(text_array)):
        row = text_array[i]
        if i != len(text_array) - 1:
            print(row)
            print(re.findall(r'\d{4}', row))
reader = PdfReader("./data/pdf_data/fall_2017_final_exam_results.pdf")
number_of_pages = len(reader.pages)
page_number = 0
for page in reader.pages:
    
    text = page.extract_text()

    text_array = text.split("\n")
    if get_is_student_response_report(text_array):
        get_form_code(text_array)
        if get_form_code(text_array):
            form_code = get_form_code(text_array)
            if page_has_question_array(text_array):
                question_array = get_question_array(text_array)
                get_first_student_row_index(text_array)
    page_number += 1
    #print(page_number)