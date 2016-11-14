import os
import sys

#Import QGIS
from qgis import *
from qgis.core import *
from qgis.analysis import * 
from PyQt4.QtCore import *
import PyQt4
from PyQt4 import QtCore, QtGui

### Working Path
main_path="/Users/juancarlosmunoz/Dropbox/Documents/Teaching/00_GIS_Applied_Economics/data_and_syntaxis"
murdock=main_path+"/Session_2/01_Replication/murdock_shapefile1_0/borders_tribes.shp"
africa_level1=main_path+"/Session_2/Polygons/Africa_dvp_level0.shp"
output=main_path+"/Session_2/QGIS_step_0.shp"

### Step 0 -  Making the Intersection
murdock_shp = QgsVectorLayer( murdock  , "murdock", "ogr")
africa_shp = QgsVectorLayer( africa_level1  , "layerB", "ogr")

### As Rtree let's first create the index for the country
index = QgsSpatialIndex()
for feat in africa_shp.getFeatures():
    index.insertFeature(feat)

# Create a memory layer to store the result
resultl = QgsVectorLayer("Polygon?crs=epsg:4326", "result", "memory")
resultpr = resultl.dataProvider()
QgsMapLayerRegistry.instance().addMapLayer(resultl)

for feat in murdock_shp.getFeatures():
    # Get the properties for each feature in Murdock layer
    geom1 = feat.geometry()
    area_murdock=feat.geometry().area()
    # We check the intersections
    ids_intersect = index.intersects(feat.geometry().boundingBox())
    selected = [feature for (feature) in africa_shp.getFeatures() if feature.id() in ids_intersect]
    for feat_country in selected:
        for id in selected:
            geom2 = id.geometry()
            if geom1.intersects(geom2) is True:
                geom3 = geom1.intersection(geom2)
                area_a=geom3.geometry().area()
                per_area=area_a/area_murdock
                if per_area>0.1:
                    if per_area<0.9:
                        ### Define new feature
                        feature = QgsFeature()
                        #set geometry
                        feature.setGeometry(geom3)
                        # Define Attribies
#                        feature.setAttributes([feat[0],id[0],area_a])
                        # Add ne feature
                        resultpr.addFeatures([feature])
                        # Update extend
#                        resultl.updateExtents()
                        
        