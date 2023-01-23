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
from flask import Flask
import matplotlib.pyplot as plt
import json
import dash_auth

# Connect to main app.py file
from app import app
from app import server
from apps import main, detail, detail_vitarasa, detail_mie, inputdata, tambahdata, apptambah

# Connect to your app pages
client = pymongo.MongoClient("mongodb://localhost:27017")
# Create database called animals
mydb = client["Penjualan"]
# Create Collection (table) called shelterA
collection = mydb.DataPenjualan222

df = pd.DataFrame(list(collection.find()))

sales = pd.read_csv('../miniProject/skrispi/penjualan.csv')


year_sale = df['tahun'].unique()
product_brand = df['brand'].unique()

provinsi = df['prov'].unique()
provinsi = provinsi

# app = Flask(__name__)
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

auth = dash_auth.BasicAuth(
    app,
    {'user' : 'user',
     'admin' : 'admin'}
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/main':
        return main.layout
    if pathname == '/apps/inputdata':
        return inputdata.layout
    if pathname == '/apps/tambahdata':
        return tambahdata.layout
    # if pathname == '/apps/apptambah':
    #     return apptambah.layout
    if pathname == '/apps/all':
        return main.layout
    if pathname == '/apps/detail':
        return detail.layout
    if pathname == '/apps/detail_vitarasa':
        return detail_vitarasa.layout
    if pathname == '/apps/detail_mie':
        return detail_mie.layout

    else:
        return main.layout

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
        
        df.drop_duplicates(subset='Nama', keep='first', inplace=True)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

def year_sale(data):
    df = pd.DataFrame(data)
    
    return html.Div([
         dcc.Dropdown(id='yaxis-data',
                     options=[{'label':x, 'value':x} for x in df.columns['tahun']])
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
                '<b>Total</b>: Rp.' + [f'{x:,.0f}' for x in sales2['total']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Top 5 Penjualan' + ' ' + str((select_brand)) + ' Tahun' + ' ' + str((select_years)),
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
            title={'text': 'Pencapaian Penjualan Setiap Sales' + '<br>'+ 'Pada Tahun ' + ' ' + str((select_years)),
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
    prov1 = df.groupby(['tahun', 'bulan', 'brand','gudang', 'prov'])['total'].sum().reset_index()
    prov2 = prov1[(prov1['tahun'] == select_years) & (prov1['brand'] == select_brand) & (prov1['prov'] == select_prov)][['tahun', 'bulan', 'gudang', 'brand', 'prov','total']].reset_index()

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

# -------------------------------------------DETAIL BIHUN-----------------------------------------------------------------------------------------

@app.callback(Output('mongo-datatable', 'children'),
              [Input('interval_db', 'n_intervals')],
              [Input('select_years','value')],
              [Input('select_produk','value')])
def populate_datatable(n_intervals, select_years, select_produk):
    print(n_intervals)
    # Convert the Collection (table) date to a pandas DataFrame
    sales = df[['order_date', 'tahun', 'sales_no', 'gudang','prov', 'kota', 'kec', 'stock_name','brand', 'qty', 'unit', 'in_pcs', 'in_ctn', 'total', 'driver', 'helper1']]
    data_table = sales[(sales['tahun'] == select_years) & (sales['brand'] == 'BIHUN') & (sales['stock_name'] == select_produk)]

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
                        'font': 'Poppins',
                        'color': 'orange',
                         'border': '#425C5A'},
            style_as_list_view=True,
            style_data={'styleOverflow': 'hidden', 'color': 'white'},
            fixed_rows={'headers': True},
            sort_action='native',
            sort_mode='multi'

        )
    ]

@app.callback(Output('histogram_bihun', 'figure'),
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

@app.callback(Output('barchart_bihun', 'figure'),
              [Input('select_years','value')],
              [Input('select_month','value')])
def update_graph(select_years,  select_month):
    salesbihun = df.groupby(['tahun', 'bulan', 'brand', 'scode'])['total'].sum().reset_index()
    salesbihun2 = salesbihun[(salesbihun['tahun'] == select_years)  & (salesbihun['brand'] == 'BIHUN') & (salesbihun['bulan'] == select_month)].sort_values(by = ['total'], ascending = False)


    return {
        'data': [
            go.Bar(
                x=salesbihun2['total'],
                y=salesbihun2['scode'],
                text = salesbihun2['total'],
                texttemplate= 'Rp.' + '%{text:,.2s}',
                textposition='auto',
                orientation= 'h',
                marker=dict(color='#C99C33'),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + salesbihun2['tahun'].astype(str) + '<br>' +
                '<b>Brand Type</b>: ' + salesbihun2['scode'].astype(str) + '<br>' +
                '<b>Total</b>: Rp' + [f'{x:,.0f}' for x in salesbihun2['total']] + '<br>'

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

@app.callback(Output('histogram_bihun2', 'figure'),
              [Input('select_years','value')],
              [Input('select_produk','value')],
              [Input('select_prov','value')])
def update_graph(select_years, select_produk, select_prov):
    provbihun = df.groupby(['tahun', 'bulan', 'stock_name', 'prov','gudang'])['total'].sum().reset_index()
    provbihun2 = provbihun[(provbihun['tahun'] == select_years) & (provbihun['stock_name'] == select_produk) & (provbihun['prov'] == select_prov)][['tahun', 'bulan', 'gudang', 'stock_name','prov', 'total']].reset_index()

    return {
        'data': [go.Bar(
            x=provbihun2['gudang'].tail(30),
            y=provbihun2['total'].tail(30),
            name='Tingkat Penjualan Setiap Wilayah',
            marker=dict(color='#18B3A7'),
            hoverinfo='text',
            hovertext=
            '<b>Tahun</b>: ' + provbihun2['tahun'].tail(30).astype(str) + '<br>' +
            '<b>Wilayah</b>: ' + provbihun2['gudang'].tail(30).astype(str) + '<br>' +
            '<b>Total Penjualan</b>: ' + [f'{x:,.0f}' for x in provbihun2['total'].tail(30)] + '<br>' 

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

@app.callback(Output('pie_chart', 'figure'),
              [Input('select_years','value')])
def update_graph(select_years):
    salesbihun = df.groupby(['tahun', 'scode'])['total'].sum().reset_index()
    Bijag12X300gr = salesbihun[(salesbihun['tahun'] == select_years)  & (salesbihun['scode'] == 'Bijag 12X300gr')]['total'].sum()
    Bijag24X150gr = salesbihun[(salesbihun['tahun'] == select_years)  & (salesbihun['scode'] == 'Bijag 24X150gr')]['total'].sum()
    Bijag60X60gr = salesbihun[(salesbihun['tahun'] == select_years)  & (salesbihun['scode'] == 'Bijag 60X60gr')]['total'].sum()
    BijagLos2kg = salesbihun[(salesbihun['tahun'] == select_years)  & (salesbihun['scode'] == 'Bijag Los 2kg')]['total'].sum()
    BijagLos4kg = salesbihun[(salesbihun['tahun'] == select_years)  & (salesbihun['scode'] == 'Bijag Los 4kg')]['total'].sum()
    BijagPdm175gr = salesbihun[(salesbihun['tahun'] == select_years)  & (salesbihun['scode'] == 'Bijag Pdm 175gr')]['total'].sum()
    BijagPdm350gr = salesbihun[(salesbihun['tahun'] == select_years)  & (salesbihun['scode'] == 'Bijag Pdm 350gr')]['total'].sum()
    BijagPdm60gr = salesbihun[(salesbihun['tahun'] == select_years)  & (salesbihun['scode'] == 'Bijag Pdm 60gr')]['total'].sum()
    Sohun18X60gr = salesbihun[(salesbihun['tahun'] == select_years)  & (salesbihun['scode'] == 'Sohun 18X60gr')]['total'].sum()

    colors = ['#1890B3', '#425C5A', '#D6AF14', '#30C9C7', '#7A45D1', 'orange', '#EC5333', '#4133EC', '#2C3E50']



    return {
            'data': [go.Pie(labels = ['Bijag 12X300gr', 'Bijag 24X150gr', 'Bijag 60X60gr', 'Bijag Los 2kg', 
                                        'Bijag Los 4kg', 'Bijag Pdm 175gr', 'Bijag Pdm 350gr', 'Bijag Pdm 60gr', 'Sohun 18X60gr' ],
                            values = [Bijag12X300gr, Bijag24X150gr, Bijag60X60gr, BijagLos2kg, BijagLos4kg,
                                       BijagPdm175gr, BijagPdm350gr, BijagPdm60gr, Sohun18X60gr],
                            marker = dict(colors = colors),
                            hoverinfo = 'label+value+percent',
                            # textinfo = 'label+value',
                            # textfont = dict(size = 13),
                            # texttemplate = '%{label} <br>%{value:,.0f}',
                            # textposition = 'auto',
                            # hole = .7,
                            rotation = 360,
                            insidetextorientation='radial',

                            )],

            'layout': go.Layout(
                margin=dict(l=129, r=122),
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode = 'x',
                title = {'text': 'Sebaran penjualan Bihun pada Tahun ' + (select_years),

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
# -------------------------------------------AKHIR DETAIL BIHUN-----------------------------------------------------------------------------------------
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
# -----------------------------------------AKHIR DETAIL VITARASA---------------------------------------------------------

# -----------------------------------------AWAL DETAIL MIE---------------------------------------------------------
@app.callback(Output('datatable_mie', 'children'),
              [Input('interval_db', 'n_intervals')],
              [Input('select_years','value')],
              [Input('select_produk','value')])
def populate_datatable(n_intervals, select_years, select_produk):
    print(n_intervals)
    # Convert the Collection (table) date to a pandas DataFrame
    sales = df[['order_date', 'tahun', 'sales_no', 'gudang','prov', 'kota', 'kec', 'stock_name','brand', 'qty', 'unit', 'in_pcs', 'in_ctn', 'total', 'driver', 'helper1']]
    data_table = sales[(sales['tahun'] == select_years) & (sales['brand'] == 'MIE KERING') & (sales['stock_name'] == select_produk)]

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

@app.callback(Output('histogram_mie', 'figure'),
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

@app.callback(Output('barchart_mie', 'figure'),
              [Input('select_years','value')],
              [Input('select_month','value')])
def update_graph(select_years,  select_month):
    salesmie = df.groupby(['tahun', 'bulan', 'brand', 'scode'])['total'].sum().reset_index()
    salesmie2 = salesmie[(salesmie['tahun'] == select_years)  & (salesmie['brand'] == 'MIE KERING') & (salesmie['bulan'] == select_month)].sort_values(by = ['total'], ascending = False)


    return {
        'data': [
            go.Bar(
                x=salesmie2['total'],
                y=salesmie2['scode'],
                text = salesmie2['total'],
                texttemplate= 'Rp.' + '%{text:,.2s}',
                textposition='auto',
                orientation= 'h',
                marker=dict(color='#C99C33'),
                hoverinfo='text',
                hovertext=
                '<b>Year</b>: ' + salesmie2['tahun'].astype(str) + '<br>' +
                '<b>Brand Type</b>: ' + salesmie2['scode'].astype(str) + '<br>' +
                '<b>Total</b>: Rp' + [f'{x:,.0f}' for x in salesmie2['total']] + '<br>'

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

@app.callback(Output('histogram_mie2', 'figure'),
              [Input('select_years','value')],
              [Input('select_produk','value')],
              [Input('select_prov','value')])
def update_graph(select_years, select_produk, select_prov):
    provmie = df.groupby(['tahun', 'bulan', 'stock_name', 'prov','gudang'])['total'].sum().reset_index()
    provmie2 = provmie[(provmie['tahun'] == select_years) & (provmie['stock_name'] == select_produk) & (provmie['prov'] == select_prov)][['tahun', 'bulan', 'gudang', 'stock_name','prov', 'total']].reset_index()

    return {
        'data': [go.Bar(
            x=provmie2['gudang'].tail(30),
            y=provmie2['total'].tail(30),
            name='Tingkat Penjualan Setiap Wilayah',
            marker=dict(color='#18B3A7'),
            hoverinfo='text',
            hovertext=
            '<b>Tahun</b>: ' + provmie2['tahun'].tail(30).astype(str) + '<br>' +
            '<b>Wilayah</b>: ' + provmie2['gudang'].tail(30).astype(str) + '<br>' +
            '<b>Total Penjualan</b>: ' + [f'{x:,.0f}' for x in provmie2['total'].tail(30)] + '<br>' 

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

@app.callback(Output('pie_chartmie', 'figure'),
              [Input('select_years','value')])
def update_graph(select_years):
    salesmie = df.groupby(['tahun', 'scode'])['total'].sum().reset_index()
    MimoraPipih140grX24pak = salesmie[(salesmie['tahun'] == select_years)  & (salesmie['scode'] == 'MIMORA PIPIH 140GR/24PAK')]['total'].sum()
    MkLangitBiru25x60gr = salesmie[(salesmie['tahun'] == select_years)  & (salesmie['scode'] == 'Mk Langit Biru 25x60gr')]['total'].sum()
    Mklangitbiru3KG = salesmie[(salesmie['tahun'] == select_years)  & (salesmie['scode'] == 'MK LANGIT BIRU 3KG')]['total'].sum()
    MkLangitBiru600x5pak = salesmie[(salesmie['tahun'] == select_years)  & (salesmie['scode'] == 'Mk Langit Biru 600/5pak')]['total'].sum()
    MkLangitBiru750gr = salesmie[(salesmie['tahun'] == select_years)  & (salesmie['scode'] == 'Mk Langit Biru 750gr')]['total'].sum()
    Mtmimora6X136GR = salesmie[(salesmie['tahun'] == select_years)  & (salesmie['scode'] == 'MT MIMORA 6X136GR')]['total'].sum()

    colors = ['#1890B3', '#425C5A', '#D6AF14', '#30C9C7', '#7A45D1', 'orange', '#EC5333', '#4133EC', '#2C3E50']



    return {
            'data': [go.Pie(labels = ['MIMORA PIPIH 140GR/24PAK', 'Mk Langit Biru 25x60gr', 'MK LANGIT BIRU 3KG', 'Mk Langit Biru 600/5pak', 'Mk Langit Biru 750gr', 'MT MIMORA 6X136GR'],
                            values = [MimoraPipih140grX24pak, MkLangitBiru25x60gr, Mklangitbiru3KG, MkLangitBiru600x5pak, MkLangitBiru750gr, Mtmimora6X136GR],
                            marker = dict(colors = colors),
                            hoverinfo = 'label+value+percent',
                            # textinfo = 'label+value',
                            # textfont = dict(size = 13),
                            # texttemplate = '%{label} <br>%{value:,.0f}',
                            # textposition = 'auto',
                            # hole = .7,
                            rotation = 360,
                            insidetextorientation='radial',

                            )],

            'layout': go.Layout(
                margin=dict(l=129, r=122),
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode = 'x',
                title = {'text': 'Sebaran penjualan Bihun pada Tahun ' + (select_years),

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

# ----------------------------------------INPUT DATA---------------------------------------------------------------------
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
        dt.DataTable(
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
            # page_size=6,  # number of rows visible per page
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
                           color='#425C5A',
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

@app.callback(
    Output("output", "children"),
    Input("form", "data"),
    Input("save", "n_submit"),
    State("nomorsales", "value"),
    State("tahun", "value"),
    State("bulan", "value"),
    State("hari", "value"),
    State("tgltransaksi", "value"),
    State("gudang", "value"),
    State("depo", "value"),
    State("custid", "value"),
    State("companyname", "value"),
    State("alamat", "value"),
    State("provinsi", "value"),
    State("kota", "value"),
    State("kecamatan", "value"),
    State("outletcat", "value"),
    State("outlettype", "value"),
    State("outletgroup", "value"),
    State("salesvisit", "value"),
    State("stockid", "value"),
    State("scode", "value"),
    State("stockname", "value"),
    State("brand", "value"),
    State("stockcat", "value"),
    State("supplier", "value"),
    State("salesman", "value"),
    State("team", "value"),
    State("rute", "value"),
    State("quantity", "value"),
    State("unit", "value"),
    State("inpcs", "value"),
    State("inctn", "value"),
    State("subtotal", "value"),
    State("dpp", "value"),
    State("ppn", "value"),
    State("total", "value"),
    State("tglantar", "value"),
    State("driver", "value"),
    State("helper", "value"),
    State("stationid", "value"),

    prevent_initial_call=True,
)

def handle_submit(data, n_submit, tahun, bulan, hari, tgltransaksi, gudang, depo, custid, 
                    companyname, alamat, provinsi, kota, kecamatan, outletcat, outlettype, 
                    outletgroup, salesvisit, stockid, scode, stockname, brand, stockcat, 
                    supplier, salesman, team, rute, quantity, unit, inpcs, inctn, subtotal, 
                    dpp, ppn, total, tglantar, driver, helper, stationid):

    df = pd.DataFrame(
        {
            "sales_no": [nomorsales], 
            "tahun": [tahun], 
            "hari": [hari],
            "order_date": [tgltransaksi],
            "gudang": [gudang],
            "depo": [depo],
            "cust_id": [custid],
            "company_name": [companyname],
            "address_1": [alamat],
            "prov": [provinsi],
            "kota": [kota],
            "kec": [kecamatan],
            "outlet_cat": [outletcat],
            "outlet_type": [outlettype],
            "outlet_group": [outletgroup],
            "sales_visit": [salesvisit],
            "stock_id": [stockid],
            "scode": [scode],
            "stock_name": [stockname],
            "brand": [brand],
            "stock_cat": [stockcat],
            "supplier": [supplier],
            "salesman": [salesman],
            "team": [team],
            "rute": [rute],
            "qty": [quantity],
            "unit": [unit],
            "in_pcs": [inpcs],
            "in_ctn": [inctn],
            "subtotal": [subtotal],
            "dpp": [dpp],
            "PPn": [PPn],
            "total": [total],
            "delivered_date": [tglantar],
            "driver": [driver],
            "helper1": [helper],
            "station_id": [stationid],  

        }
    )

    if n_submit:
        dff = pd.DataFrame(data)
        collection.delete_many({})
        collection.insert_many(dff.to_dict('records'))
        return "succes"
        # df.to_mongodb("table", con=db.engine, if_exists="append", index=False)
        # return "success"
    return ""



if __name__ == '__main__':
    app.run_server(debug=False)