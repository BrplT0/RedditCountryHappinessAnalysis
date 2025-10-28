from datetime import datetime
import warnings
import pandas as pd
from datetime import datetime, timedelta
from src.core.connect_reddit import connect_reddit
from src.core.logger import setup_logger
from src.core.config_utils import get_config
from src.checkers.check_subreddits import main as check_main
from src.scrapers.subreddit_scraper import main as scrape_posts_main
from src.scrapers.comment_scraper import main as scrape_comments_main

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

# Setup
today_str = datetime.today().strftime("%Y-%m-%d")
logger = setup_logger()
reddit = connect_reddit(logger)

# Config
post_limit = get_config("reddit_post_scraper", "post_limit", type=int)
post_comment_approve_limit = get_config("reddit_post_scraper", "post_comment_approve_limit", type=int)
comment_link_limit = get_config("reddit_comment_scraper", "comment_link_limit", type=int)
scrape_till = datetime.utcnow() - timedelta(get_config("global", "comment_max_days", type=int))

# Step 1: Check subreddits
subreddit_template = pd.read_csv("data/raw/templates/subreddits.csv")
subreddits_checked = check_main(
    subreddits=subreddit_template,
    reddit=reddit,
    logger=logger
)

# Step 2: Scrape posts
posts_scraped = scrape_posts_main(
    subreddits=subreddits_checked,
    logger=logger,
    reddit=reddit,
    post_limit=post_limit,
    post_comment_approve_limit=post_comment_approve_limit,
    scrape_till=scrape_till
)

# Step 3: Scrape comments
comments_scraped = scrape_comments_main(
    posts_scraped=posts_scraped,
    logger=logger,
    reddit=reddit,
    comment_limit=comment_link_limit
)
