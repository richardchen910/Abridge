from flask import Flask, render_template, request
import easy_maps_ui

app = Flask(__name__)

app.secret_key = '7723af75fdfbab5656f0ca1b2187878f'


@app.route('/')
def index():
	return render_template('home.html')


@app.route('/submit', methods=['POST'])
def input():
	# User input
	location = request.form['location']
	query = request.form['query']
	travel_mode = request.form['travel_mode']
	# Get place id and get lat/lng of place to get list of locations matching user's search 
	place_id = easy_maps_ui.get_place_id(location)["candidates"][0]["place_id"]
	place_details = easy_maps_ui.get_place_details(place_id)
	place_lat = place_details["result"]["geometry"]["location"]["lat"]
	place_lng = place_details["result"]["geometry"]["location"]["lng"]
	destination = easy_maps_ui.get_results(place_lat, place_lng, query, travel_mode, location)
	#Get name of destination
	destination_place_id = easy_maps_ui.get_place_id(query + " " + destination)["candidates"][0]["place_id"]
	destination_name = easy_maps_ui.get_place_details(destination_place_id)["result"]["name"]
	# Get output
	data = easy_maps_ui.run_application(location, destination, travel_mode)
	directions_map_url = easy_maps_ui.get_directions_map_url(location, destination, travel_mode)
	start_lat = data["latlng"]["start"]["lat"]
	start_lng = data["latlng"]["start"]["lng"]
	end_lat = data["latlng"]["end"]["lat"]
	end_lng = data["latlng"]["end"]["lng"]
	start_street_map_url = easy_maps_ui.get_street_map_url(start_lat, start_lng)
	end_street_map_url = easy_maps_ui.get_street_map_url(end_lat, end_lng)
	return render_template('submit.html', data=data, destination_name=destination_name, directions_map_url=directions_map_url, start_street_map_url=start_street_map_url, end_street_map_url=end_street_map_url)



if __name__ == "__main__":
	app.run(debug=True)