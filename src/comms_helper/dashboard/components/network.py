from comms_helper.analysis.network import (
    create_edgelist,
    create_process_graph,
    get_edgelist,
)
from comms_helper.visualisation.network import NetworkVisualiser
import random
from comms_helper.dashboard.dataloading import DashDataFromScrape, DashDataFromDatabase
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from __init__ import dashapp
import os

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")

network_layout = html.Div(
    [
        dcc.Graph(
            id="network",
        )
    ],
    id="network-layout",
)


@dashapp.callback(
    Output("network", "figure"),
    Input("data", "children"),
    Input("data-mentions", "children"),
)
def update_network(json_data, json_data_mentions):
    df = pd.read_json(json_data, orient="split")
    df_mentions = pd.read_json(json_data_mentions, orient="split")
    df_edgelist = create_edgelist(df, df_mentions)
    g = create_process_graph(df_edgelist)

    random.seed(42)

    layout = g.layout("fr")
    edgelist = get_edgelist(g)
    # visualiser
    visualiser = NetworkVisualiser(g, layout, edgelist)

    visualiser.get_nodes()

    visualiser.get_edges()

    visualiser.get_node_colors()

    visualiser.get_node_sizes()
    graph_fig = visualiser.visualise_network()
    return graph_fig
