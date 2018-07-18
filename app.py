from flask import Flask, render_template, request
import easy_maps_ui

app = Flask(__name__)

app.secret_key = '7723af75fdfbab5656f0ca1b2187878f'


@app.route('/')
def index():
	return render_template('home.html')


@app.route('/submit', methods=['POST'])
def input():
	error = set()

	origin = request.form['origin']
	destination = request.form['destination']
	if origin == "":
		error.add("Please enter a start location")
	if destination == "":
		error.add("Please enter a end location")
	if len(error) > 0:
		return render_template('home.html', error=error)
	try:
		travel_mode = request.form['travel_mode']
	except KeyError:
		error.add("Please select a mode of transportation")
		return render_template('home.html', error=error)
	else:
		data = easy_maps_ui.run_application(origin, destination, travel_mode)
		directions_map_url = easy_maps_ui.get_directions_map_url(origin, destination, travel_mode)
		start_lat = data["latlng"]["start"]["lat"]
		start_lng = data["latlng"]["start"]["lng"]
		end_lat = data["latlng"]["end"]["lat"]
		end_lng = data["latlng"]["end"]["lng"]
		start_street_map_url = easy_maps_ui.get_street_map_url(start_lat, start_lng)
		end_street_map_url = easy_maps_ui.get_street_map_url(end_lat, end_lng)
		return render_template('submit.html', data=data, directions_map_url=directions_map_url, start_street_map_url=start_street_map_url, end_street_map_url=end_street_map_url)
	





if __name__ == "__main__":
	app.run(debug=True)