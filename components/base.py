from dash import html, dcc
import dash_bootstrap_components as dbc

def build_nav():
    return dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Home", active=True, href="#", style={'height':'40px'}), style={'height':'40px'}),
                dbc.NavItem(dbc.NavLink("Author", href="https://ty-martz.github.io/", target='_blank', style={'height':'40px'}), style={'height':'40px'}),
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem("Georgia Tech", href="https://pe.gatech.edu/degrees/analytics", target='_blank', style={'height':'40px'}),
                        dbc.DropdownMenuItem("MacroX Studio", href="https://www.macroxstudio.com/", target='_blank', style={'height':'40px'})
                    ],
                    label="Project Sponsors",
                    nav=True,
                    style={'height':'40px'}
                ),
            ],
            className="navbar navbar-expand-lg navbar-dark bg-primary fixed-top",
            style={'top':0, 'margin-bottom':'10px', 'height':'40px', 'padding':'5px'}
        )

def build_tabs():
    return html.Div(
                    id="tabs",
                    className="nav-div",
                    style={'height':'60px', 'background-color': '#272b30'},
                    children=[
                        dcc.Tabs(
                            id="app-tabs",
                            value="hist",
                            className="custom-tabs nav nav-tabs",
                            style={'height':'60px', 'backgroundColor':'#272b30'},
                            children=[
                                dcc.Tab(
                                    id="hist-tab",
                                    label="Historic Data",
                                    value="hist",
                                    className="nav-item nav-link",
                                    selected_className="custom-tab--selected",
                                    style={'height':'60px', 'backgroundColor':'#3a3f44'},
                                    selected_style={'height':'60px', 'backgroundColor':'#7a8288', 'borderTop': '1px solid #19D3F3', 'color':'#19D3F3'}
                                ),
                                dcc.Tab(
                                    id="matrix-tab",
                                    label="City Pollution + Growth",
                                    value="matrix",
                                    className="custom-tab nav-item nav-link",
                                    selected_className="custom-tab--selected",
                                    style={'height':'60px', 'backgroundColor':'#3a3f44'},
                                    selected_style={'height':'60px', 'backgroundColor':'#7a8288', 'borderTop': '1px solid #19D3F3', 'color':'#19D3F3'}
                                ),
                                dcc.Tab(
                                    id="map-tab",
                                    label="Correlations by City",
                                    value="map-corr",
                                    className="custom-tab nav-item nav-link",
                                    selected_className="custom-tab--selected",
                                    style={'height':'60px', 'backgroundColor':'#3a3f44'},
                                    selected_style={'height':'60px', 'backgroundColor':'#7a8288', 'borderTop': '1px solid #19D3F3', 'color':'#19D3F3'}
                                ),
                                dcc.Tab(
                                    id="covid-tab",
                                    label="COVID Analysis",
                                    value="covid",
                                    className="custom-tab nav-item nav-link",
                                    selected_className="custom-tab--selected",
                                    style={'height':'60px', 'backgroundColor':'#3a3f44'},
                                    selected_style={'height':'60px', 'backgroundColor':'#7a8288', 'borderTop': '1px solid #19D3F3', 'color':'#19D3F3'}
                                ),
                            ],
                        )
                    ],
    )