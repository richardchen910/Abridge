#Easy Maps Data
import re

class StartAddress:
    """
    The start address of the trip, contains __init__ and calculate methods
    """
    def __init__(self, json_object):
        """
        Creates an attribute holding a json object
        """
        self._json_object = json_object

    def calculate(self) -> str:
        """
        Returns the start address from the json object
        """
        return self._json_object["routes"][0]["legs"][0]["start_address"]


class EndAddress:
    """
    The end address of the trip, contains __init__ and calculate methods
    """
    def __init__(self, json_object):
        """
        Creates an attribute holding a json object
        """
        self._json_object = json_object

    def calculate(self) -> str:
        """
        Returns the end address from the json object
        """  
        return self._json_object["routes"][0]["legs"][0]["end_address"]


class Directions:
    """
    Directions object, contains __init__ and calculate methods
    """
    def __init__(self, json_object):
        """
        Creates an attribute holding a json object
        """
        self._directions = []
        self._json_object = json_object

    def calculate(self) -> list:
        """
        Retrieves the directions from the json object and returns a list of the directions
        """
        route = self._json_object["routes"][0]["legs"][0]
        for step in route["steps"]:
            instruction = step["html_instructions"]
            #instruction = re.sub('<div[^>]*>', ', ', instruction)   #remove starting <div> tags
            #instruction = re.sub('</div[^>]*>', '', instruction)   #remove ending </div> tags
            #instruction = re.sub('<[^>]*>', '', instruction)        #remove all other tags
            self._directions.append(instruction)
        return self._directions


class Distance:
    """
    TotalDistance object, contains __init__ and calculate methods
    """
    def __init__(self, json_object):
        """
        Creates an attribute holding a json object
        """
        self._json_object = json_object
        
    def calculate(self) -> float:
        """
        Returns the total distance from the json object as a float
        """
        return round(self._json_object["routes"][0]["legs"][0]["distance"]["value"] / 1609.34, 1)    #meters to miles, 2 sigfigs
                                                  

class Time:
    """
    TotalTime object, contains __init__ and calculate methods 
    """
    def __init__(self, json_object):
        """
        Creates an attribute holding a json object
        """
        self._json_object = json_object

    def calculate(self) -> int:
        """
        Returns the total time from the json object as an int
        """
        return round(self._json_object["routes"][0]["legs"][0]["duration"]["value"] / 60)      #seconds to minutes
    

"""
class LatLong:
    
    #LatLong object, contains __init__ and calculate methods
    
    def __init__(self, json_object):
        
        #Creates a list attribute to hold a list of latitude and longitude
        #pairs, also creates an attribute holding a json object
        
        self._lat_long_list = []
        self._json_object = json_object

    def calculate(self) -> None:
        
        #Retrieves the latitude and longitude from the json object as a float,
        #converts them to the proper notation, and prints the result
        
        locations = self._json_object["route"]["locations"]

        for i in range(len(locations)):
            lat = locations[i]["latLng"]["lat"]
            long = locations[i]["latLng"]["lng"]
            lat, long = self._convert_notation(lat, long)
            self._lat_long_list.append((lat, long))
        return self._lat_long_list

    def _convert_notation(self, lat: float, long: float) -> ("lat", "long"):
        
        #Converts the latitude and longitude to the proper notation (North,
        #South, East, West) and returns the pair
        
        if lat < 0:
            lat = str(round(abs(lat), 2)) + "S"
        else:
            lat = str(round(lat, 2)) + "N"

        if long < 0:
            long = str(round(abs(long), 2)) + "W"
        else:
            long = str(round(long)) + "E"

        return lat, long
"""
            
