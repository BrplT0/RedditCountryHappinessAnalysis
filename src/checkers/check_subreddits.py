from prawcore.exceptions import Redirect, NotFound
import pandas as pd
from datetime import datetime, timedelta
import warnings
from src.core.config_utils import get_config
from src.core.logger import setup_logger
from src.core.connect_reddit import connect_reddit
from src.checkers.filter_subreddits import filter_subreddit
from src.utils.save_csv import save_csv

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

subreddits = pd.read_csv("../../data/raw/templates/subreddits.csv")

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
        sub = reddit.subreddit(subreddit_name)
        subscriber_count = sub.subscribers
        try:
            for _ in sub.new(limit=1):
                pass
            logger.info("✅ Found ===")
            subreddits.at[index, "subscribers"] = subscriber_count
            subreddits.at[index, "active"] = True
        except (Redirect, NotFound):
            logger.info("❌ Not Found ===")
            subreddits.at[index, "active"] = False
        except Exception as e:
            logger.info(f"❌ Other Error: {e} ===")
    return subreddits

def approve_subscribers(subreddits, reddit, logger, category, sub_approve_point):
    filtered_df = filter_subreddit(subreddits, logger, category)
    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        country_name = row['country']
        subreddit_active = row['active']
        subreddit_subscribers = row['subscribers']
        logger.info(f"⏳ Approving subscribers of {country_name}: r/{subreddit_name} ===")
        if pd.isna(subreddit_active):
            logger.info(f"⏭️  {subreddit_name}: is not active ===")
            continue
        try:
            if subreddit_subscribers < sub_approve_point:
                continue
            else:
                subreddits.at[index, "enough_subscribers"] = True
                logger.info(f"✅ Subscribers Approved: r/{subreddit_name} ===")
        except Exception as e:
            logger.info(str(e))
    return subreddits

def count_comments_last_week(sub, logger, comment_approve_point, comment_max_days):
    one_week_ago = datetime.utcnow() - timedelta(comment_max_days)
    comment_count = 0
    try:
        for submission in sub.new(limit=None):
            created = datetime.utcfromtimestamp(submission.created_utc)
            if created < one_week_ago:
                break
            comment_count += submission.num_comments
            if comment_count >= comment_approve_point:
                comment_count = comment_approve_point
                break
    except Exception as e:
        logger.info(f" Error counting comments for r/{sub.display_name}: {e} ===")
        comment_count = 0

    return comment_count

def approve_comments(subreddits, reddit, logger, category, comment_approve_point, comment_max_days):
    filtered_df = filter_subreddit(subreddits, logger, category)

    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        country_name = row['country']
        enough_subscribers = row.get('enough_subscribers', False)

        if pd.isna(subreddit_name):
            logger.info(f" ⏭️  {country_name}: No subreddit ===")
            continue

        if not enough_subscribers:
            logger.info(" ❌ Not enough subscribers ===")
            continue

        logger.info(f"⏳ Approving comments of {country_name}: r/{subreddit_name} ===")

        try:
            sub = reddit.subreddit(subreddit_name)
            comment_count = count_comments_last_week(sub, logger, comment_approve_point=comment_approve_point, comment_max_days=comment_max_days)
        except (Redirect, NotFound):
            logger.info(f" ❌ r/{subreddit_name} not found ===")
            comment_count = 0
        except Exception as e:
            logger.info(f" ❌ Error: {e} ===")
            comment_count = 0

        logger.info(f"🔍 r/{subreddit_name} comments last week: {comment_count} ===")

        subreddits.at[index, "comments_last_week"] = comment_count
        subreddits.at[index, "enough_comments"] = comment_count >= comment_approve_point

    return subreddits

def approve_subreddits(subreddits, reddit, logger, category):
    filtered_df = filter_subreddit(subreddits, logger, category)

    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        enough_subscribers = row.get('enough_subscribers', False)
        enough_comments = row.get('enough_comments', False)

        if pd.isna(enough_subscribers) or pd.isna(enough_comments):
            subreddits.at[index, "approved"] = False
            continue
        logger.info(f"⏳ Approving r/{subreddit_name} ===")
        if enough_subscribers == True and enough_comments == True:
            subreddits.at[index, "approved"] = True
            logger.info(f"✅ r/{subreddit_name} is APPROVED ===")
        else:
            subreddits.at[index, "approved"] = False
            logger.info(f"❌ r/{subreddit_name} is NOT APPROVED ===")

    return subreddits

def finalize(subreddits):
    logger = setup_logger()
    reddit = connect_reddit(logger)
    file_location = "../../data/raw/subreddits/"

    comment_max_days = get_config("check_subreddits", "comment_max_days", type=int)
    comment_approve_point = get_config("check_subreddits", "comment_approve_point", type=int)
    sub_approve_point = get_config("check_subreddits", "sub_approve_point", type=int)
    category = get_config("global", "category")

    logger.info("⏳ CHECKING SUBREDDITS ===")
    subreddits_checked = check_subreddits(subreddits, reddit, logger, category)

    logger.info("⏳ APPROVING SUBSCRIBERS ===")
    subreddits_approved_subs = approve_subscribers(subreddits_checked, reddit, logger, category, sub_approve_point)

    logger.info("⏳ APPROVING COMMENTS ===")
    subreddits_approved_comments = approve_comments(subreddits_approved_subs, reddit, logger, category, comment_approve_point, comment_max_days)

    logger.info("⏳ FINAL APPROVAL ===")
    subreddits_final = approve_subreddits(subreddits_approved_comments, reddit, logger, category)

    save_csv(subreddits_final, logger, file_location)
    logger.info("✅ PROCESS COMPLETE ===")


finalize(subreddits)