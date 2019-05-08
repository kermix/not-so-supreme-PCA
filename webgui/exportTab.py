from urllib.parse import quote

import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

from .server import app

df = app.context.original_data


layout = html.Div([
    html.H5("1. Import: "),
    html.A(
        'Download original data',
        id='original-link',
        download="original_data.csv",
        href="",
        target="_blank"
    ),
    html.Br(),
    html.A(
        'Download filtered data',
        id='filtered-link',
        download="filtered_data.csv",
        href="",
        target="_blank"
    ),
    html.Br(),
    html.H5("2. Preprocessing: "),
    html.A(
        'Download mean vector',
        id='mean-link',
        download="mean.csv",
        href="",
        target="_blank"
    ),
    html.Br(),
    html.A(
        'Download standard deviation vector',
        id='std-link',
        download="std.csv",
        href="",
        target="_blank"
    ),
    html.Br(),
    html.A(
        'Download normalized data',
        id='normalized-link',
        download="normalized_data.csv",
        href="",
        target="_blank"
    ),
    html.Br(),
    html.H5("3. PCA: "),
    html.A(
        'Download explained variance',
        id='variance-link',
        download="variance.csv",
        href="",
        target="_blank"
    ),
    html.Br(),
    html.A(
        'Download eigenvalues vector',
        id='eigenvalues-link',
        download="eigenvalues.csv",
        href="",
        target="_blank"
    ),
    html.Br(),
    html.A(
        'Download eigenvectors matrix',
        id='eigenvectors-link',
        download="eigenvectors.csv",
        href="",
        target="_blank"
    ),
    html.Br(),
    html.H4("Result data set: "),
    html.A(
        'Download transformed data',
        id='transformed-link',
        download="transformed_data.csv",
        href="",
        target="_blank"
    ),
])


@app.callback(
    Output('original-link', 'href'),
    [Input('tabs', 'value')])
def original_data_download_link(tab):
    csv_string = "data:text/csv;charset=utf-8,"
    if tab == 'export':
        data = app.context.original_data.to_csv(encoding='utf-8')
        csv_string += quote(data)
    return csv_string


@app.callback(
    Output('filtered-link', 'href'),
    [Input('tabs', 'value')])
def filtered_data_download_link(tab):
    csv_string = "data:text/csv;charset=utf-8,"
    if tab == 'export':
        data = app.context.data.to_csv(encoding='utf-8')
        csv_string += quote(data)
    return csv_string


@app.callback(
    Output('mean-link', 'href'),
    [Input('tabs', 'value')])
def mean_download_link(tab):
    csv_string = "data:text/csv;charset=utf-8,"
    if tab == 'export' and app.context.scaler:
        columns = app.context.normalized_data.columns if app.context.axis else app.context.normalized_data.index
        data = pd.DataFrame(app.context.scaler.mean_vector, index=columns).to_csv(encoding='utf-8')
        csv_string += quote(data)
    return csv_string


@app.callback(
    Output('std-link', 'href'),
    [Input('tabs', 'value')])
def std_download_link(tab):
    csv_string = "data:text/csv;charset=utf-8,"
    if tab == 'export' and app.context.scaler:
        columns = app.context.normalized_data.columns if app.context.axis else app.context.normalized_data.index
        data = pd.DataFrame(app.context.scaler.std_vector, index=columns).to_csv(encoding='utf-8')
        csv_string += quote(data)
    return csv_string


@app.callback(
    Output('normalized-link', 'href'),
    [Input('tabs', 'value')])
def normalized_data_download_link(tab):
    csv_string = "data:text/csv;charset=utf-8,"
    if tab == 'export':
        data = app.context.normalized_data.to_csv(encoding='utf-8')
        csv_string += quote(data)
    return csv_string


@app.callback(
    Output('variance-link', 'href'),
    [Input('tabs', 'value')])
def var_download_link(tab):
    csv_string = "data:text/csv;charset=utf-8,"
    if tab == 'export' and app.context.PCA:
        columns = ["".join(("PC", str(i))) for i in range(1, int(len(app.context.PCA.explained_ratio)) + 1)]
        data = pd.DataFrame(app.context.PCA.explained_ratio, index=columns).to_csv(encoding='utf-8')
        csv_string += quote(data)
    return csv_string


@app.callback(
    Output('eigenvalues-link', 'href'),
    [Input('tabs', 'value')])
def eigenvalues_download_link(tab):
    csv_string = "data:text/csv;charset=utf-8,"
    if tab == 'export' and app.context.PCA:
        columns = ["".join(("PC", str(i))) for i in range(1, int(len(app.context.PCA.eigen_values)) + 1)]
        data = pd.DataFrame(app.context.PCA.eigen_values, index=columns).to_csv(encoding='utf-8')
        csv_string += quote(data)
    return csv_string


@app.callback(
    Output('eigenvectors-link', 'href'),
    [Input('tabs', 'value')])
def eigenvectors_download_link(tab):
    csv_string = "data:text/csv;charset=utf-8,"
    if tab == 'export' and app.context.PCA:
        columns = app.context.normalized_data.columns
        index = ["".join(("PC", str(i))) for i in range(1, int(len(app.context.PCA.components)) + 1)]
        data = pd.DataFrame(app.context.PCA.components, index=index, columns=columns).to_csv(encoding='utf-8')
        csv_string += quote(data)
    return csv_string


@app.callback(
    Output('transformed-link', 'href'),
    [Input('tabs', 'value')])
def transformed_data_download_link(tab):
    csv_string = "data:text/csv;charset=utf-8,"
    if tab == 'export':
        data = app.context.transformed_data.to_csv(encoding='utf-8')
        csv_string += quote(data)
    return csv_string
