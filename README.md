# datathon
datathon melbourne 2019

## One-sentence desription

The task is to build an interactive App (e.g. browser based) which utilises satellite data to provide insight into the production of sugarcane over time. 


## Data description:

For each region (e.g. a town, a state) we have 1 metadata per date, which includes info such as coordinates, cloud coverage etc. Each region is also chopped up into some hundred tiles, which are created by the corresponding *.geojson files respectively. Each tile contains 1 mask, which reprensents sugarcane field. Each tile also contains approx. 13 satellite images including images captured by 12 different sensing bands and 1 True Color Image (TCI). The link provided below contains more info about satellite images.   

For [**phase 1**](https://medium.com/satellite-intelligence/phase-one-data-code-release-65ba4b5b03bb) we only have 1 tile. [**Phase 2**](https://medium.com/satellite-intelligence/phase-two-data-code-release-c72bde3ef7c2) we have a whole region of Prosperpine with hundreds of tiles. [**Phase 3**](https://medium.com/satellite-intelligence/phase-three-data-code-release-cdc89210f869) we have whole of Auatralia. 


## useful links:
- Basic info: https://medium.com/satellite-intelligence/datathon-guide-ac6539cfd623
- Copernicus: [videos](https://medium.com/satellite-intelligence/introduction-to-the-european-space-agencys-copernicus-program-24497fc99364), [wiki](https://en.wikipedia.org/wiki/Copernicus_Programme) 
- Ideas to get started: https://medium.com/satellite-intelligence/phase-three-data-code-release-cdc89210f869
- Satellite images explained, also examples on app: https://farmonaut.com/satellite-imagery-login/ 
- How tiles are created: https://medium.com/satellite-intelligence/generating-tile-geometry-files-1776d75b1f3
- How masks are created: https://medium.com/satellite-intelligence/creating-masks-84abbe6ecc93 
- Corrected mask for phase 1: https://medium.com/satellite-intelligence/mask-correction-3c380c2ff588
- Other satellite API: https://gisgeography.com/free-satellite-imagery-data-list/

## Prep 
### step 1:
map the mask on real image
https://towardsdatascience.com/satellite-imagery-access-and-analysis-in-python-jupyter-notebooks-387971ece84b

### step 2:
calculate vegetation level
https://medium.com/analytics-vidhya/satellite-imagery-analysis-with-python-3f8ccf8a7c32

### step 2.5:
other agriculture indexes 

### step 3:
learn how to generate tiles and masks (phase 2 'mask-generation' folder contains .py on how to)

### future steps:
create our own pipeline to pull data from SARA (so we have live data)

## Convention in storing files:
- data
    - sentinel-{sentinel_number}-tile-{tile_x}x-{tile_y}y
        - cropped (cropped png files, cropped-{tile_x}-{tile_y}-{band_number}-{yyyy}-{mm}-{dd}.png)
        - geometry (geojson file containt polygon coords, file-x{tile_x}-y{tile_y}.geojson)
        - masks (png files for different purpose, e.g. {sugarcane-region}-mask.png)
        - metadata (json files in different time)
        - timeserires (png files from different sensing bands in different time)
