### Open Packages
from shapely.geometry import shape, mapping
import os,sys
import fiona
import rtree 
from fiona.crs import from_epsg

### Define Functions

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

def extract_poly_coords(geom):
    if geom.type == 'Polygon':
        exterior_coords = geom.exterior.coords[:]
        interior_coords = []
        for i in geom.interiors:
            interior_coords += i.coords[:]
    elif geom.type == 'MultiPolygon':
        exterior_coords = []
        interior_coords = []
        for part in geom:
            epc = extract_poly_coords(part)  # Recursive call
            exterior_coords += epc['exterior_coords']
            interior_coords += epc['interior_coords']
    else:
        raise ValueError('Unhandled geometry type: ' + repr(geom.type))
    return {'exterior_coords': exterior_coords,
            'interior_coords': interior_coords}


## Declare the working folders
path_work="/Users/juancarlosmunoz/Dropbox/Documents/Teaching/00_GIS_Applied_Economics/data_and_syntaxis/Session_3/"


output=main_path+"/Session_2/Ethnic_partioned.shp"


## Declare the working folders
with fiona.open(path_work+"Polygons/Africa_dvp_level0.shp", 'r') as africa_shp:
    schema = {'geometry':'Point','properties': {'country_id': 'str'}}
    with fiona.open(path_work+"output/Africa_centroid.shp", 'w', 'ESRI Shapefile', schema,crs=from_epsg(4326)) as output:

        ### Create the variables
        for feat in obs_layer:
            geom1 = shape(feat['geometry'])
            country_name=feat['properties']['ADM0_NAME']
            ## Get centroids
            lon,lat=np.mean([extract_poly_coords(geom1)['exterior_coords'][0]], axis=0)
            output.write({'properties': {'country_id': 'str'},
                            'geometry': mapping(Point(lon,lat))
                            })







