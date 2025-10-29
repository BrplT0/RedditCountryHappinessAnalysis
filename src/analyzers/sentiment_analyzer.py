import pandas as pd
from transformers import pipeline
from src.core.logger import setup_logger
from multiprocessing import Pool
import numpy as np

model_pipeline_worker = None

def load_sentiment_model():
    model_pipeline = pipeline("sentiment-analysis",
                              model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
                              device="cpu",
                              framework="pt",
                              truncation=True,
                              max_length=512)
    return model_pipeline

def analyze_sentiment_batch(text_list, model):
    result = model(text_list)
    return result

def init_worker():
    global model_pipeline_worker
    print("Initializing sentiment model for new worker process...")
    model_pipeline_worker = load_sentiment_model()
    print("Worker model loaded.")


def process_chunk(df_chunk):
    global model_pipeline_worker

    if model_pipeline_worker is None:
        init_worker()

    text_list = df_chunk['body'].tolist()

    results = model_pipeline_worker(text_list, batch_size=64)

    results_df = pd.DataFrame(results)

    df_chunk = df_chunk.reset_index(drop=True)
    df_chunk['sentiment_label'] = results_df['label']
    df_chunk['sentiment_score'] = results_df['score']

    return df_chunk