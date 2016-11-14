### Open Packages
from shapely.geometry import shape, mapping
import os,sys
import fiona
import rtree 
from fiona.crs import from_epsg

## Declare the working folders
main_path="/Users/juancarlosmunoz/Dropbox/Documents/Teaching/00_GIS_Applied_Economics/data_and_syntaxis"
murdock=main_path+"/Session_2/01_Replication/murdock_shapefile1_0/borders_tribes.shp"
africa_level1=main_path+"/Session_2/Polygons/Africa_dvp_level0.shp"
output=main_path+"/Session_2/Ethnic_partioned.shp"


## Declare the working folders
with fiona.open(murdock, 'r') as murdock_shp:
    with fiona.open(africa_level1, 'r') as africa:

        ### Define the schema for the final output
        schema = {'geometry':'Polygon','properties': {'murdock_group': 'str','partition': 'int:10','area': 'float'}}
        with fiona.open(output, 'w', 'ESRI Shapefile', schema,crs=from_epsg(4326)) as output:

            ### Build Spatial Index
            index = rtree.index.Index()
            print "Creating the Spatial index - coastline"
            for feat1 in africa:
                fid = int(feat1['id'])
                geom1 = shape(feat1['geometry'])
                index.insert(fid, geom1.bounds)

            ## Iterate over Murdock features
            for feat in murdock_shp:
                geom = shape(feat['geometry'])
                area_orig= geom.area

                ## Now, we check whether it intersects
                for fid in list(index.intersection(geom.bounds)):
                    feat2=africa[fid]
                    geom3 = shape(feat2['geometry'])
                    ## Define the number of intersection
                    if geom.intersects(geom3):
                        area_int= shape(geom.intersection(geom3)).area
                        per=area_int/area_orig
                        if per>0.1:
                            if per!=1:
                                prop={'murdock_group': feat['properties']['NAME'],'partition': 1,'area': area_int}
                                output.write({
                                'properties': prop,
                                'geometry': mapping(geom.intersection(geom3))
                            })





