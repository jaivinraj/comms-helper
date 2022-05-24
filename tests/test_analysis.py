from comms_helper.analysis.time_series import get_tweet_count
import pandas as pd

def_test = pd.DataFrame(
    {
        "date": [pd.to_datetime("2022-01-01"), pd.to_datetime("2022-01-02")],
        "content": ["a tweet", "another tweet"],
    }
)
# TIME SERIES
def test_time_series():
    assert len(get_tweet_count(def_test)) == 1
