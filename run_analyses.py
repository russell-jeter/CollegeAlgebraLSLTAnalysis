from analyses import (
    exam_and_distractor_counts,
    effective_distractors_analysis,
    item_summary,
    student_summary,
    item_difficulty,
    kr_20_analysis,
    observed_score_statistics_and_distributions,
    rasch_analysis,
)


def main():
    """
    Main execution script for College Algebra LSLT Analysis.
    Runs various statistical analyses and generates reports/figures.
    """
    print("Starting Analysis...")

    # Observed Score Statistics
    print("Calculating observed score statistics...")
    observed_score_statistics_and_distributions.get_student_exam_taken_count()
    observed_score_statistics_and_distributions.export_observed_score_statistics()
    #observed_score_statistics_and_distributions.save_os_distribution_plots()
    #Display Exam and distractor counts
    exam_and_distractor_counts.show_question_counts()
    exam_and_distractor_counts.show_exam_question_distractor_counts()
    exam_and_distractor_counts.show_student_distractor_selection_counts()

    # Distractor Analysis (Commented out in original, kept commented)
    # effective_distractors_analysis.show_effective_distractors_by_form()
    # effective_distractors_analysis.show_percent_of_distractors_by_form()

    #Save KR-20 Analysis
    kr_20_analysis.get_kr_20_frame().to_excel('KR_20_frame.xlsx')

    #Save item difficulty plots
    #item_difficulty.save_item_difficulty_distributions()
    #item_difficulty.save_pbc_distribution_plots()
    #item_difficulty.show_pbc_ranges()

    # Item Summary
    print("Saving item summary...")
    item_summary_frame = item_summary.get_item_summary_frame()
    item_summary_frame.to_excel("item_summary.xlsx", index=False)

    # Student Summary
    print("Saving student summary...")
    student_summary_frame = student_summary.get_student_summary_frame()
    student_summary_frame.to_excel("student_summary.xlsx", index=False)
