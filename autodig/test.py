import pandas as pd
import os

from learning_objective_code.real_complex_numbers import divide_complex_numbers
from learning_objective_code.real_complex_numbers import multiply_complex_numbers
from learning_objective_code.real_complex_numbers import order_of_operations
from learning_objective_code.real_complex_numbers import subgroup_real_numbers
from learning_objective_code.real_complex_numbers import subgroup_complex_numbers

dict_0, df_0 = divide_complex_numbers.divide_complex_numbers_function("Multiple-Choice")
dict_1, df_1 = multiply_complex_numbers.multiply_complex_numbers_function("Multiple-Choice")
dict_2, df_2 = order_of_operations.order_of_operations_function("Multiple-Choice")
dict_3, df_3 = subgroup_real_numbers.subgroup_real_numbers_function("Multiple-Choice")
dict_4, df_4 = subgroup_complex_numbers.subgroup_complex_numbers_function("Multiple-Choice")

base_dir = os.getcwd()
save_questions_df_file_path = os.path.join(base_dir, 'temp_files', 'questions_to_create_df.xlsx')
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

with pd.ExcelWriter(r'c:\Users\dcham\Documents\GitHub\CollegeAlgebraLSLTAnalysis\autodig\test.xlsx') as writer:
    df_of_dicts.to_excel(writer, sheet_name='question_info')
    concated_dfs.to_excel(writer, sheet_name='question_options_info')
