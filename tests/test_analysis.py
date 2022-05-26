from venv import create
from comms_helper.analysis.time_series import get_tweet_count
from comms_helper.data.dummy import df_dummy
from comms_helper.preprocessing.handle_extraction import extract_handles
from comms_helper.analysis.network import create_edgelist, create_process_graph
import pandas as pd

# df_test = pd.DataFrame(
#     {
#         "timestamp": [pd.to_datetime("2022-01-01"), pd.to_datetime("2022-01-02")],
#         "content": ["a tweet", "another tweet"],
#     }
# )
# TIME SERIES
def test_time_series():
    assert len(get_tweet_count(df_dummy)) == 2


# NETWORK CREATION
def test_edgelist_creation():
    df_mentions = (
        extract_handles(df_dummy.set_index("tweet_id")["content"])
        .to_frame("username")
        .reset_index()
    )
    df_edgelist = create_edgelist(df_dummy, df_mentions)


def test_graph_creation():
    df_mentions = (
        extract_handles(df_dummy.set_index("tweet_id")["content"])
        .to_frame("username")
        .reset_index()
    )
    df_edgelist = create_edgelist(df_dummy, df_mentions)
    g = create_process_graph(df_edgelist)
