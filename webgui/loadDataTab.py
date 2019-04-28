import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

from nssPCA.data import read_data
from .server import app

# TODO: dcc.Upload for creating temp file, and reading this file using read_data().

FILENAME = "/home/mateusz/data.xlsx"

layout = html.Div([
    dcc.ConfirmDialog(
        id='exception'
    ),
    html.Div([
        html.H5("Set the data:"),
        html.Div([
            html.Span("1. Choose columns to analyze:", style={"padding": 10, "text-align": "right"}),
            html.Div(dcc.Dropdown(id="columns",
                                  options=[{'label': column, 'value': column}
                                           for column in app.context.original_data.columns],
                                  value="",
                                  clearable=True,
                                  multi=True
                                  ), style={"margin": 0})]),
        html.Div([
            html.Span("2. Choose index column:", style={"padding": 10, "text-align": "right"}),
            html.Div(dcc.Dropdown(id="index-column",
                                  options=[{'label': column, 'value': column}
                                           for column in app.context.original_data.columns],
                                  value=""
                                  ), style={"margin": 0})]),
        html.Br(),
        html.Button(id='load-button', n_clicks=0, children='Submit')
    ], className="two columns"),
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Upload comma separated value file or Microsoft Excel spreadsheet. ',
                html.A('Select File')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px 0'
            }
        ),
        dash_table.DataTable(
            id='datatable-paging',
            data=app.context.data.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in app.context.data.columns],
            style_table={
                'height': '645px',
                'overflowY': 'scroll',
                'border': 'thin lightgrey solid'
            },
            pagination_mode="be",
            pagination_settings={
                "current_page": 0,
                "page_size": 20,
            },
        )
    ], className="ten columns"),
])


@app.callback([
    Output('datatable-paging', 'data'),
    Output('datatable-paging', 'columns'),
    Output('columns', 'options'),
    Output('index-column', 'options')],
    [Input('load-button', 'n_clicks'),
     Input('tabs', 'value'),
     Input('datatable-paging', 'pagination_settings')],
    [State("index-column", "value"),
     State('columns', 'value')])
def update_data(_n_clicks, tab, pagination_settings, index_column, columns):
    if tab in ["import"]:
        app.context.data = app.context.original_data.copy()

        if not columns:
            columns = [column for column in app.context.original_data.columns]
        app.context.data = app.context.original_data.filter(items=columns, axis=1)

        if index_column:
            app.context.data = app.context.data.set_index(index_column)
        else:
            app.context.data = app.context.data.reindex(index=range(app.context.data.shape[0]))

        columns = [{'label': column, 'value': column} for column in app.context.original_data.columns]

    page_data = app.context.data.iloc[
                pagination_settings['current_page'] * pagination_settings['page_size']:
                (pagination_settings['current_page'] + 1) * pagination_settings['page_size']
                ].to_dict('rows')
    page_columns = [{'name': i, 'id': i} for i in app.context.data.columns]

    return page_data, page_columns, columns, columns


@app.callback([Output('load-button', 'n_clicks'),
               Output('exception', 'message'),
               Output('exception', 'displayed')],
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('load-button', 'n_clicks'),
               State('tabs', 'value')])
def parse_contents(contents, filename, n_clicks, tab):
    if tab == 'import' and contents is not None:
        content_type, content_string = contents.split(',')
        try:
            app.context.original_data = read_data(file_name=filename, buffer=content_string)
        except Exception as e:
            return n_clicks, e, True

    return n_clicks + 1, '', False
