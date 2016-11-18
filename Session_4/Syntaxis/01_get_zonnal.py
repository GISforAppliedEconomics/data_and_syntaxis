import sys
sys.path.remove("/Library/Python/2.7/site-packages/numpy-override")
import os
from osgeo import ogr
from os.path import expanduser
home = expanduser("~")
from shapely.geometry import mapping, shape
import fiona
import glob
import os
import csv
import math
from rasterstats import zonal_stats

################
## 00 - 
################

virtual_country="/Users/juancarlosmunoz/Dropbox/Documents/Teaching/00_GIS_Applied_Economics/data_and_syntaxis/Session_4/Virtual_country/virtual_cntrygrid.shp"

######################
### Zonnal Stats 
######################

final_path="/Users/juancarlosmunoz/Dropbox/Documents/Teaching/00_GIS_Applied_Economics/data_and_syntaxis/Session_4"

orig_raster=final_path+"/suit/suit_original.tif"
# orig_raster=final_path+"/rasters/suit_categories_5.tif"

#### Zonnal Stats 
stats = zonal_stats(virtual_country,orig_raster,geojson_out=True, stats=['mean', 'sum', 'std', 'median'])

data_output={}
for h in stats:
	# [adm0_code,FID,OBS,std,sum,median,mean]
	point5_id=h['properties'].values()[1]
	n=len(h['properties'].values())
	## DAta
	data_output[point5_id]=h['properties'].values()[n-4:n]

#### check if is 
def check_value(val):
	if val is None:
		out=0
	else:
		out=float(val)
	return out

####### Export
cvs=final_path+"/outputs/point5_id+zonnal.cvs"

fieldnames = ['point5_id','agrindex_std','agrindex_mean','agrindex_sum']
with open(cvs,'w') as output_file:
	dict_writer = csv.DictWriter(output_file,fieldnames=fieldnames)
	dict_writer.writeheader()
	for row in data_output:
		row_write={}
		row_write['point5_id']=row
		row_write['agrindex_std']=check_value(data_output[row][0])
		row_write['agrindex_mean']=check_value(data_output[row][3])
		row_write['agrindex_sum']=check_value(data_output[row][1])
		dict_writer.writerow(row_write)

