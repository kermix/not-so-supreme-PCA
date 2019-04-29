import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

import nssPCA.decomposition as decomposition
import nssPCA.preprocessing as preprocessing
from .server import app

layout = html.Div([
    html.Div([
        html.H5("Fit the data:"),
        html.Span("1. Choose decompostion algorithm", style={"padding": 10, "text-align": "right"}),
        html.Div(dcc.RadioItems(
            id="radio-algorithm",
            options=[
                {'label': 'Eigen Value Decomposition (standard method, may be numerical unstable or imprecise)',
                 'value': 'eig'},
                {'label': 'Singular Value Decomposition (numerical stable method)', 'value': 'svd'},
                {'label': 'QR/SVD (recommended for large covariance matrices)', 'value': 'qrsvd'},
            ],
            value=''
        )),
        html.Br(),
        html.Button(id='pca-fit-button', n_clicks=0, children='Fit'),
        html.Hr(),
        html.H5("Transform the data:"),
        html.Span("2. Choose number of PC used to analysis", style={"padding": 10, "text-align": "right"}),
        dcc.Input(
            id='no-pcs-slider',
            inputmode='numeric',
            type='number',
            min=1,
            max=1,
            step=1,
            value=1,
        ),
        html.Br(),
        html.Button(id='pca-transform-button', n_clicks=0, children='Transform'),
    ], className="four columns"),
    html.Div([
        html.Div([dcc.Graph(id='explainded-variance-graph')], className="row"),
        html.Div([
            html.Div("Loadings TODO", className="six columns"),
            html.Div("R^2 TODO", className="six columns"),
        ], className='row')
    ], id='pca-output', className='eight columns')
])


@app.callback([Output('explainded-variance-graph', 'figure'),
               Output('no-pcs-slider', 'max')],
              [Input('pca-fit-button', 'n_clicks'),
               Input('tabs', 'value')],
              [State('radio-algorithm', 'value')])
def fit_data(_n_clicks, tab, algorithm):
    data, max_no_pcs = [], 1
    if tab in ["pca"]:
        if algorithm == 'eig':
            app.context.covariance_matix = preprocessing.covariance(app.context.normalized_data, axis=app.context.axis)
            app.context.PCA = decomposition.EigenDecomposition(axis=app.context.axis)
            app.context.PCA.fit(app.context.covariance_matix)
        elif algorithm == 'svd':
            app.context.PCA = decomposition.SVDecomposition(axis=app.context.axis)
            app.context.PCA.fit(app.context.normalized_data)
        elif algorithm == 'qrsvd':
            app.context.covariance_matix = preprocessing.covariance(app.context.normalized_data, axis=app.context.axis)
            app.context.PCA = decomposition.QRSVDecomposition(axis=app.context.axis)
            app.context.PCA.fit(app.context.covariance_matix)

        if app.context.PCA:
            # https://plot.ly/ipython-notebooks/principal-component-analysis/
            individual_trace = dict(
                type='bar',
                x=['PC{}'.format(i) for i in range(1, len(app.context.PCA.explained_ratio) + 1)],
                y=app.context.PCA.explained_ratio,
                name='Individual'
            )

            cummulatice_trace = dict(
                type='scatter',
                x=['PC{}'.format(i) for i in range(1, len(app.context.PCA.explained_ratio_cumulative) + 1)],
                y=app.context.PCA.explained_ratio_cumulative,
                name='Cumulative'
            )

            data = [individual_trace, cummulatice_trace]

            max_no_pcs = len(app.context.PCA.eigen_values)

    return {
               'data': data,
               'layout': go.Layout(
                   dict(
                       title='Explained variance by different principal components',
                       yaxis=dict(
                           title='Explained variance in percent'
                       ),
                       annotations=list([
                           dict(
                               xref='paper',
                               yref='paper',
                               text='Explained Variance',
                               showarrow=False,
                           )
                       ])
                   ))
           }, max_no_pcs


@app.callback([Output("xaxis", "options"),
               Output("yaxis", "options")],
              [Input('pca-transform-button', 'n_clicks')],
              [State('no-pcs-slider', 'value')])
def transform_data(_n_clicks, no_pcs):
    if app.context.PCA:
        app.context.PCA.number_of_components = no_pcs
        transformed_data = app.context.PCA.transform(app.context.normalized_data)

        app.context.transformed_data = pd.DataFrame(transformed_data,
                                                    index=app.context.normalized_data.index if app.context.axis else app.context.normalized_data.columns,
                                                    columns=["".join(("PC", str(i))) for i in
                                                             range(1, int(no_pcs) + 1)])

    axes = [{'label': column, 'value': column}
            for column in app.context.transformed_data.columns]

    return axes, axes
