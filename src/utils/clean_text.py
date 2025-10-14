def clean_text(text):
    if not text:
        return ""
    return (
        str(text)
        .replace("\n", " ")
        .replace("\r", " ")
        .replace("\t", " ")
        .replace('"', "'")
        .strip()
    )