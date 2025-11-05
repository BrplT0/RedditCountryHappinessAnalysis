import pandas as pd

def aggregate_main(sentiment_scores):
    df = pd.DataFrame(sentiment_scores)
    df["happiness_value"] = df["sentiment_label"]
    df["happiness_value"].replace({"POSITIVE": 1, "NEGATIVE": -1, "NEUTRAL":0}, inplace=True)

    aggregated_df = df.groupby("country")["happiness_value"].mean().reset_index()
    return aggregated_df
