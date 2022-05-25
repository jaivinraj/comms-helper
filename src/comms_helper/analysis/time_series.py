resample_rule = "W"
rolling_window = 4

RULE_MAP = {"W": "Weekly", "M": "Monthly"}


def get_tweet_count(df, resample_rule="W"):
    return df.set_index("timestamp").resample(resample_rule).count()["content"]


def tweet_count_to_rolling(tweet_count, rolling_window=4):
    return tweet_count.rolling(rolling_window).mean()
