########################################################
# Copyright © Growing Data Pty Ltd, Australia
# AUTHOR: Michael-James Coetzee, Amit Wats
# EMAIL: mj@growingdata.com.au, amit@growingdata.com.au
########################################################


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

## The file GeneratTiles.py generated the .geojson files that contain the tile GPS coordinates (in the geometries folder) and tile .png images (in the tiles folder)  

with open(FULL_IMAGE_GEOMETRY) as f:
    pic = json.load(f)["geometry"]

fullImage=Image.open(FULL_IMAGE_PATH)
fullImageWidth,fullImageHeight = fullImage.size


#we will have 2 lines across and down.
# so staring in top left corner each datetime and denotiong p as 512/dimension(fullImageWidth or fullImageHeight depending)
# go right p portrion across TR tile, down p portion to get BL tile and go portion across followed by p portion down to get BR tile
#note: assumption pictures are squares! Check lines for parallel
# approach scale in x p portion of (x2-x1) and for y scale p portion of (y2-y1) at the started off set of (x1,y1) + current_tile_offset *scale across approach*

top_left_lat_long=tuple([k for k in pic['coordinates'][0][0]])
top_right_lat_long=tuple([k for k in pic['coordinates'][0][1]])
bottom_right_lat_long=tuple([k for k in pic['coordinates'][0][2]])
bottom_left_lat_long=tuple([k for k in pic['coordinates'][0][3]])

def saveGeo(TL,TR,BR,BL,x_bit,y_bit):
    point_TL=geometry.Point(TL[0],TL[1])
    point_TR=geometry.Point(TR[0],TR[1])
    point_BR=geometry.Point(BR[0],BR[1])
    point_BL=geometry.Point(BL[0],BL[1])
    tile= geometry.Polygon([p.x,p.y] for p in [point_TL,point_TR,point_BR,point_BL])
    tile_geoseries=gpd.GeoSeries([tile])
    tile_gpd= gpd.GeoDataFrame(geometry=tile_geoseries)
    tile_gpd.crs = {'init': 'epsg:4326', 'no_defs': True}
    tile_gpd.to_file(GetGeoJSONName(x_bit,y_bit), driver="GeoJSON")

# the GeoLibrary file uses a convention where the
# latitute and longitute are in opposite orders
# This function heps swap the position while passing parameters
# As well as when results from the library are returned


def CreateCroppedImage(coords):
    tile=fullImage.crop((coords[0][0],coords[0][1],coords[2][0],coords[2][1]))
    # top, left, down, right
    tile.save(GetTileName(coords[0][0],coords[0][1]))

def GetFourPositions(x,y):
    top_left_pos=(GRID_WIDTH*x,GRID_HEIGHT*y)
    top_right_pos=(GRID_WIDTH*(x+1)-1,GRID_HEIGHT*y)
    bottom_left_pos=(GRID_WIDTH*x,GRID_HEIGHT*(y+1)-1)
    bottom_right_pos=(GRID_WIDTH*(x+1)-1,GRID_HEIGHT*(y+1)-1)
    return [top_left_pos,top_right_pos,bottom_right_pos, bottom_left_pos]

def GetLatLongForCoords(x,y):
    angle=0
    if x!=0:
        angle=math.atan(y/x)
    else:
        angle=1.570796 # 90 degrees in radians
        
    bearing=GetBearing(swapLatLon(top_left_lat_long),swapLatLon(top_right_lat_long))
    total_bearing=(bearing+degrees(angle) + 360) % 360
    
    
    distance_hor=GetDistanceMeters(swapLatLon(top_left_lat_long),swapLatLon(top_right_lat_long))
    distance_ver=GetDistanceMeters(swapLatLon(top_left_lat_long),swapLatLon(bottom_left_lat_long))
    distance_x=distance_hor/fullImageWidth*x
    distance_y=distance_ver/fullImageHeight*y
    distance_from_top_left=sqrt(distance_x**2+distance_y**2)
    retLatLon=GetLatLongFromPointBearingDistance(
        swapLatLon(top_left_lat_long),total_bearing,distance_from_top_left)
    return swapLatLon(retLatLon)


# Can be invoked externally to generate the
# Geo JSON of the x'th and y'th square position
def GenerateAndSaveTileGeo(x,y):
    fourLatLongPositions=[GetLatLongForCoords(r[0],r[1]) for r in GetFourPositions(x,y)]
    saveGeo(fourLatLongPositions[0],fourLatLongPositions[1],
            fourLatLongPositions[2],fourLatLongPositions[3],x*GRID_WIDTH,y*GRID_HEIGHT)
    fourCoordinates=GetFourPositions(x,y)
    CreateCroppedImage(fourCoordinates)


start=time.time()

with open(SUGAR_JSON_PATH) as f:
    features = json.load(f)["features"]
    
    
# The main method generates the GEO JSON files in the configured
# folder
if __name__ == "__main__":
    im = Image.open(FULL_IMAGE_PATH)
    numOfXSquares=fullImageWidth//GRID_WIDTH
    numOfYSquares=fullImageHeight//GRID_HEIGHT
    im = Image.open(FULL_IMAGE_PATH)
    print("Generating files ......") # only crop the TCI full image
    [GenerateAndSaveTileGeo(x,y) for y in range(numOfYSquares) for x in range(numOfXSquares)]
    print("File Generation completed")


########################################################
# Copyright © Growing Data Pty Ltd, Australia
# AUTHOR: Michael-James Coetzee, Amit Wats
# EMAIL: mj@growingdata.com.au, amit@growingdata.com.au
########################################################

## The file GenerateMaskFiles.py generated the .png files that 
## contain the tile with non-sugar areas masked 
## (Tile generation must be completed first)


RAWNESS=1 #this is used in generating the mask image.
# RAWNESS For production is 1.
# For testing it can vary betwen 1 to 6
# Increasing it generates the mask faster with lots of parts missed out
# varying it makes it human eye testable
# When using for generation SHOULD BE 1




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

    tile=geometry.GeometryCollection(
        [geometry.shape(feature["geometry"]).buffer(0) for feature in geo_json_features])
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

    ranStartX=3
    ranEndX=4
    ranStartY=2
    ranEndY=3

    #the 512 by 512 bit tiles make for 21 rows and 21 columns in the case of sentinel 2a images.

    for x in range(ranStartX,ranEndX):
        for y in range(ranStartY,ranEndY):
            posX=x
            posY=y
            xCoord=posX*GRID_WIDTH
            yCoord=posY*GRID_HEIGHT
            tileName=GetTileBandName(xCoord,yCoord,band='tci',date='2016-12-22')
            GeoJsonFile=GetGeoJSONName(xCoord,yCoord)
            maskOutput=GetMaskName(xCoord,yCoord)
            print("All Names", posX,posY,tileName,GeoJsonFile,maskOutput)
            GenerateMask(posX,posY,tileName,GeoJsonFile,maskOutput)
            print("Generated Mask of {0} and {1} tiles ".format(x,y))
    end=time.time()
    print("execution time is", end-start)







