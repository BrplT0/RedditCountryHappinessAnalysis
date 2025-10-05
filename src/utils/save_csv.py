from datetime import datetime

def save_csv(subreddits, logger, file_location):
    """
    :param subreddits: pandas dataframe
    :param logger: event logger
    :param file_location: raw file location and name without any datetime and .csv
    example:
    save_csv(df, logger, data/raw/filename)

    :return:
    """
    today = datetime.today()
    today_str = today.strftime("%Y-%m-%d")
    subreddits.to_csv(f"{file_location}{today_str}.csv", index=False)
    logger.info(f"📁 CSV saved: {today_str}.csv ===")

    f"../data/raw/subreddits/{today_str}.csv"