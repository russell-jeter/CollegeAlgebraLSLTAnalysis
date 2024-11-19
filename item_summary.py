import utils
import pandas as pd
import effective_distractors_analysis
import item_difficulty
import rasch_analysis

def get_item_summary_frame(dict_of_dfs = None):
    if type(dict_of_dfs) == type(None):
        dict_of_dfs = utils.load_database_to_dict_of_dfs()

    distractor_counts_frame = effective_distractors_analysis.get_distractor_counts_frame(dict_of_dfs = dict_of_dfs)
    distractor_counts_frame = distractor_counts_frame.rename(columns = {"count": "option_selected_count"})

    item_difficulty_frame = item_difficulty.get_item_difficulty_frame().reset_index()
    item_difficulty_frame = item_difficulty_frame.drop(columns = ["exam_id", "index"])
    item_difficulty_frame = item_difficulty_frame.rename(columns = {"count": "student_response_count"})

    pbc_frame = item_difficulty.get_point_biserial_coefficient_frame().reset_index()
    pbc_frame = pbc_frame.drop(columns = ["exam_id", "index"])

    rasch_item_frame = rasch_analysis.get_rasch_students_and_items_frames_as_dict()["rasch_items_df"].reset_index()

    item_summary_frame = pd.merge(pbc_frame, item_difficulty_frame, on = "question_id")
    #item_summary_frame = pd.merge(distractor_counts_frame, item_summary_frame, on = "question_id")
    item_summary_frame = pd.merge(rasch_item_frame, item_summary_frame, on = "question_id")
    
    return item_summary_frame

if __name__ == "__main__":
    item_summary_frame = get_item_summary_frame()

    item_summary_frame.to_excel("item_summary.xlsx", index = False)
