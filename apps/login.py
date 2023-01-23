import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from app import app

# app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div([
    html.Div([], className='loginpage'),
    html.Div([
        html.H3("PTM User Login", id='loginlabel'),
        html.Hr(id='hrlogin')
    ]),

    html.Div([
        html.H5("Username", id="username")
    ]),

    html.Div([
        dbc.Input(id="inputuser", placeholder="Username", type="text"),
        html.Br(),
        html.P(id="output"),
    ], className='input'),

     html.Div([
        html.H5("Password", id="password")
    ]),

    html.Div([
        dbc.Input(id="inputpass", placeholder="Password", type="text"),
        html.Br(),
        # html.P(id="output"),
    ], className='input'),

    html.Div([
        dbc.Button("Login", href="/apps/main", color="primary", id='buttonlogin', className="me-1")
    ])

])

