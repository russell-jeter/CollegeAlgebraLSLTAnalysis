import pandas as pd
import numpy as np
try:
    from analyses import item_difficulty
except ImportError:
    import item_difficulty

def get_item_difficulty_counts(item_difficulty_frame=None):
    """
    Counts the number of items in "Ideal", "Acceptable", and "Poor" categories
    per exam, based on item difficulty deviation from 0.74.
    """
    if item_difficulty_frame is None:
        item_difficulty_frame = item_difficulty.get_item_difficulty_frame()

    # Ensure exam_id is present
    if "exam_id" not in item_difficulty_frame.columns:
        # Assuming exam_id can be derived if missing, but it should be there from get_item_difficulty_frame
        # If not, let's try to extract it from question_id
        if "question_id" in item_difficulty_frame.columns:
             item_difficulty_frame["exam_id"] = item_difficulty_frame["question_id"].str[:2]
        else:
            raise ValueError("item_difficulty_frame must contain 'exam_id' or 'question_id'")

    results = []

    # Process each exam
    for exam_id, group in item_difficulty_frame.groupby("exam_id"):
        difficulties = group["item_difficulty"]
        std_dev = difficulties.std()
        
        # Define counts
        ideal_count = 0
        acceptable_count = 0
        poor_count = 0
        
        target = 0.74
        
        for diff in difficulties:
            deviation = abs(diff - target)
            
            if deviation <= std_dev:
                ideal_count += 1
            elif deviation <= 2 * std_dev:
                acceptable_count += 1
            else:
                poor_count += 1
        
        results.append({
            "exam_id": exam_id,
            "Ideal": ideal_count,
            "Acceptable": acceptable_count,
            "Poor": poor_count,
            "Total": len(difficulties),
            "StdDev": std_dev
        })

    # Create summary DataFrame
    summary_df = pd.DataFrame(results)
    
    return summary_df

if __name__ == "__main__":
    df = get_item_difficulty_counts()
    print(df)
    
    output_filename = "item_difficulty_counts.xlsx"
    df.to_excel(output_filename, index=False)
    print(f"\nSaved item difficulty counts to {output_filename}")
