#Easy Maps UI

import easy_maps_data
import easy_maps_api
import urllib.error


def _get_json_object(origin: str, destination: str, travel_mode: str) -> {"json text"}:
    """
    Gets and returns the content of a json format web page; the json text
    is a dictionary
    """
    url = easy_maps_api.build_directions_url(origin, destination, travel_mode)
    json_object = easy_maps_api.get_json_data(url) #dict
    return json_object


def _create_output_objects(json_object: {"json text"}) -> ["output object"]:
    """
    Given the list of output requested by the user, creates a class object
    for each desired output and returns a list of those objects
    """
    output_objects = []
    output_objects.append(easy_maps_data.StartAddress(json_object))    
    output_objects.append(easy_maps_data.EndAddress(json_object))    
    output_objects.append(easy_maps_data.Directions(json_object))    
    output_objects.append(easy_maps_data.Time(json_object))
    output_objects.append(easy_maps_data.Distance(json_object))
    #output_objects.append(easy_maps_data.LatLong(json_object))        
    return output_objects


def _get_output(output_objects: dict) -> None:
    """
    Calculates the output
    """
    data = dict()
    data["start_address"] = output_objects[0].calculate()     #StartAddress
    data["end_address"] = output_objects[1].calculate()      #EndAddress
    data["directions"] = output_objects[2].calculate()     #Directions
    data["time"] = output_objects[3].calculate()      #Time
    data["distance"] = output_objects[4].calculate()      #Distance
    #data.append(output_objects[3].calculate()      #LatLong
    return data
        
    
def get_maps_url(origin: str, destination: str, travel_mode: str) -> str:
    return easy_maps_api.build_maps_url(origin, destination, travel_mode)


def run_application(origin: str, destination: str, travel_mode: str) -> ["Directions", "TotalTime", "TotalDistance", "LatLong"]:
    try:
        json_object = _get_json_object(origin, destination, travel_mode)
        output_objects = _create_output_objects(json_object)
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
    
        
