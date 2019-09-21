# Data Prepoccess

Preproccess includes fetching data from sentinel API, tiles generation, sugar segementation, mask generation and cropping images with masks. 



**Tile generation**: given full geometry json file and full image, GeneratTiles.py generates the *.geojson files that contain the tile GPS coordinates (in the geometries folder) and  *.png images for each tile (in the tiles folder).  

**Sugar segementation**: proposed to use autoencoder to find sugarcane field mask, i.e. generates full sugar .geojson.  


**Mask generation**: given full sugar .geojson, the file GenerateMaskFiles.py generated the .png files that contain the tile with non-sugar areas masked (in the mask folder)(Tile generation must be completed first)
 
 
**cropping images with masks**: given mask png files, map mask over tile images and cut out the parts that are not in the mask (non-sugar).

