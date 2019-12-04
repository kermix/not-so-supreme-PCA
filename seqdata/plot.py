import plotly.graph_objects as go
from plotly.subplots import make_subplots
import itertools
import numpy as np


def plot3d(data, clusters, labels, show=True):
    plot_data = go.Scatter3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        text=labels,
        mode='markers',
        marker=dict(
            size=5,
            color=clusters,  # set color to an array/list of desired values
            opacity=0.8
        )
    )

    if show:
        show_plot(plot_data)

    return plot_data


def plot2d(data, clusters, labels, show=True):
    plot_data = go.Scatter(
        x=data[:, 0],
        y=data[:, 1],
        text=labels,
        mode='markers',
        marker=dict(
            size=7,
            color=clusters,  # set color to an array/list of desired values
            opacity=0.8
        )
    )

    if show:
        show_plot(plot_data)

    return plot_data


def plot2d_subplots(data, clusters, labels):
    dims_combination = list(itertools.combinations(range(data.shape[1]), 2))
    n_combinations = len(dims_combination)
    n_rows = 1 if n_combinations == 1 else n_combinations // 3 + (n_combinations % 3 > 0)
    n_cols = 1 if n_combinations == 1 else 3

    fig = make_subplots(rows=n_rows, cols=n_cols)

    for i, c in enumerate(dims_combination):
        row = (i // 3)+1
        col = (i % 3)+1
        fig.add_trace(plot2d(
            np.column_stack(
                (
                    data[:, c[0]],
                    data[:, c[1]]
                )
            ),
            clusters,
            labels,
            False
        ),
            row=row,
            col=col
        )
        fig.update_xaxes(title_text="PC" + str(c[0]+1), row=row, col=col)
        fig.update_yaxes(title_text="PC" + str(c[1]+1), row=row, col=col)

    fig.update_layout(showlegend=False)
    fig.show()


def show_plot(plot_data):
    fig = go.Figure(data=[plot_data])
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()
