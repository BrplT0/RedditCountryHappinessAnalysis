import re

def clean_text(text):
    if not text:
        return ""

    text_str = str(text)
    text_str = text_str.replace("\n", " ")
    text_str = text_str.replace("\r", " ")
    text_str = text_str.replace("\t", " ")
    text_str = text_str.replace('"', "'")

    return text_str.strip()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def nlp_preprocess(df):
    df['author'] = df['author'].fillna('unknown_user_fill')
    df['body'] = df['body'].fillna('')
    df = df[~df['author'].str.lower().isin(['automoderator', 'deleted_user', 'unknown_user_fill'])]
    df = df[~df['body'].isin(['[deleted]', '[removed]'])]
    df['body'] = df['body'].apply(preprocess_text)
    df = df.dropna(subset=['body'])
    df = df[df['body'].str.len() >= 15]
    return df
