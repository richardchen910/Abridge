#Abridge UI
#Richard Chen


import abridge_output
import abridge_api
import urllib.error
import math


def _get_place_id_json_object(location: str) -> {"json text"}:
    """
    Returns a json dictionary containing the place-id of a location given by the user
    """
    url = abridge_api.build_place_id_url(location)
    json_object = abridge_api.get_json_data(url)
    return json_object


def _get_place_details_json_object(place_id: str) -> {"json text"}:
    """
    Returns a json dictionary containing details of a location given by the user
    """
    url = abridge_api.build_place_details_url(place_id)
    json_object = abridge_api.get_json_data(url)
    return json_object


def _get_results_json_object(lat: float, lng: float, query: str) -> {"json text"}:
    """
    Returns a json dictionary containing  potential end locations given the start location and
    query given by the user
    """ 
    url = abridge_api.build_results_url(lat, lng, query)
    json_object = abridge_api.get_json_data(url)
    return json_object


def _get_directions_json_object(origin: str, destination: str, travel_mode: str) -> {"json text"}:
    """
    Returns a json dictionary containing information about the directions between the
    start and end locations given by the user
    """
    url = abridge_api.build_directions_url(origin, destination, travel_mode)
    json_object = abridge_api.get_json_data(url) #dict
    return json_object


def _create_output_objects(json_object: {"json text"}) -> ["output object"]:
    """
    Given the list of output requested by the user, creates a class object
    for each desired output and returns a list of those objects
    """
    output_objects = []
    output_objects.append(abridge_output.StartAddress(json_object))    
    output_objects.append(abridge_output.EndAddress(json_object))    
    output_objects.append(abridge_output.Directions(json_object))    
    output_objects.append(abridge_output.Time(json_object))
    output_objects.append(abridge_output.Distance(json_object))
    output_objects.append(abridge_output.LatLong(json_object))        
    return output_objects


def _get_output(output_objects: dict) -> None:
    """
    Calculates the output
    """
    data = dict()
    data["start_address"] = output_objects[0].calculate()   #StartAddress
    data["end_address"] = output_objects[1].calculate()     #EndAddress
    data["directions"] = output_objects[2].calculate()      #Directions
    data["time"] = output_objects[3].calculate()            #Time
    data["distance"] = output_objects[4].calculate()        #Distance
    data["latlng"] = output_objects[5].calculate()          #LatLong
    return data
        

def get_place_id(location: str) -> str:
    return _get_place_id_json_object(location)


def get_place_details(place_id: str) -> str:
    return _get_place_details_json_object(place_id)


def get_results(lat: float, lng: float, query: str, travel_mode: str, origin: str) -> "destination":
    """
    Takes the lat/lng of the start location and the query to get a list of end locations related to
    the user's input. The list of end locations is sorted based on distance from the start location,
    the first one being the location closest to the start location. The first location in
    the list is returned
    """
    sorted_results = dict()
    results = _get_results_json_object(lat, lng, query)["results"]
    min_distance = math.inf
    for i in range(len(results)):
        destination = results[i]["formatted_address"]
        directions_json_object = _get_directions_json_object(origin, destination, travel_mode)
        distance = directions_json_object["routes"][0]["legs"][0]["distance"]["value"] / 1609.34
        if distance < min_distance:
            sorted_results[results[i]["formatted_address"]] = distance
            min_distance = distance
    return sorted(sorted_results, key=(lambda location : sorted_results[location]))[0]


def get_directions_map_url(origin: str, destination: str, travel_mode: str) -> str:
    return abridge_api.build_directions_map_url(origin, destination, travel_mode)


def get_street_map_url(lat: float, lng: float) -> str:
    return abridge_api.build_street_map_url(lat, lng)


def run_application(origin: str, destination: str, travel_mode: str) -> ["Directions", "TotalTime", "TotalDistance", "LatLong"]:
    try:
        directions_json_object = _get_directions_json_object(origin, destination, travel_mode)
        output_objects = _create_output_objects(directions_json_object)
        data = _get_output(output_objects)
        return data

    except IndexError:
        print("NO ROUTE FOUND")
        return None
    except KeyError:
        print("NO ROUTE FOUND")
        return None
    except urllib.error.URLError:
        print("GOOGLE_MAPS ERROR")
        return None
    except urllib.error.HTTPError:
        print("GOOGLE_MAPS ERROR")
        return None
    except urllib.error.ContentTooShortError:
        print("GOOGLE_MAPS ERROR")
        return None
    
        
