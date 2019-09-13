########################################################
# Copyright © Growing Data Pty Ltd, Australia 
# AUTHOR: Michael-James Coetzee, Amit Wats
# EMAIL: mj@growingdata.com.au, amit@growingdata.com.au
########################################################

import math
import geopy.distance
from geopy.distance import vincenty

def GetBearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def GetDistanceMeters(lat_long_point1, lat_long_point2):
    return geopy.distance.geodesic(lat_long_point1, lat_long_point2).meters

def GetLatLongFromPointBearingDistance(lat_long_point,bearing,distance):
    retVal=geopy.distance.geodesic(meters=distance).destination(lat_long_point,bearing)
    return retVal

if __name__ == "__main__":
    lat_long_a=(-19.893321306346,147.9552989984)
    lat_long_b=(-19.884605137462 ,149.00386329475)
    lat_long_d=(-20.876176661406,149.01671779369 )

    print("We are here")
    bearing=GetBearing(lat_long_a,lat_long_b)
    print("The Bearing is {0}".format(bearing))

    d1=GetDistanceMeters(lat_long_a,lat_long_b)
    d2=GetDistanceMeters(lat_long_b,lat_long_d)

    print("The Distance is {0}".format(d1))
    print("The Distance is {0}".format(d2))
    print("The Area is {0}".format(d1*d2/1000000))
    print("Lat long of a ",lat_long_a)
    print("Lat long of b ",lat_long_b)
    print("Testing bearing alternat ", GetLatLongFromPointBearingDistance(lat_long_a,bearing,d1))
