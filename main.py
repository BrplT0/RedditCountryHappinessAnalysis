import time
import warnings
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from multiprocessing import Pool
import numpy as np
from src.core.connect_reddit import connect_reddit
from src.core.logger import setup_logger
from src.core.config_utils import get_config
from src.checkers.check_subreddits import main as check_main
from src.scrapers.subreddit_scraper import main as scrape_posts_main
from src.scrapers.comment_scraper import main as scrape_comments_main
from src.utils.cleaners import nlp_preprocess
from src.utils.save_csv import save_csv
from src.analyzers.sentiment_analyzer import load_sentiment_model, analyze_sentiment_batch
from src.analyzers.sentiment_analyzer import init_worker, process_chunk


warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

# Setup
today_str = datetime.today().strftime("%Y-%m-%d")
logger = setup_logger()
reddit = connect_reddit(logger)

# Config
post_limit = get_config("reddit_post_scraper", "post_limit", type=int)
post_comment_approve_limit = get_config("reddit_post_scraper", "post_comment_approve_limit", type=int)
comment_link_limit = None if get_config("reddit_comment_scraper", "comment_link_limit", type=int) == -1 else get_config("reddit_comment_scraper", "comment_link_limit", type=int)
scrape_till = datetime.utcnow() - timedelta(get_config("global", "comment_max_days", type=int))

processed_dir = Path("data/processed/preprocessed_comments/")
CLEANED_FILE_PATH = processed_dir / f"{today_str}.csv"

if __name__ == "__main__":

    processed_dir = Path("data/processed/preprocessed_comments/")
    CLEANED_FILE_PATH = processed_dir / f"{today_str}.csv"

    if CLEANED_FILE_PATH.exists():
        logger.info(f"✅ Found cleaned data file: {CLEANED_FILE_PATH.name}")
        logger.info("⏳ Skipping Scraping and Preprocessing steps. Loading file...")
        processed_df = pd.read_csv(CLEANED_FILE_PATH)
    else:
        logger.warning(f"⚠️ Cleaned data file not found at: {CLEANED_FILE_PATH}")
        logger.info("⏳ Running the full pipeline...")
        # Step 1: Check subreddits
        subreddit_template = pd.read_csv("assets/subreddits.csv")
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
        # Step 4: Preprocessing
        processed_df = nlp_preprocess(comments_scraped)
        save_csv(processed_df, logger, str(processed_dir))
        logger.info(f"✅ Pipeline finished, cleaned data saved to: {processed_dir}")

        if not CLEANED_FILE_PATH.exists():
            logger.error(
                "❌ Pipeline failed to create the cleaned data file. Cannot proceed with sentiment analysis. Exiting.")
            exit()
        else:
            processed_df = pd.read_csv(CLEANED_FILE_PATH)


    if processed_df is None or processed_df.empty:
        logger.error("❌ No preprocessed data found or generated. Sentiment analysis cannot proceed. Exiting.")
    else:
        logger.info("-" * 50)
        num_cores = 4
        logger.info(f"🚀 Step 8.C: Starting Multiprocessing Sentiment Analysis ({num_cores} Cores)...")
        logger.info(f"Total {len(processed_df)} comments will be split across {num_cores} cores.")

        df_chunks = np.array_split(processed_df, num_cores)

        start_time = time.time()

        with Pool(processes=num_cores, initializer=init_worker) as pool:

            logger.info(f"Pool initialized with {num_cores} cores. Starting parallel analysis...")

            results_list = pool.map(process_chunk, df_chunks)

            logger.info("Parallel analysis complete. Concatenating results...")

        final_scored_df = pd.concat(results_list, ignore_index=True)

        end_time = time.time()
        total_time_seconds = end_time - start_time
        total_time_minutes = total_time_seconds / 60

        logger.info("-" * 50)
        logger.info(f"✅✅✅ SENTIMENT ANALYSIS COMPLETE ✅✅✅")
        logger.info(f"Successfully analyzed {len(final_scored_df)} comments in total.")
        logger.info(f"Total Time: {total_time_minutes:.2f} minutes.")

        scores_dir = Path("data/processed/sentiment_scores/")
        scores_dir.mkdir(parents=True, exist_ok=True)

        save_csv(final_scored_df, logger, str(scores_dir))
        logger.info(f"Scored data saved to: {scores_dir}")