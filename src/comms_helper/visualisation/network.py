from sklearn.preprocessing import minmax_scale
import plotly.graph_objects as go
import numpy as np
import seaborn as sns


DEFAULT_VERTEX_RANGE = (5, 20)
DEFAULT_EDGE_RANGE = (0.1, 2)

def node_coords(layout, N=None):
    if N is None:
        N = len(layout)
    Xn = [layout[k][0] for k in range(N)]
    Yn = [layout[k][1] for k in range(N)]
    return Xn, Yn

def edge_coords(layout, edgelist):
    Xe = []
    Ye = []
    for e in edgelist:
        Xe += [layout[e[0]][0], layout[e[1]][0], None]
        Ye += [layout[e[0]][1], layout[e[1]][1], None]
    return Xe, Ye

def get_node_sizes(arr, feature_range=DEFAULT_VERTEX_RANGE):
    return minmax_scale(arr, feature_range=feature_range)

def community_color_map(communities, colorpal=None):
    n_communities = len(communities)
    if colorpal is None:
        colorpal = sns.color_palette
    colorpal_n = colorpal(n_colors=n_communities)
    hexvals = colorpal_n.as_hex()
    return {communities[i]: j for i, j in enumerate(hexvals)}

def get_node_colors(series, communities=None, colorpal=None):
    if communities is None:
        communities = np.unique(series)
    cmap = community_color_map(communities, colorpal=colorpal)
    return series.map(cmap).values


def plot_graph_plotly(
    labels, Xn, Yn, Xe, Ye, node_sizes=None, node_colors=None, title="Social network"
):
    if node_sizes is None:
        node_sizes = 5
    if node_colors is None:
        node_colors = "#6959CD"
    trace1 = go.Scatter(
        x=Xe,
        y=Ye,
        mode="lines",
        line=dict(color="rgb(210,210,210)", width=1),
        hoverinfo="none",
    )
    trace2 = go.Scatter(
        x=Xn,
        y=Yn,
        mode="markers",
        name="ntw",
        marker=dict(
            symbol="circle-dot",
            size=node_sizes,
            color=node_colors,
            line=dict(color="rgb(50,50,50)", width=0.5),
        ),
        text=labels,
        hoverinfo="text",
    )

    axis = dict(
        showline=False,  # hide axis line, grid, ticklabels and  title
        zeroline=False,
        showgrid=False,
        showticklabels=False,
        title="",
    )

    width = 800
    height = 800
    layout = go.Layout(
        title=title,
        font=dict(size=12),
        showlegend=False,
        autosize=False,
        width=width,
        height=height,
        xaxis=go.layout.XAxis(axis),
        yaxis=go.layout.YAxis(axis),
        margin=go.layout.Margin(
            l=40,
            r=40,
            b=85,
            t=100,
        ),
        hovermode="closest",
        annotations=[
            dict(
                showarrow=False,
                text="Visualisation of a social network",
                xref="paper",
                yref="paper",
                x=0,
                y=-0.1,
                xanchor="left",
                yanchor="bottom",
                font=dict(size=14),
            )
        ],
    )

    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    return fig

def plot_graph_plotly(
    labels, Xn, Yn, Xe, Ye, node_sizes=None, node_colors=None, title="Social network"
):
    if node_sizes is None:
        node_sizes = 5
    if node_colors is None:
        node_colors = "#6959CD"
    trace1 = go.Scatter(
        x=Xe,
        y=Ye,
        mode="lines",
        line=dict(color="rgb(210,210,210)", width=1),
        hoverinfo="none",
    )
    trace2 = go.Scatter(
        x=Xn,
        y=Yn,
        mode="markers",
        name="ntw",
        marker=dict(
            symbol="circle-dot",
            size=node_sizes,
            color=node_colors,
            line=dict(color="rgb(50,50,50)", width=0.5),
        ),
        text=labels,
        hoverinfo="text",
    )

    axis = dict(
        showline=False,  # hide axis line, grid, ticklabels and  title
        zeroline=False,
        showgrid=False,
        showticklabels=False,
        title="",
    )

    width = 800
    height = 800
    layout = go.Layout(
        title=title,
        font=dict(size=12),
        showlegend=False,
        autosize=False,
        width=width,
        height=height,
        xaxis=go.layout.XAxis(axis),
        yaxis=go.layout.YAxis(axis),
        margin=go.layout.Margin(
            l=40,
            r=40,
            b=85,
            t=100,
        ),
        hovermode="closest",
        annotations=[
            dict(
                showarrow=False,
                text="Visualisation of a social network",
                xref="paper",
                yref="paper",
                x=0,
                y=-0.1,
                xanchor="left",
                yanchor="bottom",
                font=dict(size=14),
            )
        ],
    )

    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    return fig

class NetworkVisualiser:
    def __init__(self,g,layout,edgelist):
        self.g = g
        self.layout = layout
        self.edgelist = edgelist

    def get_nodes(self):
        self.Xn, self.Yn = node_coords(self.layout)

    def get_edges(self):
        self.Xe, self.Ye = edge_coords(self.layout, self.edgelist)

    def get_node_sizes(self):
        self.node_sizes = get_node_sizes(self.g.info_table.betweenness.values)

    def get_node_colors(self):
        self.node_colors = get_node_colors(self.g.info_table.community)

    def visualise_network(self):
        return plot_graph_plotly(self.g.namearr, self.Xn, self.Yn, self.Xe, self.Ye, node_sizes=self.node_sizes, node_colors=self.node_colors, title="Social network")