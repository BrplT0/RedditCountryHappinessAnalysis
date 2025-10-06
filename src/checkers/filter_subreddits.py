import pandas as pd
from pathlib import Path

def filter_subreddit(subreddits, logger, category):
    if isinstance(subreddits, (str, Path)):
        subreddits = pd.read_csv(subreddits)

    if category == "all":
        filtered_df = subreddits
    else:
        filtered_df = subreddits[subreddits["category"] == category]

    return filtered_df
