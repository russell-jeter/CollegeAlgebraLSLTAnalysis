import utils
from effective_distractors_analysis import get_distractor_counts_frame
import matplotlib.pyplot as plt


def get_item_difficulty_frame():

    distractor_selection_counts = get_distractor_counts_frame()
    item_difficulty_frame = distractor_selection_counts[distractor_selection_counts["is_distractor"] == 0]

    item_difficulty_frame = item_difficulty_frame[["question_id", "exam_id", "count", "percent"]]
    item_difficulty_frame = item_difficulty_frame.rename(columns = {"percent": "item_difficulty"})

    return item_difficulty_frame

def add_item_difficulty_subplot(item_difficulty_frame, axis, bins, exam_keys, title):
    data_list = []
    for key in exam_keys:
        data_list.append(item_difficulty_frame[item_difficulty_frame["exam_id"].isin([key])]["item_difficulty"].values)
    axis.hist(data_list, bins, histtype='bar', label=exam_keys)
    axis.legend(prop={'size': 10})
    axis.set_xlabel("Item Difficulty")
    axis.set_ylabel("Number of Questions")
    axis.set_title(title)

def save_item_difficulty_distributions(item_difficulty_frame = None, filename = None):
    if type(item_difficulty_frame) == type(None):
        item_difficulty_frame = get_item_difficulty_frame()
    if type(filename) == type(None):
        filename = "./figures/item_difficulty_distributions.png"
    bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]


    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(10,6))

    add_item_difficulty_subplot(item_difficulty_frame, ax0, bins, ["1A", "1B"], "Exam 1")
    add_item_difficulty_subplot(item_difficulty_frame, ax1, bins, ["2A", "2B", "2C"], "Exam 2")
    add_item_difficulty_subplot(item_difficulty_frame, ax2, bins, ["3A", "3B", "3C"], "Exam 3")
    add_item_difficulty_subplot(item_difficulty_frame, ax3, bins, ["4A", "4B", "4C"], "Exam 4")

    fig.tight_layout()
    plt.savefig(filename)

if __name__ == "__main__":
    print(get_item_difficulty_frame())
    save_item_difficulty_distributions()