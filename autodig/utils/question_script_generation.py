import os

# Build script to run questions
def line_break_for_script(file_name):
    with open(f'{file_name}.py', 'a') as script:
        script.write('\n')
        script.close()

def open_and_write(file_name, list_of_lines_to_add, write_or_append='a'):
    with open(f'{file_name}.py', write_or_append) as script:
        for line_to_add in list_of_lines_to_add:
            script.write(f"{line_to_add}\n")
        script.close()

def add_initial_import_statements(file_name):
    lines_to_add = [
        'import pandas as pd',
        'import os'
    ]
    open_and_write(file_name, lines_to_add, write_or_append='w')

def add_code_import_statement(row, file_name):
    import_statement = f'from learning_objective_code.{row["folder_name"]} import {row["code_name"]}'
    open_and_write(file_name, [import_statement])

def add_dict_and_df_for_question(row, file_name):
    question_number = row['question_number']
    code_name = row['code_name']
    response_type = row['response_type']
    version = row['version']
    if row['need_version'] == 0: 
        run_line = f'dict_{question_number}, df_{question_number} = {code_name}.{code_name}_function("{response_type}")'
    else: # Graphs currently need version
        run_line = f'dict_{question_number}, df_{question_number} = {code_name}.{code_name}_function("{response_type}", "{version}")'
    open_and_write(file_name, [run_line])

def add_load_questions_df(file_name):
    lines_to_add = [
        "base_dir = os.getcwd()",
        "save_questions_df_file_path = os.path.join(base_dir, 'temp_files', 'build_exams', 'questions_to_create_df.xlsx')",
        "questions_to_create_df = pd.read_excel(save_questions_df_file_path)"
    ]
    open_and_write(file_name, lines_to_add)

def add_variable_lists_statement(file_name):
    lines_to_add = [
        "questions_to_create_df['dict_var_names'] = f" + '"' + "dict_{questions_to_create_df['question_number']}" + '"',
        "questions_to_create_df['df_var_names'] = f" + '"' + "df_{questions_to_create_df['question_number']}" + '"'
    ]
    open_and_write(file_name, lines_to_add)

def add_combine_dicts_to_separate_dfs(file_name):
    lines_to_add = [
        "list_of_dicts = []",
        "list_of_dfs = []",
        "for index in range(0, len(questions_to_create_df)):", 
        r"    list_of_dicts.append(eval(f'dict_{index}'))",
        r"    list_of_dfs.append(eval(f'df_{index}'))",
        "df_of_dicts = pd.DataFrame(list_of_dicts)",
        "concated_dfs = pd.concat(list_of_dfs, axis=0)"
    ]
    open_and_write(file_name, lines_to_add)

def add_combine_dfs_as_sheets(file_name):
    lines_to_add = [
        "with pd.ExcelWriter(r'" + f'{file_name}' + ".xlsx') as writer:",
        "    df_of_dicts.to_excel(writer, sheet_name='question_info')",
        "    concated_dfs.to_excel(writer, sheet_name='question_options_info')"
    ]
    open_and_write(file_name, lines_to_add)
    

def generate_question_running_script(file_name, questions_to_create_df):
    add_initial_import_statements(file_name)
    line_break_for_script(file_name)

    # Leverage .apply() to iteratively add statements to script by row
    questions_to_create_df.apply(add_code_import_statement, args=(file_name, ), axis=1)
    line_break_for_script(file_name)

    questions_to_create_df.apply(add_dict_and_df_for_question, args=(file_name, ), axis=1)
    line_break_for_script(file_name)

    # Create lists
    add_load_questions_df(file_name)
    add_variable_lists_statement(file_name)
    line_break_for_script(file_name)

    # Combines into separate dfs with lists
    add_combine_dicts_to_separate_dfs(file_name)
    line_break_for_script(file_name)

    # Combines into single workbook
    add_combine_dfs_as_sheets(file_name)

def move_files(file_name):
    temp_file_path_location = os.path.join(os.path.dirname(file_name), 'temp_files', 'build_exams')
    
    try:
        final_py_location = os.path.join(temp_file_path_location, f'{os.path.basename(file_name)}.py')
        os.rename(f'{file_name}.py', final_py_location)
    except: 
        os.remove(final_py_location)
        os.rename(f'{file_name}.py', final_py_location)
    
    try: 
        final_xlsx_location = os.path.join(temp_file_path_location, f'{os.path.basename(file_name)}.xlsx')
        os.rename(f'{file_name}.xlsx', final_xlsx_location)
    except:
        os.remove(final_xlsx_location)
        os.rename(f'{file_name}.xlsx', final_xlsx_location)