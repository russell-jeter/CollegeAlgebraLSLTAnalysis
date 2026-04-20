from pathlib import Path # To touch files within python
import os

def create_feedback_file(file_name, exam_name, footnote_left, footnote_right, version, DIR):
    feedback_path = os.path.join(DIR, 'temp_files', 'build_exams', 'feedback', f'feedback_{file_name}_{version}.tex')
    feedbackFile = open(feedback_path, 'w') # Opening with write clears any previous version
    feedbackFile.write(r"""\documentclass{extbook}[14pt]
\usepackage{multicol, enumerate, enumitem, hyperref, color, soul, setspace, parskip, fancyhdr, amssymb, amsthm, amsmath, latexsym, units, mathtools}
\everymath{\displaystyle}
\usepackage[headsep=0.5cm,headheight=0cm, left=1 in,right= 1 in,top= 1 in,bottom= 1 in]{geometry}
\usepackage{dashrule}
\newcommand{\litem}[1]{\item#1\hspace*{-1cm}\rule{\textwidth}{0.4pt}}
\pagestyle{fancy}
\lhead{}
\chead{Feedback for %s on %s}
\rhead{}
\lfoot{%s}
\cfoot{}
\rfoot{%s}
\begin{document}
\textbf{This feedback should allow you to understand why you choose the option you did (beyond just getting a question right or wrong) and how to improve. It is generated based on the way you answered.}

\textit{Note: This feedback is auto-generated and may contain issues and/or errors. This feedback is a work-in-progress to give students as many resources to improve as possible.}

\rule{\textwidth}{0.4pt}

\begin{enumerate}""" %(exam_name, version, footnote_left, footnote_right)   )
    feedbackFile.close()

def create_key_file(file_name, exam_name, footnote_left, footnote_right, version, DIR):
    key_path = os.path.join(DIR, 'temp_files', 'build_exams', 'key', f'key_{file_name}_{version}.tex')
    keyFile = open(key_path, 'w')
    keyFile.write(r"""\documentclass{extbook}[14pt]
\usepackage{multicol, enumerate, enumitem, hyperref, color, soul, setspace, parskip, fancyhdr, amssymb, amsthm, amsmath, latexsym, units, mathtools}
\everymath{\displaystyle}
\usepackage[headsep=0.5cm,headheight=0cm, left=1 in,right= 1 in,top= 1 in,bottom= 1 in]{geometry}
\usepackage{dashrule}  %% Package to use the command below to create lines between items
\newcommand{\litem}[1]{\item #1

\rule{\textwidth}{0.4pt}}
\pagestyle{fancy}
\lhead{}
\chead{Answer Key for %s Version %s}
\rhead{}
\lfoot{%s}
\cfoot{}
\rfoot{%s}
\begin{document}
\textbf{This key should allow you to understand why you choose the option you did (beyond just getting a question right or wrong). \href{https://xronos.clas.ufl.edu/mac1105spring2020/courseDescriptionAndMisc/Exams/LearningFromResults}{More instructions on how to use this key can be found here}.}

\textbf{If you have a suggestion to make the keys better, \href{https://forms.gle/CZkbZmPbC9XALEE88}{please fill out the short survey here}.}

\textit{Note: This key is auto-generated and may contain issues and/or errors. The keys are reviewed after each exam to ensure grading is done accurately. If there are issues (like duplicate options), they are noted in the offline gradebook. The keys are a work-in-progress to give students as many resources to improve as possible.}

\rule{\textwidth}{0.4pt}

\begin{enumerate}""" %(exam_name, version, footnote_left, footnote_right)   )
    keyFile.close()

def create_exam_file(file_name, exam_name, footnote_left, footnote_right, version, DIR):
    exam_path = os.path.join(DIR, 'temp_files', 'build_exams', 'administer_version', f'exam_{file_name}_{version}.tex')
    examFile = open(exam_path, 'w')
    examFile.write(r"""\documentclass[14pt]{extbook}
\usepackage{multicol, enumerate, enumitem, hyperref, color, soul, setspace, parskip, fancyhdr} %%General Packages
\usepackage{amssymb, amsthm, amsmath, latexsym, units, mathtools} %%Math Packages
\everymath{\displaystyle} %%All math in Display Style
%% Packages with additional options
\usepackage[headsep=0.5cm,headheight=12pt, left=1 in,right= 1 in,top= 1 in,bottom= 1 in]{geometry}
\usepackage[usenames,dvipsnames]{xcolor}
\usepackage{dashrule}  %% Package to use the command below to create lines between items
\newcommand{\litem}[1]{\item#1\hspace*{-1cm}\rule{\textwidth}{0.4pt}}
\pagestyle{fancy}
\lhead{%s}
\chead{}
\rhead{Version %s}
\lfoot{%s}
\cfoot{}
\rfoot{%s}
\begin{document}

\begin{enumerate}
""" %(exam_name, version, footnote_left, footnote_right))
    examFile.close()

def start_all_latex_files(file_name, exam_name, footnote_left, footnote_right, version, DIR):
    # Individual student feedback is depreciated for now
    # create_feedback_file(file_name, exam_name, footnote_left, footnote_right, version, DIR)
    create_exam_file(file_name, exam_name, footnote_left, footnote_right, version, DIR)
    create_key_file(file_name, exam_name, footnote_left, footnote_right, version, DIR)

def finish_key_file(file_name, version, DIR):
    key_path = os.path.join(DIR, 'temp_files', 'build_exams', 'key', f'key_{file_name}_{version}.tex')
    keyFile = open(key_path, 'a')
    keyFile.write(r"""\end{enumerate}

\end{document}""")
    keyFile.close()

def finish_exam_file(file_name, version, DIR):
    exam_path = os.path.join(DIR, 'temp_files', 'build_exams', 'administer_version', f'exam_{file_name}_{version}.tex')
    examFile = open(exam_path, 'a')
    examFile.write(r"""\end{enumerate}

\end{document}""")
    examFile.close()

def finish_feedback_file(file_name, version, DIR):
    feedback_path = os.path.join(DIR, 'temp_files', 'build_exams', 'feedback', f'feedback_{file_name}_{version}.tex')
    feedbackFile = open(feedback_path, 'a')
    feedbackFile.write(r"""\end{enumerate}

\end{document}""")
    feedbackFile.close()

def end_all_latex_files(file_name, version, DIR):
    # Individual student feedback is depreciated for now
    #finish_feedback_file(file_name, version, DIR)
    finish_exam_file(file_name, version, DIR)
    finish_key_file(file_name, version, DIR)