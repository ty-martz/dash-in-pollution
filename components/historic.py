from dash import html, dcc
import numpy as np

def add_hist_filters(df, default_city, default_df=None):
    if default_df is None:
        default_df = df.copy()
    return html.Div([ # entire section
            html.Div([ # dropdown and title
                html.H4(children='City (Multi-Select):'),
                dcc.Dropdown(df['city'].unique(),
                            placeholder='Choose 1 or more cities',
                            id='city-filter-value',
                            multi=True,
                            maxHeight=100)
            ], style={'width': '25%', 'float': 'left', 'display':'inline-block'}),
            html.Div( # KPI Card
                id='aqi-kpi',
                style={'float': 'right', 'width':'20%'},
                className="card text-white bg-primary mb-3",
                children=[
                    html.Div(className='card-header', children=['Mean AQI'], style={'font-size':'26px', 'text-align':'center'}),
                    html.Div(className='card-body', children=[
                        html.H4(id='aqi-value', className='card-title', children=round(np.mean(default_df['aqi']), 2), style={'text-align':'center'})
                    ])
                ]
            ),
            html.Div( # pollutant radios
                children=[
                html.H4(children='Pollutant:'),
                dcc.RadioItems(['CO', 'NO2', 'SO2', 'PM2.5'],
                                'CO',
                                id='gas-filter-value',
                                className='btn-group',
                                inputClassName='btn-check',
                                labelClassName='btn btn-outline-primary')
                         ], style={'width': '25%', 'float': 'center', 'display': 'inline-block'}
            )], style={'padding':'5px'})

def add_hist_timeline(df):
    return html.Div([
            html.H4(children='Date Range'),
            # TODO: update to filter to drag from both sides
            dcc.Slider(min=df['year'].min(),
                       max=df['year'].max(),
                       marks={str(year):str(year) for year in df['year'].unique()},
                       value=df['year'].max(),
                       id='year-filter')], style={'width': '100%', 'float': 'center'})

def build_hist_graphic():
    return html.Div([
                html.Br(),
                html.Div(
                    id='core-graphic',
                    children=[dcc.Graph(id='line-graph')]
                )
            ])