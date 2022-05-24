from dash import Dash, dash_table
from dash_bootstrap_components import themes

dashapp = Dash(
    __name__,
    external_stylesheets=[
        themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
    ],
)
