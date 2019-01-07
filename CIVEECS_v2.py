from flask import Flask, url_for, redirect, render_template, request, Response
from datascience import *
import numpy as np
import pandas
from geopy.geocoders import Nominatim
import pymapd




# API Connection
mapdhost = 'use2-api.mapd.cloud'
mapdport = '443'
mapduser = 'KA36D70AB09E04A57852'
mapdpass = 'tZbCgQGZJKd4M0N6Cy9eTvbYWtEYYFaXh2UhgBGw'
mapddbname = 'mapd'
mapdprotocol = 'https'
mapdtable = 'san_francisco_taz2'
mapdcon = pymapd.connect(user=mapduser, password=mapdpass, host=mapdhost, dbname=mapddbname, port=mapdport, protocol=mapdprotocol)
geolocator = Nominatim()

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    somedata = "new_Data"
    return render_template('index.html')

@app.route("/", methods=['POST'])
def data():
    return redirect(url_for('Calculate'), code=307)
    pass

@app.route('/Calculate/', methods = ["POST"])
def Calculate():
    print(request.form['location'])
    # Get addresses input by users
    location = request.form['location']
    location2 = request.form['location2']
    # Used to translate address to coordinates adnt then to taz using sf_taz_data for the first user input address
    location_refined = geolocator.geocode(location)
    helper = {'long':location_refined.longitude,'lat':location_refined.latitude}
    query  = "SELECT MOVEMENT_ID FROM san_francisco_taz2 WHERE ST_CONTAINS(san_francisco_taz2.omnisci_geo, ST_GeomFromText('POINT(%(long)f %(lat)f)', 4326))" % helper
    df = mapdcon.execute(query)
    start_taz = list(df)[0]
    # Used to translate address to coordinates adnt then to taz using sf_taz_data for the second user input address
    location2_refined = geolocator.geocode(location2)
    helper2 = {'long':location2_refined.longitude,'lat':location2_refined.latitude}
    query2  = "SELECT MOVEMENT_ID FROM san_francisco_taz2 WHERE ST_CONTAINS(san_francisco_taz2.omnisci_geo, ST_GeomFromText('POINT(%(long)f %(lat)f)', 4326))" % helper2
    df2 = mapdcon.execute(query2)
    end_taz = list(df2)[0]
    helper3 = {'start':start_taz,'end':end_taz}
    #needed to hardcode because the api query would't return a tuple
    #df_final = mapdcon.execute("SELECT mov_hod, tt_mean FROM uber_movement_data1 WHERE sourceid = %(start)f AND dstid = %(end)f" % helper3)

    return render_template('Calculate.html', location=location, location2=location2)


if __name__ == '__main__':
	app.run(port=443, debug=True)
