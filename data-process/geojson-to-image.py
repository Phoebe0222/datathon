# generates user defined polygon image cut from full image
# example with tci fullimage, and testing.geojson 

import json
from PIL import Image
from shapely import geometry
import geopandas as gpd
import pandas as pd
import numpy as np
import os
from math import atan,degrees,sqrt
import configparser as ConfigParser
import time
from datetime import date

from GeoLibrary import *

#Prevent Image from throwing warning as the
#Image File is Big
Image.MAX_IMAGE_PIXELS = 1000000000

#Initialise the Config File
config = ConfigParser.ConfigParser()
config.read('geo.config')


GRID_WIDTH=int(config.get('Master Image', 'GRID_WIDTH'))
GRID_HEIGHT=int(config.get('Master Image', 'GRID_HEIGHT'))

FULL_IMAGE_GEOMETRY=config.get('Master Image', 'FULL_GEOMETRY_PATH')
FULL_IMAGE_PATH=config.get('Master Image', 'FULL_IMAGE_PATH')
SUGAR_JSON_PATH=config.get('Master Image', 'MASTER_SUGAR_DATA_GEOJSON_PATH')
TILE_IMAGE_FOLDER=config.get('Master Image', 'TILE_IMAGE_FOLDER')
MASK_IMAGE_FOLDER=config.get('Master Image', 'MASK_IMAGE_FOLDER')
GEO_GEOMETRY_OUTPUT_FOLDER=config.get('Master Image', 'GEO_JSON_FOLDER')
USER_POLYGON_PATH=config.get('Others', 'USER_POLYGON_PATH')


fullImage=Image.open(FULL_IMAGE_PATH)

with open(USER_POLYGON_PATH) as f:
    features = json.load(f)["features"]
    
    
# coordinates
polygon=features[0]
coords=polygon.get("geometry").get("coordinates")

# pixel index 
def GetFourPositions(x,y):
    top_left_pos=(GRID_WIDTH*x,GRID_HEIGHT*y)
    top_right_pos=(GRID_WIDTH*(x+1)-1,GRID_HEIGHT*y)
    bottom_left_pos=(GRID_WIDTH*x,GRID_HEIGHT*(y+1)-1)
    bottom_right_pos=(GRID_WIDTH*(x+1)-1,GRID_HEIGHT*(y+1)-1)
    return [top_left_pos,top_right_pos,bottom_right_pos, bottom_left_pos]

coords=GetFourPositions(0,0)
print(coords)
print(coords[0][0],coords[0][1],coords[2][0],coords[2][1])


# using setinel2loader
import logging
import os
#from osgeo import gdal
import matplotlib.pyplot as plt
from sentinelloader import sentinel2loader
from shapely.geometry import Polygon

sl = sentinel2loader.Sentinel2Loader('/notebooks/data/output/sentinelcache', 
                    'phoebe0222', 'Lyw12345',
                    apiUrl='https://scihub.copernicus.eu/apihub/', showProgressbars=True, loglevel=logging.DEBUG)

area = Polygon([(-47.873796, -16.044801), (-47.933796, -16.044801),
        (-47.933796, -15.924801), (-47.873796, -15.924801)])

geoTiffs = sl.getRegionHistory(area, 'TCI', '60m', '2019-01-06', '2019-01-30', daysStep=5)
for geoTiff in geoTiffs:
    print('Desired image was prepared at')
    print(geoTiff)
    os.remove(geoTiff)

