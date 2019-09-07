########################################################
# Copyright © Growing Data Pty Ltd, Australia 
# AUTHOR: Michael-James Coetzee, Amit Wats
# EMAIL: mj@growingdata.com.au, amit@growingdata.com.au
########################################################

REQUIRED LIBRARIES
++++++++++++++++++
pillow
shapely
geopandas
geopy

READ THE FOLLOWING INSTRUCTIONS TO GET STARTED
===============================================
1. Create the following folders in the base directory of your choice "tiles", "mask" and "geometries"
2. The default configurations should work fine, however in case you need to modify the settings do so in the "geo.config" file
3. Ensure no quotations(") are put in the geo.config file
4. The file GeneratGeoJSON.py generated the .geojson files that contain the tile GPS coordinates and tile .png images
5. The file GenerateMaskFiles.py generated the .png files that contain the tile with non-sugar areas masked (Step 4 must be completed first)