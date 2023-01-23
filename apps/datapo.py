import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
# from app import app

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div([

    html.Div([
        html.Img(src=app.get_asset_url('user.png'), style={'position': 'relative', 'width': '35px', 'left':'900px', 'top':'15px'}),
        dbc.NavLink("Dashboard", href="/apps/main", id='menumain'),
        # dbc.NavLink("Pre Order", href="/apps/po", id='menupo'),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Pre Order", href="/apps/po"),
                dbc.DropdownMenuItem("Delivered Order", href="/apps/do"),
                dbc.DropdownMenuItem("Upload File", href="/apps/upload"),
            ],
            nav=True,
            in_navbar=True,
            label="Input Data",
            id='menupo',
        ),
        dbc.NavLink("Data PO", href="/apps/datapo", id='datapo'),
        dbc.NavLink("Logout", href="/apps/login", id='login'),
        # html.H6("Logout")
    ], className='header'),

    html.Div([
        # html.Img(src=app.get_asset_url('login5.png'), style={'position': 'relative', 'width': '35%', 'left': '50px', 'top': '40px'}),
        # html.H1(children='ADMIN', style={'font-size':'17px'}),
    ], className='side_bar'),
    
    html.Div([
        html.Div([
            html.Div([], className='boxpo'),
             html.Div([
                    html.H2("Data Permintaan Barang"),
                    html.Hr(id='hrpo')
            ]),
        ], className='main'),
    ]),    
])

