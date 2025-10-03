import praw
import os
from dotenv import load_dotenv
from prawcore.exceptions import Redirect, NotFound
import pandas as pd
from datetime import datetime, timedelta
import warnings
import sys
import logging

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

subreddits = pd.read_csv("../data/raw/subreddits.csv")

def connect_reddit(logger):
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("secret"),
        user_agent="happiness-analyzer/0.1"
    )
    logger.info("✅ Connected to Reddit")
    return reddit

def filter_subreddit(subreddits, logger, category = "all"):
    if category == "all":
        filtered_df = subreddits
    else:
        filtered_df = subreddits[subreddits['category'] == category]
        logger.info(f"Approving {category.capitalize()}")
    return filtered_df

def check_subreddits(subreddits, reddit, logger, category = "all"):
    filtered_df = filter_subreddit(subreddits, logger, category)

    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        country_name = row['country']
        logger.info(f"\n=== Checking subreddit of {country_name}: r/{subreddit_name} ===\n")
        if pd.isna(subreddit_name):
            logger.info(f"⏭️  {country_name}: No subreddit")
            continue
        subreddits.at[index, "checked"] = True
        sub = reddit.subreddit(subreddit_name)
        subscriber_count = sub.subscribers
        try:
            for _ in sub.new(limit=1):
                pass
            logger.info("✅ Found")
            subreddits.at[index, "subscribers"] = subscriber_count
            subreddits.at[index, "active"] = True
        except (Redirect, NotFound):
            logger.info("❌ Not Found")
            subreddits.at[index, "active"] = False
        except Exception as e:
            logger.info(f"❌ Other Error: {e}")
    return subreddits

def approve_subscribers(subreddits, reddit, logger, category = "all"):
    filtered_df = filter_subreddit(subreddits, logger, category)
    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        country_name = row['country']
        subreddit_active = row['active']
        subreddit_subscribers = row['subscribers']
        logger.info(f"\n=== Approving subscribers of {country_name}: r/{subreddit_name} ===\n")
        if pd.isna(subreddit_active):
            logger.info(f"⏭️  {subreddit_name}: is not active")
            continue
        try:
            if subreddit_subscribers < 20000:
                continue
            else:
                subreddits.at[index, "enough_subscribers"] = True
                logger.info(f"Subscribers Approved: r/{subreddit_name}")
        except Exception as e:
            logger.info(str(e))
    return subreddits

def count_comments_last_week(sub, logger, max_count=50):
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    comment_count = 0
    try:
        for submission in sub.new(limit=None):
            created = datetime.utcfromtimestamp(submission.created_utc)
            if created < one_week_ago:
                break
            comment_count += submission.num_comments
            if comment_count >= max_count:
                comment_count = max_count
                break
    except Exception as e:
        logger.info(f"Error counting comments for r/{sub.display_name}: {e}")
        comment_count = 0

    return comment_count

def approve_comments(subreddits, reddit, logger, category="all", approve_point=50):
    filtered_df = filter_subreddit(subreddits, logger, category)

    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        country_name = row['country']
        subscribers = row['subscribers']
        enough_subscribers = row.get('enough_subscribers', False)

        if pd.isna(subreddit_name):
            logger.info(f"⏭️  {country_name}: No subreddit")
            continue

        if not enough_subscribers:
            continue

        logger.info(f"\n=== Approving comments of {country_name}: r/{subreddit_name} ===")

        try:
            sub = reddit.subreddit(subreddit_name)
            comment_count = count_comments_last_week(sub, logger, max_count=approve_point)
        except (Redirect, NotFound):
            logger.info(f"❌ r/{subreddit_name} not found")
            comment_count = 0
        except Exception as e:
            logger.info(f"❌ Error: {e}")
            comment_count = 0

        logger.info(f"r/{subreddit_name} comments last week: {comment_count}")

        subreddits.at[index, "comments_last_week"] = comment_count
        subreddits.at[index, "enough_comments"] = comment_count >= approve_point

    return subreddits

def approve_subreddits(subreddits, reddit, logger, category="all"):
    filtered_df = filter_subreddit(subreddits, logger, category)

    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        country_name = row['country']
        subscribers = row['subscribers']
        enough_subscribers = row.get('enough_subscribers', False)
        enough_comments = row.get('enough_comments', False)

        if pd.isna(enough_subscribers) or pd.isna(enough_comments):
            continue
        logger.info(f"\n=== Approving r/{subreddit_name} ===")
        if enough_subscribers == True and enough_comments == True:
            subreddits.at[index, "approved"] = True
        else:
            subreddits.at[index, "approved"] = False

    return subreddits

def save_subreddits_csv(subreddits, logger):
    today = datetime.today()
    today_str = today.strftime("%Y-%m-%d")
    subreddits.to_csv(f"../data/raw/weekly_subreddits/subreddits_dataframe_{today_str}.csv", index=False)
    logger.info(f"CSV saved: subreddits_dataframe_{today_str}.csv")

def setup_logger():
    today_str = datetime.today().strftime("%Y-%m-%d")
    log_filename = f"../data/log/log_{today_str}.txt"

    logger = logging.getLogger("reddit_logger")
    logger.setLevel(logging.INFO)
    logger.handlers = []

    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

def finalize(subreddits, category="all"):
    logger = setup_logger()
    reddit = connect_reddit(logger)

    logger.info("\n=== Checking Subreddits ===")
    subreddits_checked = check_subreddits(subreddits, reddit, logger, category)

    logger.info("\n=== Approving Subscribers ===")
    subreddits_approved_subs = approve_subscribers(subreddits_checked, reddit, logger, category)

    logger.info("\n=== Approving Comments ===")
    subreddits_approved_comments = approve_comments(subreddits_approved_subs, reddit, logger, category)

    logger.info("\n=== Final Approval ===")
    subreddits_final = approve_subreddits(subreddits_approved_comments, reddit, logger, category)

    save_subreddits_csv(subreddits_final, logger)
    logger.info("\n=== Process Complete ===")

finalize(subreddits)