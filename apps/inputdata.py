import dash     # need Dash version 1.21.0 or higher
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import dcc, html

import pandas as pd
import plotly.express as px
import pymongo
from pymongo import MongoClient
from bson import ObjectId


# Connect to local server
client = MongoClient("mongodb://127.0.0.1:27017/")
# Create database called animals
mydb = client["Penjualan"]
# Create Collection (table) called shelterA
collection = mydb.DataPenjualan222

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# app = dash.Dash(__name__, suppress_callback_exceptions=True,
#                 external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

layout = html.Div([

    html.Div([
        # html.Img(src=app.get_asset_url('user.png'), style={'position': 'relative', 'width': '35px', 'left':'900px', 'top':'15px'}),
        dbc.NavLink("Dashboard", href="/apps/main", id='menumain', style={'color': 'black'}),
        dbc.NavLink("Input Data", href="/apps/inputdata", id='input_data', style={'color': 'black'}),
        # dbc.NavLink("tambah data", href="/apps/tambahdata", id='tambah_data', style={'color': 'black'}),
        # dbc.NavLink("Logout", href="/apps/login", id='login'),
        # html.H6("Logout")
    ], className='header'),

    html.Div([
        html.Label('PT. Pelita Terang Makmur merupakan sebuah perusahaan yang bergerak pada bidang distributor makanan, yang dimana memiliki beberapa cabang di area sulselbar dan sulawesi tenggara' , style={'position': 'relative',  'width' : '80%', 'text-align' : 'justify', 'color' : 'white', 'left': '30px', 'top': '300px'}),
        html.Label('Silahkan upload file data penjualan disini (format file .csv)' , style={'position': 'relative',  'width' : '80%', 'text-align' : 'justify', 'color' : 'white', 'left': '31px', 'top': '30px', 'font-size' : '12px'}),
        html.Img(src=app.get_asset_url('imgside.png'), style={'position': 'relative', 'width': '110%', 'left': '-15px', 'top': '320px'}),
        html.Hr(id='hrside', style={'position': 'relative', 'color' : 'white', 'width': '80%', 'height': '2px', 'left': '30px', 'top': '-165px'})
        # html.H1(children='ADMIN', style={'font-size':'17px'}),
    ], className='side_bar'),

    html.Div([
        html.Div([

            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children= dbc.Button("Upload File", outline=True, color="warning", className="me-1",  id='uploadinput'),
                    multiple=True
                )
            ]),

            html.Div([], className='boxinput'),
            html.Div([
                    html.H2("Data Penjualan", id='labelinput'),
                    html.Hr(id='hrinput')
            ]),

            html.Div([], className='boxtabelinput'),

            html.Div(id='datatable_inputdata', children=[]),

            # activated once/week or when page refreshed
            dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),

            html.Div(
                        [
                            dbc.Button("Simpan", color="primary", className="me-1", id="save-it"),
                            dbc.Button("Tambah Data", color="danger", className="me-1", id='adding-rows-btn', n_clicks=0),
                            dbc.Button("Download", color="info", className="me-1", id="btn"),
                            dcc.Download(id="download-component"),
                        ], className="buttoninput"
                    ),

            html.Div(id="show-graphs", children=[]),
            html.Div(id="placeholder")


        ])
    ])
  
])

# Display Datatable with data from Mongo database *************************
@app.callback(Output('datatable_inputdata', 'children'),
              [Input('interval_db', 'n_intervals')])
def populate_datatable(n_intervals):
    print(n_intervals)
    # Convert the Collection (table) date to a pandas DataFrame
    df = pd.DataFrame(list(collection.find()))
    #Drop the _id column generated automatically by Mongo
    df = df.iloc[:, 1:]

    return [
        dash_table.DataTable(
            id='my-table',
            columns=[{
                'name': x,
                'id': x,
            } for x in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            filter_options={"case": "sensitive"},
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_current=0,  # page number that user is on
            page_size=6,  # number of rows visible per page
            virtualization=True,
            style_cell={'textAlign': 'left',
                        'min-width': '100px',
                        'backgroundColor': '#425C5A',
                        'color': '#FEFEFE',
                        'border-bottom': '0.01rem solid #19AAE1'},
            style_header={'backgroundColor': '#425C5A',
                        'fontWeight': 'bold',
                        'font': 'Poppins',
                        'color': 'orange',
                         'border': '#425C5A'},
            style_as_list_view=True,
            style_data={'styleOverflow': 'hidden', 'color': 'white'},
            fixed_rows={'headers': True},
        #     style_cell={'textAlign': 'left', 'minWidth': '100px',
        #                 'width': '100px', 'maxWidth': '100px'},
        )
    ]


# Add new rows to DataTable ***********************************************
@app.callback(
    Output('my-table', 'data'),
    [Input('adding-rows-btn', 'n_clicks')],
    [State('my-table', 'data'),
     State('my-table', 'columns')],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


# Save new DataTable data to the Mongo database ***************************
@app.callback(
    Output("placeholder", "children"),
    Input("save-it", "n_clicks"),
    State("my-table", "data"),
    prevent_initial_call=True
)
def save_data(n_clicks, data):
    dff = pd.DataFrame(data)
    collection.delete_many({})
    collection.insert_many(dff.to_dict('records'))
    return ""

@app.callback(
    Output("download-component", "data"),
    Input("btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    # return dict(content="Always remember, we're better together.", filename="hello.txt")
    return dcc.send_data_frame(df.to_csv, "data_penjualan.csv")
    # return dcc.send_data_frame(df.to_excel, "mydf_excel.xlsx", sheet_name="Sheet_name_1")
    # return dcc.send_file("./assets/data_file.txt")
    # return dcc.send_file("./assets/bees-by-Lisa-from-Pexels.jpg")

