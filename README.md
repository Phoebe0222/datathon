# datathon
# dev-branch: Python call using flask
datathon melbourne 2019

<<<<<<< HEAD
everything: https://medium.com/satellite-intelligence

=======
## One-sentence desription

The task is to build an interactive App (e.g. browser based) which utilises satellite data to provide insight into the production of sugarcane over time. 


## Data description: [DOWNLOAD LINK](https://1drv.ms/u/s!Al9oqaKvmvr0g8p2KgCbZQ-JJQGCoQ?e=eZrRyv)

For each region (e.g. a town, a state) we have 1 metadata per date, which includes info such as coordinates, cloud coverage etc. Each region is also chopped up into some hundred tiles, which are created by the corresponding *.geojson files respectively. Each tile contains 1 mask, which reprensents sugarcane field. Each tile also contains approx. 13 satellite images including images captured by 12 different sensing bands and 1 True Color Image (TCI). The link provided below contains more info about satellite images.   

For [**phase 1**](https://medium.com/satellite-intelligence/phase-one-data-code-release-65ba4b5b03bb) we only have 1 tile. [**Phase 2**](https://medium.com/satellite-intelligence/phase-two-data-code-release-c72bde3ef7c2) we have a whole region of Prosperpine with hundreds of tiles. [**Phase 3**](https://medium.com/satellite-intelligence/phase-three-data-code-release-cdc89210f869) we have whole of Auatralia. 


## data-process
- data: folder storing data
- Output: folder storing output
- libraries: GeoLibrary.py, ImageGen.py, sentinelloader
- tile-and-mask-generation.py: tile and mask generators
- OutputGen.py: generates image outputs
- geojson-to-image.py: create small image from full image based on user defined polygon
- requirement.txt: required python packages


## Convention in storing data:
- data
    - geometries 
        - geojson files containt polygon coords to create tiles: geo-x{tile_x}-y{tile_y}.geojson
    - metadata 
        - metadata for the whole region: {yyyy}-{mm}-{dd}.json
    - sugarcanemasks
        - masks for sugarcane fields for each tile: mask-x{tile_x}-y{tile_y}.png  
    - tiles
        - bands for each tile per band per day: {tile_x}-{tile_y}-{band}-{yyyy}-{mm}-{dd}.png 

- output
    - ndvi 
        - ndvi maps for each tile per day: ndvimap-{tile_x}-{tile_y}-{yyyy}-{mm}-{dd}.png
        
    - tci
        - tci for each tile per day: tci-{tile_x}-{tile_y}-{yyyy}-{mm}-{dd}.png
    - fci-mode1
        - vegetation fci for each tile per day: fci-mode1-{tile_x}-{tile_y}-{yyyy}-{mm}-{dd}.png
    - fci-mode2
        - newly burnt land fci for each tile per day: fci-mode2-{tile_x}-{tile_y}-{yyyy}-{mm}-{dd}.png
    - fci-mode3
        - clouds fci for each tile per day: fci-mode3-{tile_x}-{tile_y}-{yyyy}-{mm}-{dd}.png
    - cropped
        - cropped png files for tiles: cropped-{tile_x}-{tile_y}-{img}-{yyyy}-{mm}-{dd}.png
      
      
      
## useful links:
- Basic info: https://medium.com/satellite-intelligence/datathon-guide-ac6539cfd623
- Copernicus: [videos](https://medium.com/satellite-intelligence/introduction-to-the-european-space-agencys-copernicus-program-24497fc99364), [wiki](https://en.wikipedia.org/wiki/Copernicus_Programme) 
- Ideas to get started: https://medium.com/satellite-intelligence/getting-started-370a87971a99
- Satellite images explained, also examples on app: https://farmonaut.com/satellite-imagery-login/ 
- more ap examples: https://land.copernicus.eu/global/products/ndvi, https://www.sentinel-hub.com/explore/industries-and-showcases/sentinel-2-ndvi-maps, https://farmonaut.com/satellite-based-crop-health-monitoring/
- How tiles are created: https://medium.com/satellite-intelligence/generating-tile-geometry-files-1776d75b1f3
- How masks are created: https://medium.com/satellite-intelligence/creating-masks-84abbe6ecc93 
- Geopandas: https://medium.com/starschema-blog/create-a-map-of-budapest-districts-colored-by-income-using-folium-in-python-8ab0becf4491 
- Corrected mask for phase 1: https://medium.com/satellite-intelligence/mask-correction-3c380c2ff588
- Other satellite API: https://gisgeography.com/free-satellite-imagery-data-list/

