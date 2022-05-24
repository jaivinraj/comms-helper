from comms_helper.dashboard.dataloading import DashDataFromScrape
from dash import html
from dash.dependencies import Input, Output, State
from __init__ import dashapp


hidden_layout = html.Div([html.Div(id="data", style={"display": "none"})])


@dashapp.callback(
    Output("data", "children"),
    Input("search-selection", "value"),
)
def update_data(value):
    dataloader = DashDataFromScrape(searchname=value)
    dataloader.get_tweets()
    return dataloader.df.to_json(date_format="iso", orient="split")
