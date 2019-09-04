# datathon
datathon melbourne 2019

## One-sentence desription

The task is to build an interactive App (e.g. browser based) which utilises satellite data to provide insight into the production of sugarcane over time. 


## Data description:

For each region (e.g. a town, a state) we have 1 metadata per date, which includes info such as coordinates, cloud coverage etc. Each region is also chopped up into some hundred tiles, which are created by the corresponding *.geojson files respectively. Each tile contains 1 mask, which reprensents sugarcane field. Each tile also contains approx. 13 satellite images including images captured by 12 different sensing bands and 1 True Color Image (TCI). The link provided below contains more info about satellite images.   

For **phase 1** we only have 1 tile. **Phase 2** we have a whole region of Prosperpine with hundreds of tiles. **Phase 3** we have whole of Auatralia. 


## useful links:
Basic info: https://medium.com/satellite-intelligence/datathon-guide-ac6539cfd623
Satellite image explain: https://farmonaut.com/satellite-imagery-login/

## Prep 
### step 1:
map the mask on real image
https://towardsdatascience.com/satellite-imagery-access-and-analysis-in-python-jupyter-notebooks-387971ece84b

### step 2:
calculate vegetation level
https://medium.com/analytics-vidhya/satellite-imagery-analysis-with-python-3f8ccf8a7c32


### future steps:
create our own pipeline to pull data from SARA (so we have live data)
create our own pipeline to build masks (e.g. sugarcane regions, river regions etc.) 


