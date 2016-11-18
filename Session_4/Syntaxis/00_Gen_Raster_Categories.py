# -*- coding: utf-8 -*-
# """
# Created on Wed Aug 12 21:33:20 2015

# @author: rutgerhofste

# This script will replace values in a raster and save the result in geotiff format

# """

from osgeo import gdal 
import numpy as np
from copy import deepcopy

######### Function
### 0 - Delete the NaN
def readFile(filename):
    filehandle = gdal.Open(filename)
    band1 = filehandle.GetRasterBand(1)
    geotransform = filehandle.GetGeoTransform()
    geoproj = filehandle.GetProjection()
    Z = band1.ReadAsArray()
    xsize = filehandle.RasterXSize
    ysize = filehandle.RasterYSize
    return xsize,ysize,geotransform,geoproj,Z

def writeFile(filename,geotransform,geoprojection,data):
    (x,y) = data.shape
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    # you can change the dataformat but be sure to be able to store negative values including -9999
    dst_datatype = gdal.GDT_Byte
    dst_ds = driver.Create(filename,y,x,1,dst_datatype)
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(geoprojection)
    return 1

############### MAIN 

### Working Directory
final_path="/Users/juancarlosmunoz/Dropbox/Documents/Teaching/00_GIS_Applied_Economics/data_and_syntaxis/Session_4"

### 0 - Create TIFF from TXT
# Create the txt to GeoTIFF
infile=final_path+"/suit/suit_original.tif"

### Read Raster
[xsize,ysize,geotransform,geoproj,Z] = readFile(infile)

Z[Z<0]= np.nan

Z_5groups=deepcopy(Z)

#### 5 Groups
Z_5groups[Z_5groups<0]= np.nan
Z_5groups[Z_5groups==1]= 5
Z_5groups[Z_5groups<=.2]= 1
Z_5groups[Z_5groups<=.4]= 2
Z_5groups[Z_5groups<=.6]= 3
Z_5groups[Z_5groups<=.8]= 4
Z_5groups[Z_5groups<=1]= 5

output_5=final_path+"/output/suit_categories_5.tif"

writeFile(output_5,geotransform,geoproj,Z_5groups)

