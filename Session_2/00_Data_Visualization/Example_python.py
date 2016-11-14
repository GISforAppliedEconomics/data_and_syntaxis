

import geopandas as gp
import matplotlib.pyplot as plt

# Open file
data_folder=
shp_file="/Users/juancarlosmunoz/Dropbox/Documents/Teaching/00_GIS_Applied_Economics/"
africa = gp.GeoDataFrame.from_file(shp_file+"data_and_syntaxis/Session_2/Polygons/Africa_dvp_level0.shp")


## Make the map
fig     = plt.figure()
africa.plot(column='REGION', colormap='OrRd')
pplt.show().show()

