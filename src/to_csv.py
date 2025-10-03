import json
import pandas as pd  # ← "as pd" ekle
from pathlib import Path

with open("data/subreddits_2.json", "r") as f:
    json_data = json.load(f)

rows = []

for category, countries in json_data.items():
    for item in countries:
        rows.append({
            'subreddit': item['subreddit'],
            'country': item['country'],
            'category': category,
            'checked': False,
            'active': None,
            'subscribers': None
        })

df = pd.DataFrame(rows)
df.to_csv('data/subreddits.csv', index=False)
print(f"Total: {len(df)}")
print(df.head())

