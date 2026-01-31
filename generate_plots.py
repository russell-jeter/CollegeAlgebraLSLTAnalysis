from analyses import (
    observed_score_statistics_and_distributions,
    item_difficulty,
    rasch_analysis,
    effective_distractors_analysis,
    integrated_methodology
)

if __name__ == "__main__":

    # Observed Score Distribution
    print("Generating Observed Score Distribution plots...")
    observed_score_statistics_and_distributions.save_os_distribution_plots()

    # Save item difficulty plots
    print("Generating Item Difficulty plots...")
    item_difficulty.save_item_difficulty_distributions()
    item_difficulty.save_pbc_distribution_plots_with_thresholds()

    # Save 1PL and 3PL models
    print("Running Rasch Analysis and saving distributions...")
    rasch_analysis_dict = rasch_analysis.get_rasch_students_and_items_frames_as_dict()

    rasch_items_df = rasch_analysis_dict["rasch_items_df"]
    rasch_analysis.save_rasch_distributions_both_PL('items', rasch_df = rasch_items_df)

    rasch_student_df = rasch_analysis_dict["rasch_student_df"]
    rasch_analysis.save_rasch_distributions_both_PL('students', rasch_df = rasch_student_df)

    # Save fit plots
    print("Generating Fit plots...")
    rasch_analysis.save_fit_plots(rasch_items_df, 'infit', 'items')
    rasch_analysis.save_fit_plots(rasch_items_df, 'outfit', 'items')

    # Distractors 
    print("Generating Distractor plots...")
    exam_distractors_chosen_frame = effective_distractors_analysis.get_percent_of_distractors_by_form()
    effective_distractors_analysis.save_distractors_chosen_plots(exam_distractors_chosen_frame, filename=None)
    
    distractor_counts_dict = effective_distractors_analysis.get_effective_distractors_by_form()
    effective_distractors_analysis.save_effective_distractors_plots(distractor_counts_dict, filename=None)

    effective_distractors_analysis.save_effective_distractor_category_plots(distractor_counts_dict, filename=None)

    print("Generating integrated methodology heatmaps.")
    integrated_methodology.generate_integrated_methodology_heatmaps()

    print("All plots generated successfully.")
