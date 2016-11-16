### Open Packages
from shapely.geometry import shape, mapping,Point
import fiona
import os,sys
import rtree
import csv
import math

## Haversine Distance

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    km = 6367 * c
    return km


## Declare the working folders
path_work="/Users/juancarlosmunoz/Dropbox/Documents/Teaching/00_GIS_Applied_Economics/data_and_syntaxis/Session_3/"
countr_shp=path_work+"output/Africa_centroid.shp"
coast_shp=path_work+"10m-coastline/10m_coastline_atlantic.shp"
slaves_data=path_work+"trade_centers_nun2008.csv"

### 00 - Before Starting we create the data set slave trade centers

## Trade centers
data_slaves={}
with open(slaves_data, 'rb') as f:
   reader = csv.DictReader(f)
   id=1
   for row in reader:
   	data_slaves[id]={'lon':row['lon'],'lat':row['lat'],'long_name':row['fallingrain_name'],'name':row['name']}
   	id+=1

## Now we create an index for the slaves trades
idx_trade = rtree.index.Index()
for id in data_slaves:
	idx_trade.insert(id, (float(data_slaves[id]['lat']), float(data_slaves[id]['lon']), float(data_slaves[id]['lat']), float(data_slaves[id]['lon'])))

### 01 - Now let's iterate 

## Declare the working folders
country_distance={}
with fiona.open(countr_shp, 'r') as country_layer:
	with fiona.open(coast_shp, 'r') as coast_layer:
		### Create index for coast-line nodes
		print "Creating the Spatial index - coastline"
		index = rtree.index.Index()
		for feat1 in coast_layer:
			fid = int(feat1['id'])
			geom1 = shape(feat1['geometry'])
			index.insert(fid, geom1.bounds)
		### Now iterate over african countries
		print "Iterating over coastline"
		for feat in country_layer:
			## Get Geometries from centroid
			geom1 = shape(feat['geometry'])
			country=feat['properties']['country_id']
			lon,lat=feat['geometry']['coordinates']
			### Get the distance to the closest point in the coast
			for fid_coast in list(index.nearest(geom1.bounds,1)):
				feat1=coast_layer[fid_coast]
				dist={}
				for lon_coast,lat_coast in feat1['geometry']['coordinates']:
					dist[(lat_coast,lon_coast)]=haversine(lon,lat,lon_coast,lat_coast)
			## Now we get closest distance
			dist_coast=min(dist.items(), key=lambda x: x[1]) 
			## It will give us [(lon),value]
			## Now we are ready to estimate the distance to the coastline to the trade market
			# Get the coordinates for 
			lon_coast_1,lat_coast_1=dist_coast[0]
			for fid_market in list(idx_trade.nearest(shape(Point(lon_coast_1,lat_coast_1)).bounds,1)):
				dist_coast_to_market=haversine(float(data_slaves[fid_market]['lon']),float(data_slaves[fid_market]['lat']),lon_coast_1,lat_coast_1)
			### Now, we are ready to estimate the final distance
			dist_final=dist_coast[1]+dist_coast_to_market

			### Get the value for the shapefile
			try:
				country_distance[country].append(dist_final)
			except:
				country_distance[country]=[dist_final]
			# 

## Finally we need to get he closest feature to each country
final_data = dict(zip(country_distance.keys(), [[min(item)] for item in country_distance.values()]))
for i in final_data:
	print "The distance of %s to the nearest market is %d km" %(i,final_data[i][0])





