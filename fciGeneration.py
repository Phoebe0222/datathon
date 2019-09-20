##################################################################################
#  Script to gnerate cropped bands, combine (cropped) bands to generate TCI, FCI #
#  save_cropped works for per tile, per date, per band                           #
#  TCI requires bands 2,3,4, and works for per tile, per date                    #
#  FCI requires bands 2,3,4,8,10,11,12, and works for per tile, per date         #  
#  NVDI requires band 3,4,8, and works for per tile, per date                    #
##################################################################################


# pip install -r requirements.txt


import glob
import os
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib import colors
import rasterio as rio
from rasterio import plot

# Get the physical path to the PNG image containing the mask file
def get_mask_path(tile_x, tile_y, mask_type): #mask_type is sugarcane coz it's in the file name
    path = f"./data/{mask_type}masks/mask-x{tile_x}-y{tile_y}.png"
    return path


# Get a list of all the image tiles for a specific x,y coordinate
# for the specified band
def get_tiles_band_paths(tile_x, tile_y, band, date):
    path = f"./data/tiles/{tile_x}-{tile_y}-{band}-{date}.png"
    #path = glob.glob(path) # a list of paths
    #path = path[0] # get the first date 
    return path 

def get_cropped_band_paths(tile_x, tile_y, band, date):
    path = f"./data/cropped/cropped-{tile_x}-{tile_y}-{band}-{date}.png"
    #path = glob.glob(path)
    #path = path[0] # get the first date 
    return path 


# Open an image file and get all the pixels, be careful of the x,y swaps
def get_image_pixels(path):
    img = Image.open(path)
    pixels = img.load() 
    return pixels

  
def is_in_mask(mask_pixels, pixel_x, pixel_y):
    if mask_pixels[pixel_x,pixel_y] == IS_IN_MASK_PIXEL_VALUE: # the pixel in the mask file is black 
        return True 
    else:
        return False

    
def get_cropped_pixels(tile_x, tile_y, mask_type, band, date):
    
    # get the pixels from mask and image 
    mask_pixels = get_image_pixels(get_mask_path(tile_x, tile_y, mask_type))
    image_pixels = get_image_pixels(get_tiles_band_paths(tile_x, tile_y, band, date))
    
    
    width = TILE_WIDTH_PX 
    height = TILE_HEIGHT_PX 
    bands = Image.open(get_tiles_band_paths(tile_x, tile_y, band, date)).getbands()
    num_channels = np.shape(bands)[0]

    for x in range(0, width):
        for y in range(0, height):

            # is the pixel in my mask?
            in_mask = is_in_mask(mask_pixels, x, y)
            if in_mask:
                pass
            else:
                if num_channels == 3:
                    image_pixels[x,y] = (0,0,0,0) #if not in mask, change to transparent
                else:
                    image_pixels[x,y] = 0 # not sure about this, what does 0 in "I" mean?
    
    cropped_pixels = image_pixels
    #print("The png file is in " + str(bands) + " mode.")
    return cropped_pixels
    

def sequence_cropped_pixels(tile_x, tile_y, mask_type, band, date):
    
    # get the pixels from cropped
    cropped_pixels = get_cropped_pixels(tile_x, tile_y, mask_type, band, date)

    cropped_sequence = []
    
    width = TILE_WIDTH_PX 
    height = TILE_HEIGHT_PX 
    for i in range(0, width):
        for j in range(0, height):
            cropped_sequence.append(cropped_pixels[j,i]) 
            # flipping the image coz of the way load() reads pixels
    return cropped_sequence



def save_cropped(tile_x, tile_y, mask_type, band, date):
    cropped = Image.new("I", (512, 512))
    cropped.putdata(sequence_cropped_pixels(tile_x, tile_y, mask_type, band, date))
    #cropped.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
    cropped.save(f'./data/cropped/cropped-{tile_x}-{tile_y}-{band}-{date}.png')
    return cropped

def save_cropped_TCI(tile_x, tile_y, mask_type, date, band='TCI'):
    cropped = Image.new("RGBA", (512, 512))
    cropped.putdata(sequence_cropped_pixels(tile_x, tile_y, mask_type, band, date))
    #cropped.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
    cropped.save(f'./data/cropped/cropped-{tile_x}-{tile_y}-{band}-{date}.png')
    return cropped


def normalize(array):
    array_min, array_max = array.min(), array.max()
    return ((array - array_min)/(array_max - array_min))

# get band pixels, setting ceopped = Ture to use cropped bands 
def get_band(tile_x, tile_y, date, band, cropped = False):
    if cropped == True:
        path = get_cropped_band_paths(tile_x, tile_y, band, date)
    else:
        path = get_tiles_band_paths(tile_x, tile_y, band, date)
    
    b = rio.open(path)
    read = normalize(b.read(1))
    
    get_band = dict()
    get_band['read'] = read; get_band['b'] = b

    return get_band

def TCI(tile_x, tile_y, date):
    get_blue = get_band(tile_x, tile_y, date, band='B02')
    b2 = get_blue['b']; blue = get_blue['read']
    
    get_green = get_band(tile_x, tile_y, date, band='B03')
    b3 = get_green['b']; green = get_green['read']
    
    get_red = get_band(tile_x, tile_y, date, band='B04')
    b4 = get_red['b']; red = get_red['read']
    
   
    # Stack bands
    tci = np.dstack((red, green, blue))


    # View the color composite
    plt.imshow(tci)
    plt.savefig(f'./Output/tci/tci-{tile_x}-{tile_y}-{date}.png')    
    
    return tci

def tci_hist(tile_x, tile_y, date):
    #generate histogram
    trueColor = rio.open(f'./Output/tci/tci-{tile_x}-{tile_y}-{date}.png', count=3)
    plot.show_hist(trueColor, bins=50, lw=0.0, stacked=False, 
                   alpha=0.3, histtype='stepfilled', title="Histogram")

    
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
    plt.imshow(fci)
    plt.savefig(f'./Output/fci-mode{mode}/fci-mode{mode}-{tile_x}-{tile_y}-{date}.png')    
    
    return fci


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
    plt.imshow(ndvi)
    plt.savefig(f'./Output/ndvi/ndvimap-{tile_x}-{tile_y}-{date}.png')

    return ndvi




# The initial release contains only one tile, so lets hardcode its location
# here.  When you have more tiles, you can update this
TILE_X = 1536 # ranges from 1536 to 8704
TILE_Y = 1024 # ranges from 1024 to 10240


# The expected value of a Pixel in a mask file indicating that the pixel is
# within that region.  Tuple value, (Red, Green, Blue, Alpha)
IS_IN_MASK_PIXEL_VALUE = (0, 0, 0, 255)

# Tile width / height in pixels
TILE_WIDTH_PX = 512 - 1 
TILE_HEIGHT_PX = 512 - 1 



start_arg_crop = {
    "tile_x":TILE_X,
    "tile_y":TILE_Y,
    "mask_type":'sugarcane',
    "band":'B01',
    "date":'2016-12-22'}
save_cropped(**start_arg_crop)


start_arg_img = {
    "tile_x":TILE_X,
    "tile_y":TILE_Y,
    "date":'2016-12-22'}
NDVI(**start_arg_img)
TCI(**start_arg_img)
FCI(**start_arg_img)ndvi

