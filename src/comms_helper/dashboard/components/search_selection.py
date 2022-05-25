from turtle import update
from comms_helper.data.db_utils import get_engine
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from __init__ import dashapp
from comms_helper.data.update_tables import create_schema_and_tables, scrape_to_database
import os

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")

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
        html.Button("Update", id="update-tweets-button", n_clicks=0),
        html.Div(id="update_output", style={"display": "none"}),
    ]
)


@dashapp.callback(
    Output("update_output", "children"),
    Input("update-tweets-button", "n_clicks"),
    prevent_initial_call=True,
)
def update_database(n_clicks):
    create_schema_and_tables("tweets", user, password)
    engine = get_engine(user, password, schema="tweets")
    with engine.connect() as conn:
        max_timestamp = pd.read_sql(
            "SELECT MAX(timestamp) AS max_timestamp FROM tweets", con=conn
        )["max_timestamp"].iloc[0]
    scrape_to_database(
        "Robert Hazell",
        schema="tweets",
        user=user,
        password=password,
        start_date=max_timestamp,
    )
    return None
