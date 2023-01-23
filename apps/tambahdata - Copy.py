import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc

import pymongo
from pymongo import MongoClient

from flask import Flask
import matplotlib.pyplot as plt
import json
import dash_auth

from app import app



# Connect to local server
client = MongoClient("mongodb://127.0.0.1:27017/")
# Create database called animals
mydb = client["Penjualan"]
# Create Collection (table) called shelterA
collection = mydb.DataPenjualan222



# app = Flask(__name__)

# app = Flask(__name__)

server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# app = dash.Dash(__name__, server=server)

layout = html.Div([

     html.Div([
        # html.Img(src=app.get_asset_url('user.png'), style={'position': 'relative', 'width': '35px', 'left':'900px', 'top':'15px'}),
        dbc.NavLink("Dashboard", href="/apps/main", id='menumain'),
        dbc.NavLink("Input Data", href="/apps/inputdata", id='input_data'),
        dbc.NavLink("Tambah Data", href="/apps/tambahdata", id='tambah_data'),
        # dbc.NavLink("Logout", href="/apps/login", id='login'),
        # html.H6("Logout")
    ], className='header'),

    html.Div([
        html.Label('PT. Pelita Terang Makmur merupakan sebuah perusahaan yang bergerak pada bidang distributor makanan, yang dimana memiliki beberapa cabang di area sulselbar dan sulawesi tenggara' , style={'position': 'relative',  'width' : '80%', 'text-align' : 'justify', 'color' : 'white', 'left': '30px', 'top': '300px'}),
        html.Img(src=app.get_asset_url('imgside.png'), style={'position': 'relative', 'width': '110%', 'left': '-15px', 'top': '320px'}),
        html.Hr(id='hrside', style={'position': 'relative', 'color' : 'white', 'width': '80%', 'height': '2px', 'left': '30px', 'top': '-165px'})
        # html.H1(children='ADMIN', style={'font-size':'17px'}),
    ], className='side_bar'),


    
    html.Div([
        html.Div([ 
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children= dbc.Button("Upload File", outline=True, color="warning", className="me-1",  id='upload'),
                    multiple=True
                )
            ]),

            html.Div([], className='boxpo'),
            html.Div([
                    html.H2("Tambah Data", id='labeltambah'),
                    html.Hr(id='hrpo')
            ]),

            html.Div([
                dbc.InputGroup(
                    [
                        dbc.Label("Nomor Sales : ", html_for="nomorsales"), 
                        dbc.Input(id="nomorsales", placeholder="")
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Tanggal Transaksi : ", html_for="tgltransaksi"), 
                        dbc.Input(id="tgltransaksi", placeholder="Date", type="date")
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.Label("Gudang : ", html_for="gudang"),
                        dbc.Select(id="gudang",
                            options=[
                                {"label": "Bone", "value": "Bone"},
                                {"label": "Bulukumba", "value": "Bulukumba"},
                                {"label": "Kolaka", "value": "Kolaka"},
                                {"label": "Makassar", "value": "Makassar"},
                                {"label": "Mamuju", "value": "Mamuju"},
                                {"label": "Mangkutana", "value": "Mangkutana"},
                                {"label": "Palopo", "value": "Palopo"},
                                {"label": "Pare-Pare", "value": "Pare-Pare"},
                                {"label": "Polman", "value": "Polman"},
                                {"label": "Sengkang", "value": "Sengkang"},
                                {"label": "Sinjai", "value": "Sinjai"},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup([
                        dbc.Label("Depo : ", html_for="depo"),
                        dbc.Select(id="depo",
                            options=[
                                {"label": "Bone", "value": "Bone"},
                                {"label": "Bulukumba", "value": "Bulukumba"},
                                {"label": "Kolaka", "value": "Kolaka"},
                                {"label": "Makassar", "value": "Makassar"},
                                {"label": "Mamuju", "value": "Mamuju"},
                                {"label": "Mangkutana", "value": "Mangkutana"},
                                {"label": "Palopo", "value": "Palopo"},
                                {"label": "Pare-Pare", "value": "Pare-Pare"},
                                {"label": "Polman", "value": "Polman"},
                                {"label": "Sengkang", "value": "Sengkang"},
                                {"label": "Sinjai", "value": "Sinjai"},
                            ]),
                    ], className="mb-3"),
                
                dbc.InputGroup(
                    [
                        dbc.Label("ID Pelanggan : ", html_for="idpelanggan"), 
                        dbc.Input(id="idpelanggan",placeholder="")],
                    className="mb-3",
                ),
                 dbc.InputGroup(
                    [
                        dbc.Label("Nama Usaha : ", html_for="namausaha"), 
                        dbc.Input(id="namausaha",placeholder="")
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Alamat : ", html_for="alamat"), 
                        dbc.Input(id="alamat",placeholder="")
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.Label("Provinsi : ", html_for="provinsi"),
                        dbc.Select(id="provinsi",
                            options=[
                                {"label": "Sulawesi Selatan", "value": "Sulawesi Selatan"},
                                {"label": "Sulawesi Barat", "value": "Sulawesi Barat"},
                                {"label": "Sulawesi Tenggara", "value": "Sulawesi Tenggara"},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup([
                        dbc.Label("Kabupaten/Kota : ", html_for="kabupaten"),
                        dbc.Select(id="kabupaten",
                            options=[
                                {"label": "Bantaeng", "value": "Bantaeng"},
                                {"label": "Barru", "value": "Barru"},
                                {"label": "Bau-Bau", "value": "Bau-Bau"},
                                {"label": "Bombana", "value":"Bombana"},
                                {"label": "Bone", "value": "Bone"},
                                {"label": "Bulukumba", "value": "Bulukumba"},
                                {"label": "Enrekang", "value": "Enrekang"},
                                {"label": "Gowa", "value": "Gowa"},
                                {"label": "Jeneponto", "value": "Jeneponto"},
                                {"label": "Kepulauan Selayar", "value": "Kepulauan Selayar"},
                                {"label": "Kolaka", "value": "Kolaka"},
                                {"label": "Kolaka Timur", "value": "Kolaka Timur"},
                                {"label": "Kolaka Utara", "value": "Kolaka Utara"},
                                {"label": "Luwu", "value": "Luwu"},
                                {"label": "Luwu Timur", "value": "Luwu Timur"},
                                {"label": "Luwu Utara", "value": "Luwu Utara"},
                                {"label": "Majene", "value": "Majene"},
                                {"label": "Makassar", "value": "Makassar"},
                                {"label": "Mamasa", "value": "Mamasa"},
                                {"label": "Mamuju", "value": "Mamuju"},
                                {"label": "Mamuju Tengah", "value": "Mamuju Tengah"},
                                {"label": "Mamuju Utara", "value": "Mamuju Utara"},
                                {"label": "Maros", "value": "Maros"},
                                {"label": "Palopo", "value": "Palopo"},
                                {"label": "Pangkajene Kepulauan", "value":"Pangkajene Kepulauan"},
                                {"label": "Pare-Pare", "value": "Pare-Pare"},
                                {"label": "Pinrang", "value": "Pinrang"},
                                {"label": "Polewali Mandar", "value": "Polewali Mandar"},
                                {"label": "Sidenren Rappan", "value": "Sidenren Rappan"},
                                {"label": "Sinjai", "value": "Sinjai"},
                                {"label": "Soppeng", "value": "Soppeng"},
                                {"label": "Takalar", "value": "Takalar"},
                                {"label": "Tana Toraja", "value": "Tana Toraja"},
                                {"label": "Toraja Utara", "value": "Toraja Utara"},
                                {"label": "Wajo", "value": "Wajo"},
                                
                            ]),
                    ], className="mb-3"
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Kecamatan : ", html_for="kecamatan"), 
                        dbc.Input(id="kecamatan",placeholder="")
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.Label("Outlet Cat : ", html_for="outletcat"),
                        dbc.Select(id="outletcat",
                            options=[
                                {"label": "GT", "value": "GT"},
                                {"label": "MT", "value": "MT"},
                            ]),
                    ], className="mb-3"),
                    dbc.InputGroup(
                    [
                        dbc.Label("Tipe Outlet : ", html_for="tipeoutlet"), 
                        dbc.Input(id="tipeoutlet", placeholder="")
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.Label("Kelompok Outlet : ", html_for="kelompok_outlet"),
                        dbc.Select(id="kelompok_outlet",
                            options=[
                                {"label": "Grosir", "value": "Grosir"},
                                {"label": "Minimarket", "value": "Minimarket"},
                                {"label": "Retail", "value": "Retail"},
                                {"label": "Supermarket", "value": "Supermarket"},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup([
                        dbc.Label("Hari Kunjungan : ", html_for="hari_kunjungan"),
                        dbc.Select(id="hari_kunjungan",
                            options=[
                                {"label": "Senin", "value": "Senin"},
                                {"label": "Selasa", "value": "Selasa"},
                                {"label": "Rabu", "value": "Rabu"},
                                {"label": "Kamis", "value": "Kamis"},
                                {"label": "Jumat", "value": "Jumat"},
                                {"label": "Sabtu", "value": "Sabtu"},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup(
                    [
                        dbc.Label("ID Stok : ", html_for="idstok"), 
                        dbc.Input(id="idstok", placeholder="")
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Scode : ", html_for="scode"), 
                        dbc.Input(id="scode", placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.Label("Nama Stok : ", html_for="namastok"),
                        dbc.Select(id="namastok",
                            options=[
                                {"label": "BIHUN JAGUNG 12X300GR", "value": "BIHUN JAGUNG 12X300GR"},
                                {"label": "BIHUN JAGUNG 24X150GR", "value": "BIHUN JAGUNG 24X150GR"},
                                {"label": "BIHUN JAGUNG 60X60GR", "value": "BIHUN JAGUNG 60X60GR"},
                                {"label": "BIHUN JAGUNG BIJAG LOS 4 KG", "value": "BIHUN JAGUNG BIJAG LOS 4 KG"},
                                {"label": "BIHUN JAGUNG PADAMU 175 GR / 24 PACK", "value": "BIHUN JAGUNG PADAMU 175 GR / 24 PACK"},
                                {"label": "BIHUN JAGUNG PADAMU 350 GR / 12 PACK", "value": "BIHUN JAGUNG PADAMU 350 GR / 12 PACK"},
                                {"label": "BIHUN JAGUNG PADAMU 60 GR / 60 PACK", "value": "BIHUN JAGUNG PADAMU 60 GR / 60 PACK"},
                                {"label": "BIJAG LOS 2 KG / 2 PACK", "value": "BIJAG LOS 2 KG / 2 PACK"},
                                {"label": "MIE KERING LANGIT BIRU 3KG", "value": "MIE KERING LANGIT BIRU 3KG"},
                                {"label": "MIE KERING LANGIT BIRU 4PX750GR", "value": "MIE KERING LANGIT BIRU 4PX750GR"},
                                {"label": "MIE TELUR MIMORA 6X136GR", "value": "MIE TELUR MIMORA 6X136GR"},
                                {"label": "SOHUN KACA 18RX60GR", "value": "SOHUN KACA 18RX60GR"},
                                {"label": "VIT SARI BAWANG 250 GR/20 PAK", "value": "VIT SARI BAWANG 250 GR/20 PAK"},
                                {"label": "VIT SARI BW ANK WARNA 5KG KRT", "value": "VIT SARI BW ANK WARNA 5KG KRT"},
                            ]),
                    ], className="mb-3"
                ),
                dbc.InputGroup([
                        dbc.Label("Brand : ", html_for="brand"),
                        dbc.Select(id="brand",
                            options=[
                                {"label": "Bihun", "value": "Bihun"},
                                {"label": "Mie Kering", "value": "Mie Kering"},
                                {"label": "Vitarasa", "value": "Vitarasa"},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup([
                        dbc.Label("Stok Cat : ", html_for="stokcat"),
                        dbc.Select(id="stokcat",
                            options=[
                                {"label": "Kerupuk", "value": "Kerupuk"},
                                {"label": "Mie Bihun", "value": "Mie Bihun"},
                                {"label": "Mie Kering", "value": "Mie Kering"},
                                {"label": "NOODLE", "value": "NOODLE"},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup([
                        dbc.Label("Supplier : ", html_for="supplier"),
                        dbc.Select(id="supplier",
                            options=[
                                {"label": "PT. SINAR PANGAN SEJAHTERA", "value": "PT. SINAR PANGAN SEJAHTERA"},
                                {"label": "PT. SINAR PANGAN SEJAHTERA / SAN", "value": "PT. SINAR PANGAN SEJAHTERA / SAN"},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup(
                    [
                        dbc.Label("Nama Sales : ", html_for="namasales"), 
                        dbc.Input(id="namasales", placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.Label("Team : ", html_for="team"),
                        dbc.Select(id="team",
                            options=[
                                {"label": "BLK1", "value": "BLK1"},
                                {"label": "BLK2", "value": "BLK2"},
                                {"label": "BONE1", "value": "BONE1"},
                                {"label": "BONE2", "value": "BONE2"},
                                {"label": "KLK1", "value": "KLK1"},
                                {"label": "KLK2", "value": "KLK2"},
                                {"label": "MKS1", "value": "MKS1"},
                                {"label": "MKS2", "value": "MKS2"},
                                {"label": "MKS3", "value": "MKS3"},
                                {"label": "MKS4", "value": "MKS4"},
                                {"label": "MKS5", "value": "MKS5"},
                                {"label": "MKS6", "value": "MKS6"},
                                {"label": "MKT1", "value": "MKT1"},
                                {"label": "MKT2", "value": "MKT2"},
                                {"label": "MMJ1", "value": "MMJ1"},
                                {"label": "MMJ2", "value": "MMJ2"},
                                {"label": "PARE1", "value": "PARE1"},
                                {"label": "PARE2", "value": "PARE2"},
                                {"label": "PARE3", "value": "PARE3"},
                                {"label": "PLM1", "value": "PLM1"},
                                {"label": "PLM2", "value": "PLM2"},
                                {"label": "PLP1", "value": "PLP1"},
                                {"label": "PLP2", "value": "PLP2"},
                                {"label": "PLP3", "value": "PLP3"},
                                {"label": "PLP4", "value":"PLP4"},
                                {"label": "PTM", "value": "PTM"},
                                {"label": "SJI1", "value": "SJI1"},
                                {"label": "SJI2", "value": "SJI2"},
                                {"label": "SKG1", "value": "SKG1"},
                                {"label": "SKG2", "value": "SKG2"},
                                {"label": "SKG3", "value": "SKG3"},
                                {"label": "SPS", "value": "SPS"},
                            ]),
                    ], className="mb-3"
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Rute : ", html_for="rute"), 
                        dbc.Input(id="rute", placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Quantity : ", html_for="quantity"),
                        dbc.Input(id="quantity", placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.Label("Unit : ", html_for="unit"),
                        dbc.Select(id="unit",
                            options=[
                                {"label": "Bal", "value": "Bal"},
                                {"label": "Karton", "value": "Karton"},
                                {"label": "Pcs", "value": "Pcs"},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup(
                    [
                        dbc.Label("In Pcs : ", html_for="inpcs"),
                        dbc.Input(id="inpcs", placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("In Ctn : ", html_for="inctn"),
                        dbc.Input(id="inctn", placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Subtotal : ", html_for="subtotal"),
                        dbc.Input(id="subtotal", placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Dpp : ", html_for="dpp"),
                        dbc.Input(id="dpp", placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("PPn : ", html_for="ppn"),
                        dbc.Input(id="ppn", placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Total : ", html_for="total"),
                        dbc.Input(id="total", placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Tanggal Pengantaran : ", html_for="tglantar"), 
                        dbc.Input(id="tglantar", placeholder="Date", type="date")
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Driver : ", html_for="driver"), 
                        dbc.Input(id="driver", placeholder="")
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Helper : ", html_for="helper"), 
                        dbc.Input(id="helper", placeholder="")
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Label("Nama Sales : ", html_for="namasales"), 
                        dbc.Input(id="namasales", placeholder="")
                    ],
                    className="mb-3",
                ),
                 dbc.InputGroup(
                    [
                        dbc.Label("Station Id : ", html_for="stationid"),
                        dbc.Input(id="stationid", placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
            ], className='inputpo', id="output"),

            html.Div(
                [
                    dbc.Button("Simpan",type="submit", color="primary", className="me-1", id='button-kirim'),
                    dbc.Button("Reset", color="danger", className="me-1"),
                ], className="buttonpo"
            ),

            html.Div(id="placeholder")   
        ]),
    ]),    
])


# route to get data from html form and insert data into database
@server.route('/data', methods=["GET", "POST"])
def data():
    data = {}
    if request.method == "POST":
        data['sales_no'] = request.form['nomorsales']
        # data['trans_date'] = request.form['transdate']
        data['tahun'] = request.form['tahun']
        data['bulan'] = request.form['bulan']
        data['hari'] = request.form['hari']
        data['order_date'] = request.form['tgltransaksi']
        data['gudang'] = request.form['gudang']
        data['depo'] = request.form['depo']
        data['cust_id'] = request.form['custid']
        data['company_name'] = request.form['companyname']
        data['address_1'] = request.form['alamat']
        data['prov'] = request.form['provinsi']
        data['kota'] = request.form['kota']
        data['kec'] = request.form['kecamatan']
        data['outlet_cat'] = request.form['outletcat']
        data['outlet_type'] = request.form['outlettype']
        data['outlet_group'] = request.form['outletgroup']
        data['sales_visit'] = request.form['salesvisit']
        data['stock_id'] = request.form['stockid']
        data['scode'] = request.form['scode']
        data['stock_name'] = request.form['stockname']
        data['brand'] = request.form['brand']
        data['stock_cat'] = request.form['stockcat']
        data['supplier'] = request.form['supplier']
        data['salesman'] = request.form['salesman']
        data['team'] = request.form['team']
        data['rute'] = request.form['rute']
        data['qty'] = request.form['quantity']
        data['unit'] = request.form['unit']
        data['in_pcs'] = request.form['inpcs']
        data['in_ctn'] = request.form['inctn']
        data['subtotal'] = request.form['subtotal']
        data['dpp'] = request.form['dpp']
        data['PPn'] = request.form['ppn']
        data['total'] = request.form['total']
        data['delivered_date'] = request.form['tglantar']
        data['driver'] = request.form['driver']
        data['helper1'] = request.form['helper']
        data['station_id'] = request.form['stationid']
        
        mydb.DataPenjualan222.insert_one(data)



