# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
import requests
import pickle
from components.base import build_tabs, build_nav
from components.historic import add_hist_filters, add_hist_timeline, build_hist_graphic
from components.map import india_map, build_map, corr_table, add_map_filter
from components.matrix import build_city_matrix, build_matrix_fig, add_matrix_filters
from components.covid import build_covid_graphic, add_covid_gas_filters, build_covid_fig
#from data.loader import load_monthly_with_unemployment, load_grouped_covid_pollution

################################################

## APP INSTANTIATION AND VARIABLES ##

app = Dash(__name__)
app.config.suppress_callback_exceptions=True

covid_df = pickle.load(open('data/covid_grouped.pkl', 'rb'))

df = pickle.load(open('data/month_unemploy.pkl', 'rb'))
DEFAULT_CITY = 'Agartala'
DEFAULT_GAS = 'CO'
THEME = px.colors.qualitative.Plotly
in_outline = requests.get('https://raw.githubusercontent.com/mickeykedia/India-Maps/master/India_Administrative_Maps/country/india_country.geojson')

default_df = df[df['city'] == DEFAULT_CITY]

fig = px.line(default_df, x="date", y="co", color='city', title=f'{DEFAULT_GAS} Levels', color_discrete_sequence=THEME) # add color to be from city dropdown multi select

#########################################
################ LAYOUT #################
#########################################

app.layout = html.Div(className="app-header m-5",
    children=[
    build_nav(),
    html.H1(children='Pollution and Economic Growth Levels in India', id='page-title', style={'padding':'5px'}),
    build_tabs(),

    html.Div(
        id='tab-core',
        children=[
            add_hist_filters(df, default_city=DEFAULT_CITY, default_df=default_df),
            #build_map(map),
            build_hist_graphic(),
            add_hist_timeline(df),
        ]
    )#,html.Div('Copyright © Ty Martz 2022', style={'align-text': 'center'})
])



#########################################
############### CALLBACKS ###############
#########################################


#### UPDATING TAB 1 WHEN FILTERS CHANGE ####

@app.callback(
    Output(component_id='line-graph', component_property='figure'),
    Output(component_id='aqi-value', component_property='children'),
    Input(component_id='city-filter-value', component_property='value'),
    Input(component_id='gas-filter-value', component_property='value'),
    Input(component_id='year-filter', component_property='value')
)
def update_line_graph(input_city, input_gas, input_year):
    df2 = df.copy()
    if input_city is None:
        title_city = 'India'
        fig = px.line(default_df[default_df['city'] == 'Beverly'], x="date", y="co", color='city', title=f'{DEFAULT_GAS} Levels')
        mean_aqi = 'NA'
        return fig, mean_aqi
    else:
        input_list = list(input_city)
        if len(input_list) == 1:
            title_city = input_list[0]
        else:
            title_city = 'India'
        filt = df2[(df2['city'].isin(input_list)) & (df2['year'] <= input_year)]
        mean_aqi = round(np.mean(filt['aqi']), 4)
        fig = px.line(filt, x="date", y=input_gas.lower(), color="city", title=f'{input_gas} levels in {title_city}', color_discrete_sequence=THEME)
        fig.update_layout(transition_duration=500, yaxis_title=input_gas)
    
        return fig, mean_aqi


#### SWITCHING TABS ####

@app.callback(
    Output(component_id='tab-core', component_property='children'),
    Input(component_id='app-tabs', component_property='value')
)
def render_tab(tab):
    if tab == 'hist':
        return html.Div(
                        id='tab-core',
                        children=[
                            add_hist_filters(df, default_city=DEFAULT_CITY),
                            #build_map(map),
                            build_hist_graphic(),
                            add_hist_timeline(df)
                        ]
                    )
    elif tab == 'matrix':
        scat, matrix_df = build_matrix_fig()
        return html.Div(
                        id='tab-core',
                        children=[
                            add_matrix_filters(matrix_df),
                            build_city_matrix(scat)
                        ]
                    )
    elif tab == 'map-corr':
        map = india_map()
        table = corr_table(DEFAULT_CITY)
        return html.Div(
                        id='tab-core',
                        children=[
                            add_map_filter(),
                            build_map(map, table)
                        ]
                    )
    elif tab == 'covid':
        return html.Div(
                        id='tab-core',
                        children=[
                            add_covid_gas_filters(),
                            build_covid_graphic()
                        ]
                    )
    else:
        return html.H1(children='Missing Chart', id='missing-msg')

#### Updating TAB 2 FILTERS ####

@app.callback(
    Output(component_id='scatter-matrix', component_property='figure'),
    Input(component_id='quarter-filter-value', component_property='value'),
    Input(component_id='gas-filter-value-matrix', component_property='value'),
    Input(component_id='matrix-city-filter-value', component_property='value')
)
def update_matrix(input_quarter, input_gas, input_city):
    fig, _ = build_matrix_fig(input_quarter, input_gas, city_choice=input_city)
    fig.update_layout(transition_duration=500)

    return fig


#### Updating TAB 3 FILTERS ####

@app.callback(
    Output(component_id='corr-table-container', component_property='children'),
    Input(component_id='map-city-filter-value', component_property='value')
)
def update_map(city):
    corrtab = corr_table(city)
    items = [
            dbc.Label('Correlation with Unemployment', style={'font-size':'24px'}),
            dcc.Loading([corrtab]),
            dbc.Label(r'*Interpret coefficients: an increase of 1 unit of gas results in a coefficient % change in unemployment', style={'font-size':'10px'})
            ]
    return items

#### Updating TAB 4 COVID FILTERS ####

@app.callback(
    Output(component_id='covid-graph', component_property='figure'),
    Input(component_id='covid-gas-filter', component_property='value')
)
def update_covid(input_gas):
    cov_grp = covid_df.copy()
    fig = build_covid_fig(cov_grp, input_gas)
    fig.update_layout(transition_duration=500)

    return fig

#########################################################################

if __name__ == '__main__':
    app.run_server(debug=True)