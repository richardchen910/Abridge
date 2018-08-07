#Google Maps API
#Richard Chen

import urllib.request
import urllib.parse
import json

GOOGLE_API_KEY = "AIzaSyB7P-s1-zTel589B_Ngcttl2RDKQ2nFhFg"

def build_place_id_url(location: str) -> str:
    """
    Takes a location (as a string) and returns a URL containing the place ID of the location
    """
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    query_parameters = [("input", location), ("inputtype", "textquery"), ("key", GOOGLE_API_KEY)]
    return base_url + "?" + urllib.parse.urlencode(query_parameters)


def build_place_details_url(place_id: str) -> str:
    """
    Takes a place-id and returns a URL containing details about the location
    """
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    query_parameters = [("placeid", place_id), ("key", GOOGLE_API_KEY)]
    return base_url + "?" + urllib.parse.urlencode(query_parameters)


def build_results_url(lat: float, lng: float, query: str) -> str:
    """
    Takes a query and the start location's lat/lng and encodes the parameters
    into a valid URL format, returns a URL containing location results from the search
    """ 
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query_parameters = [("query", query), ("location", str(lat) + "," + str(lng)), ("radius", 5000), ("key", GOOGLE_API_KEY)]
    return base_url + "?" + urllib.parse.urlencode(query_parameters)


def build_directions_url(origin: str, destination: str, travel_mode: str) -> str:
    """
    Takes two locations and a travel mode and encodes the parameters into a valid URL
    format, returns a URL containing data about the route betwen the two locations
    """
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    query_parameters = [("origin", origin), ("destination", destination), ("mode", travel_mode), ("key", GOOGLE_API_KEY)]
    return base_url + "?" + urllib.parse.urlencode(query_parameters)


def build_directions_map_url(origin: str, destination: str, travel_mode: str) -> str:
    """
    Takes two locations and a travel mode and encodes the parameters into a valid URL
    format, returns a URL that displays the route as a map
    """
    base_url = "https://www.google.com/maps/embed/v1/directions"
    query_parameters = [("key", GOOGLE_API_KEY), ("origin", origin), ("destination", destination), ("mode", travel_mode)]
    return base_url + "?" + urllib.parse.urlencode(query_parameters)


def build_street_map_url(lat: float, lng: float) -> str:
    """
    Takes the lat/lng of a location and encodes the parameters into a valid URL
    format, returns a URL that displays the street view of that location
    """
    base_url = "https://www.google.com/maps/embed/v1/streetview"
    query_parameters = [("key", GOOGLE_API_KEY), ("location", str(lat) + "," + str(lng))]
    return base_url + "?" + urllib.parse.urlencode(query_parameters)


def get_json_data(url: str) -> {"json text"}:
    """
    Takes a URL and returns the content of the parsed json text; the parsed
    json text is a dictionary
    """
    response = None
    try:
        response = urllib.request.urlopen(url)
        json_data = response.read().decode(encoding="utf-8")
        return json.loads(json_data) #parsed json data
    finally:
        if response != None:
            response.close()
