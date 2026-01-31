try:
    from analyses import (
        item_summary,
        heatmap_utils,
    )
except ImportError:
    import item_summary
    import heatmap_utils

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_integrated_methodology_heatmaps():
    pickle_filename = "./results/item_summary.pkl"
    try:
        item_summary_frame = pd.read_pickle(pickle_filename)
    except FileNotFoundError:
        item_summary.save_item_summary()
        item_summary_frame = pd.read_pickle(pickle_filename)
        
    item_summary_frame['var_estimates_items'] = item_summary_frame['var_estimates_items_3PL']
    item_summary_frame['outfit_items'] = item_summary_frame['outfit_items_3PL']
    item_summary_frame['infit_items'] = item_summary_frame['infit_items_3PL']
    item_summary_frame['q3_star_items'] = item_summary_frame['q3_star_items_3PL']
    item_summary_frame['is_good_outfit'] = item_summary_frame['is_good_outfit_3PL']
    item_summary_frame['is_acceptable_outfit'] = item_summary_frame['is_acceptable_outfit_3PL']
    item_summary_frame['is_poor_outfit'] = item_summary_frame['is_poor_outfit_3PL']
    item_summary_frame['is_good_infit'] = item_summary_frame['is_good_infit_3PL']
    item_summary_frame['is_acceptable_infit'] = item_summary_frame['is_acceptable_infit_3PL']
    item_summary_frame['is_poor_infit'] = item_summary_frame['is_poor_infit_3PL']
    
    item_summary_frame = item_summary_frame.sort_values(
        by=["question_id"]
    ).reset_index()
    item_summary_frame = item_summary_frame.drop(columns=["index"])
    # Ensure exam_id is present for calculation
    if "exam_id" not in item_summary_frame.columns:
        item_summary_frame["exam_id"] = item_summary_frame["question_id"].str[:2]

    item_summary_frame["is_good_estimated_item_difficulty"] = 0
    item_summary_frame["is_good_item_difficulty"] = 0
    item_summary_frame["is_good_pbc"] = 0
    item_summary_frame["is_good_effective_distractors"] = 0
    item_summary_frame["is_acceptable_estimated_item_difficulty"] = 0
    item_summary_frame["is_acceptable_item_difficulty"] = 0
    item_summary_frame["is_acceptable_pbc"] = 0
    item_summary_frame["is_acceptable_effective_distractors"] = 0
    good_estimated_item_indices = item_summary_frame.query(
        "var_estimates_items <= -2 or var_estimates_items >= 2"
    ).index
    item_summary_frame.loc[
        good_estimated_item_indices, "is_good_estimated_item_difficulty"
    ] = 1
    item_summary_frame.loc[
        good_estimated_item_indices, "is_good_estimated_item_difficulty"
    ] = 1

    # Calculate SD per exam for Item Difficulty
    exam_stats = item_summary_frame.groupby("exam_id")["item_difficulty"].std().reset_index(name="std_dev")
    item_summary_frame = pd.merge(item_summary_frame, exam_stats, on="exam_id", how="left")
    
    target_difficulty = 0.74
    item_summary_frame["diff_deviation"] = (item_summary_frame["item_difficulty"] - target_difficulty).abs()
    
    # Ideal (Good): <= 1 SD
    item_summary_frame["is_good_item_difficulty"] = (
        item_summary_frame["diff_deviation"] <= item_summary_frame["std_dev"]
    ).astype(int)
    good_pbc_indices = item_summary_frame.query("pbc >= good_threshold").index
    item_summary_frame.loc[good_pbc_indices, "is_good_pbc"] = 1
    good_effective_distractors_indices = item_summary_frame.query(
        "effective_distractors >= 2"
    ).index
    item_summary_frame.loc[
        good_effective_distractors_indices, "is_good_effective_distractors"
    ] = 1

    acceptable_estimated_item_indices = item_summary_frame.query(
        "var_estimates_items <= -1 or var_estimates_items >= 1"
    ).index
    item_summary_frame.loc[
        acceptable_estimated_item_indices, "is_acceptable_estimated_item_difficulty"
    ] = 1
    item_summary_frame.loc[
        acceptable_estimated_item_indices, "is_acceptable_estimated_item_difficulty"
    ] = 1
    
    # Acceptable: <= 2 SD
    # Note: Ideal items are also Acceptable by this definition, effectively contributing +1 to tier.
    # The 'item_difficulty_tier' summation later handles this (Good + Acceptable = 2 if both true).
    item_summary_frame["is_acceptable_item_difficulty"] = (
        item_summary_frame["diff_deviation"] <= 2 * item_summary_frame["std_dev"]
    ).astype(int)
    acceptable_pbc_indices = item_summary_frame.query("pbc >= poor_threshold").index
    item_summary_frame.loc[acceptable_pbc_indices, "is_acceptable_pbc"] = 1
    acceptable_effective_distractors_indices = item_summary_frame.query(
        "effective_distractors >= 1"
    ).index
    item_summary_frame.loc[
        acceptable_effective_distractors_indices, "is_acceptable_effective_distractors"
    ] = 1

    item_summary_frame["estimated_item_difficulty_tier"] = (
        item_summary_frame["is_good_estimated_item_difficulty"]
        + item_summary_frame["is_acceptable_estimated_item_difficulty"]
    )
    item_summary_frame["item_difficulty_tier"] = (
        item_summary_frame["is_good_item_difficulty"]
        + item_summary_frame["is_acceptable_item_difficulty"]
    )
    item_summary_frame["pbc_tier"] = (
        item_summary_frame["is_good_pbc"] + item_summary_frame["is_acceptable_pbc"]
    )
    item_summary_frame["effective_distractors_tier"] = (
        item_summary_frame["is_good_effective_distractors"]
        + item_summary_frame["is_acceptable_effective_distractors"]
    )
    item_summary_frame["infit_tier"] = (
        item_summary_frame["is_good_infit"] + item_summary_frame["is_acceptable_infit"]
    )
    item_summary_frame["outfit_tier"] = (
        item_summary_frame["is_good_outfit"]
        + item_summary_frame["is_acceptable_outfit"]
    )
    exam_ids = ["1A", "1B", "2A", "2B", "2C", "3A", "3B", "3C", "4A", "4B", "4C"]
    for exam_id in exam_ids:
        exam_item_summary_frame = item_summary_frame[
            item_summary_frame["question_id"].str.contains(exam_id)
        ]
        question_ids = np.unique(exam_item_summary_frame["question_id"])

        columns_to_plot_data = [
            "outfit_items",
            "infit_items",
            "effective_distractors",
            "pbc",
            "item_difficulty",
        ]
        columns_to_plot_colors = [
            "outfit_tier",
            "infit_tier",
            "effective_distractors_tier",
            "pbc_tier",
            "item_difficulty_tier",
        ]
        columns_to_display = [
            "Item Outfit",
            "Item Infit",
            "Effective Distractors",
            "PBC",
            "Item Difficulty",
        ]

        data = exam_item_summary_frame[columns_to_plot_data].to_numpy()
        data_colors = (
            exam_item_summary_frame[columns_to_plot_colors].to_numpy().astype(float)
        )

        # This is to shift the colors in the heatmap a bit.
        green_indices = np.greater(data_colors, 1.5)
        data_colors[green_indices] += 0.35

        fig, (ax) = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))
        im, cbar = heatmap_utils.heatmap(
            data_colors,
            question_ids,
            columns_to_display,
            cmap="RdYlGn",
            ax=ax,
            aspect="auto",
            vmin=-0.65,
            vmax=2.65,
        )
        cbar.remove()
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                c = data[i, j]
                ax.text(j, i, f"{c:.2f}", va="center", ha="center")
        # texts = heatmap_utils.annotate_heatmap(im, valfmt="{x:.2f}")

        fig.tight_layout()
        plt.savefig(f"figures/{exam_id}_heatmap.png")


if __name__ == "__main__":
    generate_integrated_methodology_heatmaps()