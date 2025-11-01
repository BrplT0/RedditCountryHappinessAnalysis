import time
import warnings
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from multiprocessing import Pool
import numpy as np
import os
import torch

# Core modüller
from src.core.connect_reddit import connect_reddit
from src.core.logger import setup_logger
from src.core.config_utils import get_config

# Pipeline adımları
from src.checkers.check_subreddits import main as check_main
from src.scrapers.subreddit_scraper import main as scrape_posts_main
from src.scrapers.comment_scraper import main as scrape_comments_main
from src.utils.cleaners import nlp_preprocess
from src.utils.save_csv import save_csv
from src.analyzers.sentiment_analyzer import (
    load_sentiment_model,
    analyze_sentiment_batch,
    init_worker,
    process_chunk
)

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

if __name__ == "__main__":

    # --- Setup ---
    today_str = datetime.today().strftime("%Y-%m-%d")
    logger = setup_logger()
    reddit = connect_reddit(logger)
    logger.info("Main process started. Logger and Reddit connection initialized.")

    # --- Config ---
    try:
        post_limit = get_config("reddit_post_scraper", "post_limit", type=int)
        post_comment_approve_limit = get_config("reddit_post_scraper", "post_comment_approve_limit", type=int)
        comment_link_limit_config = get_config("reddit_comment_scraper", "comment_link_limit", type=int)
        comment_link_limit = None if comment_link_limit_config == -1 else comment_link_limit_config
        scrape_till = datetime.utcnow() - timedelta(get_config("global", "comment_max_days", type=int))

        analysis_device = get_config("analysis", "device_type", fallback="cpu")
        cpu_cores_config = get_config("analysis", "cpu_cores", type=int, fallback=4)

    except Exception as e:
        logger.error(f"❌ Failed to load configuration: {e}")
        logger.error("Exiting.")
        exit()

    # --- Step 1-5: Veri Çekme veya Dosyadan Yükleme ---
    processed_dir = Path("data/processed/preprocessed_comments/")
    CLEANED_FILE_PATH = processed_dir / f"{today_str}.csv"

    if CLEANED_FILE_PATH.exists():
        logger.info(f"✅ Found cleaned data file: {CLEANED_FILE_PATH.name}")
        logger.info("⏳ Skipping Scraping and Preprocessing steps. Loading file...")
        try:
            processed_df = pd.read_csv(CLEANED_FILE_PATH)
        except pd.errors.EmptyDataError:
            logger.warning(f"⚠️ Cleaned data file {CLEANED_FILE_PATH.name} is empty. Re-running pipeline.")
            CLEANED_FILE_PATH.unlink()
            processed_df = pd.DataFrame()
        except Exception as e:
            logger.error(f"❌ Failed to read {CLEANED_FILE_PATH.name}: {e}. Exiting.")
            exit()

    if not CLEANED_FILE_PATH.exists():
        logger.warning(f"⚠️ Cleaned data file not found at: {CLEANED_FILE_PATH}")
        logger.info("⏳ Running the full pipeline (Steps 1-7)...")

        logger.info("-" * 30 + " STEP 1: CHECK SUBREDDITS " + "-" * 30)
        subreddit_template = pd.read_csv("assets/subreddits.csv")
        subreddits_checked = check_main(
            subreddits=subreddit_template,
            reddit=reddit,
            logger=logger
        )
        logger.info("✅ Step 1 complete.")

        logger.info("-" * 30 + " STEP 2: SCRAPE POSTS " + "-" * 30)
        posts_scraped = scrape_posts_main(
            subreddits=subreddits_checked,
            logger=logger,
            reddit=reddit,
            post_limit=post_limit,
            post_comment_approve_limit=post_comment_approve_limit,
            scrape_till=scrape_till
        )
        logger.info("✅ Step 2 complete.")

        if posts_scraped.empty:
            logger.warning("⚠️ No posts were scraped. Skipping comment scraping and preprocessing.")
            processed_df = pd.DataFrame()
            save_csv(processed_df, logger, str(processed_dir))
        else:
            logger.info("-" * 30 + " STEP 3: SCRAPE COMMENTS " + "-" * 30)
            comments_scraped = scrape_comments_main(
                posts_scraped=posts_scraped,
                logger=logger,
                reddit=reddit,
                comment_limit=comment_link_limit
            )
            logger.info("✅ Step 3 complete.")

            if comments_scraped.empty:
                logger.warning("⚠️ No comments were scraped. Skipping preprocessing.")
                processed_df = pd.DataFrame()
                save_csv(processed_df, logger, str(processed_dir))
            else:
                logger.info("-" * 30 + " STEP 7: PREPROCESSING COMMENTS " + "-" * 30)
                processed_df = nlp_preprocess(comments_scraped)
                save_csv(processed_df, logger, str(processed_dir))
                logger.info(f"✅ Step 7 complete. Cleaned data saved to: {processed_dir}")

        if not processed_df.empty and not CLEANED_FILE_PATH.exists():
            logger.error(f"❌ Failed to find or create the cleaned data file at {CLEANED_FILE_PATH}. Exiting.")
            exit()
        elif not processed_df.empty and CLEANED_FILE_PATH.exists():
            processed_df = pd.read_csv(CLEANED_FILE_PATH)

            # --- Step 5: Sentiment Analysis (CPU veya GPU) ---

    if processed_df is None or processed_df.empty:
        logger.error("❌ No preprocessed data found or generated. Sentiment analysis cannot proceed. Exiting.")
    else:
        logger.info("-" * 50)

        final_scored_df = pd.DataFrame()  # Başlangıçta boş tanımla
        start_time = time.time()  # Zamanı burada başlat

        if analysis_device.lower() == "gpu":
            # --- GPU YOLU (try-except bloğu eklendi) ---
            try:
                logger.info(f"🚀 Step 8.G: Starting GPU Sentiment Analysis (NVIDIA)...")

                logger.info("Loading XLM-RoBERTa model onto GPU memory...")
                model_pipeline = load_sentiment_model()
                logger.info("✅ Model loaded to GPU successfully.")

                comment_list = processed_df['body'].tolist()
                logger.info(f"Analyzing all {len(comment_list)} comments on GPU...")

                sentimental_analysis_results = analyze_sentiment_batch(
                    text_list=comment_list,
                    model=model_pipeline
                )

                logger.info(f"Successfully analyzed {len(sentimental_analysis_results)} comments.")

                results_df = pd.DataFrame(sentimental_analysis_results)
                processed_df = processed_df.reset_index(drop=True)
                final_scored_df = pd.concat([processed_df, results_df], axis=1)

            except torch.OutOfMemoryError:
                logger.error("=" * 50)
                logger.error("❌ FATAL ERROR: CUDA Out of Memory.")
                logger.error(
                    "Your GPU does not have enough VRAM (e.g., 2GB MX350) to run this 1.6GB XLM-RoBERTa model.")
                logger.error("The model might load, but there is no memory left for the analysis batch.")
                logger.error(
                    "SOLUTION: Change 'device_type = gpu' to 'device_type = cpu' in your config.ini to use the CPU multiprocessing path.")
                logger.error("Exiting.")
                exit()
            except RuntimeError as e:
                if "Torch not compiled with CUDA" in str(e):
                    logger.error("=" * 50)
                    logger.error("❌ FATAL ERROR: PyTorch is not compiled with CUDA.")
                    logger.error("Your PyTorch installation does not have NVIDIA GPU support.")
                    logger.error(
                        "SOLUTION: Re-install PyTorch using the official CUDA-enabled command from pytorch.org.")
                    logger.error("Exiting.")
                    exit()
                else:
                    logger.error(f"An unexpected error occurred during GPU analysis: {e}")
                    exit()
            except Exception as e:
                logger.error(f"An unexpected error occurred during GPU analysis: {e}")
                exit()

        else:
            # --- CPU YOLU (Multiprocessing) ---
            num_cores = cpu_cores_config
            logger.info(f"🚀 Step 8.C: Starting Multiprocessing Sentiment Analysis ({num_cores} Cores)...")
            logger.info(f"Total {len(processed_df)} comments will be split across {num_cores} cores.")

            df_chunks = np.array_split(processed_df, num_cores)

            with Pool(processes=num_cores, initializer=init_worker) as pool:
                logger.info(f"Pool initialized with {num_cores} cores. Starting parallel analysis...")
                results_list = pool.map(process_chunk, df_chunks)
                logger.info("Parallel analysis complete. Concatenating results...")

            final_scored_df = pd.concat(results_list, ignore_index=True)
            logger.info(f"Successfully analyzed {len(final_scored_df)} comments in total.")

        # --- ORTAK BİTİŞ BLOĞU ---

        end_time = time.time()
        total_time_seconds = end_time - start_time
        total_time_minutes = total_time_seconds / 60

        logger.info("-" * 50)
        logger.info(f"✅✅✅ SENTIMENT ANALYSIS COMPLETE (Mode: {analysis_device.upper()}) ✅✅✅")
        logger.info(f"Total Time: {total_time_minutes:.2f} minutes.")

        # Sadece başarılıysa kaydet
        if not final_scored_df.empty:
            scores_dir = Path("data/processed/sentiment_scores/")
            scores_dir.mkdir(parents=True, exist_ok=True)
            save_csv(final_scored_df, logger, str(scores_dir))
            logger.info(f"Scored data saved to: {scores_dir}")
        else:
            logger.warning("⚠️ Sentiment analysis resulted in an empty DataFrame. No data was saved.")