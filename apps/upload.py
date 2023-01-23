import base64
import datetime
import io

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

import pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
import json
# from app import app

client = pymongo.MongoClient("mongodb://localhost:27017")

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
    ], className='header'),

    html.Div([
        # html.Img(src=app.get_asset_url('login5.png'), style={'position': 'relative', 'width': '35%', 'left': '50px', 'top': '40px'}),
        # html.H1(children='ADMIN', style={'font-size':'17px'}),
    ], className='side_bar'),
    
    html.Div([
        html.Div([
            html.Div([], className='boxup'),
            html.Div([
                    html.H2("Upload File"),
                    html.Hr(id='hrup')
            ]),

            html.Div([ # this code section taken from Dash docs https://dash.plotly.com/dash-core-components/upload
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
                html.Div(id='output-div'),
                html.Div(id='output-datatable'),
            ])
               
        ], className='main'),
    ]),    
])



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        
        # Import to MongoDB
        data = df.to_dict(orient = "records")
        db = client["Datacoba"]
        db.data.insert_many(data)
        df = pd.DataFrame(list(db.data.find()))
        # Convert id from ObjectId to string so it can be read by DataTable
        df['_id'] = df['_id'].astype(str)
        print(df.head(20))

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.P("Inset X axis data"),
        dcc.Dropdown(id='xaxis-data',
                     options=[{'label':x, 'value':x} for x in df.columns]),
        html.P("Inset Y axis data"),
        dcc.Dropdown(id='yaxis-data',
                     options=[{'label':x, 'value':x} for x in df.columns]),
        html.Button(id="submit-button", children="Create Graph"),
        html.Hr(),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15
        ),
        dcc.Store(id='stored-data', data=df.to_dict('records')),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])





