from dash import html, dcc
from dash.dependencies import Input, Output, State
from __init__ import dashapp

search_selection_layout = html.Div(
    [
        dcc.Dropdown(
            options=[
                {"label": i, "value": i} for i in ["Robert Hazell", "Meg Russell"]
            ],
            value=["Robert Hazell"],
            multi=False,
            id="search-selection",
        ),
    ]
)
