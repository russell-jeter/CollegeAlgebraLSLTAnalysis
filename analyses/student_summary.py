try:
    # Absolute import (for direct execution)
    from analyses import database_utils, rasch_analysis
except ImportError:
    # Relative import (for package context)
    import database_utils
    import rasch_analysis

import pandas as pd


def get_student_summary_frame(dict_of_dfs=None):
    """
    Get a summary dataframe for students from Rasch analysis.

    Args:
        dict_of_dfs (dict, optional): Dictionary of dataframes. If None, loads from default file.

    Returns:
        pd.DataFrame: Student summary dataframe.
    """
    if dict_of_dfs is None:
        dict_of_dfs = database_utils.load_database_to_dict_of_dfs()

    # Rasch analysis seems to be the source for student summary
    # Check if get_rasch_students_and_items_frames_as_dict uses dict_of_dfs?
    # It does not accept it as argument in current implementation.
    rasch_student_frame = rasch_analysis.get_rasch_students_and_items_frames_as_dict()[
        "rasch_student_df"
    ].reset_index()

    return rasch_student_frame


if __name__ == "__main__":
    student_summary_frame = get_student_summary_frame()
    student_summary_frame.to_excel("student_summary.xlsx", index=False)
