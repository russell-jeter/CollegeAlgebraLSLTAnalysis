import os
import pandas as pd

def print_question_to_exam(question_dict, options_df, file_name, base_dir):
    exam_file_path = os.path.join(base_dir, 'temp_files', 'build_exams', 'administer_version', f'{file_name}.tex')
    examFile = open(exam_file_path, 'a')
    if question_dict['Response Type'] == "Multiple-Choice":
        examFile.write(r"\litem{")
    else:
        examFile.write(r"\item{")
    examFile.write('\n')

    # display_stem_type: String, Math Mode, or Graph
    display_stem_type = question_dict['Display Stem Type']
    if display_stem_type=="String":
        examFile.write(question_dict['Display Stem'])
    elif display_stem_type=="Math Mode":
        examFile.write("$%s$" %question_dict['Display Stem'])
    elif display_stem_type=="Graph":
        examFile.write(r"""
\begin{center}
    \includegraphics[width=0.5\textwidth]{../figures/%s_%s.png}
\end{center}
""" %(question_dict['code_name'], question_dict['version']))
#    else:
#        print(f"You input {display_stem_type}, which was not a valid option.")
    # display_problem_type: String, Math Mode, Graph, or Table
    display_problem_type = question_dict['Display Problem Type']
    display_problem = question_dict['Display Problem']
    if display_problem_type == "String":
        examFile.write(r"""
\begin{center}
    \textit{ %s }
\end{center}
""" %display_problem)
    elif display_problem_type=="Math Mode":
        examFile.write(r"\[ %s \]" %display_problem)
    elif display_problem_type=="Graph":
        examFile.write(r"""
\begin{center}
    \includegraphics[width=0.5\textwidth]{../figures/%s_%s.png}
\end{center}
""" %(question_dict['code_name'], question_dict['version']))
    elif display_problem_type=="Table":
        # display_problem is now an array. Organize as [ row_1, row_2, row_3, ..., row_m ]
            # len(display_problem) is number of rows
            # len(display_problem[0]) is number of columns
        num_rows=len(display_problem)
        num_cols=len(display_problem[0])
        examFile.write('\n')
        examFile.write('\n')
        examFile.write('\\begin{tabular}{')
        for j in range(num_cols-1):
            examFile.write('c|')
        # Ends begin tabular and doesn't have a bar at the end.
        examFile.write('c}')
        examFile.write('\n')
        # Iterate through the rows and print and & between with a \tabularnewline at the end. Since last row doesn't need one it is done at the end after the loop finishes
        for i in range(num_rows-1):
            for j in range(num_cols-1):
                examFile.write(r"%s &" %display_problem[i][j])
            # Last item in row does not have an &
            examFile.write(r"%s" %display_problem[i][num_cols-1])
            examFile.write('\\tabularnewline \\hline')
            examFile.write('\n')
        for j in range(num_cols-1):
            examFile.write(r"%s &" %display_problem[num_rows-1][j])
        examFile.write(r"%s" %display_problem[num_rows-1][num_cols-1])
        examFile.write('\\end{tabular}')
    
    response_type = question_dict['Response Type']
    display_options_type = question_dict['Display Options Type']
    choices = options_df['choice_presentation'].tolist()

    if response_type=="Multiple-Choice":
        # Begins enumerate for options
        examFile.write(r"\begin{enumerate}[label=\Alph*.]")
        examFile.write('\n')
        # display_options_type: String, Math Mode, or Graph
        if display_options_type=="String":
            for i in range(len(choices)):
                examFile.write(r"\item %s" %choices[i])
                examFile.write('\n')
        elif display_options_type=="Math Mode":
            for i in range(len(choices)):
                examFile.write(r"\item \( %s \)" %choices[i])
                examFile.write('\n')
        elif display_options_type=="Graph":
            examFile.write(r"\begin{multicols}{2}")
            for i in range(len(choices)-1): # Last one is None of the above
                options=["A", "B", "C", "D", "E", "F", "G", "H"]
                examFile.write(r"\item \includegraphics[width = 0.3\textwidth]{../figures/%s_%s_%s.png}" %(question_dict['code_name'], options[i], question_dict['version']))
            examFile.write(r"\end{multicols}")
            examFile.write(r"\item None of the above.")
        examFile.write('\n')
        examFile.write(r"\end{enumerate} }") # The close bracket ends the \litem for the question
        # Ends enumerate for options
    else:
        examFile.write(r"} \newpage") # The close bracket ends the \item for the question
    examFile.write('\n')
    examFile.close()

def print_question_to_key(question_dict, options_df, file_name, base_dir):
    code_name = question_dict['code_name']
    version = question_dict['version']

    key_file_path = os.path.join(base_dir, 'temp_files', 'build_exams', 'key', f'{file_name}.tex')
    keyFile = open(key_file_path, 'a')
    keyFile.write(r"\litem{")
    keyFile.write('\n')
    # display_stem_type: String, Math Mode, or Graph
    display_stem_type = question_dict['Display Stem Type']
    display_stem = question_dict['Display Stem']
    if display_stem_type=="String":
        keyFile.write(display_stem)
    elif display_stem_type=="Math Mode":
        keyFile.write("$%s$" %display_stem)
    elif display_stem_type=="Graph":
        keyFile.write(r"""
\begin{center}
    \includegraphics[width=0.5\textwidth]{../figures/%s_%s.png}
\end{center}
""" %(code_name, version))
    keyFile.write('\n')

    display_problem_type = question_dict['Display Problem Type']
    display_problem = question_dict['Display Problem']
    # display_problem_type: String, Math Mode, Graph, or Table
    if display_problem_type=="String":
        keyFile.write(r"""
\begin{center}
    \textit{ %s }
\end{center}
""" %display_problem)
    elif display_problem_type=="Math Mode":
        keyFile.write(r"\[ %s \]" %display_problem)
    elif display_problem_type=="Graph":
        keyFile.write(r"""
\begin{center}
    \includegraphics[width=0.5\textwidth]{../figures/%s_%s.png}
\end{center}
""" %(code_name, version))
        keyFile.write('\n\n')
    elif display_problem_type=="Table":
        # display_problem is now an array. Organize as [ row_1, row_2, row_3, ..., row_m ]
            # len(display_problem) is number of rows
            # len(display_problem[0]) is number of columns
        num_rows=len(display_problem)
        num_cols=len(display_problem[0])
        keyFile.write('\n')
        keyFile.write('\n')
        keyFile.write('\\begin{tabular}{')
        for j in range(num_cols-1):
            keyFile.write('c|')
        # Ends begin tabular and doesn't have a bar at the end.
        keyFile.write('c}')
        keyFile.write('\n')
        # Iterate through the rows and print and & between with a \tabularnewline at the end. Since last row doesn't need one it is done at the end after the loop finishes
        for i in range(num_rows-1):
            for j in range(num_cols-1): # Last one is None of the above
                keyFile.write(r"%s &" %display_problem[i][j])
            # Last item in row does not have an &
            keyFile.write(r"%s" %display_problem[i][num_cols-1])
            keyFile.write('\\tabularnewline \\hline')
            keyFile.write('\n')
        for j in range(num_cols-1):
            keyFile.write(r"%s &" %display_problem[num_rows-1][j])
        keyFile.write(r"%s" %display_problem[num_rows-1][num_cols-1])
        keyFile.write('\\end{tabular}')

    response_type = question_dict['Response Type']
    display_options_type = question_dict['Display Options Type']
    solution = question_dict['Solution']
    answer_letter = question_dict['Answer Letter']
    general_comment = question_dict['General Comment']

    choices = options_df['choice_presentation'].tolist()
    choice_comments = options_df['feedback'].tolist()

    if response_type=="Multiple-Choice":
        # Begins options display
        if display_options_type=="String":
            keyFile.write("The solution is %s, which is option %s." %(solution, answer_letter))
            keyFile.write('\n')
            keyFile.write('\n')
            keyFile.write(r"\begin{enumerate}[label=\Alph*.]")
            keyFile.write('\n')
            for i in range(len(choices)):
                keyFile.write(r"\item %s" %choices[i])
                keyFile.write('\n')
                keyFile.write('\n')
                keyFile.write(choice_comments[i])
                keyFile.write('\n')
            keyFile.write(r"\end{enumerate}")
            keyFile.write('\n')
            keyFile.write('\n')
        elif display_options_type=="Math Mode":
            keyFile.write("The solution is \\( %s \\), which is option %s." %(solution, answer_letter))
            keyFile.write(r"\begin{enumerate}[label=\Alph*.]")
            keyFile.write('\n')
            for i in range(len(choices)):
                keyFile.write(r"\item \( %s \)" %choices[i])
                keyFile.write('\n')
                keyFile.write('\n')
                keyFile.write(choice_comments[i])
                keyFile.write('\n')
            keyFile.write(r"\end{enumerate}")
            keyFile.write('\n')
        elif display_options_type=="Graph":
            keyFile.write(r"""The solution is the graph below, which is option %s.
    \begin{center}
        \includegraphics[width=0.3\textwidth]{../figures/%s_%s_%s.png}
    \end{center}""" %(answer_letter, code_name, answer_letter, version) )
            keyFile.write(r"\begin{enumerate}[label=\Alph*.]")
            keyFile.write('\n')
            keyFile.write(r"\begin{multicols}{2}")
            keyFile.write('\n')
            for i in range(len(choices)-1):
                options=["A", "B", "C", "D", "E", "F", "G", "H"]
                keyFile.write(r"\item \includegraphics[width = 0.3\textwidth]{../figures/%s_%s_%s.png}" %(code_name, options[i], version))
                keyFile.write('\n')
            keyFile.write(r"\end{multicols}")
            keyFile.write(r"\item None of the above.")
            keyFile.write(r"\end{enumerate}")
        # Ends options display
    else:
        if display_options_type=="String":
            keyFile.write("The solution is %s." %(solution))
            keyFile.write('\n')
            keyFile.write('\n')
            keyFile.write(r'\textbf{Plausible alternative answers include:}')
            keyFile.write(r"\begin{enumerate}[label=\Alph*.]")
            keyFile.write('\n')
            for i in range(len(choices)):
                keyFile.write(choice_comments[i])
                keyFile.write('\n')
            keyFile.write(r"\end{enumerate}")
            keyFile.write('\n')
            keyFile.write('\n')
        elif display_options_type=="Math Mode":
            keyFile.write("The solution is \\( %s \\)." %(solution))
            keyFile.write(r"\begin{enumerate}[label=\Alph*.]")
            keyFile.write('\n')
            keyFile.write(r'\textbf{Plausible alternative answers include:}')
            for i in range(len(choices)):
                keyFile.write(choice_comments[i])
                keyFile.write('\n')
            keyFile.write(r"\end{enumerate}")
            keyFile.write('\n')
        elif display_options_type=="Graph":
            keyFile.write(r"""The solution is the graph below.
    \begin{center}
        \includegraphics[width=0.3\textwidth]{../figures/%s%s%s.png}
    \end{center}""" %(code_name, answer_letter, version) )
            keyFile.write('\n')
    keyFile.write('\n')
    keyFile.write(r"\textbf{General Comment:} %s" %general_comment)
    keyFile.write('\n')
    keyFile.write(r"}") # The close bracket ends the litem initiated in the first keyFile.write
    keyFile.write('\n')
    keyFile.close()

    # Adds letter to masterAnswerKeyFile
    letters_answer_key_csv_file_path = os.path.join(base_dir, 'temp_files', 'build_exams', 'key', 'letters_answer_key', f'{file_name}_{version}.csv')
    lettersAnswerKey = open(letters_answer_key_csv_file_path, 'a')
    lettersAnswerKey.write("%s," %answer_letter)
    lettersAnswerKey.close()

def print_questions_by_code_name(question_dict, question_options_info_df, file_name, base_dir):
    options_df = question_options_info_df[question_options_info_df['code_name'] == question_dict['code_name']]
    version = question_dict['version']
    print_question_to_exam(question_dict, options_df, f'exam_{file_name}_{version}', base_dir)
    print_question_to_key(question_dict, options_df, f'key_{file_name}_{version}', base_dir)

def print_all_questions_to_latex_files(file_name, base_dir):
    path_to_excel_file = os.path.join(base_dir, 'temp_files', 'build_exams', f'{file_name}.xlsx')
    question_info_df = pd.read_excel(path_to_excel_file, sheet_name='question_info', index_col=0)
    question_options_info_df = pd.read_excel(path_to_excel_file, sheet_name='question_options_info', index_col=0)

    if 'version' not in question_info_df.keys():
        question_info_df['version'] = 'A'
        question_options_info_df['version'] = 'A'

    question_info_df.apply(print_questions_by_code_name, args=(question_options_info_df, file_name, base_dir, ), axis=1)