<<<<<<< HEAD
from flask import Flask, render_template, session
import googlemaps
=======
from flask import Flask, render_template
>>>>>>> c306ccaa08084bd8f50ebc44f7108afaadb58c25

app = Flask(__name__)
app.secret_key = "SECRET"

###############################################
# Routes

@app.route('/')
def home():
	return render_template('base.html')

@app.route('/locate', methods=["POST"])
def locate_user():
	""" uses google maps geocode to get lat/lon of address"""

	gmapKey = os.environ.get('Google_Maps_API_Key')
	gmaps = googlemaps.Client(key=gmapKey)

	address = request.form.get("address")
	
	# Geocoding and address
	geocode_result = gmaps.geocode(address)

	#parse the geocode result to get lat/long
	geocode_info = geocode_result[0]
	geometry = geocode_info.get('geometry')
	location_data = geometry.get("location")
	
	latitude = location_data.get('lat')
	longitude = location_data.get('lng')
	radius = request.form.get("radius")
	
	return latitude, longitude, radius


###############################################
# Main

if __name__ == '__main__':
	app.run(debug=True)