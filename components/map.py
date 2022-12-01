import plotly.express as px
import pandas as pd
import requests
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import sys
sys.path.insert(0, 'data')
from loader import load_monthly_with_unemployment, load_corr_reg_table


def india_map(corr_gas='aqi'):
    in_outline = requests.get('https://raw.githubusercontent.com/mickeykedia/India-Maps/master/India_Administrative_Maps/country/india_country.geojson')

    dfm = load_monthly_with_unemployment()
    grp = dfm.groupby('city')[['aqi']].mean()
    grp['City'] = grp.index
    grouped = grp.reset_index(drop=True)
    raw = pd.read_csv("../data/refs/in_coords.csv")
    raw['City'] = raw['City'].replace({'Vijaywada':'Vijayawada', 'Pondicherry':'Puducherry'})
    df_coords = pd.merge(grouped, raw, how='left', on='City')
    
    df = df_coords.copy()
    df['id'] = df.index

    fig = px.scatter_mapbox(df,
                            lat="center1", # latitude from df
                            lon="center2", # longitude from df
                            color=corr_gas, # color if based on df column
                            hover_name='City',
                            zoom=2.75,
                            mapbox_style='carto-positron',#white-bg
                            height=500,
                            width=700,
                            title=f'Mean AQI by City (2018-2022)',
                            color_continuous_scale='turbo',
                            )
    fig.update_layout(mapbox={'layers':[{
                                        'source':in_outline.json(), # India Country outline in geoJSON
                                        'type':'line',
                                        'color':'black',
                                        "line": {"width": 0.65},
                            }]},
                    )

    return fig


def corr_table(city='Agartala'):
    tab = load_corr_reg_table(city)
    dashtab = dash_table.DataTable(tab.to_dict('records'), [{"name": i, "id": i} for i in tab.columns], id='corr-table',
                                    style_table={'width':'40%', 'display':'inline-block'})

    return dashtab


def add_map_filter():
    raw = pd.read_csv("data/in_coords.csv")
    raw['City'] = raw['City'].replace({'Vijaywada':'Vijayawada', 'Pondicherry':'Puducherry'})
    city_list = raw['City'].unique()
    city_list.sort()
    return html.Div([
                    html.Div([ # dropdown and title
                    html.H4(children='City:'),
                    dcc.Dropdown(city_list,
                                'Agartala',
                                placeholder='Select City',
                                id='map-city-filter-value',
                                maxHeight=100)
                ], style={'width': '25%', 'float': 'left', 'display':'inline-block'})
    ], style={'padding':'5px'})


def build_map(map, table):
    return html.Div([
                html.Br(),
                html.Br(),
                html.Br(),
                html.Div(
                    id='core-map',
                    children=[
                        html.Div([dcc.Graph(id='choropleth-1', figure=map)], style={'display': 'inline-block'}),
                        html.Div([dbc.Container([
                                                dbc.Label('Correlation with Unemployment', style={'font-size':'24px'}),
                                                dcc.Loading([table]),
                                                dbc.Label(r'*Interpret coefficients: an increase of 1 unit of gas results in a coefficient % change in unemployment', style={'font-size':'10px'})
                                                ], id='corr-table-container')], style={'display': 'inline-block', 'float':'right'})
                    ]
                )
            ])