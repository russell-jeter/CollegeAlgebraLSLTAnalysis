import pandas as pd
import os

from learning_objective_code.linear_functions import solve_linear_integer_coefficients
from learning_objective_code.linear_functions import solve_linear_rational_coefficients
from learning_objective_code.linear_functions import linear_graph_to_standard_form
from learning_objective_code.linear_functions import build_linear_from_two_points
from learning_objective_code.linear_functions import build_parallel_or_perpendicular_line

dict_0, df_0 = solve_linear_integer_coefficients.solve_linear_integer_coefficients_function("Multiple-Choice")
dict_1, df_1 = solve_linear_rational_coefficients.solve_linear_rational_coefficients_function("Multiple-Choice")
dict_2, df_2 = linear_graph_to_standard_form.linear_graph_to_standard_form_function("Multiple-Choice", "A")
dict_3, df_3 = build_linear_from_two_points.build_linear_from_two_points_function("Multiple-Choice")
dict_4, df_4 = build_parallel_or_perpendicular_line.build_parallel_or_perpendicular_line_function("Multiple-Choice")

base_dir = os.getcwd()
save_questions_df_file_path = os.path.join(base_dir, 'temp_files', 'build_exams', 'questions_to_create_df.xlsx')
questions_to_create_df = pd.read_excel(save_questions_df_file_path)
questions_to_create_df['dict_var_names'] = f"dict_{questions_to_create_df['question_number']}"
questions_to_create_df['df_var_names'] = f"df_{questions_to_create_df['question_number']}"

list_of_dicts = []
list_of_dfs = []
for index in range(0, len(questions_to_create_df)):
    list_of_dicts.append(eval(f'dict_{index}'))
    list_of_dfs.append(eval(f'df_{index}'))
df_of_dicts = pd.DataFrame(list_of_dicts)
concated_dfs = pd.concat(list_of_dfs, axis=0)

with pd.ExcelWriter(r'c:\Users\dcham\Documents\GitHub\CollegeAlgebraLSLTAnalysis\autodig\test_file_name.xlsx') as writer:
    df_of_dicts.to_excel(writer, sheet_name='question_info')
    concated_dfs.to_excel(writer, sheet_name='question_options_info')
