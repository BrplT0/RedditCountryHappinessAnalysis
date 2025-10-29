import pandas as pd
from transformers import pipeline

model_pipeline_worker = None

def load_sentiment_model():
    model_pipeline = pipeline("sentiment-analysis",
                              model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
                              device="cpu",
                              framework="pt",
                              truncation=True,
                              max_length=512)
    return model_pipeline

def init_worker():
    global model_pipeline_worker
    print(f"Initializing sentiment model for worker process...")
    model_pipeline_worker = load_sentiment_model()
    print(f"Worker model loaded successfully.")

def process_chunk(df_chunk):
    global model_pipeline_worker

    if model_pipeline_worker is None:
        print("WARN: Model was not loaded during init_worker, loading now...")
        init_worker()

    try:
        text_list = df_chunk['body'].tolist()
        results = model_pipeline_worker(text_list, batch_size=64)
        results_df = pd.DataFrame(results)
        df_chunk = df_chunk.reset_index(drop=True)
        df_chunk['sentiment_label'] = results_df['label']
        df_chunk['sentiment_score'] = results_df['score']

    except Exception as e:
        print(f"ERROR: Failed to process chunk: {e}")
        df_chunk['sentiment_label'] = 'Error'
        df_chunk['sentiment_score'] = 0.0

    return df_chunk