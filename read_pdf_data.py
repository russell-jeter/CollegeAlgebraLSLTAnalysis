from pypdf import PdfReader

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
            print(row)
            question_split = row.split("Question")
            print(question_split)
            return len(row.split("Question")) - 1
    #There is no question row, use the previous count.
    return 0
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
            print(form_code)
            get_number_of_questions(text_array)
    page_number += 1
    print(page_number)