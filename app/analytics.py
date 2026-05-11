import pandas as pd
import numpy as np

def get_analytics(tasks):
    # Handle empty state early
    if not tasks:
        return {
            "total": 0,
            "completed": 0,
            "pending": 0,
            "in_progress": 0,
            "completion_percentage": 0,
            "priority_breakdown": {"low": 0, "medium": 0, "high": 0}
        }

    df = pd.DataFrame(tasks)

    # Use len() for total and numpy for status counts
    total = len(df)
    completed = np.sum(df["status"] == "completed")
    pending = np.sum(df["status"] == "pending")
    in_progress = np.sum(df["status"] == "in_progress")

    # Use numpy to calculate the percentage to satisfy assignment requirements
    completion_pct = 0
    if total > 0:
        raw_pct = (completed / total) * 100
        completion_pct = np.round(raw_pct, 2)

    # Get counts for priorities
    p_counts = df["priority"].value_counts().to_dict()
    
    return {
        "total": int(total),
        "completed": int(completed),
        "pending": int(pending),
        "in_progress": int(in_progress),
        "completion_percentage": float(completion_pct),
        "priority_breakdown": {
            "low": p_counts.get("low", 0),
            "medium": p_counts.get("medium", 0),
            "high": p_counts.get("high", 0)
        }
    }