from datetime import datetime
import pandas as pd
from src.core.logger import setup_logger
from src.core.connect_reddit import connect_reddit
from src.utils.save_csv import save_csv
from pathlib import Path
from src.utils.cleaners import clean_text
from prawcore.exceptions import TooManyRequests
import time

def scrape_a_comment(subreddit_id, logger, comment):
    try:
        return {
            "post_id": subreddit_id,
            "comment_id": comment.id,
            "author": comment.author.name if comment.author else "deleted_user",
            "subreddit": None,
            "country" : None,
            "body": clean_text(comment.body),
            "score": comment.score,
            "created_utc": datetime.utcfromtimestamp(comment.created_utc).strftime("%Y-%m-%d")
        }
    except Exception as e:
        logger.error(f"❌ Error while scraping comment, subreddit_id={subreddit_id}: {e}")
        return None

def scrape_all_comments(posts_scraped, logger, reddit, comment_link_limit):
    approved_posts = posts_scraped[posts_scraped['approved'] == True]
    all_comments = []

    for row in approved_posts.itertuples():
        post_id = row.post_id
        subreddit = row.subreddit
        country = row.country

        if pd.isna(post_id):
            continue

        logger.info(f"⏳ Scraping {post_id} ===")
        post = reddit.submission(id=post_id)

        try:
            post.comments.replace_more(limit=comment_link_limit)
            for comment in post.comments.list():
                comment_dict = scrape_a_comment(post_id, logger, comment)
                if comment_dict:
                    comment_dict["country"] = country
                    comment_dict["subreddit"] = subreddit
                    all_comments.append(comment_dict)
        except TooManyRequests:
            logger.warning("Rate limit (429) hit. Sleeping for 60 seconds...")
            time.sleep(60)


    comments_df = pd.DataFrame(all_comments)
    return comments_df

def main(posts_scraped, logger, reddit, comment_limit):
    if logger is None:
        logger = setup_logger()
    if reddit is None:
        reddit = connect_reddit(logger)

    if isinstance(posts_scraped, (str, Path)):
        today_str = datetime.today().strftime("%Y-%m-%d")
        csv_path = Path(posts_scraped) / f"{today_str}.csv"
        posts_scraped = pd.read_csv(csv_path)

    logger.info("⏳ SCRAPING COMMENTS ===")
    scraped_comments = scrape_all_comments(posts_scraped, logger, reddit, comment_limit)

    file_location = "data/raw/weekly_scrapings/comments/"

    save_csv(scraped_comments, logger, file_location)
    logger.info("✅ PROCESS COMPLETE ===")

    return scraped_comments