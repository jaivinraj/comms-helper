from comms_helper.dashboard.dataloading import DashDataFromScrape, DashDataFromDatabase
from dash import html
from dash.dependencies import Input, Output, State
from __init__ import dashapp
import os

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")

hidden_layout = html.Div(
    [
        html.Div(id="data", style={"display": "none"}),
        html.Div(id="data-mentions", style={"display": "none"}),
    ]
)


@dashapp.callback(
    Output("data", "children"),
    Input("search-selection", "value"),
    Input("update_output", "children"),
)
def update_data(value, child):
    dataloader = DashDataFromDatabase(searchname=value, user=user, password=password)
    df = dataloader.get_tweets()
    return df.to_json(date_format="iso", orient="split")


@dashapp.callback(
    Output("data-mentions", "children"),
    Input("search-selection", "value"),
    Input("update_output", "children"),
)
def update_data_mentions(value, child):
    dataloader = DashDataFromDatabase(searchname=value, user=user, password=password)
    df = dataloader.get_mentions()
    return df.to_json(date_format="iso", orient="split")
