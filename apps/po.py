import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
# from app import app

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div([

    html.Div([
        html.Img(src=app.get_asset_url('user.png'), style={'position': 'relative', 'width': '35px', 'left':'900px', 'top':'15px'}),
        dbc.NavLink("Dashboard", href="/apps/main", id='menumain'),
        dbc.NavLink("Input Data", href="/apps/po", id='input_data'),
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
                    html.H2("Input Data Penjualan"),
                    html.Hr(id='hrpo')
            ]),

            html.Div([
                dbc.InputGroup(
                    [dbc.InputGroupText("Nomor Sales"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [dbc.InputGroupText("Tanggal Transaksi"), dbc.Input(placeholder="Date", type="date")],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.InputGroupText("Gudang"),
                        dbc.Select(
                            options=[
                                {"label": "Bone", "value": 1},
                                {"label": "Bulukumba", "value": 2},
                                {"label": "Kolaka", "value": 3},
                                {"label": "Makassar", "value": 4},
                                {"label": "Mamuju", "value": 5},
                                {"label": "Mangkutana", "value": 6},
                                {"label": "Palopo", "value": 7},
                                {"label": "Pare-Pare", "value": 8},
                                {"label": "Polman", "value": 9},
                                {"label": "Sengkang", "value": 10},
                                {"label": "Sinjai", "value": 11},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup([
                        dbc.InputGroupText("Depo"),
                        dbc.Select(
                            options=[
                                {"label": "Bone", "value": 1},
                                {"label": "Bulukumba", "value": 2},
                                {"label": "Kolaka", "value": 3},
                                {"label": "Makassar", "value": 4},
                                {"label": "Mamuju", "value": 5},
                                {"label": "Mangkutana", "value": 6},
                                {"label": "Palopo", "value": 7},
                                {"label": "Pare-Pare", "value": 8},
                                {"label": "Polman", "value": 9},
                                {"label": "Sengkang", "value": 10},
                                {"label": "Sinjai", "value": 11},
                            ]),
                    ], className="mb-3"),
                
                dbc.InputGroup(
                    [dbc.InputGroupText("ID Pelanggan"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                 dbc.InputGroup(
                    [dbc.InputGroupText("Nama Usaha"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [dbc.InputGroupText("Alamat"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.InputGroupText("Provinsi"),
                        dbc.Select(
                            options=[
                                {"label": "Sulawesi Selatan", "value": 1},
                                {"label": "Sulawesi Barat", "value": 2},
                                {"label": "Sulawesi Tenggara", "value": 3},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup([
                        dbc.InputGroupText("Kabupaten/Kota"),
                        dbc.Select(
                            options=[
                                {"label": "Bantaeng", "value": 1},
                                {"label": "Barru", "value": 2},
                                {"label": "Bau-Bau", "value": 3},
                                {"label": "Bombana", "value": 4},
                                {"label": "Bone", "value": 5},
                                {"label": "Bulukumba", "value": 6},
                                {"label": "Enrekang", "value": 7},
                                {"label": "Gowa", "value": 8},
                                {"label": "Jeneponto", "value": 9},
                                {"label": "Kepulauan Selayar", "value": 10},
                                {"label": "Kolaka", "value": 11},
                                {"label": "Kolaka Timur", "value": 12},
                                {"label": "Kolaka Utara", "value": 13},
                                {"label": "Luwu", "value": 14},
                                {"label": "Luwu Timur", "value": 15},
                                {"label": "Luwu Utara", "value": 16},
                                {"label": "Majene", "value": 17},
                                {"label": "Makassar", "value": 18},
                                {"label": "Mamasa", "value": 19},
                                {"label": "Mamuju", "value": 20},
                                {"label": "Mamuju Tengah", "value": 21},
                                {"label": "Mamuju Utara", "value": 22},
                                {"label": "Maros", "value": 23},
                                {"label": "Palopo", "value": 24},
                                {"label": "Pangkajene Kepulauan", "value":25},
                                {"label": "Pare-Pare", "value": 26},
                                {"label": "Pinrang", "value": 27},
                                {"label": "Polewali Mandar", "value": 28},
                                {"label": "Sidenren Rappan", "value": 29},
                                {"label": "Sinjai", "value": 30},
                                {"label": "Soppeng", "value": 31},
                                {"label": "Takalar", "value": 32},
                                {"label": "Tana Toraja", "value": 33},
                                {"label": "Toraja Utara", "value": 34},
                                {"label": "Wajo", "value": 35},
                                
                            ]),
                    ], className="mb-3"
                ),
                dbc.InputGroup(
                    [dbc.InputGroupText("Kecamatan"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.InputGroupText("Outlet Cat"),
                        dbc.Select(
                            options=[
                                {"label": "GT", "value": 1},
                                {"label": "MT", "value": 2},
                            ]),
                    ], className="mb-3"),
                    dbc.InputGroup(
                    [dbc.InputGroupText("Tipe Outlet"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.InputGroupText("Kelompok Outlet"),
                        dbc.Select(
                            options=[
                                {"label": "Grosir", "value": 1},
                                {"label": "Minimarket", "value": 2},
                                {"label": "Retail", "value": 3},
                                {"label": "Supermarket", "value": 4},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup([
                        dbc.InputGroupText("Hari Kunjungan"),
                        dbc.Select(
                            options=[
                                {"label": "Senin", "value": 1},
                                {"label": "Selasa", "value": 2},
                                {"label": "Rabu", "value": 3},
                                {"label": "Kamis", "value": 4},
                                {"label": "Jumat", "value": 5},
                                {"label": "Sabtu", "value": 6},
                                {"label": "DOPIN PENEKI", "value": 7},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup(
                    [dbc.InputGroupText("ID Stok"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [dbc.InputGroupText("Scode"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.InputGroupText("Nama Stok"),
                        dbc.Select(
                            options=[
                                {"label": "BIHUN JAGUNG 12X300GR", "value": 1},
                                {"label": "BIHUN JAGUNG 24X150GR", "value": 2},
                                {"label": "BIHUN JAGUNG 60X60GR", "value": 3},
                                {"label": "BIHUN JAGUNG BIJAG LOS 4 KG", "value": 4},
                                {"label": "BIHUN JAGUNG PADAMU 175 GR / 24 PACK", "value": 5},
                                {"label": "BIHUN JAGUNG PADAMU 350 GR / 12 PACK", "value": 6},
                                {"label": "BIHUN JAGUNG PADAMU 60 GR / 60 PACK", "value": 7},
                                {"label": "BIJAG LOS 2 KG / 2 PACK", "value": 8},
                                {"label": "MIE KERING LANGIT BIRU 3KG", "value": 9},
                                {"label": "MIE KERING LANGIT BIRU 4PX750GR", "value": 10},
                                {"label": "MIE TELUR MIMORA 6X136GR", "value": 11},
                                {"label": "SOHUN KACA 18RX60GR", "value": 12},
                                {"label": "VIT SARI BAWANG 250 GR/20 PAK", "value": 13},
                                {"label": "VIT SARI BW ANK WARNA 5KG KRT", "value": 14},
                            ]),
                    ], className="mb-3"
                ),
                dbc.InputGroup([
                        dbc.InputGroupText("Brand"),
                        dbc.Select(
                            options=[
                                {"label": "Bihun", "value": 1},
                                {"label": "Mie Kering", "value": 2},
                                {"label": "Vitarasa", "value": 3},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup([
                        dbc.InputGroupText("Stok Cat"),
                        dbc.Select(
                            options=[
                                {"label": "Kerupuk", "value": 1},
                                {"label": "Mie Bihun", "value": 2},
                                {"label": "Mie Kering", "value": 3},
                                {"label": "NOODLE", "value": 4},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup([
                        dbc.InputGroupText("Supplier"),
                        dbc.Select(
                            options=[
                                {"label": "PT. SINAR PANGAN SEJAHTERA", "value": 1},
                                {"label": "PT. SINAR PANGAN SEJAHTERA / SAN", "value": 2},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup(
                    [dbc.InputGroupText("Nama Sales"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.InputGroupText("Team"),
                        dbc.Select(
                            options=[
                                {"label": "BLK1", "value": 1},
                                {"label": "BLK2", "value": 2},
                                {"label": "BONE1", "value": 3},
                                {"label": "BONE2", "value": 4},
                                {"label": "KLK1", "value": 5},
                                {"label": "KLK2", "value": 6},
                                {"label": "MKS1", "value": 7},
                                {"label": "MKS2", "value": 8},
                                {"label": "MKS3", "value": 9},
                                {"label": "MKS4", "value": 10},
                                {"label": "MKS5", "value": 11},
                                {"label": "MKS6", "value": 12},
                                {"label": "MKT1", "value": 13},
                                {"label": "MKT2", "value": 14},
                                {"label": "MMJ1", "value": 15},
                                {"label": "MMJ2", "value": 16},
                                {"label": "PARE1", "value": 17},
                                {"label": "PARE2", "value": 18},
                                {"label": "PARE3", "value": 19},
                                {"label": "PLM1", "value": 20},
                                {"label": "PLM2", "value": 21},
                                {"label": "PLP1", "value": 22},
                                {"label": "PLP2", "value": 23},
                                {"label": "PLP3", "value": 24},
                                {"label": "PLP4", "value":25},
                                {"label": "PTM", "value": 26},
                                {"label": "SJI1", "value": 27},
                                {"label": "SJI2", "value": 28},
                                {"label": "SKG1", "value": 29},
                                {"label": "SKG2", "value": 30},
                                {"label": "SKG3", "value": 31},
                                {"label": "SPS", "value": 32},
                            ]),
                    ], className="mb-3"
                ),
                dbc.InputGroup(
                    [dbc.InputGroupText("Rute"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Quantity"),
                        dbc.Input(placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup([
                        dbc.InputGroupText("Unit"),
                        dbc.Select(
                            options=[
                                {"label": "Bal", "value": 1},
                                {"label": "Karton", "value": 2},
                                {"label": "Pcs", "value": 3},
                            ]),
                    ], className="mb-3"),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("In Pcs"),
                        dbc.Input(placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("In Ctn"),
                        dbc.Input(placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Subtotal"),
                        dbc.Input(placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Dpp"),
                        dbc.Input(placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("PPn"),
                        dbc.Input(placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Total"),
                        dbc.Input(placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [dbc.InputGroupText("Tanggal Pengantaran"), dbc.Input(placeholder="Date", type="date")],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [dbc.InputGroupText("Driver"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [dbc.InputGroupText("Helper"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                dbc.InputGroup(
                    [dbc.InputGroupText("Nama Sales"), dbc.Input(placeholder="")],
                    className="mb-3",
                ),
                 dbc.InputGroup(
                    [
                        dbc.InputGroupText("Station Id"),
                        dbc.Input(placeholder="", type="number"),
                    ],
                    className="mb-3",
                ),
            ], className='inputpo'),

            html.Div(
                [
                    dbc.Button("Simpan", color="primary", className="me-1"),
                    dbc.Button("Reset", color="danger", className="me-1"),
                ], className="buttonpo"
            )
            
        ], className='main'),
    ]),    
])

