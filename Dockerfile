FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data/dashboard/live
RUN mkdir -p /app/data/dashboard/time_series
RUN mkdir -p /app/data/processed/preprocessed_comments
RUN mkdir -p /app/data/processed/sentiment_scores
RUN mkdir -p /app/data/raw/subreddits
RUN mkdir -p /app/data/raw/weekly_scrapings/comments
RUN mkdir -p /app/data/raw/weekly_scrapings/posts
RUN mkdir -p /app/data/logs

CMD [ "python", "main.py" ]