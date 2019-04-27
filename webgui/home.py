import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from . import welcomeTab, loadDataTab, preprocessingTab, pcaTab, plotTab, exportTab
from .server import app

app.layout = html.Div([
    html.H1('Welcome in not so supreme PCA program.'),
    dcc.Tabs(
        children=[
            dcc.Tab(label='Home', children=[welcomeTab.layout]),
            dcc.Tab(label='Import Data', children=[loadDataTab.layout]),
            dcc.Tab(label='Preprocessing', children=[preprocessingTab.layout]),
            dcc.Tab(label='PCA', children=[pcaTab.layout]),
            dcc.Tab(label='Plot', children=[plotTab.layout]),
            dcc.Tab(label='Export results', children=[exportTab.layout])
        ],
        id='tabs'
    ),
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-home':
        return welcomeTab.layout
    elif tab == 'tab-import':
        return loadDataTab.layout
    elif tab == 'tab-preprocessing':
        return preprocessingTab.layout
    elif tab == 'tab-pca':
        return pcaTab.layout
    elif tab == 'tab-plot':
        return plotTab.layout
    elif tab == 'tab-export':
        return exportTab.layout


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
