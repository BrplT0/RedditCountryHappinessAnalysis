from datetime import datetime
from src.core.connect_reddit import connect_reddit
from src.core.logger import setup_logger
import pandas as pd
from src.core.config_utils import get_config
from src.checkers.check_subreddits import main as check_main
from src.scrapers.subreddit_scraper import main as scrape_posts_main
from src.utils.save_csv import parent_root
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

today_str = datetime.today().strftime("%Y-%m-%d")
subreddit_df = pd.read_csv("data/raw/templates/subreddits.csv")

logger = setup_logger()
reddit = connect_reddit(logger)

comment_max_days = get_config("global", "comment_max_days", type=int)
comment_approve_point = get_config("check_subreddits", "comment_approve_point", type=int)
sub_approve_point = get_config("check_subreddits", "sub_approve_point", type=int)
category = get_config("global", "category")
post_limit = get_config("reddit_comment_scraper", "post_limit", type=int)

subreddits_checked = check_main(
    subreddits=subreddit_df,
    reddit=reddit,
    logger=logger
)

checked_subreddit_df = "data/raw/subreddits/"
checked_subreddit_df = parent_root(checked_subreddit_df)

scrape_posts_main(
    subreddits=checked_subreddit_df,
    logger=logger,
    reddit=reddit,
    post_limit=post_limit,
    category=category
)

