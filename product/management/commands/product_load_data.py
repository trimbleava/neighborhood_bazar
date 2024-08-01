from __future__ import print_function

""" Populates database with spatial datasets """

import logging
import os, sys
import csv, json, djgeojson, xmltodict, collections
import xml.etree.cElementTree as ElementTree
import codecs


from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.serializers import deserialize
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import Point, Polygon, GEOSGeometry


logger = logging.getLogger('gisapp')

from gisapp.models import WorldBorder, WeatherStation, CoopsActiveMeters, \
                          CoopsWaterLevel, WorldOcean, WorldCoastline, NDBCObsv, \
                          ChesapeakBay, DelawareBay, DelawareRiver, PamlicoSound, \
                          DflowLandBoundary


from gisapp.utils import dms2dec

# system default data directory
if 'DATA_SHARE' not in os.environ:
    os.environ['DATA_SHARE'] = settings.DATA_DIR


# xml format
def ndbc_buoy():
    xml_file = os.path.join(os.environ['DATA_SHARE'], 'gis/NDBC.xml')  # BUOY stations

    # Note: even with encoding mode rb had problem parsing "&"!! I changed two stations (station id="42396" and id="42380")
    # from "&" to "and" to parse!! See data/gis/NDBC.out for the format
    with open(xml_file) as fd:
        doc = xmltodict.parse(fd.read(), process_namespaces=True, encoding='utf-8')
        # print(json.dumps(doc, indent=4))
        stations = doc['stations']['station']
        # print(json.dumps(stations, indent=4))
        for station in stations:
            id = station['@id']
            name = station["@name"]
            owner = station["@owner"]     # too long name, only gets 50 len
            pgm = station["@pgm"]
            type = station["@type"]
            histories = station["history"]
            lat = lng = 0.0
            if isinstance(histories, collections.Mapping):
                lat = histories["@lat"]
                lng = histories["@lng"]
            else:
                for hist in histories:
                    lat = hist["@lat"]
                    lng = hist["@lng"]
                    break
            print(id, lng, lat)
            NDBCObsv(sid=id, name=name, owner=owner[:49], pgm=pgm, type=type, geom=Point(float(lng), float(lat))).save()


# for csv
"""
http://blog.mathieu-leplatre.info/geodjango-maps-with-leaflet.html
The World Meteorological Organization publishes a list of all major weather stations, in a CSV format.
https://www.wmo.int/pages/index_en.html
Unfortunately, this format is not very friendly (especially latitudes and longitudes) :

StationId   StationName         Latitude    Longitude ...
60351       JIJEL- ACHOUAT      36 48 00N   05 53 00E
...
07630       TOULOUSE BLAGNAC    43 37 16N   01 22 44E
...
We will convert coordinates from degrees minutes seconds to decimal degrees. See util.py

Note: could not find the csv format of the weather data. However found partial station list from:
https://www.dwd.de/DE/leistungen/klimadatenweltweit/stationsverzeichnis.html?lsbId=374532
and reformat the file and the code accordingly. This data set is only for USA weather stations
and I am not sure is they are official. I am using this data for presentation only.
Header: STATION NAME,STATION ID,LONGITUDE,LATITUDE,ELEVATION (M),COUNTRY CODE,COUNTRY,CONTINENT
"""
def run_weather_station(verbose=True):

    csv_file = os.path.join(os.environ['DATA_SHARE'], 'gis/weather_stations.csv')  # 'Pub9volA130819x.flatfile.txt'

    reader = csv.DictReader(open(csv_file, 'r'), delimiter=",")
    for line in reader:

        name = line.pop('STATION NAME').title()
        wmoid = int(line.pop('STATION ID'))

        lat = lng = 0.0
        degres, rest = line.pop('LONGITUDE').split()
        min, direction = rest[:-1], rest[-1]
        lng = float(degres) + float(min) / 60
        if direction in ('S', 'W'):
            lng = -lng

        degres, rest = line.pop('LATITUDE').split()
        min, direction = rest[:-1], rest[-1]
        lat = float(degres) + float(min) / 60
        if direction in ('S', 'W'):
            lat = -lat

        elev = int(line.pop('ELEVATION (M)'))
        cntcode = line.pop('COUNTRY CODE')
        cntry = line.pop('COUNTRY')
        cont = line.pop('CONTINENT')

        print(lng,lat)
        WeatherStation(wmoid=wmoid, name=name, geom=Point(lng, lat)).save()


def coops_waterlevel(verbose=True):
    # Source: https://opendap.co-ops.nos.noaa.gov/ioos-dif-sos/ClientGetter?p=6
    # Station ID      Station Name    Deployed        Latitude        Longitude
    csv_file = os.path.join(os.environ['DATA_SHARE'], 'gis/coops_waterlevel.csv')

    reader = csv.DictReader(open(csv_file, 'r'), delimiter="\t")
    for line in reader:
        sid = line.pop('Station ID').strip()
        name = line.pop('Station Name').strip()
        deployed = line.pop('Deployed').strip()
        lat = float(line.pop('Latitude').strip())
        lng = float(line.pop('Longitude').strip())
        print(lng, lat)
        CoopsWaterLevel(sid=sid, name=name, deployed=deployed, geom=Point(lng, lat)).save()


def coops_active_meters(verbose=True):
    # Source: https://opendap.co-ops.nos.noaa.gov/ioos-dif-sos/ClientGetter?p=4
    # Station ID      Station Name    Deployed     Recovered   Latitude        Longitude
    csv_file = os.path.join(os.environ['DATA_SHARE'], 'gis/coops_active_meters.csv')

    reader = csv.DictReader(open(csv_file, 'r'), delimiter="\t")
    for line in reader:
        sid = line.pop('Station ID').strip()
        name = line.pop('Station Name').strip()
        deployed = line.pop('Deployed').strip()
        recovered = line.pop('Recovered').strip()
        lat = float(line.pop('Latitude').strip())
        lng = float(line.pop('Longitude').strip())
        print(sid, name, deployed, recovered, lng, lat)
        CoopsActiveMeters(sid=sid, name=name, deployed=deployed, recovered=recovered, geom=Point(lng, lat)).save()

# https://www.ndbc.noaa.gov/wstat.shtml  BUOYS

# another example for csv - not used
# Good source: https://krzysztofzuraw.com/blog/2016/geodjango-leaflet-part-two.html
# from django.contrib.gis import geos
# from .models import Point
#
def dflow_landboundary():
    land_bnd = os.path.join(os.environ['DATA_SHARE'], 'gis/regional.ldb')

    data = []

    # read the land boundary data, and save into memory
    with open(land_bnd) as fptr:
        line = fptr.readline()
        # print(line)

        while line:
            name, cnt = read_name_line(line)
            line = fptr.readline()
            num_coords, cnt = read_control_line(line, cnt)
            # print(name, num_coords, cnt)

            poly_arr = []
            for i in range(num_coords):
                line = fptr.readline()
                # print(line)
                cnt = append_polygon(poly_arr, line, cnt)

            if cnt == num_coords + 2:    # L001, control line, coord lines
                data.append( {name: poly_arr})

            line = fptr.readline()

        # this variable is the in memory of land boundary
        # not formatted as geojson, however, coordinates are
        # ready for geojson formatting
        # print(data)

    # format and write into a geojson file
    geojson_data = land_bnd + ".geojson"
    format_2_polycollection(data, geojson_data)

    # load into database
    load_dflow_landbnd(geojson_data)



def load_dflow_landbnd(geojson_data):

    # un-comment these two lines if only one to run this instead of
    # re-creating the geojson file.
    land_bnd = os.path.join(os.environ['DATA_SHARE'], 'gis/regional.ldb')
    geojson_data = land_bnd + ".geojson"

    with open(geojson_data, 'r') as fd:
        data = json.load(fd)

        for feature in data['features']:

            geom = GEOSGeometry(str(feature['geometry']))
            geoname = feature['properties']['name']

            land_bnd = DflowLandBoundary(
                name=geoname,
                geom=GEOSGeometry(geom))
            land_bnd.save()



# Expected input format:
# [ { key: [[long, lat], [long, lat], ...] }, {}, ... ]
# [
#  {'L001': [[-81.966701, 24.523758], [-81.978366, 24.5231], [-81.979655, 24.524691],
#            [-81.97462, 24.526934]]},
#  {'L002': [[],[],[],...,[]]}
# ]
# Output format:
# {"type": "FeatureCollection","features": [
#    {"type": "Feature","properties": { "name": "49518"},
#     "geometry": {"type":"Polygon","coordinates":[[
#        [29.96,-2.327],[29.919,-2.703],[29.724,-2.819],[29.438,-2.798],[29.371,-2.84],
# 	     [29.326,-2.654],[29.15,-2.592],[29.062,-2.602],[29.04,-2.745],[28.897,-2.66],
# 	     [28.862,-2.531],[28.884,-2.393],[29.119,-2.249],[29.175,-2.119],[29.136,-1.86],
# 	     [29.362,-1.509],[29.45,-1.506],[29.566,-1.387],[29.66,-1.393],[29.735,-1.34]]] }
#    },
#    {"type": "Feature","properties": { "name": "49518"},
#     "geometry": {"type":"Polygon","coordinates":[[ [],[], ..., [] ]]}
#    },
# ]}

# {"type": "FeatureCollection", "features": [
# { "type": "Feature",
#      "geometry": {
#        "type": "Polygon",
#        "coordinates": [
#          [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
#            [100.0, 1.0], [100.0, 0.0] ]
#          ]
#      },
#      "properties": {
#        "prop0": "value0",
#        "prop1": {"this": "that"}
#        }
# }
# ]}
def format_2_polycollection(data, outfile):

    # sample
    #
    geotype_str = \
        {"type": "Feature", "properties": { "name": "somename" },
         "geometry": { "type": "Polygon", "coordinates": [ [], [], ..., [] ]}
        },

    geocollection_str = \
        {"type": "FeatureCollection", "features": [ geotype_str ]}


    # write to file
    with open(outfile, 'w+') as fptr:
        fptr.write('{"type": "FeatureCollection", "features": [\n')

        # pay attention to order of coords
        last_line_index = len(data)
        i = 0
        for each_poly in data:
            i += 1
            # this only keeps the order if each_poly has only one key, as in land_bnd case
            for key in each_poly.keys():
                str = '\t{"type": "Feature", "properties": { "name": "' + key + '" },' + \
                      ' "geometry": { "type": "Polygon", "coordinates": [['

                coords_arr = each_poly[key]
                coord_str = ""
                open_braket = '['
                close_bracket = '],'
                for each_coord in coords_arr:
                    lon = each_coord[0]
                    lat = each_coord[1]
                    lon_lat = "%f,%f" % (lon, lat)
                    coord_str += open_braket + lon_lat + close_bracket

                if i == last_line_index:
                    str += coord_str[:-1] + ']]}}\n'
                else:
                    str += coord_str[:-1] + ']]}},\n'
                fptr.write(str)
        print(last_line_index, i)
        fptr.write('\n]}\n')   # needs this extra \n!!



def read_name_line(line):
    name = " "
    cnt = 0
    if line.startswith("L"):
        name = line.strip()
        cnt = 1
    return (name, cnt)


def read_control_line(line, cnt):
    num_coords = 0
    arr = line.split(" ")
    tmp_arr = []
    for str in arr:
        s = str.strip()
        if len(s) > 0:
            tmp_arr.append(s)

    if len(tmp_arr) == 2:
        num_coords = int(tmp_arr[0])
        num_cols = int(tmp_arr[1])
        cnt += 1

    return (num_coords, cnt)


def append_polygon(poly_arr, line, cnt):
    tmp_arr = []
    arr = line.split(" ")
    for str in arr:
        s = str.strip()
        if len(s) > 0:
            tmp_arr.append(float(s))
    poly_arr.append([tmp_arr[0], tmp_arr[1]])
    cnt += 1
    return cnt

# for shapefile

# TM_WORLD_BORDERS-0.1.ZIP
# encoding='iso-8859-1'
# The original shapefile (world_borders.zip, 3.2 MB) was downloaded from the Mapping Hacks website:
# http://www.mappinghacks.com/data/

# for shapefiles
world_mapping = {
    'fips': 'FIPS',
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'un': 'UN',
    'name': 'NAME',
    'area': 'AREA',
    'pop2005': 'POP2005',
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'lon': 'LON',
    'lat': 'LAT',
    'geom': 'MULTIPOLYGON',
}

world_shp = os.path.abspath(
    os.path.join(os.environ['DATA_SHARE'], 'gis', 'TM_WORLD_BORDERS-0.3.shp'),  # encoding='iso-8859-1'
)


def run_world_border(verbose=True):
    lm = LayerMapping(
        WorldBorder, world_shp, world_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)


# shape file - source: http://www.naturalearthdata.com/downloads/50m-physical-vectors/
# python manage.py ogrinspect /media/sf_BEHEEN/PROJECTS/owp-nwm-coastal/dflow-visual/data/gis/ne_50m_ocean.shp WorldOcean --srid=4326--mapping --multi
# Auto-generated `LayerMapping` dictionary for WorldOcean model
worldocean_mapping = {
    'scalerank': 'scalerank',
    'featurecla': 'featurecla',
    'min_zoom': 'min_zoom',
    'geom': 'MULTIPOLYGON',
}

ocean_shp = os.path.abspath(
    os.path.join(os.environ['DATA_SHARE'], 'gis', 'ne_50m_ocean.shp'),
)

def run_world_ocean(verbose=True):
    lm = LayerMapping(
        WorldOcean, ocean_shp, worldocean_mapping
    )
    lm.save(strict=True, verbose=verbose)


# Auto-generated `LayerMapping` dictionary for ChesapeakBay model
chesapeakbay_mapping = {
    'ccaname': 'ccaname',
    'geom': 'MULTIPOLYGON',
}

chesapeakbay_shp = os.path.abspath(
    os.path.join(os.environ['DATA_SHARE'], 'gis', 'chesapeake_bay_projected.shp'),
)

def run_chesapeakbay(verbose=True):
    lm = LayerMapping(
        ChesapeakBay, chesapeakbay_shp, chesapeakbay_mapping
    )
    lm.save(strict=True, verbose=verbose)


# Auto-generated `LayerMapping` dictionary for DelawareBayBnd model
delawarebay_mapping = {
    'name': 'NAME',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'area_sqmil': 'area_sqmil',
    'publicarea': 'publicarea',
    'geom': 'MULTIPOLYGON',
}

delawarebay_shp = os.path.abspath(
    os.path.join(os.environ['DATA_SHARE'], 'gis', 'delaware_bnd_projected.shp'),
)

def run_delawarebay(verbose=True):
    lm = LayerMapping(
        DelawareBay, delawarebay_shp, delawarebay_mapping
    )
    lm.save(strict=True, verbose=verbose)



# Auto-generated `LayerMapping` dictionary for DelawareRiver model
delawareriver_mapping = {
    'type': 'TYPE',
    'name': 'NAME',
    'sqmi': 'SQMI',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON',
}
delawareriver_shp = os.path.abspath(
    os.path.join(os.environ['DATA_SHARE'], 'gis', 'delaware_river_projected.shp'),
)

def run_delawareriver(verbose=True):
    lm = LayerMapping(
        DelawareRiver, delawareriver_shp, delawareriver_mapping
    )
    lm.save(strict=True, verbose=verbose)


# Auto-generated `LayerMapping` dictionary for PamlicoSound model
pamlicosound_mapping = {
    'shape_area': 'SHAPE_AREA',
    'areasqkm': 'AREASQKM',
    'elevation': 'ELEVATION',
    'resolution': 'RESOLUTION',
    'fdate': 'FDATE',
    'permanent_field': 'PERMANENT_',
    'gnis_id': 'GNIS_ID',
    'gnis_name': 'GNIS_NAME',
    'ftype': 'FTYPE',
    'fcode': 'FCODE',
    'shape_leng': 'SHAPE_LENG',
    'geom': 'MULTIPOLYGON',
}
pamlicosound_shp = os.path.abspath(
    os.path.join(os.environ['DATA_SHARE'], 'gis', 'pamlico_sound_projected.shp'),
)

def run_pamlicosound(verbose=True):
    lm = LayerMapping(
        PamlicoSound, pamlicosound_shp, pamlicosound_mapping
    )
    lm.save(strict=True, verbose=verbose)




# python manage.py ogrinspect /media/sf_BEHEEN/PROJECTS/owp-nwm-coastal/dflow-visual/data/gis/ne_50m_coastline.shp WorldCoastline --srid=4326 --mapping --multi
# Auto-generated `LayerMapping` dictionary for WorldCoastline model
worldcoastline_mapping = {
    'scalerank': 'scalerank',
    'featurecla': 'featurecla',
    'min_zoom': 'min_zoom',
    'geom': 'MULTILINESTRING',
}
coastline_shp = os.path.abspath(
    os.path.join(os.environ['DATA_SHARE'], 'gis', 'ne_50m_coastline.shp'),
)

def run_world_coastline(verbose=True):
    lm = LayerMapping(
        WorldCoastline, coastline_shp, worldcoastline_mapping
    )
    lm.save(strict=True, verbose=verbose)


# csv to geojson - it is not geojson - must be fixed!!
def coops_wl_csv2json():
    # Source: https://opendap.co-ops.nos.noaa.gov/ioos-dif-sos/ClientGetter?p=6
    # Station ID      Station Name    Deployed        Latitude        Longitude
    csv_file = os.path.join(os.environ['DATA_SHARE'], 'gis/coops_waterlevel.csv')

    reader = csv.DictReader(open(csv_file, 'rU'),
                            fieldnames=('Station ID', 'Station Name', 'Deployed', 'Latitude', 'Longitude'),
                            delimiter="\t")

    # Parse the CSV into JSON
    out = json.dumps([row for row in reader])

    # Save the JSON
    f = open(os.path.join(os.environ['DATA_SHARE'], 'gis/coops_waterlevel.json'), 'w')
    f.write(out)



# for geojson file format
def read_geojson_file(jsonfile):
    json_file = os.path.join(os.environ['DATA_SHARE'], 'gis', jsonfile)
    source = open(json_file)
    for ws in deserialize('geojson', source):
        print(type(ws))
        # ws.save()
        print(ws)   # not completed yet

"""
https://gis.stackexchange.com/questions/48949/epsg-3857-or-4326-for-googlemaps-openstreetmap-and-leaflet

Google Earth is in a Geographic coordinate system with the wgs84 datum. (EPSG: 4326)
Google Maps is in a projected coordinate system that is based on the wgs84 datum. (EPSG 3857)
The data in Open Street Map database is stored in a gcs with units decimal degrees & datum of wgs84. (EPSG: 4326)
The Open Street Map tiles and the WMS webservice, are in the projected coordinate system that is based on 
the wgs84 datum. (EPSG 3857)

So if you are making a web map, which uses the tiles from Google Maps or tiles from the Open Street Map webservice, 
they will be in Sperical Mercator (EPSG 3857 or srid: 900913) and hence your map has to have the same projection.

Edit:

I'll like to expand the point raised by mkennedy
All of this further confused by that fact that often even though the map is in Web Mercator(EPSG: 3857), 
the actual coordinates used are in lat-long (EPSG: 4326). This convention is used in many places, such as:

In Most Mapping API's You can give the coordinates in Lat-long, and the API automatically transforms it to the 
appropriate Web Mercator coordinates.
While Making a KML, you will always give the coordinates in geographic Lat-long, even though it might be showed on 
top of a web Mercator map.
Most mobile mapping Libraries use lat-long for position, while the map is in web Mercator.

Just to add, EPSG:3857 calls its units metres, but they are not real metres. The more to the north you come, 
the more squeezed they are.

What's also confusing is that you often interact with Google Maps or Bing Maps using EPSG: 4326, for instance in KML 
files. Internally the servers convert the data to their equivalent of EPSG: 3857. 
If you're mashing up data against one of their tiles, the tile is using EPSG: 3857 so it's faster for you to convert 
your data to that first.

Does this mean that when calculating the projection values, it is safe to use OSM for Google Maps? 
Such as converting lat to y: wiki.openstreetmap.org/wiki/Mercator#Spherical_Mercator
Yes. you can use the same coordinates for OSM, as well as Google Maps (as well as many others including Bing, here etc.)

"""

# set shell env > DATA_SHARE='path to datafile locations'
# default path is base_dir/data/gis
# to create mapping and the model use this command:
# python manage.py ogrinspect [options] <data_source> <model_name> [options]
# python manage.py ogrinspect world/data/TM_WORLD_BORDERS-0.3.shp WorldBorder --srid=4326 --mapping --multi >> voivodeships/models.py
# copy mapping part here (see world_mapping above )
#
# to run > python manage.py gisapp_load_data

class Command(BaseCommand):

    def load_data(self, arg=None):
        # coops_wl_csv2json()
        # run_world_border()
        # run_weather_station()
        # coops_active_meters()
        # coops_waterlevel()
        # run_world_ocean()
        # run_world_coastline()
        # ndbc_buoy()
        # run_chesapeakbay()
        # run_delawarebay()
        # run_delawareriver()
        # run_pamlicosound()
        # dflow_landboundary()          # run if geojson file does not exit and in general this is the main method.
        load_dflow_landbnd("filename")  # run if geojson file exits and you don't want to re-create

    def handle(self, *args, **options):
        self.load_data()

