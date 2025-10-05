import praw
import os
from dotenv import load_dotenv

def connect_reddit(logger):
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent="happiness-analyzer/0.1"
    )
    logger.info("✅ Connected to Reddit ===")
    return reddit