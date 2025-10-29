from datetime import datetime
import pandas as pd
from src.core.logger import setup_logger
from src.core.connect_reddit import connect_reddit
from src.utils.save_csv import save_csv
from pathlib import Path
from src.utils.cleaners import clean_text
from prawcore.exceptions import TooManyRequests
import time


def scrape_a_comment(post_id, subreddit, country, logger, comment):
    try:
        author_name = comment.author.name if comment.author else "deleted_user"
        return {
            "post_id": post_id,
            "comment_id": comment.id,
            "author": author_name,
            "subreddit": subreddit,
            "country": country,
            "body": clean_text(comment.body),
            "score": comment.score,
            "created_utc": datetime.utcfromtimestamp(comment.created_utc).strftime("%Y-%m-%d")
        }
    except Exception as e:
        logger.error(f"❌ Error processing comment {comment.id} under post {post_id}: {e}")
        return None


def scrape_all_comments(posts_scraped, logger, reddit, comment_link_limit):
    approved_posts = posts_scraped[posts_scraped['approved'] == True]
    all_comments = []

    total_posts_to_scrape = len(approved_posts)
    logger.info(f"Found {total_posts_to_scrape} approved posts to scrape comments from.")

    for i, row in enumerate(approved_posts.itertuples()):
        post_id = row.post_id
        subreddit = row.subreddit
        country = row.country

        if pd.isna(post_id):
            logger.warning(f"⚠️ Skipping row {i + 1} due to missing post_id.")
            continue

        logger.info(f"⏳ Scraping comments for post {post_id} (r/{subreddit}) [{i + 1}/{total_posts_to_scrape}] ===")

        try:
            post = reddit.submission(id=post_id)

            limit_value_for_praw = None if comment_link_limit == -1 else comment_link_limit

            post.comments.replace_more(limit=limit_value_for_praw)

            comment_count_for_post = 0
            for comment in post.comments.list():
                comment_dict = scrape_a_comment(post_id, subreddit, country, logger, comment)
                if comment_dict:
                    all_comments.append(comment_dict)
                    comment_count_for_post += 1
            logger.info(f"✅ Found {comment_count_for_post} comments for post {post_id}.")

        except TooManyRequests:
            logger.warning(f"⚠️ Rate limit (429) hit while processing post {post_id}. Sleeping for 60 seconds...")
            time.sleep(60)
            logger.warning(f"⏭️ Skipping to next post after rate limit sleep.")
            continue
        except Exception as e:
            logger.error(f"❌ Failed to process comments for post {post_id}: {e}")
            continue

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
        try:
            posts_scraped = pd.read_csv(csv_path)
        except FileNotFoundError:
            logger.error(f"❌ Posts file not found at: {csv_path}. Cannot scrape comments.")
            return pd.DataFrame()

    if posts_scraped.empty:
        logger.warning("⚠️ Input DataFrame 'posts_scraped' is empty. No comments to scrape.")
        return pd.DataFrame()

    scraped_comments = scrape_all_comments(posts_scraped, logger, reddit, comment_limit)

    file_location = "data/raw/weekly_scrapings/comments/"

    save_csv(scraped_comments, logger, file_location)

    return scraped_comments