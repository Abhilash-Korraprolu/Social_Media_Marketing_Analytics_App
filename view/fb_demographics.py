import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pandas_datareader as pdr
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px


def age_groups():
    df = pd.read_excel('model/8_insta_age_gender.xlsx')

    fig = px.bar(df, x='count', y='age_group', title='Age Groups')
    graph = dcc.Graph(figure=fig, responsive=True)

    return graph


layout = html.Div(
    children=[
        age_groups()
    ])
