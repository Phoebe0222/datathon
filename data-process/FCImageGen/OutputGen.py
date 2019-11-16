import os 
import subprocess
from Util.ImageGen import *

#####################  Create a text file of tile names in the Data Directory  #####################

def tile_name_gen():
    if not os.path.exists('./Output'):
        os.makedirs('./Output')
    subprocess.run("ls ../data/tiles | cut -d'-' -f1 -f2 -f4 -f5 -f6|sort --unique > ./Output/tilenames.txt",shell=True)
    f = open("./Output/tilenames.txt")
    count = int(subprocess.run("ls ../data/tiles | cut -d'-' -f1 -f2 -f4 -f5 -f6|sort --unique | wc -l", stdout=subprocess.PIPE,shell=True).stdout.decode('utf-8'))
    
    tile_x = []
    tile_y = []
    date = []
    
    print("Crating the tile names list .....")
    
    for x in f:
        tile_x.append(str(x).split("-",2)[0])
        tile_y.append(str(x).split("-",2)[1])
        date.append((str(x).split("-",2)[2]).replace(".png\n",""))
        
    #subprocess.run('rm -rf ./Output/tilenames.txt', shell= True)
    return tile_x, tile_y, date, count




#####################  Generate NDVI, FCI, FCI for each tile #####################

tile_x, tile_y, date, count = tile_name_gen()

print("Generating Images .....")

for i in range(count):
    start_arg_crop = {
        "tile_x":tile_x[i],
        "tile_y":tile_y[i],
        "mask_type":'sugarcane',
        "img":'ndvi', # We want to crop the ndvi images, if else put tci or fci 
        "date":date[i]}

    start_arg_img = {
        "tile_x":tile_x[i],
        "tile_y":tile_y[i],
        "date":date[i]}

    NDVI(**start_arg_img)
    print("{} NDVI Done".format(i))
    TCI(**start_arg_img)
    print("{} TCI Done".format(i))
    FCI(**start_arg_img)
    print("{} FCI Done".format(i))
    
    #ImageGen.save_cropped(**start_arg_crop)
    #print("{} Cropped Done".format(count))
    
print("Done")
####################################################################################################

