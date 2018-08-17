#Abridge app
#Richard Chen

from flask import Flask, render_template, request, redirect, url_for, flash
import abridge_ui
import urllib.error

app = Flask(__name__)


@app.route('/') 
def index():
	return render_template('home.html')


@app.route('/submit', methods=['POST'])
def submit():
	# User input
	location = request.form['location']
	query = request.form['query']
	travel_mode = request.form['travel_mode']
	# Get place id and get lat/lng of place to get list of locations matching user's search 
	try:
		place_id = abridge_ui.get_place_id(location)["candidates"][0]["place_id"]
	except IndexError:
		flash('Location does not exist. Please enter a valid start location.', 'danger')
		return redirect(url_for('index'))
	except urllib.error.URLError:
		flash('Sorry, an error occurred. Please enter your search again.', 'danger')
		return redirect(url_for('index'))
	else:
		place_details = abridge_ui.get_place_details(place_id)
		place_lat = place_details["result"]["geometry"]["location"]["lat"]
		place_lng = place_details["result"]["geometry"]["location"]["lng"]
		try:
			destination = abridge_ui.get_results(place_lat, place_lng, query, travel_mode, location)
		except IndexError:
			flash('No results found. Please search for a different destination.', 'danger')
			return redirect(url_for('index'))
		else:
			#Get name of destination
			destination_place_id = abridge_ui.get_place_id(query + " " + destination)["candidates"][0]["place_id"]
			destination_name = abridge_ui.get_place_details(destination_place_id)["result"]["name"]
			# Get output
			data = abridge_ui.run_application(location, destination, travel_mode)
			directions_map_url = abridge_ui.get_directions_map_url(location, destination, travel_mode)
			start_lat = data["latlng"]["start"]["lat"]
			start_lng = data["latlng"]["start"]["lng"]
			end_lat = data["latlng"]["end"]["lat"]
			end_lng = data["latlng"]["end"]["lng"]
			start_street_map_url = abridge_ui.get_street_map_url(start_lat, start_lng)
			end_street_map_url = abridge_ui.get_street_map_url(end_lat, end_lng)
			return render_template('submit.html', data=data, destination_name=destination_name, directions_map_url=directions_map_url, start_street_map_url=start_street_map_url, end_street_map_url=end_street_map_url)



if __name__ == "__main__":
	app.run(debug=True)