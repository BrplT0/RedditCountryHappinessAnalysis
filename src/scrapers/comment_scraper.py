from datetime import datetime
from src.core.connect_reddit import connect_reddit
from src.core.logger import setup_logger
import pandas as pd
from src.core.config_utils import get_config
from src.checkers.filter_subreddits import filter_subreddit

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.display.float_format = '{:,.2f}'.format

today_str = datetime.today().strftime("%Y-%m-%d")

checked_subreddits = pd.read_csv(f"../../data/raw/subreddits/{today_str}.csv")

print(checked_subreddits.head())

def reddit_post_scraper(subreddits, reddit, logger, category):
    filtered_df = filter_subreddit(subreddits, logger, category)

    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        sub = reddit.subreddit(subreddit_name)

        for post in sub.new(limit=5):
            logger.info(f"Başlık: {post.title}")
            logger.info(f"Score: {post.score}")
            logger.info(f"Yorumlar: {post.num_comments}")
            logger.info("-" * 50)



def finalize(subreddits):

    category = get_config("global", "category")
    logger = setup_logger()
    reddit = connect_reddit(logger)
    reddit_post_scraper(subreddits, reddit, logger, category)


finalize(checked_subreddits)

