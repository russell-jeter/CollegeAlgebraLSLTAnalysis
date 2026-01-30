try:
    from analyses import database_utils
except ImportError:
    import database_utils

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Color palette for plots
CUSTOM_PALETTE = ["#cf4456", "#f29566", "#831c64", "#2f0f3e", "#feedb0"]
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", CUSTOM_PALETTE)


def get_distractor_counts_frame(dict_of_dfs=None):
    """
    Get a dataframe of counts for each distractor for each question.

    Args:
        dict_of_dfs (dict, optional): Dictionary of dataframes. If None, loads from default file.

    Returns:
        pd.DataFrame: DataFrame of counts for each distractor for each question.
        Fields: question_id, option_id, is_distractor, count, percent, exam_id.
    """
    if dict_of_dfs is None:
        dict_of_dfs = database_utils.load_database_to_dict_of_dfs()

    student_responses_with_details = database_utils.get_student_responses_with_details(
        dict_of_dfs=dict_of_dfs
    )
    completed_answer_choices = database_utils.get_completed_answer_choices(
        dict_of_dfs=dict_of_dfs
    )

    # Count occurrences of each selected option per question
    distractor_selection_counts = student_responses_with_details.groupby(
        by=["question_id", "selected_option"]
    ).size()
    distractor_selection_counts = distractor_selection_counts.to_frame(
        name="count"
    ).reset_index()

    # Merge with completed answer choices to get details about the options
    distractor_selection_counts = pd.merge(
        left=completed_answer_choices[["question_id", "option_id", "is_distractor"]],
        right=distractor_selection_counts,
        how="left",
        left_on=["question_id", "option_id"],
        right_on=["question_id", "selected_option"],
    )

    distractor_selection_counts = distractor_selection_counts.drop(
        columns=["selected_option"]
    )
    distractor_selection_counts = distractor_selection_counts.fillna(0)

    # Setup exam_id
    distractor_selection_counts["exam_id"] = distractor_selection_counts[
        "question_id"
    ].str[:2]

    # Calculate percent of question answers that a given option got.
    # Vectorized approach: group by question and transform sum to get total answers per question
    total_counts = distractor_selection_counts.groupby("question_id")[
        "count"
    ].transform("sum")

    # Avoid division by zero
    distractor_selection_counts["percent"] = 0.0
    mask = total_counts > 0
    distractor_selection_counts.loc[mask, "percent"] = (
        distractor_selection_counts.loc[mask, "count"] / total_counts.loc[mask]
    )

    return distractor_selection_counts


def get_percent_of_distractors_by_form(distractor_selection_counts=None):
    """
    Print summary of distractor selection by exam.

    The categories are:
        never_chosen: selected 0% of the time
        rarely_chosen: selected > 0% and <= 5% of the time
        sometimes_chosen: selected > 5% of the time

    Args:
        distractor_selection_counts (pd.DataFrame, optional): Dataframe of counts.
            If None, calls get_distractor_counts_frame().

    Returns:
        pd.DataFrame: Summary dataframe with counts and percentages of distractor selection types per exam.
    """
    if distractor_selection_counts is None:
        distractor_selection_counts = get_distractor_counts_frame()

    exam_ids = pd.unique(distractor_selection_counts["exam_id"].values)
    distractors_chosen_list = []

    for exam_id in exam_ids:
        exam_distractors_chosen_dict = dict()
        exam_distractors_chosen_dict["exam_id"] = exam_id

        # Filter for this exam and only distractors
        exam_selection_frame = distractor_selection_counts[
            (distractor_selection_counts["exam_id"] == exam_id)
            & (distractor_selection_counts["is_distractor"] == 1)
        ]

        # Calculate categories
        exam_distractors_chosen_dict["never_chosen"] = len(
            exam_selection_frame[exam_selection_frame["percent"] == 0]
        )
        exam_distractors_chosen_dict["rarely_chosen"] = len(
            exam_selection_frame[
                (exam_selection_frame["percent"] > 0)
                & (exam_selection_frame["percent"] <= 0.05)
            ]
        )
        exam_distractors_chosen_dict["sometimes_chosen"] = len(
            exam_selection_frame[exam_selection_frame["percent"] > 0.05]
        )
        exam_distractors_chosen_dict["total_distractors"] = len(exam_selection_frame)

        distractors_chosen_list.append(exam_distractors_chosen_dict)

    exam_distractors_chosen_frame = pd.DataFrame(distractors_chosen_list)

    # Calculate percentages
    # Use fillna(0) implicitly or handle division by zero? Assuming total_distractors > 0
    total = exam_distractors_chosen_frame["total_distractors"]

    exam_distractors_chosen_frame["never_chosen_percent"] = (
        exam_distractors_chosen_frame["never_chosen"] / total
    )
    exam_distractors_chosen_frame["rarely_chosen_percent"] = (
        exam_distractors_chosen_frame["rarely_chosen"] / total
    )
    exam_distractors_chosen_frame["sometimes_chosen_percent"] = (
        exam_distractors_chosen_frame["sometimes_chosen"] / total
    )

    # Form IDs derived from exam_id (e.g., 1A -> form A, exam 1)
    exam_distractors_chosen_frame["exam_form_id"] = exam_distractors_chosen_frame[
        "exam_id"
    ]
    exam_distractors_chosen_frame["form"] = exam_distractors_chosen_frame[
        "exam_id"
    ].str[1]
    exam_distractors_chosen_frame["exam_id"] = exam_distractors_chosen_frame[
        "exam_id"
    ].str[0]

    return exam_distractors_chosen_frame


def add_distractors_chosen_subplot(
    exam_distractors_chosen_frame, axis, exam_keys, title
):
    labels = ["Never Chosen", "Rarely Chosen", "Sometimes Chosen"]
    text_color = ["black", "black", "white"]
    bar_bottoms = [0, 0, 0]
    bar_count = 0

    for key in exam_keys:
        exam_bar_data = []
        exam_distractors_chosen = exam_distractors_chosen_frame[
            exam_distractors_chosen_frame["exam_form_id"].isin([key])
        ]

        if exam_distractors_chosen.empty:
            continue

        # extract values
        exam_bar_data.append(exam_distractors_chosen["never_chosen_percent"].values[0])
        exam_bar_data.append(exam_distractors_chosen["rarely_chosen_percent"].values[0])
        exam_bar_data.append(
            exam_distractors_chosen["sometimes_chosen_percent"].values[0]
        )

        exam_bar_data = np.array(exam_bar_data) * 100
        axis.bar(labels, exam_bar_data, label=key, bottom=bar_bottoms)

        # Update bottoms for stacking
        for i in range(len(bar_bottoms)):
            bar_bottoms[i] += exam_bar_data[i]

        # Add text labels
        for j in range(len(exam_bar_data)):
            y_position = bar_bottoms[j] - exam_bar_data[j] / 2
            if exam_bar_data[j] >= 25:
                # Cycle colors based on bar_count if needed, here mimicking logic
                color = text_color[bar_count % len(text_color)]
                axis.text(
                    labels[j],
                    y_position,
                    f"{exam_bar_data[j]:.2f}",
                    color=color,
                    ha="center",
                    va="bottom",
                    fontsize=10,
                )
        bar_count += 1

    axis.legend(prop={"size": 10})
    axis.set_xlabel("Distractors Chosen Category")
    axis.set_ylabel("Percent of Distractor Answer Choices")
    axis.set_title(title)


def save_distractors_chosen_plots(exam_distractors_chosen_frame=None, filename=None):
    if exam_distractors_chosen_frame is None:
        exam_distractors_chosen_frame = get_percent_of_distractors_by_form()

    if filename is None:
        filename = "./figures/distractors_chosen_bar_chart.png"

    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(10, 6))

    print(exam_distractors_chosen_frame)
    add_distractors_chosen_subplot(
        exam_distractors_chosen_frame, ax0, ["1A", "1B"], "Exam 1"
    )
    add_distractors_chosen_subplot(
        exam_distractors_chosen_frame, ax1, ["2A", "2B", "2C"], "Exam 2"
    )
    add_distractors_chosen_subplot(
        exam_distractors_chosen_frame, ax2, ["3A", "3B", "3C"], "Exam 3"
    )
    add_distractors_chosen_subplot(
        exam_distractors_chosen_frame, ax3, ["4A", "4B", "4C"], "Exam 4"
    )

    fig.tight_layout()

    try:
        plt.savefig(filename)
    except FileNotFoundError:
        if not filename.startswith("."):
            filename = "." + filename
        plt.savefig(filename)

    plt.close(fig)


def create_effective_distractor_counts_list():
    """
    Returns a blank array of zeros for counting effective distractors (0 to 4).
    """
    return [0, 0, 0, 0, 0]


def get_effective_distractors_by_form(distractor_selection_counts=None):
    """
    Get summary of effective distractors (Selected > 5% of the time) by form.

    Returns:
        dict: Keys are form IDs/exam IDs, values are lists of percents for 0, 1, 2, 3, 4 effective distractors.
    """
    if distractor_selection_counts is None:
        distractor_selection_counts = get_distractor_counts_frame()

    distractor_selection_counts = distractor_selection_counts.copy()
    distractor_selection_counts["is_effective"] = (
        distractor_selection_counts["percent"] > 0.05
    )

    # We need to count effective distractors PER QUESTION
    # Filter only distractors that are effective
    # But we need to count how many effective distractors each question has.

    # First, filter to distractors row
    distractors_only = distractor_selection_counts[
        distractor_selection_counts["is_distractor"] == 1
    ]

    # Group by question_id to count effective ones
    # We sum 'is_effective' (boolean becomes int)
    effective_counts_per_question = (
        distractors_only.groupby("question_id")["is_effective"].sum().reset_index()
    )
    effective_counts_per_question.rename(
        columns={"is_effective": "num_effective"}, inplace=True
    )

    # We also need exam_id for each question
    # Map question_id to exam_id (take first, they are consistent)
    exam_id_map = distractor_selection_counts.groupby("question_id")["exam_id"].first()
    effective_counts_per_question["exam_id"] = effective_counts_per_question[
        "question_id"
    ].map(exam_id_map)

    effective_distractor_count_dict = dict()

    # Iterate through questions to populate counts
    for _, row in effective_counts_per_question.iterrows():
        exam_id = row["exam_id"]
        num_effective = int(row["num_effective"])  # 0 to 4 usually

        if exam_id not in effective_distractor_count_dict:
            effective_distractor_count_dict[exam_id] = (
                create_effective_distractor_counts_list()
            )

        # Safety check for index out of bounds
        if num_effective < len(effective_distractor_count_dict[exam_id]):
            effective_distractor_count_dict[exam_id][num_effective] += 1
        else:
            # Should not happen typically given 4 distractors max, but handle safe?
            pass

    # Normalize to percentages
    for key in effective_distractor_count_dict.keys():
        list_sum = sum(effective_distractor_count_dict[key])
        if list_sum > 0:
            for i in range(len(effective_distractor_count_dict[key])):
                effective_distractor_count_dict[key][i] = (
                    effective_distractor_count_dict[key][i] / list_sum
                )

    return effective_distractor_count_dict


def show_effective_distractor_counts(effective_distractor_count_dict):
    for key in effective_distractor_count_dict.keys():
        print(key, effective_distractor_count_dict[key])


def get_effective_distractors_per_question(distractor_counts_frame=None):
    """
    Get a dataframe with the number of effective distractors for each question.
    """
    if distractor_counts_frame is None:
        distractor_counts_frame = get_distractor_counts_frame()

    # Vectorized calculation
    # Filter to distractors that are effective
    effective_only = distractor_counts_frame[
        (distractor_counts_frame["is_distractor"] > 0)
        & (distractor_counts_frame["percent"] > 0.05)
    ]

    # Count per question
    counts = (
        effective_only.groupby("question_id")
        .size()
        .reset_index(name="effective_distractors")
    )

    # Ensure all questions are represented (some might have 0 effective distractors)
    all_questions = pd.unique(distractor_counts_frame["question_id"])
    full_df = pd.DataFrame({"question_id": all_questions})

    effective_distractors_frame = pd.merge(
        full_df, counts, on="question_id", how="left"
    ).fillna(0)
    effective_distractors_frame["effective_distractors"] = effective_distractors_frame[
        "effective_distractors"
    ].astype(int)

    return effective_distractors_frame


def add_effective_distractors_subplot(distractor_counts_dict, axis, exam_keys, title):
    labels = ["0", "1", "2", "3"]
    text_color = ["black", "black", "white"]
    bar_bottoms = [0, 0, 0, 0]
    bar_count = 0
    for key in exam_keys:
        if key not in distractor_counts_dict:
            continue

        exam_effective_distractor_percents = distractor_counts_dict[key][
            :4
        ]  # Take first 4 bins

        if len(exam_effective_distractor_percents) < 4:
            while len(exam_effective_distractor_percents) < 4:
                exam_effective_distractor_percents.append(0)

        exam_effective_distractor_percents = (
            np.array(exam_effective_distractor_percents) * 100
        )
        axis.bar(
            labels, exam_effective_distractor_percents, label=key, bottom=bar_bottoms
        )

        for i in range(len(bar_bottoms)):
            bar_bottoms[i] += exam_effective_distractor_percents[i]

        for j in range(len(exam_effective_distractor_percents)):
            y_position = bar_bottoms[j] - exam_effective_distractor_percents[j] / 2
            if exam_effective_distractor_percents[j] >= 20:
                color = text_color[bar_count % len(text_color)]
                axis.text(
                    labels[j],
                    y_position,
                    f"{exam_effective_distractor_percents[j]:.2f}",
                    color=color,
                    ha="center",
                    va="bottom",
                    fontsize=10,
                )
        bar_count += 1

    axis.legend(prop={"size": 10})
    axis.set_xlabel("Number of Effective Distractors")
    axis.set_ylabel("Percent of Questions")
    axis.set_title(title)


def save_effective_distractors_plots(distractor_counts_dict=None, filename=None):
    if distractor_counts_dict is None:
        distractor_counts_dict = get_effective_distractors_by_form()
    if filename is None:
        filename = "./figures/effective_distractors_bar_chart.png"

    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(10, 6))

    add_effective_distractors_subplot(
        distractor_counts_dict, ax0, ["1A", "1B"], "Exam 1"
    )
    add_effective_distractors_subplot(
        distractor_counts_dict, ax1, ["2A", "2B", "2C"], "Exam 2"
    )
    add_effective_distractors_subplot(
        distractor_counts_dict, ax2, ["3A", "3B", "3C"], "Exam 3"
    )
    add_effective_distractors_subplot(
        distractor_counts_dict, ax3, ["4A", "4B", "4C"], "Exam 4"
    )

    fig.tight_layout()

    try:
        plt.savefig(filename)
    except FileNotFoundError:
        if not filename.startswith("."):
            filename = "." + filename
        plt.savefig(filename)

    plt.close(fig)


if __name__ == "__main__":
    dict_of_dfs = database_utils.load_database_to_dict_of_dfs()

    exam_distractors_chosen_frame = get_percent_of_distractors_by_form()
    save_distractors_chosen_plots(exam_distractors_chosen_frame, filename=None)

    print(get_distractor_counts_frame(dict_of_dfs))

    distractor_counts_dict = get_effective_distractors_by_form()
    show_effective_distractor_counts(distractor_counts_dict)
    save_effective_distractors_plots(distractor_counts_dict, filename=None)
