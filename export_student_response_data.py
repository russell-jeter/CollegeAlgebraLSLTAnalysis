import pandas as pd

data_files = ["./data/exam_one.txt", "./data/exam_two.txt", "./data/exam_three.txt", "./data/final_exam.txt"]
exam_ids = ["1", "2", "3", "4"]

question_dict_list = []

for index, data_file in enumerate(data_files):

    exam_data_frame = pd.read_csv(data_file, sep = "|")
    frame_columns = exam_data_frame.columns

    exam_id = exam_ids[index]

    for index, row in exam_data_frame.iterrows():
        exam_form = row["form"]
        
        for column in frame_columns:
            if column.isnumeric():
                key_name = exam_id + exam_form + column.zfill(2)
                student_dict = dict()
                student_dict["question_id"] = key_name
                student_dict["studen_id"] = row["student_id"]
                student_dict["selected_option"] = row[column]
                question_dict_list.append(student_dict)

pd.DataFrame(question_dict_list).to_csv("./data/student_responses.txt", sep = "|", index = False)
