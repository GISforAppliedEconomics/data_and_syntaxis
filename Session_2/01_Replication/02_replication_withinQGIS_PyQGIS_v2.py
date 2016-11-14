import os
import sys

#Import QGIS
from qgis import *
from qgis.core import *
from qgis.analysis import * 


### Working Path
main_path="/Users/juancarlosmunoz/Dropbox/Documents/Teaching/00_GIS_Applied_Economics/data_and_syntaxis"
murdock=main_path+"/Session_2/01_Replication/murdock_shapefile1_0/borders_tribes.shp"
africa_level1=main_path+"/Session_2/Polygons/Africa_dvp_level0.shp"
output=main_path+"/Session_2/QGIS_step_0.shp"

### Step 0 -  Making the Intersection
murdock_shp = QgsVectorLayer( murdock  , "murdock", "ogr")
africa_shp = QgsVectorLayer( africa_level1  , "layerB", "ogr")


# Create a memory layer to store the result
# Create a memory layer to store the result
resultl = QgsVectorLayer("Polygon?crs=epsg:4326", "result", "memory")
resultpr = resultl.dataProvider()
QgsMapLayerRegistry.instance().addMapLayer(resultl)
resultl.startEditing()

for feat in murdock_shp.getFeatures():
  # Save the original geometry
  geom1 = feat.geometry()
  area_murdock=feat.geometry().area()
  # print geometry
  for country in africa_shp.getFeatures():
    geom2 = country.geometry()
    if geom1.intersects(geom2) is True:
      print "Tribe %s intersects country %s" %(feat[0],country['ADM0_NAME'])
      geom3 = geom1.intersection(geom2)
      area_a=geom3.geometry().area()
      ## get the per
      per_area=area_a/area_murdock
      print per_area
      if per_area>0.1:
        if per_area<1:
        ## Add to new layer
        # QgsMapLayerRegistry.instance().addMapLayer(resultl)
        ### Start Editing
        #Set features
        feature = QgsFeature()
        #set geometry
        feature.setGeometry(geom3)
        #set attributes values
        feature.setAttributes([1])
        resultl.addFeature(feature, True)
                # resultl.updateExtents()
                # QgsMapLayerRegistry.instance().addMapLayers([resultl])

resultl.commitChanges()