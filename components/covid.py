from dash import html, dcc
#import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def build_covid_fig(df, gas='CO'):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['New_cases'], name="cases"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df['date'], y=df[f'{gas.lower()}_api'], name="gas"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text=f"Covid Cases vs. Mean {gas} Levels Across India"
    )

    # Set axes
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text="COVID-19 Cases", secondary_y=False)
    fig.update_yaxes(title_text=f"{gas} Levels", secondary_y=True)
    fig.update_layout(
        yaxis=dict(
        title=f"{gas} Levels",
        titlefont=dict(
            color="#1f77b4"
        ),
        tickfont=dict(
            color="#1f77b4"
        )
        )
    )

    return fig


def build_covid_graphic():
    return html.Div([
                html.Br(),
                html.Div(
                    id='core-graphic',
                    children=[dcc.Graph(id='covid-graph')]
                )
            ])

def add_covid_gas_filters():
    return html.Div([ # entire section
            html.Div( # pollutant radios
                children=[
                html.H4(children='Pollutant:'),
                dcc.RadioItems(['CO', 'NO2', 'SO2', 'PM2.5'],
                                'CO',
                                id='covid-gas-filter',
                                className='btn-group',
                                inputClassName='btn-check',
                                labelClassName='btn btn-outline-primary')
                         ], style={'width': '25%', 'float': 'center', 'display': 'inline-block'}
            )], style={'padding':'5px'})