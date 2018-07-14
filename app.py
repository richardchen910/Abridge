from flask import Flask, render_template, request
import easy_maps_ui


app = Flask(__name__)

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
		maps_url = easy_maps_ui.get_maps_url(origin, destination, travel_mode)
		return render_template('submit.html', data=data, maps_url=maps_url)

	





if __name__ == "__main__":
	app.run(debug=True)