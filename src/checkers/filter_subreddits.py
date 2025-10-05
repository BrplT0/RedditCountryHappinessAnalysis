def filter_subreddit(subreddits, logger, category):
    if category == "all":
        filtered_df = subreddits
    else:
        filtered_df = subreddits[subreddits['category'] == category]
    return filtered_df