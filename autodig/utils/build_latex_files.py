import os
import subprocess

def build_latex_files_function(base_dir, file_name, version):
    administer_dir_path = os.path.join(base_dir, 'temp_files', 'build_exams', 'administer_version')
    os.chdir(administer_dir_path)
    subprocess.call(['pdflatex', '-synctex=1', '-interaction=nonstopmode', f'exam_{file_name}_{version}.tex'])

    key_dir_path = os.path.join(base_dir, 'temp_files', 'build_exams', 'key')
    os.chdir(key_dir_path)
    subprocess.call(['pdflatex', '-synctex=1', '-interaction=nonstopmode',  f'key_{file_name}_{version}.tex'])

    os.chdir(base_dir)