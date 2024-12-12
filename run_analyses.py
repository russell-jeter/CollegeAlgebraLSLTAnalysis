from analyses import exam_and_distractor_counts, effective_distractors_analysis, item_summary, item_difficulty, kr_20_analysis, observed_score_statistics_and_distributions

if __name__ == "__main__":

    observed_score_statistics_and_distributions.get_student_exam_taken_count()
    observed_score_statistics_and_distributions.export_observed_score_statistics()
    observed_score_statistics_and_distributions.save_os_distribution_plots()
    #Display Exam and distractor counts
    exam_and_distractor_counts.show_question_counts()
    exam_and_distractor_counts.show_exam_question_distractor_counts()
    exam_and_distractor_counts.show_student_distractor_selection_counts()

    #Display distractor analysis
    effective_distractors_analysis.show_effective_distractors_by_form()
    effective_distractors_analysis.show_percent_of_distractors_by_form()

    #Display KR-20 Analysis
    print(kr_20_analysis.get_kr_20_frame())

    #Save item difficulty plots
    item_difficulty.save_item_difficulty_distributions()
    item_difficulty.save_pbc_distribution_plots()

    #Save item summary frame
    item_summary_frame = item_summary.get_item_summary_frame()
    item_summary_frame.to_excel("item_summary.xlsx", index = False)