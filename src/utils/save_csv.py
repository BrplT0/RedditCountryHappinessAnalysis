from datetime import datetime
from pathlib import Path

def parent_root(file_location):
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent

    full_path = project_root / file_location
    target_dir = full_path if not full_path.suffix else full_path.parent
    target_dir.mkdir(parents=True, exist_ok=True)

    today_str = datetime.today().strftime("%Y-%m-%d")

    file_path = (
        full_path / f"{today_str}.csv"
        if not full_path.suffix
        else full_path
    )

    return file_path


def save_csv(df, logger, file_location):
    file_path = parent_root(file_location)
    df.to_csv(file_path, index=False)
    project_root = Path(__file__).parent.parent.parent
    logger.info(f"📁 CSV successfully saved: {file_path.relative_to(project_root)}")

#data/raw/subreddits/
# C:\Users\Ichigo\PycharmProjects\RedditCountryHappinessAnalysis\src\utils\save_csv.py
# C:\Users\Ichigo\PycharmProjects\RedditCountryHappinessAnalysis
# C:\Users\Ichigo\PycharmProjects\RedditCountryHappinessAnalysis\data\raw\subreddits
