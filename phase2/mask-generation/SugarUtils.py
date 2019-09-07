########################################################
# Copyright © Growing Data Pty Ltd, Australia 
# AUTHOR: Michael-James Coetzee, Amit Wats
# EMAIL: mj@growingdata.com.au, amit@growingdata.com.au
########################################################

import configparser as ConfigParser

#Initialise the Config File
config = ConfigParser.ConfigParser()
config.read('geo.config')

SUGAR_JSON=config.get('Master Image', 'MASTER_SUGAR_DATA_GEOJSON_PATH')
GRID_WIDTH=int(config.get('Master Image', 'GRID_WIDTH'))
GRID_HEIGHT=int(config.get('Master Image', 'GRID_HEIGHT'))
TILE_IMAGE_FOLDER=config.get('Master Image', 'TILE_IMAGE_FOLDER')
MASK_IMAGE_FOLDER=config.get('Master Image', 'MASK_IMAGE_FOLDER')
GEO_JSON_FOLDER=config.get('Master Image', 'GEO_JSON_FOLDER')

def GetName(xPos,yPos):
    return "x"+str(xPos)+"-y"+str(yPos)

def GetFullPath(folder,prefix,ext,xPos,yPos):
    return folder+"/"+prefix+GetName(xPos,yPos)+ext

def GetTileName(xPos,yPos):
    return GetFullPath(TILE_IMAGE_FOLDER,"tile-",".png",xPos,yPos) 

def GetGeoJSONName(xPos,yPos):
    return GetFullPath(GEO_JSON_FOLDER,"geo-",".geojson",xPos,yPos)

def GetMaskName(xPos,yPos):
    return GetFullPath(MASK_IMAGE_FOLDER,"mask-",".png",xPos,yPos)

if __name__ == "__main__":
    print(GetTileName(7620,7600))
    print(GetGeoJSONName(7620,7600))
    print(GetMaskName(7620,7600))

