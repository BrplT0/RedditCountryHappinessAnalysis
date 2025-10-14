from datetime import datetime
import pandas as pd
from src.core.logger import setup_logger
from src.core.connect_reddit import connect_reddit
from src.core.config_utils import get_config
from src.checkers.check_subreddits import main as check_subreddits_main
from src.checkers.filter_subreddits import filter_subreddit
from src.utils.save_csv import save_csv
from pathlib import Path
from src.utils.clean_text import clean_text


def scrape_a_post(subreddit_name, logger, post, post_comment_approve_limit):
    try:
        return {
            "post_id": post.id,
            "subreddit": subreddit_name,
            "country": None,
            "title": clean_text(post.title),
            "selftext": clean_text(post.selftext),
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": datetime.utcfromtimestamp(post.created_utc).strftime("%Y-%m-%d"),
            "post_url": f"https://www.reddit.com/r/{subreddit_name}/comments/{post.id}",
            "approved": post.num_comments > post_comment_approve_limit,
        }
    except Exception as e:
        logger.error(f"❌ Error while scraping post in r/{subreddit_name}: {e}")
        return None


def scrape_all_posts(subreddits, logger, reddit, post_limit, post_comment_approve_limit):
    approved_subs = subreddits[subreddits['approved'] == True]
    posts = []

    for _, row in approved_subs.iterrows():
        subreddit_name = row["subreddit"]
        country = row["country"]

        if pd.isna(subreddit_name):
            continue

        logger.info(f"⏳ Scraping r/{subreddit_name} ({country}) ===")
        sub = reddit.subreddit(subreddit_name)

        for post in sub.new(limit=post_limit):
            post_dict = scrape_a_post(subreddit_name, logger, post, post_comment_approve_limit)
            if post_dict:
                post_dict["country"] = country
                posts.append(post_dict)

    posts_df = pd.DataFrame(posts)
    return posts_df


def main(subreddits, logger, reddit, post_limit, post_comment_approve_limit):
    if logger is None:
        logger = setup_logger()
    if reddit is None:
        reddit = connect_reddit(logger)

    if isinstance(subreddits, (str, Path)):
        today_str = datetime.today().strftime("%Y-%m-%d")
        csv_path = Path(subreddits) / f"{today_str}.csv"
        subreddits = pd.read_csv(csv_path)

    file_location = "data/raw/weekly_scrapings/posts/"

    logger.info("⏳ SCRAPING POSTS ===")
    scraped_posts = scrape_all_posts(subreddits, logger, reddit, post_limit, post_comment_approve_limit)

    save_csv(scraped_posts, logger, file_location)
    logger.info("✅ PROCESS COMPLETE ===")

    return scraped_posts


if __name__ == "__main__":
    main()