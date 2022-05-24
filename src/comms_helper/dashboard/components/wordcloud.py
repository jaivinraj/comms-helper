from dash import html
from dash.dependencies import Input, Output, State
from __init__ import dashapp
import pandas as pd
from comms_helper.visualisation.wordclouds import ser_to_fig_wordcloud
from comms_helper.dashboard.dash_utils import fig_to_uri
from plotly.tools import mpl_to_plotly
from dash import dcc, html

import io
import base64


wordcloud_layout = html.Div([html.Img(id="wordcloud")], id="wordcloud_layout")


@dashapp.callback(
    Output("wordcloud", "src"),
    Input("data", "children"),
)
def update_wordcloud(json_data):
    dff = pd.read_json(json_data, orient="split")
    fig, ax = ser_to_fig_wordcloud(
        dff.content, random_state=42, title="Most common words in tweets"
    )
    return fig_to_uri(fig)
