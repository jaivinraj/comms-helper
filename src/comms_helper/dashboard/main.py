"""Script to run the Dash app"""

from __init__ import dashapp
from dash import Dash
from dash import html
import pandas as pd
from comms_helper.dashboard.components.hidden import hidden_layout
from comms_helper.dashboard.components.wordcloud import wordcloud_layout
from comms_helper.dashboard.components.search_selection import search_selection_layout

dashapp.layout = html.Div(
    [
        # html.Div(id="test", children="hello world"),
        search_selection_layout,
        wordcloud_layout,
        hidden_layout,
    ]
)


if __name__ == "__main__":
    dashapp.run_server(
        debug=True,
        host="0.0.0.0",
    )
