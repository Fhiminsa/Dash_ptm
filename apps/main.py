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

year_sale = df['tahun'].unique()
product_brand = df['brand'].unique()
provinsi = df['prov'].unique()
gudang = df['gudang'].unique()
bulanpenjualan = df['bulan'].astype(int).unique()


# -------------------------------------App----------------------------------------------------------------------------


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div([

    html.Div([
        # html.Img(src=app.get_asset_url('user.png'), style={'position': 'relative', 'width': '35px', 'left':'900px', 'top':'15px'}),
        dbc.NavLink("Dashboard", href="/apps/main", id='menumain', style={'color': 'black'}),
        dbc.NavLink("Input Data", href="/apps/inputdata", id='input_data', style={'color': 'black'}),
        dbc.NavLink("tambah data", href="/apps/tambahdata", id='tambah_data', style={'color': 'black'}),
        # dbc.NavLink("tambah data", href="/apps/apptambah", id='app_tambah')
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
            html.Div([], className='box1'),

            html.Div([
                html.Img(src=app.get_asset_url('LogoPTM.png'), style={'width':'160px'}),
                html.H3("PT.PELITA TERANG MAKMUR", id='ptm', style={'font-family':'Poppins'})
            ], className='logo'),

            html.Div([], className='box2'),
            html.Div([], className='box3'),
            html.Div([], className='box4'),
            html.Div([], className='box12'),

            html.Div([
                html.Div(id = 'text1'),
                html.Div(id = 'text2'),
                html.Div(id = 'text3'),
                html.Div(id = 'text4'),
            ], className='text'),

            html.Div([
                dbc.NavLink("Detail", href="/apps/all", id='all'),
                dbc.NavLink("Detail", href="/apps/detail", id='detail_bihun'),
                dbc.NavLink("Detail", href="/apps/detail_vitarasa", id='detail_vitarasa'),
                dbc.NavLink("Detail", href="/apps/detail_mie", id='detail_mie'),
            ], className='menu_detail'),

            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children= dbc.Button("Upload File", outline=True, color="warning", className="me-1",  id='upload'),
                    multiple=True
                )

            ]),

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
                dcc.Dropdown(id='select_brand',
                    value='MIE KERING',
                    options=[{'label':x, 'value':x} for x in product_brand]),
            ], id = 'product-brand'),

            html.Div([], className='box7'),
            html.Div([
                dcc.Graph(id = 'histogram', config={'displayModeBar': 'hover'})
            ], id = 'Histogram'),

            html.Div([], className='box8'),
            html.Div([
                dcc.Graph(id = 'bar_chart', config={'displayModeBar': 'hover'},
                      style={'height': '300px'})

            ], id = 'BarChart'),

            html.Div([], className='box9'),

            html.Div([
                dcc.Graph(id = 'donut_chart', config={'displayModeBar': 'hover'},
                        style={'height': '300px'})

            ], id = 'DonutChart'),

            html.Div([], className='box10'),

            html.Div([
                dcc.Dropdown(id='select_prov',
                    value='Sulawesi Selatan',
                    options=[{'label':x, 'value':x} for x in provinsi]),
            ], id = 'provinsi'),

            html.Div([
                dcc.Graph(id = 'histogram2', config={'displayModeBar': 'hover'})
            ], id = 'Histogram2'),

            html.Div([], className='box11'),

            html.Div([
                dcc.Graph(id = 'bar_chart2', config={'displayModeBar': 'hover'},
                      style={'height': '480px'})

            ], id = 'BarChart2'),

            html.Div([
                dcc.Graph(id = 'histogram3', config={'displayModeBar': 'hover'})
            ], id = 'Histogram3'),

            html.Div([], className='box15'),

            html.Div([], className='box16'),

            html.Div([
                dcc.Graph(id='linechart', config={'displayModeBar': 'hover'})
            ],id='Linechart'),
                
            # ], className='side_section'),
            
                            
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
        
        data = df.to_dict(orient = "records")
        db = client["Penjualan2"]
        db.DataPenjualan2.insert_many(data)

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

@app.callback(Output('histogram', 'figure'),
              [Input('select_years','value')])
def update_graph(select_years):
    sales11 = df.groupby(['tahun', 'bulan'])['total'].sum().reset_index()
    sales12 = sales11[(sales11['tahun'] == select_years)][['tahun', 'bulan', 'total']].reset_index()

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


@app.callback(Output('bar_chart', 'figure'),
              [Input('select_years','value')],
              [Input('select_brand','value')])
def update_graph(select_years, select_brand):
    sales1 = df.groupby(['tahun', 'brand', 'scode'])['total'].sum().reset_index()
    sales2 = sales1[(sales1['tahun'] == select_years) & (sales1['brand'] == select_brand)].sort_values(by = ['total'], ascending = False).nlargest(5, columns = ['total'])


    return {
        'data': [
            go.Bar(
                x=sales2['total'],
                y=sales2['scode'],
                text = sales2['total'],
                texttemplate= 'Rp.' + '%{text:,.2s}',
                textposition='auto',
                orientation= 'h',
                marker=dict(color='#C99C33'),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + sales2['tahun'].astype(str) + '<br>' +
                '<b>Brand Type</b>: ' + sales2['scode'].astype(str) + '<br>' +
                '<b>Total</b>: Rp' + [f'{x:,.0f}' for x in sales2['total']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Top 5 Penjualan' + ' ' + str((select_brand)) + 'Tahun' + ' ' + str((select_years)),
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


@app.callback(Output('donut_chart', 'figure'),
              [Input('select_years','value')])
def update_graph(select_years):
    sales3 = df.groupby(['tahun', 'brand'])['total'].sum().reset_index()
    bihun = sales3[(sales3['tahun'] == select_years)  & (sales3['brand'] == 'BIHUN')]['total'].sum()
    mie_kering = sales3[(sales3['tahun'] == select_years)  & (sales3['brand'] == 'MIE KERING')]['total'].sum()
    vitasari = sales3[(sales3['tahun'] == select_years)  & (sales3['brand'] == 'VITASARI')]['total'].sum()
    colors = ['#1890B3', '#425C5A', '#D6AF14']



    return {
            'data': [go.Pie(
                labels=['Bihun', 'Mie Kering', 'Vitasari'],
                values=[bihun, mie_kering,  vitasari],
                marker=dict(colors=colors),
                hoverinfo='label+value+percent',
                textinfo='label+value',
                texttemplate='%{label} <br>Rp.%{value:,.2f}',
                textposition='auto',
                textfont=dict(size=13),
                hole=.7,
                rotation=160,
                # insidetextorientation= 'radial'

            )],

            'layout': go.Layout(
                title={'text': 'Perbandingan Penjualan pada Setiap Produk' + '<br>'+ 'Tahun' + ' ' + str((select_years)),
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
                        'xanchor': 'center', 'x': 0.5, 'y': -0.9}

            )
        }

@app.callback(Output('bar_chart2', 'figure'),
              [Input('select_years','value')])
def update_graph(select_years):
    sales9 = df.groupby(['tahun', 'salesman'])['total'].sum().reset_index()
    sales10 = sales9[(sales9['tahun'] == select_years)].sort_values(by = ['total'], ascending = False).nlargest(10, columns = ['total'])


    return {
        'data': [
            go.Bar(
                x=sales10['total'],
                y=sales10['salesman'],
                # text = sales10['total'],
                # texttemplate= 'Rp.' + '%{text:,.2s}',
                # textposition='auto',
                orientation= 'h',
                marker=dict(color='#425C5A'),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + sales10['tahun'].astype(str) + '<br>' +
                '<b>Salesman</b>: ' + sales10['salesman'].astype(str) + '<br>' +
                '<b>Total</b>: Rp.' + [f'{x:,.0f}' for x in sales10['total']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Pencapaian Penjualan Setiap Sales' +'<br>'+ 'Pada Tahun ' + ' ' + str((select_years)),
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
            margin=dict(t = 50, l = 90, r=0),
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

@app.callback(Output('text1', 'children'),
               [Input('select_years','value')])
def update_graph(select_years):
    allbrnd = df.groupby(['tahun'])['total'].sum().reset_index()
    allbrnd2 = allbrnd[(allbrnd['tahun'] == select_years)]['total'].sum()

    return [
        html.H5('Rp.{0:,.2f}'.format(allbrnd2)),

        html.P(children='All Product')

    ]

@app.callback(Output('text2', 'children'),
               [Input('select_years','value')])
def update_graph(select_years):
    bihun = df.groupby(['tahun', 'brand'])['total'].sum().reset_index()
    bihun2 = bihun[(bihun['tahun'] == select_years) & (bihun['brand'] == 'BIHUN')]['total'].sum()

    return [
         html.H5('Rp.{0:,.2f}'.format(bihun2)),

        html.P(children='Bihun',)

    ]

@app.callback(Output('text3', 'children'),
               [Input('select_years','value')])
def update_graph(select_years):
    vitasari = df.groupby(['tahun', 'brand'])['total'].sum().reset_index()
    vitasari2 = vitasari[(vitasari['tahun'] == select_years) & (vitasari['brand'] == 'VITASARI')]['total'].sum()

    return [
         html.H5('Rp.{0:,.2f}'.format(vitasari2)),

        html.P(children='Vitasari',)

    ]

@app.callback(Output('text4', 'children'),
               [Input('select_years','value')])
def update_graph(select_years):
    mie = df.groupby(['tahun', 'brand'])['total'].sum().reset_index()
    mie2 = mie[(mie['tahun'] == select_years) & (mie['brand'] == 'MIE KERING')]['total'].sum()

    return [
         html.H5('Rp.{0:,.2f}'.format(mie2)),

        html.P(children='Mie Kering',)

    ]

@app.callback(Output('histogram2', 'figure'),
              [Input('select_years','value')],
              [Input('select_brand','value')],
              [Input('select_prov','value')])
def update_graph(select_years, select_brand, select_prov):
    prov1 = df.groupby(['tahun', 'bulan', 'brand', 'prov','gudang'])['total'].sum().reset_index()
    prov2 = prov1[(prov1['tahun'] == select_years) & (prov1['brand'] == select_brand) & (prov1['prov'] == select_prov)][['tahun', 'bulan', 'gudang', 'brand','prov', 'total']].reset_index()

    return {
        'data': [go.Bar(
            x=prov2['gudang'].tail(30),
            y=prov2['total'].tail(30),
            name='Tingkat Penjualan Setiap Wilayah',
            marker=dict(color='#18B3A7'),
            hoverinfo='text',
            hovertext=
            '<b>Tahun</b>: ' + prov2['tahun'].tail(30).astype(str) + '<br>' +
            '<b>Wilayah</b>: ' + prov2['gudang'].tail(30).astype(str) + '<br>' +
            '<b>Total Penjualan</b>: ' + [f'{x:,.0f}' for x in prov2['total'].tail(30)] + '<br>' 

        )],
    
        'layout': go.Layout(
            title={'text': 'Penjualan ' + (select_brand) + ' di Setiap Wilayah' + '<br>'+ 
                            'pada Tahun  ' + (select_years),
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

@app.callback(Output('histogram3', 'figure'),
              [Input('select_years','value')],
              [Input('select_brand','value')])
def update_graph(select_years, select_brand):
    prov1 = df.groupby(['tahun', 'bulan', 'brand', 'prov'])['total'].sum().reset_index()
    prov2 = prov1[(prov1['tahun'] == select_years) & (prov1['brand'] == select_brand)][['tahun', 'bulan', 'brand','prov', 'total']].reset_index()

    return {
        'data': [go.Bar(
            x=prov2['prov'].tail(30),
            y=prov2['total'].tail(30),
            name='Tingkat Penjualan Pada Semua Provinsi',
            marker=dict(color='#18B3A7'),
            hoverinfo='text',
            hovertext=
            '<b>Tahun</b>: ' + prov2['tahun'].tail(30).astype(str) + '<br>' +
            '<b>Provinsi</b>: ' + prov2['prov'].tail(30).astype(str) + '<br>' +
            '<b>Total Penjualan</b>: ' + [f'{x:,.0f}' for x in prov2['total'].tail(30)] + '<br>' 

        )],
    
        'layout': go.Layout(
            title={'text': 'Penjualan ' + (select_brand) + ' di Setiap provinsi' + '<br>'+ 
                            'pada Tahun  ' + (select_years),
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

@app.callback(Output('linechart', 'figure'),
              [Input('select_years','value')])
def update_graph(select_years):
    line1 = df.groupby(['tahun', 'bulan'])['total'].sum().reset_index()
    line2 = line1[(line1['tahun'] == select_years)][['tahun', 'bulan', 'total']].reset_index()

    return {
        'data': [
            go.Scatter(
                x=line2['bulan'],
                y=line2['total'],
                text = line2['total'],
                texttemplate= 'Rp.' + '%{text:,.2s}',
                textposition='bottom left',
                mode='markers+lines+text',
                line=dict(width=3, color='#D6A217'),
                marker=dict(color='#18B3A7', size=10, symbol='circle',
                            line=dict(color='#18B3A7', width=2)),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + line2['tahun'].astype(str) + '<br>' +
                '<b>Month</b>: ' + line2['bulan'].astype(str) + '<br>' +
                '<b>Sales</b>: Rp.' + [f'{x:,.0f}' for x in line2['total']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Trend Penjualan Pada Tahun' + ' ' + str((select_years)),
                   'y': 1.0,
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
            # legend={'orientation': 'h',
            #         'bgcolor': 'white',
            #         'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t = 5, l = 0, r=0),
            xaxis=dict(title='<b></b>',
                       color = '#425C5A',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='#425C5A',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Poppins',
                           color='orange',
                           size=12
                       )),
            yaxis=dict(title='<b></b>',
                       color='#425C5A',
                       showline=False,
                       showgrid=True,
                       showticklabels=False,
                       linecolor='#425C5A',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Poppins',
                           color='#425C5A',
                           size=12
                       )
                       )


        )
    }

    

# ----------------------------------------Akhir LineChart----------------------------------------------------------------


# ----------------------------------------Callback----------------------------------------------------------------

