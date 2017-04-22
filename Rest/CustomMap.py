import googlemaps
from datetime import datetime

threshold = 20*60;


class CustomMap:

    def __init__(self):
        self.gmaps = googlemaps.Client(key='AIzaSyAgGPjJkn2YgzkAAngqD1ghfTqv9pu2KEs')

    @staticmethod
    def show_values(dict_value):
        """read dictionary values"""
        for key in dict_value.keys():
            print dict_value[key],key

    @staticmethod
    def is_duration_matching(dur1, dur2):
        """Compare durations"""
        dur1_value = dur1[0]['legs'][0]['duration']['value']
        dur2_value = dur2[0]['legs'][0]['duration']['value']
        if abs(dur1_value - dur2_value) <= threshold:
            return [True,dur1_value - dur2_value]
        return [False]


    def get_directions(self,source,destination,mode):
        return self.gmaps.directions(source,
                                 destination,
                                 mode=mode,
                                 departure_time=datetime.now())

    def get_map_polygon(self,source,destination):
        # type: (object, object) -> object
        result = {}
        driving = self.get_directions(source, destination, mode="driving")
        bicycle = self.get_directions(source, destination, mode="bicycling")
        diff = self.is_duration_matching(driving, bicycle) if len(bicycle) >0 else [False]
        if len(driving) > 0:
            result["driving"] = driving[0]
            result["driving"]["time"] = 0
        if diff[0]:
            result["bicycling"] = bicycle[0]
            result["bicycling"]["time"] = diff[1]
        walking = self.get_directions(source, destination, mode="walking")
        diff = self.is_duration_matching(driving, walking) if len(walking) >0 else [False]
        if diff[0]:
            result["walking"] = walking[0]
            result["walking"]["time"] = diff[1]
        transit = self.get_directions(source,destination, mode="transit")
        diff = self.is_duration_matching(driving, transit) if len(transit) >0 else [False]
        if diff[0]:
            result["transit"] = transit[0]
            result["transit"]["time"] = diff[1]

        return result

if __name__ == "__main__":
    gmap = CustomMap()
    CustomMap.show_values(gmap.get_map_polygon("Arlington, Texas","818 Avenue H E, Arlington, TX 76011"))