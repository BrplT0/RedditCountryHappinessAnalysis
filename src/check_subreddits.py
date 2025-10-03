import praw
import os
from dotenv import load_dotenv
from nbconvert.utils.pandoc import pandoc
from prawcore.exceptions import Redirect, NotFound
import pandas as pd
import datetime


pd.set_option('display.max_rows', None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

subreddits = pd.read_csv("../data/subreddits.csv")
print(subreddits)

def connect_reddit():
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("secret"),
        user_agent="happiness-analyzer/0.1"
    )
    print("✅ Connected to Reddit")
    return reddit

def check_subreddits(subreddits, reddit, category = "all"):
    if category == "all":
        filtered_df = subreddits
    else:
        filtered_df = subreddits[subreddits['category'] == category]
        print(f"Checking {category.capitalize()}")

    for index, row in filtered_df.iterrows():
        subreddit_name = row['subreddit']
        country_name = row['country']
        print(f"\n=== Checking subreddit of {country_name}: r/{subreddit_name} ===\n")
        if pd.isna(subreddit_name):
            print(f"⏭️  {country_name}: No subreddit")
            continue
        subreddits.at[index, "checked"] = True
        sub = reddit.subreddit(subreddit_name)
        subscriber_count = sub.subscribers
        try:
            for _ in sub.new(limit=1):
                pass
            print("✅ Found")
            subreddits.at[index, "subscribers"] = subscriber_count
            subreddits.at[index, "active"] = True
        except (Redirect, NotFound):
            print("❌ Not Found")
            subreddits.at[index, "active"] = False
        except Exception as e:
            print(f"❌ Other Error: {e}")
    return subreddits

def approve_subreddit(subreddits_dict, reddit):
    for sub in subreddits_dict:
        try:
            for post in reddit.subreddit(sub).hot(limit=1):
                print(f"Subreddit: r/{sub}")
                print(f"Title: {post.title}")
                print(f"Score: {post.score}")
                print(f"Comments: {post.num_comments}")
                print("-" * 50)
        except (Redirect, NotFound):
            print(f"❌ r/{sub}: Not Found")
        except Exception as e:
            print(f"❌ r/{sub}: Other Error: {e}")

reddit = connect_reddit()
check_subreddits(subreddits, reddit)
print(subreddits)