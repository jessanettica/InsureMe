from flask import Flask, render_template, request, redirect, flash, session, jsonify
import os
import googlemaps
from betterdocinfo import build_ins_json


app = Flask(__name__)
app.secret_key = "SECRET"

###############################################
# Routes

@app.route('/')
def home():
	return render_template('base.html')


@app.route('/locate', methods=["POST"])
def locate_user():
	""" uses google maps geocode to get lat/long of address inputted by user & the distance from address to search (radius)"""

	gmapKey = os.environ.get('Google_Maps_API_Key')
	gmaps = googlemaps.Client(key=gmapKey)
	address = request.form.get("address")
	print "************ address"

	# Geocoding and address
	geocode_result = gmaps.geocode(address)

	#parse the geocode result to get lat/long
	geocode_info = geocode_result[0]
	geometry = geocode_info.get('geometry')
	location_data = geometry.get("location")
	
	latitude = location_data.get('lat')
	longitude = location_data.get('lng')
	#input from user on radius from location to look at
	radius = request.form.get("radius")

	#store location info needed in dictionary
	session["lat"] = latitude
	session["long"] = longitude
	session["radius"] = radius

	return "success"


@app.route('/donut_docs.json', methods=["GET"])
def make_doc_donut():

	latitude = session.get('lat')
	longitude = session.get('long')
	radius = session.get('radius')

	address_dict = build_ins_json(latitude,longitude,radius)

	return jsonify(address_dict)


###############################################
# Main

if __name__ == '__main__':
	app.run(debug=True)