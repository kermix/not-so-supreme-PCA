import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State

from nssPCA.data import generate
from nssPCA.preprocessing import Scaler
from .server import app

layout = html.Div([
    html.Div([
        html.H5("Axis:"),
        html.Div([
            html.Span("1. Dimension to compress", style={"padding": 10, "text-align": "right"}),
            html.Div(dcc.RadioItems(
                id="radio-dimensions",
                options=[
                    {'label': 'Columns ({})'.format(len(app.context.data.columns)), 'value': '1'},
                    {'label': 'Rows ({})'.format(len(app.context.data.index)), 'value': '0'},
                ],
                value='1'
            ))]),
        html.Hr(),

        html.H5("Z-normalization: "),
        html.Div([
            html.Span("2. Mean center the data", style={"padding": 10, "text-align": "right"}),
            html.Div(dcc.RadioItems(
                id="radio-mean",
                options=[
                    {'label': 'Yes', 'value': 'True'},
                    {'label': 'No', 'value': 'False'},
                ],
                value='False'
            ))]),
        html.Div([
            html.Span("3. Use variance scaling", style={"padding": 10, "text-align": "right"}),
            html.Div(dcc.RadioItems(
                id="radio-std",
                options=[
                    {'label': 'Yes', 'value': 'True'},
                    {'label': 'No', 'value': 'False'},
                ],
                value='False'
            ))]),
        html.Hr(),

        # html.H5("Transormation ln(x)"),
        # html.H5("Constant columns removing"),
        # html.H5("Cooperating with NaNs: remove col/row or insert mean"),
        # html.H5("Grouping data for mean/median"),
        # html.Hr(),
        html.Button(id='preprocessing-button', n_clicks=0, children='Submit')
    ], className="two columns"),
    html.Div([
        dash_table.DataTable(
            id='preprocessing-datatable-paging',
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
    ], className="ten columns")
])


@app.callback(
    [Output('preprocessing-datatable-paging', 'data'),
     Output('preprocessing-datatable-paging', 'columns')],
    [Input('preprocessing-datatable-paging', 'pagination_settings'),
     Input('tabs', 'value'),
     Input('preprocessing-button', 'n_clicks')],
    [State("radio-dimensions", "value"),
     State("radio-mean", "value"),
     State("radio-std", "value")])
def preprocess_data(pagination_settings, tab, _n_clicks, dimension, mean, std):
    if tab in ["pre"]:
        app.context.axis = int(dimension)

        app.context.calc_mean = False if mean == "False" else True
        app.context.calc_std = False if std == "False" else True

        matrix = generate(app.context.data)

        app.context.scaler = Scaler(
            calc_mean=app.context.calc_mean,
            calc_std=app.context.calc_std,
            axis=(0 if app.context.axis == 1 else 1))

        normalized = app.context.scaler.transform(matrix.values)

        app.context.normalized_data = pd.DataFrame(normalized,
                                                   index=matrix.index,
                                                   columns=matrix.columns)
        if not app.context.normalized_data.empty:
            page_data = app.context.normalized_data.iloc[
                        pagination_settings['current_page'] * pagination_settings['page_size']:
                        (pagination_settings['current_page'] + 1) * pagination_settings['page_size']
                        ].to_dict('rows')

            page_columns = [{'name': i, 'id': i} for i in app.context.normalized_data.columns]

        return page_data, page_columns


@app.callback(Output("radio-dimensions", "options"),
              [Input('tabs', 'value')])
def update_radio(tab):
    return [
        {'label': 'Columns ({})'.format(len(app.context.data.columns)), 'value': '1'},
        {'label': 'Rows ({})'.format(len(app.context.data.index)), 'value': '0'},
    ]
