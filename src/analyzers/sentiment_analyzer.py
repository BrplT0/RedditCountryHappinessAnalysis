import pandas as pd
from transformers import pipeline
import torch
from src.core.config_utils import get_config

model_pipeline_worker = None
model_label_map = None
current_model_name = None

def load_sentiment_model():
    try:
        device_type = get_config("analysis", "device_type", fallback="cpu")
        model_name_config = get_config("analysis", "model_name", fallback="roberta")
    except Exception:
        print("WARN: Could not read config, defaulting to CPU.")
        device_type = "cpu"
        model_name_config = "roberta"

    if model_name_config.lower() == "distilbert":
        model_path = "distilbert-base-multilingual-cased"
    else:
        model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

    if device_type.lower() == "gpu":
        print(f"Config set to GPU. Using model: {model_path}")
        device_arg = "cuda"
    else:
        print(f"Config set to CPU. Using model: {model_path}")
        device_arg = "cpu"

    model_pipeline = pipeline("sentiment-analysis",
                              model=model_path,
                              framework="pt",
                              truncation=True,
                              max_length=512,
                              device=device_arg)

    label_map = model_pipeline.model.config.id2label

    return model_pipeline, label_map, model_name_config


def init_worker():
    global model_pipeline_worker
    global model_label_map
    global current_model_name

    print(f"Initializing sentiment model for worker process...")

    model_pipeline_worker, model_label_map, current_model_name = load_sentiment_model()

    print(f"Worker model loaded successfully: {current_model_name}")


def process_chunk(df_chunk):
    global model_pipeline_worker
    global model_label_map
    global current_model_name

    if model_pipeline_worker is None:
        print("WARN: Model was not loaded during init_worker, loading now...")
        init_worker()

    try:
        text_list = df_chunk['body'].tolist()
        results = model_pipeline_worker(text_list, batch_size=64)
        results_df = pd.DataFrame(results)

        if current_model_name and current_model_name.lower() == "distilbert":
            distilbert_map = {
                'LABEL_0': 'negative',
                'LABEL_1': 'positive'
            }
            results_df['sentiment_label'] = results_df['label'].replace(distilbert_map)
        else:
            results_df['label_id'] = results_df['label'].str.split('_').str[-1].astype(int)
            results_df['sentiment_label'] = results_df['label_id'].replace(model_label_map)

        df_chunk = df_chunk.reset_index(drop=True)
        df_chunk['sentiment_label'] = results_df['sentiment_label']
        df_chunk['sentiment_score'] = results_df['score']

    except Exception as e:
        print(f"ERROR: Failed to process chunk: {e}")
        df_chunk['sentiment_label'] = 'ERROR'
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