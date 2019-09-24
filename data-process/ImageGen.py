##################################################################################
#  Script to gnerate cropped bands, combine (cropped) bands to generate TCI, FCI #
#  save_cropped works for per tile, per date, per band                           #
#  TCI requires bands 2,3,4, and works for per tile, per date                    #
#  FCI requires bands 2,3,4,8,10,11,12, and works for per tile, per date         #  
#  NVDI requires band 3,4,8, and works for per tile, per date                    #
##################################################################################


## Library for dependent scripts (OutputGen.py, UNET.py)

# pip install -r requirements.txt

import subprocess 
import glob
import os
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib import colors
import rasterio as rio
from rasterio import plot


# some initailisation param
# The expected value of a Pixel in a mask file indicating that the pixel is
# within that region.  Tuple value, (Red, Green, Blue, Alpha)
IS_IN_MASK_PIXEL_VALUE = (0, 0, 0, 255)

# Tile width / height in pixels
TILE_WIDTH_PX = 512 
TILE_HEIGHT_PX = 512 



if not os.path.exists('./Data'):
    print("No Data directory found, please download the data into the dame directory first")
    exit()

# Get the physical path to the PNG image containing the mask file
def get_mask_path(tile_x, tile_y, mask_type): #mask_type is sugarcane coz it's in the file name
    path = f"./data/{mask_type}masks/mask-x{tile_x}-y{tile_y}.png"
    return path


# Get a path of band tile for a specific x,y coordinate
# for the specified band and date
def get_tiles_band_path(tile_x, tile_y, band, date):
    path = f"./data/tiles/{tile_x}-{tile_y}-{band}-{date}.png"
    #path = glob.glob(path) # a list of paths
    #path = path[0] # get the first date 
    return path 

# Get a path of image tile for a specific x,y coordinate
# for the specified image and date
def get_img_path(tile_x, tile_y, img, date):
    path = f"./Output/{img}/{img}-{tile_x}-{tile_y}-{date}.png"
    return path 

# Open an image file and get all the pixels, be careful of the x,y swaps
def get_image_pixels(path):
    img = Image.open(path)
    pixels = img.load() 
    SIZE = img.size
    return pixels, SIZE

def is_in_mask(mask_pixels, pixel_x, pixel_y):
    if mask_pixels[pixel_x,pixel_y] == IS_IN_MASK_PIXEL_VALUE: # the pixel in the mask file is black 
        return True 
    else:
        return False

# get the pixels from cropped image    
def get_cropped_pixels(tile_x, tile_y, mask_type, img, date):
    
    # get the pixels from mask and image 
    mask = get_image_pixels(get_mask_path(tile_x, tile_y, mask_type))
    mask_pixels = mask[0]
    image = get_image_pixels(get_img_path(tile_x, tile_y, img, date))
    image_pixels = image[0]
    
    width = mask[1][0] 
    height = mask[1][1]  

    for x in range(0, width):
        for y in range(0, height):

            # is the pixel in my mask?
            in_mask = is_in_mask(mask_pixels, x, y)
            if in_mask:
                pass
            else:
                image_pixels[x,y] = (0,0,0) #if not in mask, change to transparent
                
    cropped_pixels = image_pixels
    #print("The png file is in " + str(bands) + " mode.")
    return cropped_pixels
    

# put the pixels from the cropped images in a sequence 
def sequence_cropped_pixels(tile_x, tile_y, mask_type, img, date):
        
    cropped_pixels = get_cropped_pixels(tile_x, tile_y, mask_type, img, date)

    cropped_sequence = []
    
    width = TILE_WIDTH_PX 
    height = TILE_HEIGHT_PX 
    for i in range(0, width):
        for j in range(0, height):
            cropped_sequence.append(cropped_pixels[j,i]) 
            # flipping the image coz of the way load() reads pixels
    return cropped_sequence

# save the cropped images in png format from a sequence of pixels
def save_cropped(tile_x, tile_y, mask_type, img, date):
    cropped = Image.new("RGBA", (512, 512))
    cropped.putdata(sequence_cropped_pixels(tile_x, tile_y, mask_type, img, date))
    #cropped.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
    if not os.path.exists('./Output/cropped'):
        os.makedirs('./Output/cropped')
    cropped.save(f'./Output/cropped/cropped-{tile_x}-{tile_y}-{img}-{date}.png')
    return cropped


# puting mask pixels in 0 or 1 (in mask or not in mask) values for model training purpose 
def get_mask_pixels(tile_x, tile_y,mask_type='sugarcane'):
    
    # get the pixels from mask 
    mask = get_image_pixels(get_mask_path(tile_x, tile_y, mask_type))
    mask_pixels = mask[0]
    
    width = mask[1][0] 
    height = mask[1][1]  
    mask_sequence = []

    for x in range(0, width):
        for y in range(0, height):

            # is the pixel in my mask?
            in_mask = is_in_mask(mask_pixels, y, x)
            if in_mask:
                mask_sequence.append(1)
            else:
                mask_sequence.append(0) #if not in mask, change to transparent
                
    mask = Image.new("I", (width, height))
    mask.putdata(mask_sequence)
    #mask.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
    if not os.path.exists('./ModelTrainingData/label'):
        os.makedirs('./ModelTrainingData/label')
    mask.save(f'./ModelTrainingData/label/mask-{tile_x}-{tile_y}.png')
    #print("mask-{}-{}".format(tile_x,tile_y)+" is saved")
    return mask_sequence
    

def normalize(array):
    array_min, array_max = array.min(), array.max()
    return ((array - array_min)/(array_max - array_min))

# get band pixels
def get_band(tile_x, tile_y, date, band):
    path = get_tiles_band_path(tile_x, tile_y, band, date)
    
    b = rio.open(path)
    read = normalize(b.read(1))
    
    get_band = dict()
    get_band['read'] = read; get_band['b'] = b

    return get_band

# create true color images
def TCI(tile_x, tile_y, date):
    get_blue = get_band(tile_x, tile_y, date, band='B02')
    b2 = get_blue['b']; blue = get_blue['read']
    
    get_green = get_band(tile_x, tile_y, date, band='B03')
    b3 = get_green['b']; green = get_green['read']
    
    get_red = get_band(tile_x, tile_y, date, band='B04')
    b4 = get_red['b']; red = get_red['read']
   
    # Stack bands
    tci = np.dstack((red, green, blue))
    if not os.path.exists('./Output/tci'):
        os.makedirs('./Output/tci')
    Image.fromarray((tci * 255).astype('uint8'),'RGB').save(f'./Output/tci/tci-{tile_x}-{tile_y}-{date}.png')
    
    return tci

# create histogram of different bands from tci
def tci_hist(tile_x, tile_y, date):
    #generate histogram
    trueColor = rio.open(f'./Output/tci/tci-{tile_x}-{tile_y}-{date}.png', count=3)
    plot.show_hist(trueColor, bins=50, lw=0.0, stacked=False, 
                   alpha=0.3, histtype='stepfilled', title="Histogram")


# create false color images (there are 3 modes)
def FCI(tile_x, tile_y, date, mode=1):
    get_blue = get_band(tile_x, tile_y, date, band='B02')
    b2 = get_blue['b']; blue = get_blue['read']
    
    get_green = get_band(tile_x, tile_y, date, band='B03')
    b3 = get_green['b']; green = get_green['read']
    
    get_red = get_band(tile_x, tile_y, date, band='B04')
    b4 = get_red['b']; red = get_red['read']
    
    get_nir = get_band(tile_x, tile_y, date, band='B08')
    b8 = get_nir['b']; nir = get_nir['read']
    
    get_swir_c = get_band(tile_x, tile_y, date, band='B10')
    b10 = get_swir_c['b']; swir_c = get_swir_c['read']
    
    get_swir_1 = get_band(tile_x, tile_y, date, band='B11')
    b11 = get_swir_1['b']; swir_1 = get_swir_1['read']
    
    get_swir_2 = get_band(tile_x, tile_y, date, band='B12')
    b12 = get_swir_2['b']; swir_2 = get_swir_2['read']
    
    # Stack bands
    if mode == 1: fci = np.dstack((nir, red, green)) # vegetation
    elif mode == 2: fci = np.dstack((swir_1/2+swir_2/2, nir, green)) # newly burnt land 
    elif mode == 3: fci = np.dstack((blue, swir_1, swir_2)) # clouds

    # View the color composite
    if not os.path.exists(f'./Output/fci/fci-mode{mode}'):
        os.makedirs(f'./Output/fci/fci-mode{mode}')
    Image.fromarray((fci * 255).astype('uint8'),'RGB').save(f'./Output/fci/fci-mode{mode}/fci-mode{mode}-{tile_x}-{tile_y}-{date}.png')

    return fci


# create ndvi map
def NDVI(tile_x, tile_y, date):
    get_red = get_band(tile_x, tile_y, date, band='B04')
    red = get_red['read']
    b4 = get_red['b']
    
    get_nir = get_band(tile_x, tile_y, date, band='B08')
    nir = get_nir['read']
    b8 = get_nir['b']
    
    get_green = get_band(tile_x, tile_y, date, band='B03')
    b3 = get_green['b']; green = get_green['read']
   
    ndvi = np.where((nir+red)==0., 0, (nir-red)/(nir+red))

    # Stack bands
    ndvi = np.dstack((nir, ndvi, green))

    # View the color composite
    if not os.path.exists('./Output/ndvi'):
        os.makedirs('./Output/ndvi')
    Image.fromarray((ndvi * 255).astype('uint8'),'RGB').save(f'./Output/ndvi/ndvi-{tile_x}-{tile_y}-{date}.png')

    return ndvi


# generate tile ids 
def tile_id_gen():
    if not os.path.exists('./ModelTrainingData'):
        os.makedirs('./ModelTrainingData')
    subprocess.run("ls ./ModelTrainingData/input | grep 'tci'| cut -d'-' -f2 -f3 |sort --unique > TileIds.txt",shell=True)
    f = open("./ModelTrainingData/TileIds.txt")
    count = int(subprocess.run("ls ./ModelTrainingData/input | grep 'tci'| cut -d'-' -f2 -f3 |sort --unique | wc -l", stdout=subprocess.PIPE,shell=True).stdout.decode('utf-8'))
    
    tile_x = []
    tile_y = []
    img = []
    
    print("Creating the Data list .....")
    
    for x in f:
        tile_x.append(str(x).split("-",1)[0])
        tile_y.append(str(x).split("-",1)[1].replace("\n",""))
    print('{} tiles ids are created'.format(count))    
    return tile_x, tile_y,count




# just trying with one tile 
TILE_X = 1536 # ranges from 1536 to 8704
TILE_Y = 1024 # ranges from 1024 to 10240
DATE = '2017-01-01'


start_arg_crop = {
    "tile_x":TILE_X,
    "tile_y":TILE_Y,
    "mask_type":'sugarcane',
    "img":'ndvi', # We want to crop the ndvi images, if else put tci or fci 
    "date":DATE}

start_arg_img = {
    "tile_x":TILE_X,
    "tile_y":TILE_Y,
    "date":DATE}



#NDVI(**start_arg_img)
#TCI(**start_arg_img)
MODE = 3
print('Printing fci for tile {},{}'.format(TILE_X,TILE_Y)
      +' in {}'.format(DATE)+' in mode {}.'.format(MODE))
FCI(**start_arg_img,mode=MODE)

#save_cropped(**start_arg_crop)

