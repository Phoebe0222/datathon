########################################################
# Copyright © Growing Data Pty Ltd, Australia
# AUTHOR: Michael-James Coetzee, Amit Wats
# EMAIL: mj@growingdata.com.au, amit@growingdata.com.au
########################################################

import json
from PIL import Image
from shapely import geometry
import os
import configparser as ConfigParser
import time
from GenerateGeoJSON import GetLatLongForCoords
from SugarUtils import *
from datetime import date

#Initialise the Config File
config = ConfigParser.ConfigParser()
config.read('geo.config')

SUGAR_JSON=config.get('Master Image', 'MASTER_SUGAR_DATA_GEOJSON_PATH')
GRID_WIDTH=int(config.get('Master Image', 'GRID_WIDTH'))

GRID_HEIGHT=int(config.get('Master Image', 'GRID_HEIGHT'))
TILE_IMAGE_FOLDER=config.get('Master Image', 'TILE_IMAGE_FOLDER')
MASK_IMAGE_FOLDER=config.get('Master Image', 'MASK_IMAGE_FOLDER')
GEO_JSON_FOLDER=config.get('Master Image', 'GEO_JSON_FOLDER')


RAWNESS=1 #this is used in generating the mask image.
# RAWNESS For production is 1.
# For testing it can vary betwen 1 to 6
# Increasing it generates the mask faster with lots of parts missed out
# varying it makes it human eye testable
# When using for generation SHOULD BE 1


start=time.time()

with open(SUGAR_JSON) as f:
  features = json.load(f)["features"]

##################################################################################
# GenerateMask(tileXPos,tileYPos,tileImageFilePath,geoJSONPath,outputFileName):
##################################################################################
# This is the key method to generate masks. It generates one mask in the
# specified location by reading from theGEO_JSON_FOLDER given locations
# tileXPos= the X position of the grid fGEO_JSON_FOLDERrom top left. first grid=0, second grid=1, etc
# tileYPos= the Y position of the grid fGEO_JSON_FOLDERrom top left. first grid=0, second grid=1, etc

def GenerateMask(tileXPos,tileYPos,tileImageFilePath,geoJSONPath,outputFileName):
    with open(geoJSONPath) as f:
      geo_json_features = json.load(f)["features"]

    tile=geometry.GeometryCollection([geometry.shape(feature["geometry"]).buffer(0) for feature in geo_json_features])
    img = Image.open(tileImageFilePath)

    pixels=img.load()





    result=geometry.GeometryCollection()

    for k in features:
        if geometry.shape(k["geometry"]).intersects(tile):
            result=result.union(geometry.shape(k["geometry"]).intersection(tile))
    if tile. intersects(result):
        for i in range(0,img.size[0],RAWNESS):
            for j in range(0,img.size[1],RAWNESS):
                lat_long=GetLatLongForCoords(GRID_WIDTH*(tileXPos)+i,GRID_HEIGHT*(tileYPos)+j)
                if result.intersects(geometry.Point(lat_long)):
                    pixels[i,j]=(0,0,0)
        img.save(outputFileName)




if __name__ == "__main__":

    ranStartX=0
    ranEndX=21
    ranStartY=0
    ranEndY=21
    #the 512 by 512 bit tiles make for 21 rows and 21 columns in the case of sentinel 2a images.

    for x in range(ranStartX,ranEndX):
        for y in range(ranStartY,ranEndY):
            posX=x
            posY=y
            xCoord=posX*GRID_WIDTH
            yCoord=posY*GRID_HEIGHT
            tileName=GetTileName(xCoord,yCoord)
            GeoJsonFile=GetGeoJSONName(xCoord,yCoord)
            maskOutput=GetMaskName(xCoord,yCoord)
            print("All Names", posX,posY,tileName,GeoJsonFile,maskOutput)
            GenerateMask(posX,posY,tileName,GeoJsonFile,maskOutput)
            print("Generated Mask of {0} and {1} tiles ".format(x,y))
    end=time.time()
    print("execution time is", end-start)
