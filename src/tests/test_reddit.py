import praw
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Reddit bağlantısı
reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("secret"),
    user_agent="happiness-analyzer/0.1"
)

# Test: r/Turkey'den 5 post çek
print("Reddit'e bağlanıyor...\n")

subreddit = reddit.subreddit("Turkey")

for post in subreddit.hot(limit=5):
    print(f"Başlık: {post.title}")
    print(f"Score: {post.score}")
    print(f"Yorumlar: {post.num_comments}")
    print("-" * 50)

print("\nTest başarılı!")
