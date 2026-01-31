from analyses import effective_distractors_analysis, item_difficulty, observed_score_statistics_and_distributions, rasch_analysis, database_utils

if __name__ == "__main__":

    # Observed Score Distribution
    observed_score_statistics_and_distributions.save_os_distribution_plots()

    #Save item difficulty distribution and classification
    item_difficulty.save_item_difficulty_distributions()
    item_difficulty.save_item_difficulty_category_distributions()

    # Save PBC distribution and classification
    item_difficulty.save_pbc_distribution_plots_with_thresholds()
    item_difficulty.save_pbc_distribution_plots()

    # Save 1PL and 3PL models
    rasch_analysis_dict = rasch_analysis.get_rasch_students_and_items_frames_as_dict()

    rasch_items_df = rasch_analysis_dict["rasch_items_df"]
    rasch_analysis.save_rasch_distributions_both_PL('items', rasch_df = rasch_items_df)

    rasch_student_df = rasch_analysis_dict["rasch_student_df"]
    rasch_analysis.save_rasch_distributions_both_PL('students', rasch_df = rasch_student_df)

    # Save fit plots
    rasch_analysis.save_fit_plots(rasch_items_df, 'infit', 'items')
    rasch_analysis.save_fit_plots(rasch_items_df, 'outfit', 'items')

    # Distractors 
    dict_of_dfs = database_utils.load_database_to_dict_of_dfs()
    exam_distractors_chosen_frame = effective_distractors_analysis.get_percent_of_distractors_by_form()

    effective_distractors_analysis.save_distractors_chosen_plots(exam_distractors_chosen_frame, filename = None)

    distractor_counts_dict = effective_distractors_analysis.get_effective_distractors_by_form()
    effective_distractors_analysis.save_effective_distractors_plots(distractor_counts_dict, filename = None)
    # TO DO: Effective distractors in Poor-Acceptable-Ideal classification