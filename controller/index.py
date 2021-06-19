import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from view.app import app
from view import fb_analytics, fb_demographics

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

client_id = 'soc_dps'


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/app1':
        return fb_demographics.layout
    elif pathname == '/':
        return fb_analytics.layout
    else:
        return pathname


if __name__ == '__main__':
    app.run_server(debug=True)
