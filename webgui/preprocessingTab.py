import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State

from nssPCA.data import generate, get_invalid_data
from nssPCA.preprocessing import Scaler
from .server import app

layout = html.Div([
    html.Div([
        html.H5("Group data:"),
        html.Span("1. Change value to calculate new variables for groups of data",
                  style={"padding": 10, "text-align": "right"}),
        dcc.Input(
            id='no-groups',
            inputMode='numeric',
            type='number',
            min=0,
            step=1,
            value=0,
            disabled=True
        ),
        html.Div(id='groups-dropdowns', children=[]),
        html.Button(id='group-button', children='Group', disabled=True),
        html.H5("Axis:"),
        html.Div([
            html.Span("2. Dimension to compress", style={"padding": 10, "text-align": "right"}),
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
            html.Span("3. Mean center the data", style={"padding": 10, "text-align": "right"}),
            html.Div(dcc.RadioItems(
                id="radio-mean",
                options=[
                    {'label': 'Yes', 'value': 'True'},
                    {'label': 'No', 'value': 'False'},
                ],
                value='False'
            ))]),
        html.Div([
            html.Span("4. Use variance scaling", style={"padding": 10, "text-align": "right"}),
            html.Div(dcc.RadioItems(
                id="radio-std",
                options=[
                    {'label': 'Yes', 'value': 'True'},
                    {'label': 'No', 'value': 'False'},
                ],
                value='False'
            ))]),
        html.Hr(),
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
    ], className="ten columns"),
    # html.Div(id='test'),
    html.Div(id='preprocessing-errors', children=[], style={'display': 'none'})
])


@app.callback(
    [Output('preprocessing-datatable-paging', 'data'),
     Output('preprocessing-datatable-paging', 'columns'),
     Output('preprocessing-errors', 'children')],
    [Input('preprocessing-datatable-paging', 'pagination_settings'),
     Input('tabs', 'value'),
     Input('preprocessing-button', 'n_clicks'),
     Input('group-button', 'n_clicks')
     ],
    [State("radio-dimensions", "value"),
     State("radio-mean", "value"),
     State("radio-std", "value"),
     State('groups-dropdowns', 'children')
     ])
def preprocess_data(pagination_settings, tab, _n_clicks_preprocessing, _n_clicks_group, dimension, mean, std, groups):
    if app.context.original_data.empty and tab == 'home':
        errors = []

    if tab in ["pre"]:
        grouped_data = pd.DataFrame(index=app.context.data.index)
        if groups:
            column_groups = []
            for item in groups:
                if item['type'] == 'Div':
                    for e in item['props']['children']:
                        if e['type'] == 'Dropdown' and e['props']['value']:
                            column_groups.append(e['props']['value'])

            grouped_data = pd.DataFrame(index=app.context.data.index)  # TODO move grouping to function
            for group in column_groups:
                grouped_data[', '.join(group)] = app.context.data[group].mean(axis=1)
        else:
            grouped_data = app.context.data

        errors = []

        app.context.axis = int(dimension)

        app.context.calc_mean = False if mean == "False" else True
        app.context.calc_std = False if std == "False" else True

        matrix = generate(grouped_data)

        app.context.scaler = Scaler(
            calc_mean=app.context.calc_mean,
            calc_std=app.context.calc_std,
            axis=(0 if app.context.axis == 1 else 1))

        normalized = app.context.scaler.transform(matrix.values)

        app.context.normalized_data = pd.DataFrame(normalized,
                                                   index=matrix.index,
                                                   columns=matrix.columns)

        if not app.context.normalized_data.empty:
            for t in get_invalid_data(app.context.normalized_data):
                errors.append('Invalid values in: {}'.format(t))

            page_data = app.context.normalized_data.iloc[
                        pagination_settings['current_page'] * pagination_settings['page_size']:
                        (pagination_settings['current_page'] + 1) * pagination_settings['page_size']
                        ].to_dict('rows')

            page_columns = [{'name': i, 'id': i} for i in app.context.normalized_data.columns]

            return page_data, page_columns, errors
        else:
            errors.append('Preprocessing: No data loaded.')

    return [], [], []  # errors


@app.callback(Output("radio-dimensions", "options"),
              [Input('tabs', 'value')])
def update_radio(tab):
    return [
        {'label': 'Columns ({})'.format(len(app.context.data.columns)), 'value': '1'},
        {'label': 'Rows ({})'.format(len(app.context.data.index)), 'value': '0'},
    ]


@app.callback([Output('groups-dropdowns', 'children'),
               Output('group-button', 'disabled')],
              [Input('no-groups', 'value')])
def generate_groups(no_groups):
    iterator = range(1, no_groups + 1)

    return [html.Div([html.Span('Group {}'.format(i)),
                      dcc.Dropdown(id='group-{}'.format(i),
                                   value='',
                                   clearable=True,
                                   multi=True,
                                   options=[{'label': column, 'value': column} for column in
                                            app.context.data.columns],
                                   style={'margin': '5px'})])
            for i in iterator], (False if no_groups else True)
