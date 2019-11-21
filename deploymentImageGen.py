##################################################################################
#  TCI requires bands 2,3,4,                                                     #
#  FCI requires bands 2,3,4,8,10,11,12,                                          #
#  NVDI requires band 3,4,8,                                                     #
##################################################################################
import subprocess 
import glob
import os
import numpy as np
import pandas as pd
import sys 
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib import colors
import rasterio as rio
from rasterio import plot

my_args = sys.argv
a = sys.argv[1:]
file_name = a[0]

# Tile width / height in pixels
TILE_WIDTH_PX = 1830
TILE_HEIGHT_PX = 1830 

def home_work(file_name):
    dir_path = "./{}/GRANULE".format(file_name)
    files = os.listdir(dir_path)
    print(files)
    for file in files:
        try: 
            a = str(file).split("_",3)[1]
            src = "./{}/GRANULE/{}".format(file_name,file)
            dst = "./{}/GRANULE/{}".format(file_name,file_name)
            print(src);print(dst)
            os.rename(src,dst)
        except IndexError:
            pass
        except NotADirectoryError:
            pass

    path = "./{}/GRANULE/{}/IMG_DATA/R60m/".format(file_name,file_name)

    for filename in os.listdir(path):
        try: 
            src = path + str(filename) 
            dst = path + str(filename).split("_",3)[2] + '.jp2'
            print("....Renaming the files")
            # rename all the files 
            os.rename(src, dst) 
        except IndexError:
            pass

# for the specified band and date
def get_tiles_band_path(file_name, band):
    path = f"./{file_name}/GRANULE/{file_name}/IMG_DATA/R60m/{band}.jp2"
    return path 

def normalize(array):
    array_min, array_max = array.min(), array.max()
    return ((array - array_min)/(array_max - array_min))

# get band pixels
def get_band(file_name,band):
    path = get_tiles_band_path(file_name, band)

    b = rio.open(path)
    read = normalize(b.read(1))
    
    get_band = dict()
    get_band['read'] = read; get_band['b'] = b

    return get_band

# create true color images
def TCI(file_name):
    get_blue = get_band(file_name,band='B02')
    b2 = get_blue['b']; blue = get_blue['read']
    
    get_green = get_band(file_name,band='B03')
    b3 = get_green['b']; green = get_green['read']
    
    get_red = get_band(file_name,band='B04')
    b4 = get_red['b']; red = get_red['read']

    # Stack bands
    tci = np.dstack((red, green, blue))
    if not os.path.exists(f'./Output-{file_name}/tci'):
        os.makedirs(f'./Output-{file_name}/tci')
    Image.fromarray((tci * 255).astype('uint8'),'RGB').save(f'./Output-{file_name}/tci/tci.jp2')
    
    return tci

# create false color images (there are 3 modes)
def FCI(mode,file_name):
    get_blue = get_band(file_name,band='B02')
    b2 = get_blue['b']; blue = get_blue['read']
    
    get_green = get_band(file_name,band='B03')
    b3 = get_green['b']; green = get_green['read']
    
    get_red = get_band(file_name,band='B04')
    b4 = get_red['b']; red = get_red['read']
    
    get_nir = get_band(file_name,band='B8A')
    b8 = get_nir['b']; nir = get_nir['read']
    
    get_swir_1 = get_band(file_name,band='B11')
    b11 = get_swir_1['b']; swir_1 = get_swir_1['read']
    
    get_swir_2 = get_band(file_name,band='B12')
    b12 = get_swir_2['b']; swir_2 = get_swir_2['read']
    
    # Stack bands
    if mode == 1: fci = np.dstack((nir, red, green)) # vegetation
    elif mode == 2: fci = np.dstack((swir_1/2+swir_2/2, nir, green)) # newly burnt land 
    elif mode == 3: fci = np.dstack((blue, swir_1, swir_2)) # clouds

    # View the color composite
    if not os.path.exists(f'./Output-{file_name}/fci/fci-mode{mode}'):
        os.makedirs(f'./Output-{file_name}/fci/fci-mode{mode}')
    Image.fromarray((fci * 255).astype('uint8'),'RGB').save(f'./Output-{file_name}/fci/fci-mode{mode}/fci-mode{mode}.jp2')

    return fci

# create ndvi map
def NDVI(file_name):
    get_red = get_band(file_name,band='B04')
    red = get_red['read']
    b4 = get_red['b']
    
    get_nir = get_band(file_name, band='B8A')
    nir = get_nir['read']
    b8 = get_nir['b']
    
    get_green = get_band( file_name,band='B03')
    b3 = get_green['b']; green = get_green['read']

    ndvi = np.where((nir+red)==0., 0, (nir-red)/(nir+red))

    # Stack bands
    ndvi = np.dstack((nir, ndvi, green))

    # View the color composite
    if not os.path.exists(f'./Output-{file_name}/ndvi'):
        os.makedirs(f'./Output-{file_name}/ndvi')
    Image.fromarray((ndvi * 255).astype('uint8'),'RGB').save(f'./Output-{file_name}/ndvi/ndvi.jp2')

    return ndvi

home_work(file_name)
FCI(mode=1,file_name=file_name)
FCI(mode=2,file_name=file_name)
FCI(mode=3,file_name=file_name)
NDVI(file_name= file_name)
TCI(file_name=file_name)