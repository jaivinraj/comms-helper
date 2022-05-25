from comms_helper.dashboard.dataloading import DashDataFromScrape, DashDataFromDatabase
from dash import html
from dash.dependencies import Input, Output, State
from __init__ import dashapp
import os

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")

hidden_layout = html.Div([html.Div(id="data", style={"display": "none"})])


@dashapp.callback(
    Output("data", "children"),
    Input("search-selection", "value"),
)
def update_data(value):
    dataloader = DashDataFromDatabase(searchname=value, user=user, password=password)
    df = dataloader.get_tweets()
    return df.to_json(date_format="iso", orient="split")
