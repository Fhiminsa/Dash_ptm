import base64
import datetime
import io

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table as dt
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

import pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt

from app import app

# Connect to your app pages
client = pymongo.MongoClient("mongodb://localhost:27017")
# Create database called animals
mydb = client["Penjualan"]
# Create Collection (table) called shelterA
collection = mydb.DataPenjualan222

df = pd.DataFrame(list(collection.find()))
sales = df[['order_date', 'sales_no', 'gudang','prov', 'kota', 'kec', 'stock_name','brand', 'qty', 'unit', 'in_pcs', 'in_ctn', 'total', 'driver', 'helper1']]
print(sales.head(5))

year_sale = df['tahun'].unique()

nama_prod = df[['order_date', 'tahun', 'sales_no', 'gudang','prov', 'kota', 'kec', 'stock_name','brand', 'qty', 'unit', 'in_pcs', 'in_ctn', 'total', 'driver', 'helper1']]
nama_prod = nama_prod[(nama_prod['brand'] == 'VITASARI')]
produk = nama_prod['stock_name'].unique()

month_list = list(df['bulan'].unique())

provinsi = df['prov'].unique()
gudang = df['gudang'].unique()

# -------------------------------------App----------------------------------------------------------------------------

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div([

    html.Div([
        # html.Img(src=app.get_asset_url('user.png'), style={'position': 'relative', 'width': '35px', 'left':'900px', 'top':'15px'}),
        dbc.NavLink("Dashboard", href="/apps/main", id='menumain', style={'color': 'black'}),
        dbc.NavLink("Input Data", href="/apps/inputdata", id='input_data', style={'color': 'black'}),
        dbc.NavLink("tambah data", href="/apps/tambahdata", id='tambah_data', style={'color': 'black'}),
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
                html.Img(src=app.get_asset_url('jumbotron.png'), style={'width':'910px','height':'600px','border-radius':'20px 20px 0 0'})
            ], className='jumbotron'),
            html.Div([], className='bg-color'),
            html.Div([], className='box1vit'),

            html.Div([
                html.Img(src=app.get_asset_url('LogoPTM.png'), style={'width':'160px'}),
                html.H3("PT.PELITA TERANG MAKMUR", id='ptm', style={'font-family':'Poppins'})
            ], className='logovit'),



            html.Div([], className='boxvitarasa'),
            html.H4("VITASARI", id='labelvitarasa'),

            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children= dbc.Button("Upload File", outline=True, color="warning", className="me-1",  id='upload2'),
                    multiple=True
                )
            ]),

            html.Div([
                html.Div([], className='box5'),
                html.Div([], className='box6'),
                html.Div([
                    html.P('Pilih Tahun Penjualan : ', id = 'tahun_penj')
                ]),
                html.Div([
                    html.P('Pilih Jenis Produk : ', id = 'jenis_prod')
                ]),

                html.Div([
                    dcc.Dropdown(id='select_years',
                        value='2021',
                        options=[{'label':x, 'value':x} for x in year_sale]),
                ], id = 'yaxis-data'),

                html.Div([
                    dcc.Dropdown(id='select_produk',
                        value='vitarasa bawang  5 kg',
                        options=[{'label':x, 'value':x} for x in produk]),
                ], id = 'product-brand'),
            ], className='pilih'),

            html.Div([], className='boxvitarasa2'),
            html.Div([
                dcc.Graph(id = 'histogram_vitarasa', config={'displayModeBar': 'hover'})
            ], id = 'Histogram_vitarasa'),
            
            html.Div([], className='boxvitarasa4'),
            html.Div([
                dcc.Dropdown(id='select_prov',
                    value='Sulawesi Selatan',
                    options=[{'label':x, 'value':x} for x in provinsi]),
            ], id = 'provinsi_vitarasa'),

            html.Div([
                dcc.Graph(id = 'histogram_vitarasa2', config={'displayModeBar': 'hover'})
            ], id = 'Histogram_vitarasa2'),

            html.Div([
                html.P('Pilih Bulan Penjualan : ', id = 'bulan_penj'),
                
                html.Div([
                    dcc.Dropdown(id='select_month',
                        value=1,
                        options=[{'label':x, 'value':x} for x in month_list]),
                ], id = 'pilih_bulan'),

            ], className = "dropdown_month"),

            html.Div([], className='boxvitarasa3'),
            html.Div([
                dcc.Graph(id = 'barchart_vitarasa', config={'displayModeBar': 'hover'},
                      style={'height': '480px'})

            ], id = 'BarChart_vitarasa'),

             html.Div([], className='boxvitarasa5'),

            html.Div([
                dcc.Graph(id = 'pie_chartvit', config={'displayModeBar': 'hover'},
                        style={'height': '500px'})

            ], id = 'PieChart_vit'),

        ], className='main'),

        html.Div([], className='boxvitarasa1'),
            html.Div(id='datatable_vitarasa', children=[]),

            # activated once/week or when page refreshed
            dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),

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
        
        data = df.to_dict(orient = "records")
        db = client["Penjualan"]
        db.DataPenjualan.insert_many(data)

        df = pd.DataFrame(list(db.data.find()))
        # Convert id from ObjectId to string so it can be read by DataTable
        df['_id'] = df['_id'].astype(str)
        print(df.head(20))
        
        df.drop_duplicates(subset='Nama', keep='first', inplace=True)
        print(df)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

# ------------------------------------ LINE CHART -----------------------------------------------------

    

# ----------------------------------------Akhir LineChart----------------------------------------------------------------


# ----------------------------------------Callback----------------------------------------------------------------
@app.callback(Output('datatable_vitarasa', 'children'),
              [Input('interval_db', 'n_intervals')],
              [Input('select_years','value')],
              [Input('select_produk','value')])
def populate_datatable(n_intervals, select_years, select_produk):
    print(n_intervals)
    # Convert the Collection (table) date to a pandas DataFrame
    sales = df[['order_date', 'tahun', 'sales_no', 'gudang','prov', 'kota', 'kec', 'stock_name','brand', 'qty', 'unit', 'in_pcs', 'in_ctn', 'total', 'driver', 'helper1']]
    data_table = sales[(sales['tahun'] == select_years) & (sales['brand'] == 'VITASARI') & (sales['stock_name'] == select_produk)]

    return [
        dt.DataTable(
            id='my-table',
            columns=[{
                'name': x,
                'id': x,
            } for x in sales.columns],
            data=data_table.to_dict('records'),

            virtualization=True,
            style_cell={'textAlign': 'left',
                        'min-width': '100px',
                        'backgroundColor': '#425C5A',
                        'color': '#FEFEFE',
                        'border-bottom': '0.01rem solid #19AAE1'},
            style_header={'backgroundColor': '#425C5A',
                        'fontWeight': 'bold',
                        'font' : 'Poppins',
                        'color': 'orange',
                         'border': '#425C5A'},
            style_as_list_view=True,
            style_data={'styleOverflow': 'hidden', 'color': 'white'},
            fixed_rows={'headers': True},
            sort_action='native',
            sort_mode='multi'

        )
    ]

@app.callback(Output('histogram_vitarasa', 'figure'),
              [Input('select_years','value')],
              [Input('select_produk','value')])
def update_graph(select_years,select_produk):
    sales11 = df.groupby(['tahun', 'bulan', 'stock_name'])['total'].sum().reset_index()
    sales12 = sales11[(sales11['tahun'] == select_years) & (sales11['stock_name'] == select_produk)][['tahun', 'bulan', 'stock_name','total']].reset_index()

    return {
        'data': [go.Bar(
            x=sales12['bulan'].tail(30),
            y=sales12['total'].tail(30),
            name='Total Penjualan Perbulan',
            marker=dict(color='#18B3A7'),
            hoverinfo='text',
            hovertext=
            '<b>Bulan</b>: ' + sales12['bulan'].tail(30).astype(str) + '<br>' +
            '<b>Total Penjualan</b>: ' + [f'{x:,.0f}' for x in sales12['total'].tail(30)] + '<br>' +
            '<b>Tahun</b>: ' + sales12['tahun'].tail(30).astype(str) + '<br>'


        )],
    
        'layout': go.Layout(
            title={'text': 'Total Penjualan Perbulan pada Tahun  ' + (select_years),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': '#425C5A',
                       'size': 20},
            font=dict(family='Poppins',
                      color='black',
                      size=12),
            hovermode='closest',
            paper_bgcolor='white',
            plot_bgcolor='white',
            legend={'orientation': 'h',
                    'bgcolor': 'white',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Bulan</b>',
                       color = '#425C5A',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='#425C5A',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Poppins',
                           color='black',
                           size=12
                       )),
            yaxis=dict(title='<b>Total Penjualan</b>',
                       color='#425C5A',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='#425C5A',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Poppins',
                           color='black',
                           size=12
                       )
                       )


        )
    }

@app.callback(Output('barchart_vitarasa', 'figure'),
              [Input('select_years','value')],
              [Input('select_month','value')])
def update_graph(select_years,  select_month):
    salesvitarasa = df.groupby(['tahun', 'bulan', 'brand', 'scode'])['total'].sum().reset_index()
    salesvitarasa2 = salesvitarasa[(salesvitarasa['tahun'] == select_years)  & (salesvitarasa['brand'] == 'VITASARI') & (salesvitarasa['bulan'] == select_month)].sort_values(by = ['total'], ascending = False)


    return {
        'data': [
            go.Bar(
                x=salesvitarasa2['total'],
                y=salesvitarasa2['scode'],
                text = salesvitarasa2['total'],
                texttemplate= 'Rp.' + '%{text:,.2s}',
                textposition='auto',
                orientation= 'h',
                marker=dict(color='#C99C33'),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + salesvitarasa2['tahun'].astype(str) + '<br>' +
                '<b>Brand Type</b>: ' + salesvitarasa2['scode'].astype(str) + '<br>' +
                '<b>Total</b>: Rp' + [f'{x:,.0f}' for x in salesvitarasa2['total']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Penjualan Bihun pada bulan' + ' ' + str((select_month)) + ' tahun' + ' ' + str((select_years)),
                   'y': 0.95,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'black',
                       'size': 15},
            font=dict(family='Poppins',
                      color='black',
                      size=15),
            hovermode='closest',
            paper_bgcolor='white',
            plot_bgcolor='white',
            legend={'orientation': 'h',
                    'bgcolor': '#010915',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t = 50, l = 120, r=0),
            xaxis=dict(title='<b></b>',
                       color = '#425C5A',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='#425C5A',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Poppins',
                           color='#425C5A',
                           size=12
                       )),
            yaxis=dict(title='<b></b>',
                       color='#425C5A',
                       autorange = 'reversed',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='#425C5A',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Poppins',
                           color='#425C5A',
                           size=10
                       )
                       )


        )
    }

@app.callback(Output('histogram_vitarasa2', 'figure'),
              [Input('select_years','value')],
              [Input('select_produk','value')],
              [Input('select_prov','value')])
def update_graph(select_years, select_produk, select_prov):
    provvitarasa = df.groupby(['tahun', 'bulan', 'stock_name', 'prov','gudang'])['total'].sum().reset_index()
    provvitarasa2 = provvitarasa[(provvitarasa['tahun'] == select_years) & (provvitarasa['stock_name'] == select_produk) & (provvitarasa['prov'] == select_prov)][['tahun', 'bulan', 'gudang', 'stock_name','prov', 'total']].reset_index()

    return {
        'data': [go.Bar(
            x=provvitarasa2['gudang'].tail(30),
            y=provvitarasa2['total'].tail(30),
            name='Tingkat Penjualan Setiap Wilayah',
            marker=dict(color='#18B3A7'),
            hoverinfo='text',
            hovertext=
            '<b>Tahun</b>: ' + provvitarasa2['tahun'].tail(30).astype(str) + '<br>' +
            '<b>Wilayah</b>: ' + provvitarasa2['gudang'].tail(30).astype(str) + '<br>' +
            '<b>Total Penjualan</b>: ' + [f'{x:,.0f}' for x in provvitarasa2['total'].tail(30)] + '<br>' 

        )],
    
        'layout': go.Layout(
            title={'text': 'Tingkat Penjualan  ' + (select_produk) + '<br>' +
                            ' Pada Tahun ' + (select_years), 
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'black',
                       'size': 15},
            font=dict(family='Poppins',
                      color='black',
                      size=12),
            hovermode='closest',
            paper_bgcolor='white',
            plot_bgcolor='white',
            legend={'orientation': 'h',
                    'bgcolor': 'white',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Wilayah</b>',
                       color = '#425C5A',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='#425C5A',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Poppins',
                           color='black',
                           size=10
                       )),
            yaxis=dict(title='<b>Total Penjualan</b>',
                       color='#425C5A',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='#425C5A',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Poppins',
                           color='black',
                           size=12
                       )
                       )


        )
    }

@app.callback(Output('pie_chartvit', 'figure'),
              [Input('select_years','value')])
def update_graph(select_years):
    salesvit = df.groupby(['tahun', 'scode'])['total'].sum().reset_index()
    vitceriping200gr = salesvit[(salesvit['tahun'] == select_years)  & (salesvit['scode'] == 'vit ceriping 200 gr')]['total'].sum()
    vitceriping5kgctn = salesvit[(salesvit['tahun'] == select_years)  & (salesvit['scode'] == 'vit ceriping 5kg ctn')]['total'].sum()
    vitBawang250gr = salesvit[(salesvit['tahun'] == select_years)  & (salesvit['scode'] == 'vit Bawang 250gr')]['total'].sum()
    vitudang250gr = salesvit[(salesvit['tahun'] == select_years)  & (salesvit['scode'] == 'vit udang 250gr')]['total'].sum()
    vitBw5kg = salesvit[(salesvit['tahun'] == select_years)  & (salesvit['scode'] == 'vit Bw 5kg')]['total'].sum()
    vitbwg500 = salesvit[(salesvit['tahun'] == select_years)  & (salesvit['scode'] == 'vit bwg 500')]['total'].sum()
    vitceriping45kg = salesvit[(salesvit['tahun'] == select_years)  & (salesvit['scode'] == 'vit ceriping 4.5kg')]['total'].sum()
    vitceriping400 = salesvit[(salesvit['tahun'] == select_years)  & (salesvit['scode'] == 'vit ceriping 400')]['total'].sum()
    vitudang500 = salesvit[(salesvit['tahun'] == select_years)  & (salesvit['scode'] == 'vit udang 500')]['total'].sum()
    vitudang5kg = salesvit[(salesvit['tahun'] == select_years)  & (salesvit['scode'] == 'vit udang 5kg')]['total'].sum()

    colors = ['#1890B3', '#425C5A', '#D6AF14', '#30C9C7', '#7A45D1', 'orange', '#EC5333', '#4133EC', '#2C3E50', '#0a403b']



    return {
            'data': [go.Pie(labels = ['vit ceriping 200 gr', 'vit ceriping 5kg ctn', 'vit Bawang 250gr', 'vit udang 250gr', 'vit Bw 5kg', 'vit bwg 500',
                                        'vit ceriping 4.5kg', 'vit ceriping 400', 'vit udang 500', 'vit udang 5kg'],
                            values = [vitceriping200gr, vitceriping5kgctn, vitBawang250gr, vitudang250gr, vitBw5kg, vitbwg500, 
                                        vitceriping45kg, vitceriping400, vitudang500, vitudang5kg],
                            marker = dict(colors = colors),
                            hoverinfo = 'label+value+percent',
                            # textinfo = 'label+value',
                            # textfont = dict(size = 13),
                            # texttemplate = '%{label} <br>%{value:,.0f}',
                            # textposition = 'auto',
                            # hole = .7,
                            rotation = 280,
                            insidetextorientation='radial',

                            )],

            'layout': go.Layout(
                margin=dict(l=129, r=122),
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode = 'x',
                title = {'text': 'Sebaran penjualan Vitasari pada Tahun ' + (select_years),

                    'y': 0.99,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont = {
                    'color': 'black',
                    'size': 15},
                legend = {
                    'orientation': 'h',
                    'bgcolor': 'white',
                    'xanchor': 'center', 'x': 0.5, 'y': 0.15},

                font = dict(
                    family = 'Poppins',
                    size = 12,
                    color = '#2e4a66')
            ),

        }