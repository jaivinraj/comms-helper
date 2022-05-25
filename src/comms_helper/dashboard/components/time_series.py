from dash import html, dcc

from __init__ import dashapp

import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from comms_helper.analysis.time_series import get_tweet_count


time_series_layout = html.Div(
    [
        dcc.Graph(
            id="time-series",
        )
    ],
    id="time-series-layout",
)


@dashapp.callback(
    Output("time-series", "figure"),
    Input("data", "children"),
)
def update_time_series(json_data):
    dff = pd.read_json(json_data, orient="split")
    tweet_count = get_tweet_count(dff, "W")
    pretty_names = {"n_tweets": "Number of tweets", "timestamp": "Week ending"}
    fig = px.line(
        tweet_count.to_frame("n_tweets").reset_index().rename(columns=pretty_names),
        x=pretty_names["timestamp"],
        y=pretty_names["n_tweets"],
    )
    return fig
