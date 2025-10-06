from datetime import datetime, timedelta

def count_comments(sub, logger, comment_approve_point, comment_max_days):
    one_week_ago = datetime.utcnow() - timedelta(comment_max_days)
    comment_count = 0
    try:
        for submission in sub.new(limit=None):
            created = datetime.utcfromtimestamp(submission.created_utc)
            if created < one_week_ago:
                break
            comment_count += submission.num_comments
            if comment_count >= comment_approve_point:
                comment_count = comment_approve_point
                break
    except Exception as e:
        logger.info(f" Error counting comments for r/{sub.display_name}: {e} ===")
        comment_count = 0

    return comment_count