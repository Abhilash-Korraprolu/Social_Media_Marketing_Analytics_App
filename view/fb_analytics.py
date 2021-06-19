import dash_core_components as dcc
import dash_html_components as html
import pandas_datareader as pdr
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_table

from fb_page_insights import get_df_fb_list_of_posts_of_last_n_days
from model.fb_page_insights import plot_df, get_lifetime_likes_meter_values
from view.app import app

client_id_ = 'soc_dps'
list_of_posts_df = get_df_fb_list_of_posts_of_last_n_days(client_id=client_id_, last_n_days=30)


def style_time_series_line_plot(fig, title, id):
    fig.layout = dict(title=title, title_x=0.5, plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(showline=True, linewidth=0.2, linecolor='black', gridcolor='grey', gridwidth=0.5)
    fig.update_yaxes(showline=True, linewidth=0.2, linecolor='black', gridcolor='grey', gridwidth=0.5,
                     rangemode='tozero')
    graph = dcc.Graph(id=id, figure=fig, responsive=True)
    return graph


yo = html.Div([
            dcc.RadioItems(
                id='drop_down_date_range',
                options=[
                         {'label': '1M', 'value': 1},
                         {'label': '6M', 'value': 183},
                         {'label': '1Y', 'value': 365},
                ],
                value='Animal Condition',
                style={"width": "50%"}
            ),
        ])

yo2 = html.Div(id='fb_likes_graph')


@app.callback(
    Output(component_id='fb_likes_graph', component_property='children'),
    [Input(component_id='drop_down_date_range', component_property='value')]
)
def likes_meter_with_plot(drop_down_date_range):
    print(drop_down_date_range)
    likes_recent, likes_month_ago = get_lifetime_likes_meter_values(client_id=client_id_)
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=likes_recent,
        domain={'row': 0, 'column': 1},
        title={"text": "<span style='font-size:0.8em;color:gray'>30 Day Gain</span>"},
    ))
    fig.update_layout(
        template={'data': {'indicator': [{
            'title': {'text': "Likes<br><span style='font-size:0.8em;color:gray'>& gain in 1 month</span>"},
            'mode': "number+delta+gauge",
            'delta': {'reference': likes_month_ago}}]
        }})

    likes_column = 'lifetime_total_likes'
    df = plot_df(client_id_, column=likes_column)
    fig.add_trace(go.Scatter(x=df.index, y=df[likes_column], line={'color': '#eccc68'}, opacity=1))
    graph = style_time_series_line_plot(fig, title='Likes', id='fb_likes_graph')

    return graph


def plot_fb_impressions(client_id):
    impressions_column = 'daily_total_impressions'
    df = plot_df(client_id, column=impressions_column)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[impressions_column],
        line={'color': '#eccc68'},
        opacity=1
    ))
    # fig.update_layout(dict(title='Impressions', yaxis=dict(title='', showgrid=True)))
    graph = style_time_series_line_plot(fig=fig, title='Impressions', id='impressions_graph')
    # graph = dcc.Graph(figure=fig, responsive=True)
    return graph


def display_media_type_numbers(posts_df):
    fig = go.Figure()

    # When resized to phone, all posts becomes smaller. changing column vals still has it small
    fig.add_trace(go.Indicator(
        mode="number",
        value=posts_df.shape[0],
        domain={'row': 0, 'column': 0},
        title={'text': 'All Posts'}
    ))

    fig.add_trace(go.Indicator(
        mode="number",
        value=posts_df.loc[posts_df['media_type'] == 'photo'].shape[0],
        domain={'row': 0, 'column': 1},
        title={'text': 'Photos'}
    ))

    fig.add_trace(go.Indicator(
        mode="number",
        value=posts_df.loc[posts_df['media_type'] == 'link'].shape[0],
        domain={'row': 0, 'column': 2},
        title={'text': 'Links'}
    ))

    fig.add_trace(go.Indicator(
        mode="number",
        value=posts_df.loc[posts_df['media_type'] == 'video'].shape[0],
        domain={'row': 0, 'column': 3},
        title={'text': 'Videos'}
    ))

    fig.add_trace(go.Indicator(
        mode="number",
        value=posts_df.loc[posts_df['media_type'] == 'album'].shape[0],
        domain={'row': 0, 'column': 4},
        title={'text': 'Albums'}
    ))

    fig.update_layout(
        title={'text': 'In The Last 30 Days'},
        title_x=0.5,
        title_font={'family': "Bradley Hand", 'size': 30},
        grid={'rows': 1, 'columns': 5, 'pattern': "independent"},
        autosize=True,
        paper_bgcolor='#eccc50',
    )
    # 'width': '90vh',
    graph = dcc.Graph(figure=fig, responsive=True, style={'height': '37vh'})
    return graph


def display_recent_posts_table(posts_df):
    posts_df.sort_values('created_time', inplace=True, ascending=False)  # optional
    posts_df['created_time'] = posts_df['created_time'].dt.date
    posts_df['media_type'] = posts_df['media_type'].str.title()

    # the ones on top take precedence
    return html.Div(children=[
        html.Div(dash_table.DataTable(
            id='table_list_of_posts',
            style_as_list_view=True,  # removes box borders
            columns=[
                {'id': 'created_time', 'name': 'Date'},
                {'id': 'media_type', 'name': 'Type'},
                {'id': 'admin_creator', 'name': 'Creator'},
                {'id': 'message', 'name': 'Content'},
            ],
            data=posts_df.to_dict('records'),
            page_action='none',
            style_table={'height': '100%', 'overflowY': 'auto'},
            fixed_rows={'headers': True},
            style_header={
                'textAlign': 'center',
                'fontWeight': 'bold',
                'backgroundColor': '#eccc68',
                'border': '1px solid black'
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248'},
                # {'if': {'row_index': 'even'}, 'backgroundColor': '#f7d794'},
                # {'if': {'filter_query': '{media_type} = Photo'}, 'backgroundColor': '#f7d794'}
            ],

            # style_cell is for both header and data
            style_cell={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'height': 'auto',
                'minWidth': '5px', 'width': '10px', 'maxWidth': '20px',
                'whiteSpace': 'normal',
                'font-family': 'raleway'
            },
            tooltip_data=[{
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in posts_df.to_dict('records')
            ],
            tooltip_duration=None,
            style_cell_conditional=[
                {'if': {'column_id': 'message'}, 'width': '65%', 'textAlign': 'left'},
                {'if': {'column_id': 'created_time'}, 'width': '10%', 'textAlign': 'center'},
                {'if': {'column_id': 'media_type'}, 'width': '10%', 'textAlign': 'center'},
                {'if': {'column_id': 'admin_creator'}, 'width': '15%', 'textAlign': 'center'},
            ],
        ))
    ])


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def display_ticker_plot(code):
    df = pdr.get_data_yahoo(code, start='2015-01-01')
    df['mid'] = (df['High'] + df['Low']) / 2

    plot = go.Scatter(x=df.index, y=df['mid'], name='Historical', line=dict(color='#2ed573'), opacity=1)
    layout = dict(title='Forecast Visualisation', yaxis=dict(title='Price', showgrid=True), plot_bgcolor='#535c68')
    fig = dict(data=plot, layout=layout)

    graph = dcc.Graph(
        id='first_plot',
        figure={
            'data': [
                {'x': df.index, 'y': df.mid, 'type': 'line', 'name': code}],
            'layout': {
                'title': code.upper()
            }})

    return graph


layout = html.Div([
    html.Div(children=html.H1(html.Center('Facebook Page Analytics'))),
    # html.Div(children='Symbol TO Graph'),
    # dcc.Input(id='input', value='SEKINR=X', type='text'),
    # html.Div(id='output-graph'),

    yo,
    yo2,
    plot_fb_impressions(client_id=client_id_),
    display_media_type_numbers(posts_df=list_of_posts_df),
    display_recent_posts_table(posts_df=list_of_posts_df),
])


# html.Div(children='Symbol TO Graph'),
# dcc.Input(id='input', value='SEKINR=X', type='text'),
# html.Div(id='output-graph'),
# display_likes_meter(client_id=client_id_),
# children = [  # plot_fb_likes(client_id=client_id_),
# likes_meter_with_plot(client_id=client_id_),
# plot_fb_impressions(client_id=client_id_),
# html.Div(children='In the last 7 days')]
# children += display_media_type_numbers(client_id=client_id_)
#
# layout = html.Div(children=children)

def display_likes_meter(client_id):
    likes_recent, likes_month_ago = get_lifetime_likes_meter_values(client_id=client_id)
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=likes_recent,
        domain={'row': 0, 'column': 1}))
    fig.update_layout(
        grid={'rows': 2, 'columns': 2, 'pattern': "independent"},
        template={'data': {'indicator': [{
            'title': {'text': "Likes<br><span style='font-size:0.8em;color:gray'>& gain in 1 month</span>"},
            'mode': "number+delta+gauge",
            'delta': {'reference': likes_month_ago}}]
        }})
    graph = dcc.Graph(figure=fig, responsive=True)
    return graph


def plot_fb_likes(client_id):
    likes_column = 'lifetime_total_likes'
    df = plot_df(client_id, column=likes_column)
    plot = go.Scatter(x=df.index, y=df[likes_column], line=dict(color='#eccc68'), opacity=1)
    layout_ = dict(title='Likes', yaxis=dict(title='', showgrid=True))
    fig = dict(data=[plot], layout=layout_)
    graph = dcc.Graph(figure=fig, responsive=True)
    return graph
