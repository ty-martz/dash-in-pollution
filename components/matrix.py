from dash import html, dcc
import numpy as np
import plotly.express as px
import sys
sys.path.insert(0, 'data')
from loader import load_quarterly_change_with_unemployment

def build_matrix_fig(quarter='Q2-2022', pollutant='CO', city_choice=None, df=load_quarterly_change_with_unemployment()):
    df1 = df[df['quarter_string'] == quarter]
    fig = px.scatter(df1, x='unemployment_change', y=f'diff_{pollutant.lower()}_api', hover_name='city', title=f'Changes in {pollutant} levels and Unemployment by City',
                        labels={
                            f'diff_{pollutant.lower()}_api':f'{pollutant} % Change',
                            'unemployment_change': 'Unemployment % Change'
                        },
                        )
    xlim = np.max(np.abs(df1['unemployment_change']))*1.05
    ylim = np.max(np.abs(df1[f'diff_{pollutant.lower()}_api']))*1.05
    fig.update_xaxes(range=[-xlim,xlim])
    fig.update_yaxes(range=[-ylim,ylim])
    fig.add_vline(x=0, line_color='black', line_width=2)
    fig.add_hline(y=0, line_color='black', line_width=2)

    # highlight specific city
    if city_choice is not None:
        cdf = df1[df1['city'] == city_choice]
        fig.add_scatter(x=cdf['unemployment_change'], y=cdf[f'diff_{pollutant.lower()}_api'],
                        marker={'symbol':'star', 'color':'red', 'size':15},
                        showlegend=False,
                        )

    return fig, df

def build_city_matrix(fig):
    return html.Div([
                html.Br(),
                html.Div(
                    id='core-graphic',
                    children=[dcc.Graph(id='scatter-matrix', figure=fig)]
                )
            ])

def add_matrix_filters(df, default_df=None):
    if default_df is None:
        default_df = df.copy()
    return html.Div([ # entire section
            html.Div([ # dropdown and title
                html.H4(children='Date:'),
                dcc.Dropdown(df['quarter_string'].unique(),
                            list(df['quarter_string'].unique())[0],
                            placeholder='Select Date',
                            id='quarter-filter-value',
                            maxHeight=100)
            ], style={'width': '25%', 'float': 'left', 'display':'inline-block'}),
            html.Div([ # city_filter
                html.H4(children='City:'),
                dcc.Dropdown(df['city'].unique(),
                            placeholder='Select City',
                            #multi=True,
                            id='matrix-city-filter-value',
                            maxHeight=100)
            ], style={'width': '25%', 'float': 'left', 'display':'inline-block'}),
            html.Div( # pollutant radios
                children=[
                html.H4(children='Pollutant:'),
                dcc.RadioItems(['CO', 'NO2', 'SO2', 'PM2.5'],
                                'CO',
                                id='gas-filter-value-matrix',
                                className='btn-group',
                                inputClassName='btn-check',
                                labelClassName='btn btn-outline-primary')
                         ], style={'width': '25%', 'float': 'center', 'display': 'inline-block'}
            )], style={'padding':'5px'})
