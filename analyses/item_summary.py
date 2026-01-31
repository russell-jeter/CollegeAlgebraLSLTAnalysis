try:
    from analyses import (
        database_utils,
        effective_distractors_analysis,
        item_difficulty,
        rasch_analysis,
    )
except ImportError:
    import database_utils
    import effective_distractors_analysis
    import item_difficulty
    import rasch_analysis

import pandas as pd


def get_item_summary_frame(dict_of_dfs=None):
    """
    Get a summary dataframe for items, aggregating distractor counts, difficulty, PBC, and Rasch analysis.

    Args:
        dict_of_dfs (dict, optional): Dictionary of dataframes. If None, loads from default file.

    Returns:
        pd.DataFrame: Merged item summary.
    """
    if dict_of_dfs is None:
        dict_of_dfs = database_utils.load_database_to_dict_of_dfs()

    # Get distractor counts
    # Get distractor counts
    distractor_counts_frame = (
        effective_distractors_analysis.get_effective_distractors_per_question()
    )
    distractor_counts_frame = distractor_counts_frame.rename(
        columns={"count": "option_selected_count"}
    )

    # Get item difficulty
    item_difficulty_frame = item_difficulty.get_item_difficulty_frame().reset_index()
    # "index" column removal if reset_index created it, or drop specific columns
    if "exam_id" in item_difficulty_frame.columns:
        item_difficulty_frame = item_difficulty_frame.drop(columns=["exam_id"])
    if "index" in item_difficulty_frame.columns:
        item_difficulty_frame = item_difficulty_frame.drop(columns=["index"])

    item_difficulty_frame = item_difficulty_frame.rename(
        columns={"count": "student_response_count"}
    )

    # Get Point Biserial Coefficient
    pbc_frame = item_difficulty.get_point_biserial_coefficient_frame().reset_index()
    if "exam_id" in pbc_frame.columns:
        pbc_frame = pbc_frame.drop(columns=["exam_id"])
    if "index" in pbc_frame.columns:
        pbc_frame = pbc_frame.drop(columns=["index"])

    # Get Rasch analysis items
    rasch_dict = rasch_analysis.get_rasch_students_and_items_frames_as_dict()
    rasch_item_frame = rasch_dict["rasch_items_df"].reset_index()

    # Merge all
    item_summary_frame = pd.merge(pbc_frame, item_difficulty_frame, on="question_id")
    item_summary_frame = pd.merge(
        distractor_counts_frame, item_summary_frame, on="question_id"
    )
    item_summary_frame = pd.merge(
        rasch_item_frame, item_summary_frame, on="question_id"
    )

    return item_summary_frame

def save_item_summary(filename = "./results/item_summary"):
    item_summary_frame = get_item_summary_frame()
    item_summary_frame.to_pickle(f"{filename}.pkl")
    item_summary_frame.to_excel(f"{filename}.xlsx", index=False)


if __name__ == "__main__":
    save_item_summary()
