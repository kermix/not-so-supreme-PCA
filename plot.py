import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from nssPCA.data import Holder

result = Holder("/home/mateusz/PycharmProjects/not-so-supreme-PCA/result.xlsx", index_col="Protein IDs").data

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Span("Scatter Plot x-axis", style={"width": 150, "padding": 10, "text-align": "right"}),
                html.Div(dcc.Dropdown(id="xaxis",
                                      options=[{'label': column, 'value': column} for column in result.columns],
                                      value=result.columns[0],

                                      ), style={"width": 250, "margin": 0})], className="row"),
            html.Div([
                html.Span("Scatter Plot y-axis", style={"width": 150, "padding": 10, "text-align": "right"}),
                html.Div(dcc.Dropdown(id="yaxis",
                                      options=[{'label': column, 'value': column} for column in result.columns],
                                      value=result.columns[0],

                                      ), style={"width": 250, "margin": 0})], className="row"),
        ]),
    ], className="row"),
    html.Div([
        dcc.Graph(id="my-graph")]),

], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("xaxis", "value"),
     dash.dependencies.Input("yaxis", "value")]
)
def update_graph(selected1, selected2):
    trace = [go.Scatter(
        x=result[selected1],
        y=result[selected2],
        hovertext=result.index,
        mode='markers'

    )]

    return {
        "data": trace,
        "layout": go.Layout(height=800,

                            xaxis={
                                "title": selected1,

                            },
                            yaxis={
                                "title": selected2,
                                "scaleratio": 1,
                                "scaleanchor": 'x'
                            })
    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
