from pypdf import PdfReader
import re
import pandas as pd

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

def is_student_row(row):
    if len(re.findall(r'\d{4}', row)) > 0:
        if not ('MAC 1105' in row) and not ('MAC1105' in row) :
            return True
        
    return False

def convert_student_row_to_dict(student_row, question_array):
    student_dict = dict()
    surname = student_row[0]
    if 'Average' in surname:
        surname = "N/A"
    for i in range(len(question_array)):
        student_dict[question_array[i]] = student_row[-len(question_array) + i]
    student_id = "N/A"
    for student_row_entry in student_row:
        if len(re.findall(r'\d{4}', student_row_entry)) > 0:
            student_id = student_row_entry
    student_dict["student_id"] = student_id
    student_dict["surname"] = surname

    return student_dict


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
            if is_student_row(row):
                    return i
    return 0
            
def create_aggregate_function_dict(column_list):
    aggregate_function_dict = dict()

    for column in column_list:
        aggregate_function_dict[column] = "max"
    aggregate_function_dict["surname"] = ', '.join
    del aggregate_function_dict["student_id"]
    return aggregate_function_dict

reader = PdfReader("./data/pdf_data/fall_2017_exam_three_results.pdf")
assessment_name = "Exam Three"

student_dict_array = []

for page in reader.pages:    
    text = page.extract_text()
    text_array = text.split("\n")
    
    #This is a good first check to make sure the page has student results.
    if get_is_student_response_report(text_array):
    
        #The prescence of a form code let's us know if this is a page with student results on it.
        if get_form_code(text_array):
            form_code = get_form_code(text_array)
    
            #Update the question array if there is a list of question names in the header.
            if page_has_question_array(text_array):
                question_array = get_question_array(text_array)
            #(The last line is garbage.)
            first_student_index = get_first_student_row_index(text_array)
            for i in range(first_student_index, len(text_array) - 1):
                
                text_row = text_array[i]
                if is_student_row(text_row):
                    text_row = text_row.split(" ")
                    student_dict = convert_student_row_to_dict(student_row = text_row, question_array = question_array)
                    student_dict["form"] = form_code
                    student_dict_array.append(student_dict)

student_frame = pd.DataFrame(student_dict_array)

student_frame = student_frame.fillna(-1)
numeric_columns = list(student_frame.columns.values)
numeric_columns.remove("student_id")
numeric_columns.remove("surname")
numeric_columns.remove("form")
student_frame[numeric_columns] = student_frame[numeric_columns].apply(pd.to_numeric, errors = 'coerce').fillna(-1).astype(int)
student_frame[numeric_columns] = student_frame[numeric_columns].astype(int)
student_frame = student_frame.groupby('student_id').agg(create_aggregate_function_dict(student_frame.columns)).reset_index()

student_frame.to_csv("./data/exam_three.txt", sep = '|', index = False)