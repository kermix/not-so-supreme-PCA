import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output

from nssPCA.data import read_data
from .server import app

FILENAME = "/home/mateusz/data.xlsx"

original_data = read_data(FILENAME)

data = original_data.copy()

layout = html.Div([
    html.Div([
        html.H2("Configuration"),
        html.Hr(),
        html.Div([
            html.Span("Choose columns to analyze", style={"padding": 10, "text-align": "right"}),
            html.Div(dcc.Dropdown(id="columns",
                                  options=[{'label': column, 'value': column} for column in original_data.columns],
                                  value="",
                                  clearable=True,
                                  multi=True
                                  ), style={"margin": 0})]),
        html.Hr(),
        html.Div([
            html.Span("Choose index column", style={"padding": 10, "text-align": "right"}),
            html.Div(dcc.Dropdown(id="index-column",
                                  options=[{'label': column, 'value': column} for column in original_data.columns],
                                  value=""
                                  ), style={"margin": 0})]),
        html.Div(id='columns-intermediate', style={'display': 'none'})
    ], className="two columns"),
    html.Div([
        dash_table.DataTable(
            id='datatable-paging',
            data=data.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in data.columns],
            style_table={
                'height': '670px',
                'overflowY': 'scroll',
                'border': 'thin lightgrey solid'
            },
            pagination_mode="be",
            pagination_settings={
                "current_page": 0,
                "page_size": 25,
            },
        )
    ], className="ten columns"),
])


@app.callback([
    Output('datatable-paging', 'data'),
    Output('datatable-paging', 'columns')],
    [Input('datatable-paging', 'pagination_settings'),
     Input('columns-intermediate', 'children'),
     Input("index-column", "value")])
def select_columns(pagination_settings, filtered_data, index_column):
    data = pd.read_json(filtered_data)

    if index_column:
        data = data.set_index(index_column)
    else:
        data = data.reindex(index=range(data.shape[0]))

    return data.iloc[
           pagination_settings['current_page'] * pagination_settings['page_size']:
           (pagination_settings['current_page'] + 1) * pagination_settings['page_size']
           ].to_dict('rows'), [{'name': i, 'id': i} for i in data.columns]


@app.callback(Output('columns-intermediate', 'children'), [Input('columns', 'value')])
def clean_data(value):
    if not value:
        value = [column for column in original_data.columns]
    df = original_data.filter(items=value, axis=1)
    return df.to_json()
