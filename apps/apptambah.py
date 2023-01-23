# import necessary modules
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table as dt
import dash_daq as daq
import dash_bootstrap_components as dbc

from flask import Flask, request, render_template
from pymongo import MongoClient

from app import app

# define the mongodb client
client = MongoClient(port=27017)
# define the database to use
# db = client.student_data
db = client.Datacoba

# define the flask app
server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


layout = html.Div([
    html.Div([
        html.Label('PT. Pelita Terang Makmur merupakan sebuah perusahaan yang bergerak pada bidang distributor makanan, yang dimana memiliki beberapa cabang di area sulselbar dan sulawesi tenggara' , style={'position': 'relative',  'width' : '80%', 'text-align' : 'justify', 'color' : 'white', 'left': '30px', 'top': '300px'}),
        html.Img(src=app.get_asset_url('imgside.png'), style={'position': 'relative', 'width': '110%', 'left': '-15px', 'top': '320px'}),
        html.Hr(id='hrside', style={'position': 'relative', 'color' : 'white', 'width': '80%', 'height': '2px', 'left': '30px', 'top': '-165px'})
        # html.H1(children='ADMIN', style={'font-size':'17px'}),
    ], className='side_bar'),
])


# define the home page route
@server.route('/')
def hello_world():
    return render_template("index.html")


# route to get data from html form and insert data into database
@server.route('/data', methods=["GET", "POST"])
def data():
    data = {}
    if request.method == "POST":
        data['Name'] = request.form['name']
        data['Email'] = request.form['email']
        data['Age'] = request.form['age']
        data['DOB'] = request.form['dob']
        data['Department'] = request.form['department']
        data['Gender'] = request.form['gender']
        data['Address'] = request.form['address']
        data['Pincode'] = request.form['pincode']
        lang = []
        for i in "1234567":
            try:
                if request.form['language' + i] != "":
                    lang.append(request.form['language' + i])
            except Exception as e:
                pass
        data['Language'] = lang
        db.datainput.insert_one(data)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=False)
