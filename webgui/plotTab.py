import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from .server import app

layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Span("Scatter Plot x-axis", style={"padding": 10, "text-align": "right"}),
                html.Div(dcc.Dropdown(id="xaxis",
                                      options=[{'label': column, 'value': column}
                                               for column in app.context.transformed_data.columns],
                                      value='',

                                      ))]),
            html.Div([
                html.Span("Scatter Plot y-axis", style={"padding": 10, "text-align": "right"}),
                html.Div(dcc.Dropdown(id="yaxis",
                                      options=[{'label': column, 'value': column}
                                               for column in app.context.transformed_data.columns],
                                      value='',

                                      ))]),
        ]),
    ], className="two columns"),
    html.Div([
        dcc.Graph(id="pca-graph")], className='ten columns'),

])


@app.callback(Output("pca-graph", "figure"),
              [Input("xaxis", "value"),
               Input("yaxis", "value")])
def plot(xaxis, yaxis):
    trace = []
    if xaxis and yaxis:
        trace = [go.Scatter(
            x=app.context.transformed_data[xaxis],
            y=app.context.transformed_data[yaxis],
            hovertext=app.context.transformed_data.index,
            mode='markers'

        )]

    return {
        "data": trace,
        "layout": go.Layout(height=800,

                            xaxis={
                                "title": xaxis,

                            },
                            yaxis={
                                "title": yaxis,
                                "scaleratio": 1,
                                "scaleanchor": 'x'
                            })
    }
