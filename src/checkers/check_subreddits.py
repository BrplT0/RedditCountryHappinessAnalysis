from prawcore.exceptions import Redirect, NotFound
import pandas as pd
from src.core.config_utils import get_config
from src.core.logger import setup_logger
from src.core.connect_reddit import connect_reddit
from src.checkers.filter_subreddits import filter_subreddit
from src.utils.save_csv import save_csv
from src.utils.subreddit_stats import count_comments

def check_subreddits(subreddits, reddit, logger, category):
    filtered_df = filter_subreddit(subreddits, logger, category)

    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        country_name = row['country']
        logger.info(f"⏳ Checking subreddit of {country_name}: r/{subreddit_name} ===")
        if pd.isna(subreddit_name):
            logger.info(f"⏭️  {country_name}: No subreddit ===")
            continue

        subreddits.at[index, "checked"] = True
        try:
            sub = reddit.subreddit(subreddit_name)
            subscriber_count = sub.subscribers
            sub.new(limit=1).__next__()
            logger.info("✅ Found ===")
            subreddits.at[index, "subscribers"] = subscriber_count
            subreddits.at[index, "active"] = True
        except (Redirect, NotFound):
            logger.info("❌ Not Found ===")
            subreddits.at[index, "active"] = False
        except StopIteration:
             logger.info("❌ Found but no posts (inactive check) ===")
             subreddits.at[index, "subscribers"] = subscriber_count
             subreddits.at[index, "active"] = False
        except Exception as e:
            logger.info(f"❌ Other Error: {e} ===")
            subreddits.at[index, "active"] = False

    return subreddits

def approve_subscribers(subreddits, logger, category, sub_approve_point):
    filtered_df = filter_subreddit(subreddits, logger, category)
    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        country_name = row['country']

        if pd.isna(subreddit_name):
            logger.info(f"⏭️ {country_name}: No subreddit, skipping approval ===")
            continue

        subreddit_active = row.get('active', False)
        subreddit_subscribers = row.get('subscribers', 0)

        logger.info(f"⏳ Approving subscribers of {country_name}: r/{subreddit_name} ===")
        if not subreddit_active:
            logger.info(f"⏭️  r/{subreddit_name}: is not active ===")
            continue

        if subreddit_subscribers < sub_approve_point:
            subreddits.at[index, "enough_subscribers"] = False
            logger.info(f"❌ Subscribers Not Approved: r/{subreddit_name} ({subreddit_subscribers} < {sub_approve_point}) ===")
        else:
            subreddits.at[index, "enough_subscribers"] = True
            logger.info(f"✅ Subscribers Approved: r/{subreddit_name} ({subreddit_subscribers} >= {sub_approve_point}) ===")

    return subreddits

def approve_comments(subreddits, reddit, logger, category, comment_approve_point, comment_max_days):
    filtered_df = filter_subreddit(subreddits, logger, category)

    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        country_name = row['country']
        subreddit_active = row.get('active', False)
        enough_subscribers = row.get('enough_subscribers', False)

        if pd.isna(subreddit_name) or not subreddit_active or not enough_subscribers:
            logger.info(f"⏭️  r/{subreddit_name} ({country_name}): Skipping comment check (inactive or not enough subs) ===")
            continue

        logger.info(f"⏳ Approving comments of {country_name}: r/{subreddit_name} ===")
        try:
            sub = reddit.subreddit(subreddit_name)
            comment_count = count_comments(sub, logger, comment_approve_point, comment_max_days)
        except (Redirect, NotFound):
            logger.info(f"❌ r/{subreddit_name} not found during comment check ===")
            comment_count = 0
        except Exception as e:
            logger.info(f"❌ Error during comment count for r/{subreddit_name}: {e} ===")
            comment_count = 0

        logger.info(f"🔍 r/{subreddit_name} comments last week (approx): {comment_count} ===")
        subreddits.at[index, "comments_last_week"] = comment_count
        subreddits.at[index, "enough_comments"] = comment_count >= comment_approve_point

    return subreddits

def approve_subreddits(subreddits, logger, category):
    filtered_df = filter_subreddit(subreddits, logger, category)

    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']

        if pd.isna(subreddit_name):
            subreddits.at[index, "approved"] = False
            continue

        subreddit_active = row.get('active', False)
        enough_subscribers = row.get('enough_subscribers', False)
        enough_comments = row.get('enough_comments', False)

        approved = subreddit_active and enough_subscribers and enough_comments

        subreddits.at[index, "approved"] = approved
        if approved:
            logger.info(f"✅✅✅ r/{subreddit_name} is APPROVED ===")
        else:
            logger.info(f"❌❌❌ r/{subreddit_name} is NOT APPROVED (Active: {subreddit_active}, Subs OK: {enough_subscribers}, Comments OK: {enough_comments}) ===")

    return subreddits

def main(subreddits, reddit=None, logger=None):
    if logger is None:
        logger = setup_logger()
    if reddit is None:
        reddit = connect_reddit(logger)

    file_location = "data/raw/subreddits/"

    comment_max_days = get_config("global", "comment_max_days", type=int)
    comment_approve_point = get_config("check_subreddits", "comment_approve_point", type=int)
    sub_approve_point = get_config("check_subreddits", "sub_approve_point", type=int)
    category = get_config("global", "category")

    subreddits_checked = check_subreddits(subreddits, reddit, logger, category)
    subreddits_approved_subs = approve_subscribers(subreddits_checked, logger, category, sub_approve_point)
    subreddits_approved_comments = approve_comments(subreddits_approved_subs, reddit, logger, category, comment_approve_point, comment_max_days)
    subreddits_final = approve_subreddits(subreddits_approved_comments, logger, category)

    save_csv(subreddits_final, logger, file_location)

    return subreddits_final