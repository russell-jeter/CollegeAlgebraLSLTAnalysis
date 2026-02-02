try:
    from analyses import database_utils
except ImportError:
    import database_utils

import numpy as np
import pandas as pd
import math
import statistics
import os
import matplotlib.pyplot as plt
import matplotlib

# Color palette for plots
CUSTOM_PALETTE = ["#cf4456", "#f29566", "#831c64", "#2f0f3e", "#feedb0"]
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", CUSTOM_PALETTE)


def exam_num_ver_df(num_and_ver, df):
    """Returns dataframe df with just rows with 'question_id' starting with num_and_ver."""
    # Applies lambda function searching for rows (axis=1) with 'question_id' = num_and_ver
    exam_mask = df["question_id"].str.startswith(num_and_ver)
    return df[exam_mask]


def questions_to_columns(df):
    """Reorganizes student responses to a single exam into columns by question_id."""
    # Optimization: pivot using pandas built-in functions instead of loops
    # Assuming one row per student-question pair
    restructured_df = df.pivot(
        index="student_id", columns="question_id", values="selected_option"
    )

    # Drops bad questions
    bad_question = [
        "4A01",
        "4B01",
        "4C01",
    ]  # Exam 4 question 1 is "what version exam do you have"
    restructured_df = restructured_df.drop(
        columns=[q for q in bad_question if q in restructured_df.columns]
    )

    return restructured_df


def create_num_ver_key_dict(num_and_ver, key_df):
    """Creates a key for the num_and_ver exam to be used for the correct/incorrect matrix."""
    exam_key_df = exam_num_ver_df(num_and_ver, key_df)

    # Create dictionary mapping question_id to option_id (converted to str '1'-'5')

    option_ids = exam_key_df["option_id"].replace(
        {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5"}
    )
    # Ensure it's string format of int (like '1', '2')
    try:
        answers = option_ids.astype(int).tolist()
    except ValueError:
        # Fallback if mixed types
        answers = option_ids.tolist()

    question_ids = exam_key_df["question_id"].tolist()
    return dict(zip(question_ids, answers))


def true_false_df(df, key_dict):
    """Creates 0/1 df by matching key_dict to each student's response."""
    # Vectorized comparison
    # Align columns of df with keys in key_dict
    # df columns are question_ids. key_dict keys are question_ids.

    # Only compare columns that exist in both
    common_cols = [c for c in df.columns if c in key_dict]

    # Create a series from dict to compare against
    key_series = pd.Series(key_dict)

    # Alignment ensures we compare correctly
    return df[common_cols].eq(key_series[common_cols]).astype(int)


def remove_issue_scores(df):
    """
    Remove students & questions with 100% scores and 0% scores.
    These cause issues with ability and difficulty estimates in Rasch (infinity).
    """
    temp_df = df.copy()

    # 1. Remove students (rows) with perfect or zero scores
    # Score is sum of row
    student_scores = temp_df.sum(axis=1)
    max_score = temp_df.shape[1]  # Number of questions

    students_to_drop = student_scores[
        (student_scores == max_score) | (student_scores == 0)
    ].index
    temp_df = temp_df.drop(index=students_to_drop)

    # 2. Remove questions (columns) with perfect or zero scores
    # Question score is mean of column (since 0/1)
    # If mean is 0 -> all wrong/zero. If mean is 1 -> all right/one.
    question_means = temp_df.mean(axis=0)
    questions_to_drop = question_means[
        (question_means == 0) | (question_means == 1)
    ].index
    temp_df = temp_df.drop(columns=questions_to_drop)

    return temp_df


def collect_all_exam_numbers_and_forms(df):
    """Defines list of all exam numbers [character 0-1] and exam forms [character 2?]."""
    return sorted(list(set(df["question_id"].str[:2].unique())))


def create_true_false_for_all_exams(full_df, key_df, all_exam_numbers_and_forms):
    """Generates a list of dictionaries containing True/False dataframes for each exam."""
    list_of_tf_dfs = []

    for exam_num_and_form in all_exam_numbers_and_forms:
        temp_exam_df = exam_num_ver_df(exam_num_and_form, full_df)
        if temp_exam_df.empty:
            continue

        temp_exam_responses_df = questions_to_columns(temp_exam_df)
        temp_exam_answer_key = create_num_ver_key_dict(exam_num_and_form, key_df)
        temp_exam_tf_df = true_false_df(temp_exam_responses_df, temp_exam_answer_key)

        list_of_tf_dfs.append(
            {"exam_num_and_form": exam_num_and_form, "true_false_df": temp_exam_tf_df}
        )

    return list_of_tf_dfs


def ability_estimate(avg_student_score):
    """Calculates ability estimate (theta) from average student score (proportion correct)."""
    # Logit function: log(p / (1-p))
    # Handle cases where p=0 or p=1 to avoid math domain error,
    # though remove_issue_scores should prevent this.
    try:
        return math.log(avg_student_score / (1 - avg_student_score))
    except (ValueError, ZeroDivisionError):
        return 0


def difficulty_estimate(avg_question_score):
    """Calculates difficulty estimate (beta) from average question score (proportion correct)."""
    # Logit of failure: log((1-p)/p)
    try:
        return math.log((1 - avg_question_score) / avg_question_score)
    except (ValueError, ZeroDivisionError):
        return 0


def approximate_ability_and_difficulty(df, answer_choices_df, questions_df=None):
    """
    Calculate initial ability and difficulty estimates based on 0/1 df.
    """
    if questions_df is None:
        questions_df = pd.DataFrame()

    temp_df = df.copy()

    # Student Ability (theta)
    # mean by row (axis=1)
    avg_student_score = temp_df.mean(axis=1)
    theta_s = avg_student_score.apply(ability_estimate).tolist()

    # Question Difficulty (beta)
    # mean by column (axis=0)
    avg_question_score = temp_df.mean(axis=0)
    beta_i_non_normal = avg_question_score.apply(difficulty_estimate)

    # Normalize beta
    avg_beta_i = beta_i_non_normal.mean()
    beta_i = beta_i_non_normal - avg_beta_i
    beta_i_keys = beta_i.index.tolist()

    # Extract difficulty coefficients if available
    diff_coeff_list = []

    # Check if 'difficulty_coeff' exists and is useful
    use_coeffs = False
    if "difficulty_coeff" in questions_df.columns:
        # Check if we have valid data
        if not questions_df["difficulty_coeff"].dropna().empty:
            use_coeffs = True

    if not use_coeffs:
        diff_coeff_list = [1.0] * len(beta_i)
    else:
        # Map coefficients
        # Need to join beta_i_keys (question_ids) with questions_df
        # Create a temp dataframe for mapping
        mapping_df = pd.DataFrame({"question_id": beta_i_keys})
        merged = pd.merge(
            mapping_df,
            questions_df[["question_id", "difficulty_coeff"]],
            on="question_id",
            how="left",
        )

        # Fill NaNs with 1
        merged["difficulty_coeff"] = merged["difficulty_coeff"].fillna(1.0)
        diff_coeff_list = merged["difficulty_coeff"].tolist()

    # Guessing parameters (1 / number of options)
    # Use vectorized value_counts lookup or similar
    # answer_choices_df has one row per option.
    # We want count of options per question.
    option_counts = answer_choices_df.groupby("question_id").size()

    guess_p_list = []
    for q_id in beta_i_keys:
        count = option_counts.get(q_id, 4)  # Default to 4 if not found?
        guess_p_list.append(1.0 / count)

    return {
        "beta_i_keys": beta_i_keys,
        "diff_coeff_i": diff_coeff_list,
        "beta_i": beta_i.tolist(),
        "guess_i": guess_p_list,
        "theta_s": theta_s,
    }


def iterate_variable_estimates(variable_estimates_dict, variance_df, residuals_df):
    """
    Adjust beta_i and theta_s estimates based on residuals and variance.
    """
    diff_coeff_i = list(variable_estimates_dict["diff_coeff_i"])
    beta_i = list(variable_estimates_dict["beta_i"])
    guess_i = list(variable_estimates_dict["guess_i"])
    theta_s = list(variable_estimates_dict["theta_s"])
    beta_i_keys = list(variable_estimates_dict["beta_i_keys"])

    # Update Beta (Item Difficulty)
    # Sum of columns
    residual_col_sum = residuals_df.sum(axis=0)
    variance_col_sum = variance_df.sum(axis=0)

    # Ensure alignment
    # variance_df and residuals_df columns match beta_i_keys order?
    # They should since constructed from same base_df.
    # But let's be safe and iterate by index

    new_beta_i = []
    # Using enumerate assuming order preservation
    for idx, key in enumerate(beta_i_keys):
        # residuals_df[key] might be missing if dropped?
        # But this function is called inside the loop where dfs are consistent.

        res_sum = residual_col_sum.get(key, 0)
        var_sum = variance_col_sum.get(key, 1e-9)  # avoid div 0

        current_beta = beta_i[idx]
        new_beta = current_beta - (res_sum / var_sum)
        new_beta_i.append(new_beta)

    # Update Theta (Student Ability)
    residual_row_sum = residuals_df.sum(axis=1)
    variance_row_sum = variance_df.sum(axis=1)

    new_theta_s = []
    # theta_s corresponds to rows of residuals_df

    row_indices = residuals_df.index
    for idx, student_id in enumerate(row_indices):
        res_sum = residual_row_sum.loc[student_id]
        var_sum = variance_row_sum.loc[student_id]

        current_theta = theta_s[idx]
        new_theta = current_theta + (res_sum / var_sum)
        new_theta_s.append(new_theta)

    # Normalize new betas
    beta_mean = statistics.fmean(new_beta_i)
    new_beta_i = [x - beta_mean for x in new_beta_i]

    return {
        "beta_i": new_beta_i,
        "diff_coeff_i": diff_coeff_i,
        "guess_i": guess_i,
        "theta_s": new_theta_s,
        "beta_i_keys": beta_i_keys,
    }


def calc_expected_values(variable_estimates_dict, model_parameters):
    """
    Calculate expected values (probability of correct response).
    Returns DataFrame matching indices of students and columns of items.
    """
    diff_coeff_i = np.array(variable_estimates_dict["diff_coeff_i"])
    beta_i = np.array(variable_estimates_dict["beta_i"])
    guess_i = np.array(variable_estimates_dict["guess_i"])
    theta_s = np.array(variable_estimates_dict["theta_s"])
    beta_i_keys = variable_estimates_dict["beta_i_keys"]

    # Vectorized calculation using broadcasting
    # theta_s is (n_students, 1)
    # beta_i is (1, n_items)

    theta_matrix = theta_s[:, np.newaxis]
    beta_matrix = beta_i[np.newaxis, :]
    diff_coeff_matrix = diff_coeff_i[np.newaxis, :]
    guess_matrix = guess_i[np.newaxis, :]

    if model_parameters == 3:
        # 3PL Model
        # P(theta) = c + (1-c) * (exp(1.7*a*(theta-b)) / (1 + ...))
        # Here: guess_i is c, diff_coeff_i is a, beta_i is b

        exponent = 1.7 * diff_coeff_matrix * (theta_matrix - beta_matrix)
        # Numerical stability: clip exponent? math.exp overflows for large values (>709)
        # Using np.exp with careful handling

        # Compute sigmoid part
        # exp(x) / (1 + exp(x)) = 1 / (1 + exp(-x))
        # So let's use standard logistic function

        # prob = guess + (1 - guess) * sigmoid(exponent)

        # Use np.exp with clip to avoid overflow
        exponent = np.clip(exponent, -100, 100)  # Safe range
        exp_vals = np.exp(exponent)
        sigmoid = exp_vals / (1 + exp_vals)

        expected_values = guess_matrix + ((1 - guess_matrix) * sigmoid)

    else:  # 1PL Model (Rasch)
        # P(theta) = exp(theta - beta) / (1 + exp(theta-beta))
        exponent = theta_matrix - beta_matrix
        exponent = np.clip(exponent, -100, 100)
        exp_vals = np.exp(exponent)
        expected_values = exp_vals / (1 + exp_vals)

    ev_df = pd.DataFrame(expected_values, columns=beta_i_keys)
    return ev_df


def calc_est_var(df):
    """Calculates variance of expected values: p * (1 - p)."""
    return df * (1 - df)


def calc_sum_sqr_residuals(df):
    """Calculate sum of squared residuals."""
    return df.pow(2).sum().sum()


def calc_Q3_bar(df):
    """Calculates avg correlation."""
    full_sum = df.sum().sum()
    num_of_items = df.shape[0]
    # avg_corr when i != j subtracts off diagonal and divides by 2 from double counting
    sum_distinct_corr = (full_sum - num_of_items) / 2
    combin_coeff = math.comb(num_of_items, 2)
    return (1 / combin_coeff) * sum_distinct_corr


def calc_Q3_star(df):
    """
    Calculates the maximum difference of Q3 correlations by item
    MAX( highest Q3 - q3_bar, -( lowest Q3 - q3_bar) )
    Returns series with question items as indicies
    """
    min_max_df = pd.DataFrame()

    # We ignore diagonal (self-correlation = 1).
    dropped_dig = df.copy()
    np.fill_diagonal(dropped_dig.values, np.nan)  # Safer to use nan for diagonal

    q3_bar = calc_Q3_bar(df)

    # Max and min ignoring NaNs
    min_max_df["pos_q3*"] = dropped_dig.max(axis=0) - q3_bar
    min_max_df["neg_q3*"] = -(dropped_dig.min(axis=0) - q3_bar)
    q3_star_series = min_max_df.max(axis=1)
    return q3_star_series


def build_rasch_model(base_df, answer_choices_df, model_parameters, questions_df=None):
    """
    Builds the Rasch model (1PL or 3PL) iteratively.
    """
    if questions_df is None:
        questions_df = pd.DataFrame()

    student_ids = base_df.index.tolist()

    # Initialize variables
    variable_estimates_dict = approximate_ability_and_difficulty(
        base_df, answer_choices_df, questions_df
    )

    sum_sqr_res_current = 10000
    sum_sqr_res_previous = 0
    iteration_num = 0

    # Iteration loop
    # Limit iterations to avoid infinite loops if convergence is slow/oscillating
    max_iterations = 100
    converged = False

    while (
        abs(sum_sqr_res_current - sum_sqr_res_previous) > 0.001
        and iteration_num < max_iterations
    ):
        if iteration_num > 0:
            variable_estimates_dict = iterate_variable_estimates(
                variable_estimates_dict, est_var_ex_vals_df, residuals_df
            )

        expected_values_df = calc_expected_values(
            variable_estimates_dict, model_parameters
        )
        est_var_ex_vals_df = calc_est_var(expected_values_df)

        # Align indices
        base_df.index = expected_values_df.index
        residuals_df = base_df - expected_values_df

        sum_sqr_res_previous = sum_sqr_res_current
        sum_sqr_res_current = calc_sum_sqr_residuals(residuals_df)

        iteration_num += 1

    # Final output generation

    # Q3 test for item local independence
    # exam_id from column name (e.g. '1A01') -> '1A'
    if not residuals_df.empty and not residuals_df.columns.empty:
        exam_id = residuals_df.columns[0][0:2]
    else:
        exam_id = "Unknown"

    corr_df = residuals_df.corr()

    # Q3* by item
    q3_star_series = calc_Q3_star(corr_df)
    q3_star_series.name = f"q3_star_items_{model_parameters}PL"

    # Save correlation matrix
    output_dir = "./corr_matrix"
    os.makedirs(output_dir, exist_ok=True)
    corr_df.to_excel(f"{output_dir}/residual_exam{exam_id}_{model_parameters}PL.xlsx")

    # Fit statistics
    # Standardize infinite variance to avoid division by zero?
    # Usually est_var is very small but non-zero.
    fit_df = residuals_df.pow(2) / est_var_ex_vals_df
    fit_df.index = student_ids

    var_estimates_students = pd.Series(
        variable_estimates_dict["theta_s"], index=student_ids
    )
    var_estimates_students.name = f"var_estimates_students_{model_parameters}PL"

    var_estimates_items = pd.Series(
        variable_estimates_dict["beta_i"], index=variable_estimates_dict["beta_i_keys"]
    )
    var_estimates_items.name = f"var_estimates_items_{model_parameters}PL"

    # Outfit (Outlier-Sensitivity fit) Unweighted Fit Mean Square
    outfit_students = fit_df.mean(axis=1)
    outfit_students.index = student_ids
    outfit_students.name = f"outfit_students_{model_parameters}PL"

    outfit_items = fit_df.mean(axis=0)
    outfit_items.name = f"outfit_items_{model_parameters}PL"

    # Infit (Inlier-Sensitivity fit) Weighted Fit Mean Square
    infit_students = residuals_df.pow(2).sum(axis=1) / est_var_ex_vals_df.sum(axis=1)
    infit_students.index = student_ids
    infit_students.name = f"infit_students_{model_parameters}PL"

    infit_items = residuals_df.pow(2).sum(axis=0) / est_var_ex_vals_df.sum(axis=0)
    infit_items.name = f"infit_items_{model_parameters}PL"

    return {
        "exam_id": exam_id,
        f"fit_df_{model_parameters}PL": fit_df,
        f"var_estimates_students_{model_parameters}PL": var_estimates_students,
        f"var_estimates_items_{model_parameters}PL": var_estimates_items,
        f"outfit_students_{model_parameters}PL": outfit_students,
        f"outfit_items_{model_parameters}PL": outfit_items,
        f"infit_students_{model_parameters}PL": infit_students,
        f"infit_items_{model_parameters}PL": infit_items,
        f"q3_star_items_{model_parameters}PL": q3_star_series,
        "true_false_df": base_df,  # Actually added later in loop, but useful to return if needed
    }


def join_series_from_list_on_index(list_of_series):
    """Joins list of Series into a DataFrame on shared index."""
    if not list_of_series:
        return pd.DataFrame()

    return pd.concat(list_of_series, axis=1, join="inner")


def build_rasch_dfs(list_of_rasch_dicts):
    """
    Combines Rasch analysis results from multiple exams into unified Student and Item DataFrames.
    """
    list_of_student_dfs = []
    list_of_item_dfs = []

    for rasch_dict in list_of_rasch_dicts:
        # 1. Process Students
        student_stats_keys = [
            "var_estimates_students_1PL",
            "outfit_students_1PL",
            "infit_students_1PL",
            "var_estimates_students_3PL",
            "outfit_students_3PL",
            "infit_students_3PL",
        ]
        student_series = [rasch_dict[k] for k in student_stats_keys if k in rasch_dict]

        # Calculate raw exam score
        student_score_series = rasch_dict["true_false_df"].mean(axis=1)
        student_score_series.name = "student_exam_score"
        student_series.append(student_score_series)

        temp_student_df = join_series_from_list_on_index(student_series)
        temp_student_df["exam_id"] = rasch_dict["exam_id"]

        # Standard Error for Fit Stats
        # SE = sqrt(2/N_items)
        temp_standard_error = (
            math.sqrt(2 / len(temp_student_df)) if len(temp_student_df) > 0 else 0
        )

        for model_parameters in [1, 3]:
            suffix = f"_{model_parameters}PL"

            # Helper to categorize
            def categorize(val, se):
                lower = 1 - 2 * se
                upper = 1 + 2 * se
                if val <= lower:
                    return 1  # Low fit means overly predictable
                return 1 if val <= lower else 0

            def categorize_acc(val, se):
                lower = 1 - 2 * se
                upper = 1 + 2 * se
                return 1 if (lower < val < upper) else 0

            def categorize_poor(val, se):
                upper = 1 + 2 * se
                return 1 if val >= upper else 0

            # Vectorized categorization
            for measure in ["outfit", "infit"]:
                col = f"{measure}_students{suffix}"
                if col in temp_student_df.columns:
                    val = temp_student_df[col]
                    temp_student_df[f"is_good_{measure}{suffix}"] = (
                        val <= (1 - 2 * temp_standard_error)
                    ).astype(int)
                    temp_student_df[f"is_acceptable_{measure}{suffix}"] = (
                        (val > (1 - 2 * temp_standard_error))
                        & (val < (1 + 2 * temp_standard_error))
                    ).astype(int)
                    temp_student_df[f"is_poor_{measure}{suffix}"] = (
                        val >= (1 + 2 * temp_standard_error)
                    ).astype(int)

        list_of_student_dfs.append(temp_student_df)

        # 2. Process Items
        item_stats_keys = [
            "var_estimates_items_1PL",
            "outfit_items_1PL",
            "infit_items_1PL",
            "var_estimates_items_3PL",
            "outfit_items_3PL",
            "infit_items_3PL",
            "q3_star_items_1PL",
            "q3_star_items_3PL",
        ]
        item_series = [rasch_dict[k] for k in item_stats_keys if k in rasch_dict]
        temp_item_df = join_series_from_list_on_index(item_series)

        # Categorize items
        for model_parameters in [1, 3]:
            suffix = f"_{model_parameters}PL"
            for measure in ["outfit", "infit"]:
                col = f"{measure}_items{suffix}"
                if col in temp_item_df.columns:
                    val = temp_item_df[col]
                    
                    temp_item_df[f"is_good_{measure}{suffix}"] = (
                        val <= (1 - 2 * temp_standard_error)
                    ).astype(int)
                    temp_item_df[f"is_acceptable_{measure}{suffix}"] = (
                        (val > (1 - 2 * temp_standard_error))
                        & (val < (1 + 2 * temp_standard_error))
                    ).astype(int)
                    temp_item_df[f"is_poor_{measure}{suffix}"] = (
                        val >= (1 + 2 * temp_standard_error)
                    ).astype(int)

        list_of_item_dfs.append(temp_item_df)

    rasch_students_df = (
        pd.concat(list_of_student_dfs) if list_of_student_dfs else pd.DataFrame()
    )
    rasch_students_df.index.name = "student_id"

    rasch_items_df = pd.concat(list_of_item_dfs) if list_of_item_dfs else pd.DataFrame()
    rasch_items_df.index.name = "question_id"

    return [rasch_students_df, rasch_items_df]


def get_rasch_students_and_items_frames_as_dict():
    """
    Main function to orchestrate Rasch analysis.
    Loads data, processes each exam, builds models, and aggregates results.
    """
    try:
        raw_df, key_df, options_df, questions_df = database_utils.load_all_sheets()
    except AttributeError:
        # Fallback if database_utils doesn't have load_all_sheets
        # Manually load
        dict_dfs = database_utils.load_database_to_dict_of_dfs()
        raw_df = dict_dfs.get("student_question_responses", pd.DataFrame())
        key_df = dict_dfs.get("answer_choices", pd.DataFrame())
        options_df = key_df.copy()
        questions_df = dict_dfs.get("questions", pd.DataFrame())

    # Filter key for correct answers only (is_distractor == 0)
    key_df_correct = key_df[key_df["is_distractor"] == 0]

    all_exam_numbers_and_forms = collect_all_exam_numbers_and_forms(raw_df)

    # Create True/False matrices
    list_of_tf_dfs = create_true_false_for_all_exams(
        raw_df, key_df_correct, all_exam_numbers_and_forms
    )

    list_of_rasch_dicts = []

    for exam_dict in list_of_tf_dfs:
        # Clean data
        no_error_exam_df = remove_issue_scores(exam_dict["true_false_df"])

        if no_error_exam_df.empty:
            continue

        # 1PL Model
        rasch_dict_1PL = build_rasch_model(
            no_error_exam_df.copy(), options_df, 1, questions_df
        )

        # 3PL Model
        rasch_dict_3PL = build_rasch_model(
            no_error_exam_df.copy(), options_df, 3, questions_df
        )

        # Merge results
        full_rasch_dict = {**rasch_dict_1PL, **rasch_dict_3PL}
        full_rasch_dict["exam_num_and_form"] = exam_dict["exam_num_and_form"]
        full_rasch_dict["true_false_df"] = exam_dict["true_false_df"]

        list_of_rasch_dicts.append(full_rasch_dict)

    rasch_students_df, rasch_items_df = build_rasch_dfs(list_of_rasch_dicts)
    return {"rasch_student_df": rasch_students_df, "rasch_items_df": rasch_items_df}

def add_rasch_subplot(rasch_df, axis, bins, exam_keys, title, PL, variable_type):
    data_list = []
    for key in exam_keys:
        subset = rasch_df[rasch_df["exam_id"].isin([key])]
        col_name = f"var_estimates_{variable_type}_{PL}PL"
        if col_name in subset:
            data_list.append(subset[col_name].values)
        else:
            data_list.append([])

    axis.hist(data_list, bins, histtype="bar", stacked=True, label=exam_keys)
    axis.legend(prop={"size": 10})

    fmt = matplotlib.ticker.StrMethodFormatter("{x:.1f}")
    axis.xaxis.set_major_formatter(fmt)
    fmt = matplotlib.ticker.StrMethodFormatter("{x:.0f}")
    axis.yaxis.set_major_formatter(fmt)
    if variable_type == 'items':
        axis.set_xlabel(f"Estimated Item Difficulty for {PL}PL Model, " + r"$\beta$")
        axis.set_ylabel("Number of Questions")
    elif variable_type == 'students':
        axis.set_xlabel(f"Estimated Student Ability for {PL}PL Model, " + r"$\theta$")
        axis.set_ylabel("Number of Students")
    axis.set_title(title)

def save_rasch_distributions_by_PL(PL, variable_type, rasch_df = None, filename = None):
    if type(rasch_df) == type(None):
        rasch_analysis_dict = get_rasch_students_and_items_frames_as_dict()
        if variable_type == "items":
            rasch_df = rasch_analysis_dict["rasch_items_df"]
        elif variable_type == "students":
            rasch_df = rasch_analysis_dict["rasch_students_df"]

    if filename is None:
        filename = f"./figures/rasch_{variable_type}_distributions_{PL}PL.png"

    # Ensure exam_id exists
    if "exam_id" not in rasch_df.columns:
        # Try to derive from question_id if items
        if variable_type == "items":
            # Check if index is question_id
            if rasch_df.index.name == "question_id":
                rasch_df = rasch_df.reset_index()
            if "question_id" in rasch_df.columns:
                rasch_df["exam_id"] = rasch_df["question_id"].str[:2]

    # rcParams for LaTeX? May fail if latex not installed. Using standard.
    # plt.rcParams['text.usetex'] = True
    # Commented out to improve robustness

    bins = [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]

    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(10, 6))

    add_rasch_subplot(rasch_df, ax0, bins, ["1A", "1B"], "Exam 1", PL, variable_type)
    add_rasch_subplot(
        rasch_df, ax1, bins, ["2A", "2B", "2C"], "Exam 2", PL, variable_type
    )
    add_rasch_subplot(
        rasch_df, ax2, bins, ["3A", "3B", "3C"], "Exam 3", PL, variable_type
    )
    add_rasch_subplot(
        rasch_df, ax3, bins, ["4A", "4B", "4C"], "Exam 4", PL, variable_type
    )

    fig.tight_layout()

    output_dir = os.path.dirname(filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        plt.savefig(filename)
    except FileNotFoundError:
        # Should be handled by makedirs, but just in case
        pass

    plt.close(fig)

def save_rasch_distributions_both_PL(variable_type, rasch_df = None, filename = None):
    if type(rasch_df) == type(None):
        rasch_analysis_dict = get_rasch_students_and_items_frames_as_dict()
        if variable_type == 'items':
            rasch_df = rasch_analysis_dict["rasch_items_df"]
        elif variable_type == 'students':
            rasch_df = rasch_analysis_dict["rasch_students_df"]
    if type(filename) == type(None):
        if variable_type == 'items':
            filename = f"./figures/rasch_items_distributions_all.png"
        elif variable_type == 'students':
            filename = f"./figures/rasch_students_distributions_all.png"

    rasch_df = rasch_df.reset_index()
    if variable_type == 'items':
        rasch_df["exam_id"] = rasch_df["question_id"].str[0:2]
    # rasch_df["exam_id"] already defined for students

    plt.rcParams['text.usetex'] = True

    bins = [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]

    fig, ((ax00, ax01), (ax10, ax11), (ax20, ax21), (ax30, ax31)) = plt.subplots(nrows=4, ncols=2, figsize=(10, 6), sharey=True)

    add_rasch_subplot(rasch_df, ax00, bins, ["1A", "1B"], "Exam 1", '1', variable_type)
    add_rasch_subplot(rasch_df, ax10, bins, ["2A", "2B", "2C"], "Exam 2", '1', variable_type)
    add_rasch_subplot(rasch_df, ax20, bins, ["3A", "3B", "3C"], "Exam 3", '1', variable_type)
    add_rasch_subplot(rasch_df, ax30, bins, ["4A", "4B", "4C"], "Exam 4", '1', variable_type)
    
    add_rasch_subplot(rasch_df, ax01, bins, ["1A", "1B"], "Exam 1", '3', variable_type)
    add_rasch_subplot(rasch_df, ax11, bins, ["2A", "2B", "2C"], "Exam 2", '3', variable_type)
    add_rasch_subplot(rasch_df, ax21, bins, ["3A", "3B", "3C"], "Exam 3", '3', variable_type)
    add_rasch_subplot(rasch_df, ax31, bins, ["4A", "4B", "4C"], "Exam 4", '3', variable_type)

    fig.tight_layout()
    try:
        plt.savefig(filename)
    except FileNotFoundError:
        filename = "." + filename
        plt.savefig(filename)
        
    plt.close(fig)

def create_fit_dict(fit_type, df):
    fit_dict = {}
    for exam_num in range(1, 5):
        if exam_num == 1:
            ver_list = ['A', 'B']
        else: 
            ver_list = ['A', 'B', 'C']
        for exam_ver in ver_list:
            temp_exam_num_and_ver = f'{exam_num}{exam_ver}'
            df['question_id'] = df.index
            df['exam_id'] = df['question_id'].str[0:2]
            temp_df = df[df['exam_id'] == temp_exam_num_and_ver]
            fit_dict[temp_exam_num_and_ver] = {
                'Good_1PL': 100*temp_df[f'is_good_{fit_type}_1PL'].sum()/len(temp_df[f'is_good_{fit_type}_1PL']),
                'Acceptable_1PL': 100*temp_df[f'is_acceptable_{fit_type}_1PL'].sum()/len(temp_df[f'is_acceptable_{fit_type}_1PL']),
                'Poor_1PL': 100*temp_df[f'is_poor_{fit_type}_1PL'].sum()/len(temp_df[f'is_poor_{fit_type}_1PL']),
                'Good_3PL': 100*temp_df[f'is_good_{fit_type}_3PL'].sum()/len(temp_df[f'is_good_{fit_type}_3PL']),
                'Acceptable_3PL': 100*temp_df[f'is_acceptable_{fit_type}_3PL'].sum()/len(temp_df[f'is_acceptable_{fit_type}_3PL']),
                'Poor_3PL': 100*temp_df[f'is_poor_{fit_type}_3PL'].sum()/len(temp_df[f'is_poor_{fit_type}_3PL'])
            }
    return fit_dict

def add_fit_subplot(df, exam_keys, fit_type, PL, axis, title):
    fit_dict = create_fit_dict(fit_type, df)

    labels = ["Poor", "Acceptable", "Good"]
    text_color = ["black", "black", "white"]
    bar_bottoms = [0, 0, 0]
    bar_count = 0
    for key in exam_keys:
        exam_bar_data = []
        for temp_label in [f"Poor_{PL}PL", f"Acceptable_{PL}PL", f"Good_{PL}PL"]:
            exam_bar_data.append(fit_dict[key][temp_label])
        axis.bar(labels, exam_bar_data, label=key, bottom = bar_bottoms)
        
        for i in range(len(bar_bottoms)):
            bar_bottoms[i] += exam_bar_data[i]
        for j in range(len(exam_bar_data)):
            y_position = (bar_bottoms[j] - exam_bar_data[j]/2)
            if exam_bar_data[j] >= 25:
                axis.text(labels[j], y_position, f"{exam_bar_data[j]:.2f}", color = text_color[bar_count], ha='center', va='bottom', fontsize = 10)
        bar_count += 1
    
    axis.legend(prop={'size': 10})
    axis.set_xlabel(f"{fit_type} categories")
    axis.set_ylabel("Percent of fit")
    axis.set_title(title)
    custom_palette = ['#cf4456', '#f29566', '#831c64']
    plt.rcParams['axes.prop_cycle'] = plt.cycler('color', custom_palette)

def save_fit_plots(rasch_df, fit_type, variable_type, filename = None):
    if type(filename) == type(None):
        if variable_type == 'items':
            filename = f"./figures/items_{fit_type}_all.png"
        elif variable_type == 'students':
            filename = f"./figures/students_{fit_type}_all.png"
    fig, ((ax00, ax01), (ax10, ax11), (ax20, ax21), (ax30, ax31)) = plt.subplots(nrows=4, ncols=2, figsize=(7, 9), sharey=True)

    add_fit_subplot(df=rasch_df, axis=ax00, exam_keys=["1A", "1B"], title="Exam 1", fit_type=fit_type, PL='1')
    add_fit_subplot(df=rasch_df, axis=ax10, exam_keys=["2A", "2B", "2C"], title="Exam 2", fit_type=fit_type, PL='1')
    add_fit_subplot(df=rasch_df, axis=ax20, exam_keys=["3A", "3B", "3C"], title="Exam 3", fit_type=fit_type, PL='1')
    add_fit_subplot(df=rasch_df, axis=ax30, exam_keys=["4A", "4B", "4C"], title="Exam 4", fit_type=fit_type, PL='1')

    add_fit_subplot(df=rasch_df, axis=ax01, exam_keys=["1A", "1B"], title="Exam 1", fit_type=fit_type, PL='3')
    add_fit_subplot(df=rasch_df, axis=ax11, exam_keys=["2A", "2B", "2C"], title="Exam 2", fit_type=fit_type, PL='3')
    add_fit_subplot(df=rasch_df, axis=ax21, exam_keys=["3A", "3B", "3C"], title="Exam 3", fit_type=fit_type, PL='3')
    add_fit_subplot(df=rasch_df, axis=ax31, exam_keys=["4A", "4B", "4C"], title="Exam 4", fit_type=fit_type, PL='3')

    fig.tight_layout()
    
    try:
        plt.savefig(filename)
    except FileNotFoundError:
        filename = "." + filename
        plt.savefig(filename)
    plt.close(fig)
