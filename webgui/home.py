import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from . import welcomeTab, loadDataTab, preprocessingTab, pcaTab, plotTab, exportTab
from .server import app, Context

app.layout = html.Div([
    html.Button(id='reset-button', n_clicks=0, children='Reset Analysis',
                style={'margin': '5px', "margin-right": '0', 'margin-left': 'auto', 'display': 'block'}),
    dcc.Tabs(
        children=[
            dcc.Tab(label='Home', children=[welcomeTab.layout], value='home'),
            dcc.Tab(label='1. Import Data', children=[loadDataTab.layout], value='import'),
            dcc.Tab(label='2. Preprocessing', children=[preprocessingTab.layout], value='pre'),
            dcc.Tab(label='3. PCA', children=[pcaTab.layout], value='pca'),
            dcc.Tab(label='4. Plot', children=[plotTab.layout], value='plot'),
            dcc.Tab(label='5. Export results', children=[exportTab.layout], value='export')
        ],
        id='tabs',
        value='home'
    ),
])


@app.callback([Output('tabs', 'value'),
               Output("index-column", "value"),
               Output('columns', 'value'),
               Output("radio-dimensions", "value"),
               Output("radio-mean", "value"),
               Output("radio-std", "value"),
               Output('radio-algorithm', 'value'),
               Output('no-pcs-slider', 'value'),
               Output('xaxis', 'value'),
               Output('yaxis', 'value'),
               Output('upload-data', 'contents'),
               Output('upload-data', 'filename')],
              [Input('reset-button', 'n_clicks')])
def app_reset(_n_clicks=0):
    app.context = Context()

    tab = "home"
    pagination_settings = {
        "current_page": 0,
        "page_size": 20,
    }
    index_column = ""
    selected_columns = ""
    axis = '1'
    calc_mean = 'False'
    calc_std = 'False'

    algorithm = ''

    no_pcs = '1'

    plot_pc = ''

    file_content = ""
    file_name = ""

    return tab, \
           index_column, \
           selected_columns, \
           axis, \
           calc_mean, \
           calc_std, \
           algorithm, \
           no_pcs, \
           plot_pc, \
           plot_pc, \
           file_content, \
           file_name
