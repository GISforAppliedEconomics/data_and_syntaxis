### Open Packages
from shapely.geometry import shape, mapping,Point
import os,sys
import fiona
from fiona.crs import from_epsg


## Declare the working folders
path_work="/Users/juancarlosmunoz/Dropbox/Documents/Teaching/00_GIS_Applied_Economics/data_and_syntaxis/Session_3/"


## Declare the working folders
with fiona.open(path_work+"Polygons/Africa_dvp_level0.shp", 'r') as africa_shp:
    schema = {'geometry':'Point','properties': {'country_id': 'str'}}
    with fiona.open(path_work+"output/Africa_centroid.shp", 'w', 'ESRI Shapefile', schema,crs=from_epsg(4326)) as output:

        ### Create the variables
        for feat in africa_shp:
            geom1 = shape(feat['geometry'])
            country_name=feat['properties']['ADM0_NAME']
            output.write({'properties': {'country_id': country_name},
                            'geometry': mapping(geom1.centroid)
                            })







