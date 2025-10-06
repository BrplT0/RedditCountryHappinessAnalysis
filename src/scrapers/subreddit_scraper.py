from datetime import datetime
import pandas as pd
from src.core.logger import setup_logger
from src.core.connect_reddit import connect_reddit
from src.core.config_utils import get_config
from src.checkers.check_subreddits import main as check_subreddits_main
from src.checkers.filter_subreddits import filter_subreddit
from src.utils.save_csv import save_csv

def scrape_a_post(subreddit_name, logger, post):
    try:
        return {
            "post_id": post.id,
            "subreddit": subreddit_name,
            "title": post.title,
            "selftext": post.selftext,
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": datetime.utcfromtimestamp(post.created).strftime("%Y-%m-%d"),
            "post_url": f"https://www.reddit.com/r/{subreddit_name}/comments/{post.id}"
        }
    except Exception as e:
        logger.error(f"❌ Error while scraping post in r/{subreddit_name}: {e}")
        return None

def scrape_all_posts(subreddits, logger, reddit, post_limit, category):
    filtered_subreddits = filter_subreddit(subreddits, logger, category)
    posts = []

    for _, row in filtered_subreddits.iterrows():
        subreddit_name = row["subreddit"]
        logger.info(f"⏳ Scraping r/{subreddit_name} ===")
        sub = reddit.subreddit(subreddit_name)

        for post in sub.new(limit=post_limit):
            post_dict = scrape_a_post(subreddit_name, logger, post)
            if post_dict:
                posts.append(post_dict)

    posts_df = pd.DataFrame(posts)
    return posts_df

def main(subreddits, logger, reddit, category, post_limit):
    if logger is None:
        logger = setup_logger()
    if reddit is None:
        reddit = connect_reddit(logger)

    file_location = "data/raw/weekly_scrapings/posts/"

    logger.info("⏳ SCRAPING POSTS ===")
    scraped_posts = scrape_all_posts(subreddits, logger, reddit, post_limit, category)

    save_csv(scraped_posts, logger, file_location)
    logger.info("✅ PROCESS COMPLETE ===")

if __name__ == "__main__":
    main()

