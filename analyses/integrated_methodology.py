try:
    # Absolute import (for direct execution)
    from analyses import database_utils, effective_distractors_analysis, item_difficulty, rasch_analysis, item_summary, heatmap_utils
except ImportError:
    # Relative import (for package context)
    import database_utils      
    import effective_distractors_analysis
    import item_difficulty
    import rasch_analysis
    import item_summary
    import heatmap_utils
    
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    load_item = True
    pickle_filename = "item_summary.pkl"
    if load_item:
        item_summary_frame = pd.read_pickle(pickle_filename)
    else:
        item_summary_frame = item_summary.get_item_summary_frame()
        item_summary_frame.to_pickle(pickle_filename)
    
    item_summary_frame = item_summary_frame.sort_values(by = ["question_id"]).reset_index()
    item_summary_frame = item_summary_frame.drop(columns=["index"])
    item_summary_frame["is_good_estimated_item_difficulty"] = 0
    item_summary_frame["is_good_item_difficulty"] = 0
    item_summary_frame["is_good_pbc"] = 0
    item_summary_frame["is_good_effective_distractors"] = 0
    good_estimated_item_indices = item_summary_frame.query("var_estimates_items <= -2 or var_estimates_items >= 2").index
    item_summary_frame.loc[good_estimated_item_indices, "is_good_estimated_item_difficulty"] = 1
    good_item_difficulty_indices = item_summary_frame.query("item_difficulty <= .8 and item_difficulty >= .6").index
    item_summary_frame.loc[good_item_difficulty_indices, "is_good_item_difficulty"] = 1
    good_pbc_indices = item_summary_frame.query("pbc >= good_threshold").index
    item_summary_frame.loc[good_pbc_indices, "is_good_pbc"] = 1
    good_effective_distractors_indices = item_summary_frame.query("effective_distractors >= 2").index
    item_summary_frame.loc[good_effective_distractors_indices, "is_good_effective_distractors"] = 1
    exam_ids = ["1A", "1B", "2A", "2B", "2C", "3A", "3B", "3C", "4A", "4B", "4C"]
    for exam_id in exam_ids:
        exam_item_summary_frame = item_summary_frame[item_summary_frame['question_id'].str.contains(exam_id)]
        question_ids = np.unique(exam_item_summary_frame["question_id"])
        
        
        columns_to_plot_data = ["var_estimates_items", "outfit_items", "infit_items", "effective_distractors", "pbc", "item_difficulty"]
        columns_to_plot_colors = ["is_good_estimated_item_difficulty", "is_good_outfit", "is_good_infit", "is_good_effective_distractors", "is_good_pbc", "is_good_item_difficulty"]
        columns_to_display = ["Estimated Item Difficulty", "Outfit", "Infit", "Effective Distractors", "PBC", "Item Difficulty"]

        data = exam_item_summary_frame[columns_to_plot_data].to_numpy()
        data_colors = exam_item_summary_frame[columns_to_plot_colors].to_numpy()
        fig, (ax) = plt.subplots(nrows=1, ncols=1, figsize=(10,6))
        im, cbar = heatmap_utils.heatmap(data_colors, question_ids, columns_to_display, cmap = "RdYlGn", ax=ax, aspect="auto", vmin = -1.5, vmax = 1.5)
        cbar.remove()
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                c = data[i, j]
                ax.text(j, i, f"{c:.2f}", va='center', ha='center')
        #texts = heatmap_utils.annotate_heatmap(im, valfmt="{x:.2f}")

        fig.tight_layout()
        plt.savefig(f"{exam_id}_heatmap.png")