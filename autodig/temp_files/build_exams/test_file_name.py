import pandas as pd
import os

from learning_objective_code.real_complex_numbers import divide_complex_numbers
from learning_objective_code.real_complex_numbers import multiply_complex_numbers
from learning_objective_code.real_complex_numbers import order_of_operations
from learning_objective_code.real_complex_numbers import subgroup_real_numbers
from learning_objective_code.real_complex_numbers import subgroup_complex_numbers
from learning_objective_code.linear_functions import solve_linear_integer_coefficients
from learning_objective_code.linear_functions import solve_linear_rational_coefficients
from learning_objective_code.linear_functions import linear_graph_to_standard_form
from learning_objective_code.linear_functions import build_linear_from_two_points
from learning_objective_code.linear_functions import build_parallel_or_perpendicular_line
from learning_objective_code.inequalities import describe_using_interval
from learning_objective_code.inequalities import solve_compound_and
from learning_objective_code.inequalities import solve_compound_or
from learning_objective_code.inequalities import solve_inequality_integer_coefficients
from learning_objective_code.inequalities import solve_inequality_rational_coefficients
from learning_objective_code.quadratic_functions import solve_quadratic_with_factoring
from learning_objective_code.quadratic_functions import factor_trinomial_with_a_over_1
from learning_objective_code.quadratic_functions import convert_quadratic_equation_to_graph
from learning_objective_code.quadratic_functions import solve_using_quadratic_formula
from learning_objective_code.quadratic_functions import convert_quadratic_graph_to_equation

dict_0, df_0 = divide_complex_numbers.divide_complex_numbers_function("Multiple-Choice")
dict_1, df_1 = multiply_complex_numbers.multiply_complex_numbers_function("Multiple-Choice")
dict_2, df_2 = order_of_operations.order_of_operations_function("Multiple-Choice")
dict_3, df_3 = subgroup_real_numbers.subgroup_real_numbers_function("Multiple-Choice")
dict_4, df_4 = subgroup_complex_numbers.subgroup_complex_numbers_function("Multiple-Choice")
dict_5, df_5 = solve_linear_integer_coefficients.solve_linear_integer_coefficients_function("Multiple-Choice")
dict_6, df_6 = solve_linear_rational_coefficients.solve_linear_rational_coefficients_function("Multiple-Choice")
dict_7, df_7 = linear_graph_to_standard_form.linear_graph_to_standard_form_function("Multiple-Choice", "A")
dict_8, df_8 = build_linear_from_two_points.build_linear_from_two_points_function("Multiple-Choice")
dict_9, df_9 = build_parallel_or_perpendicular_line.build_parallel_or_perpendicular_line_function("Multiple-Choice")
dict_10, df_10 = describe_using_interval.describe_using_interval_function("Multiple-Choice")
dict_11, df_11 = solve_compound_and.solve_compound_and_function("Multiple-Choice")
dict_12, df_12 = solve_compound_or.solve_compound_or_function("Multiple-Choice")
dict_13, df_13 = solve_inequality_integer_coefficients.solve_inequality_integer_coefficients_function("Multiple-Choice")
dict_14, df_14 = solve_inequality_rational_coefficients.solve_inequality_rational_coefficients_function("Multiple-Choice")
dict_15, df_15 = solve_quadratic_with_factoring.solve_quadratic_with_factoring_function("Multiple-Choice")
dict_16, df_16 = factor_trinomial_with_a_over_1.factor_trinomial_with_a_over_1_function("Multiple-Choice")
dict_17, df_17 = convert_quadratic_equation_to_graph.convert_quadratic_equation_to_graph_function("Multiple-Choice", "A")
dict_18, df_18 = solve_using_quadratic_formula.solve_using_quadratic_formula_function("Multiple-Choice")
dict_19, df_19 = convert_quadratic_graph_to_equation.convert_quadratic_graph_to_equation_function("Multiple-Choice", "A")

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
