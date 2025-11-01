import pandas as pd
from transformers import pipeline
import torch
from src.core.config_utils import get_config

model_pipeline_worker = None


def load_sentiment_model():
    try:
        device_type = get_config("analysis", "device_type", fallback="cpu")
    except Exception:
        print("WARN: Could not read config, defaulting to CPU.")
        device_type = "cpu"

    if device_type.lower() == "gpu":
        print("Config set to GPU. Attempting to use device 0 (NVIDIA CUDA)...")
        device_arg = "cuda"
    else:
        print(f"Config set to CPU (device_type={device_type}). Using device='cpu'.")
        device_arg = "cpu"

    model_pipeline = pipeline("sentiment-analysis",
                              model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
                              framework="pt",
                              truncation=True,
                              max_length=512,
                              device=device_arg)
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

        batch_size_to_try = 64
        results = model_pipeline_worker(text_list, batch_size=batch_size_to_try)

        results_df = pd.DataFrame(results)
        df_chunk = df_chunk.reset_index(drop=True)
        df_chunk['sentiment_label'] = results_df['label']
        df_chunk['sentiment_score'] = results_df['score']

    except Exception as e:
        print(f"ERROR: Failed to process chunk: {e}")
        df_chunk['sentiment_label'] = 'Error'
        df_chunk['sentiment_score'] = 0.0

    return df_chunk


def analyze_sentiment_batch(text_list, model):
    batch_size_to_try = 128

    try:
        results = model(text_list, batch_size=batch_size_to_try)
    except torch.cuda.OutOfMemoryError:
        print(f"WARN: CUDA Out of Memory with batch_size={batch_size_to_try}. Retrying with batch_size=32...")
        results = model(text_list, batch_size=32)
    except Exception as e:
        print(f"ERROR during batch analysis: {e}")
        return []

    return results