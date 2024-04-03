#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:57:10 2024

@author: boumendilp
"""

import sys
import os
from qgis.core import QgsApplication
import geopandas as gpd
from osgeo import gdal, ogr
import atexit

# Starts the qgis application without the graphical user interface
gui_flag = False
app = QgsApplication([], gui_flag)
app.initQgis()

sys.path.append('/usr/share/qgis/python/plugins/')

import processing

from processing.core.Processing import Processing


Processing.initialize()


path_geoclimate_folder = "/home/boumendilp/Documents/GeoClimate/osm_43.49_1.37_43.53_1.45/" # path of the Geoclimate output folder
path_geoclimate_modify_folder = os.path.join(path_geoclimate_folder, 'modify_geojson') # path of the folder from Step 1
path_geoclimate_raster_folder = os.path.join(path_geoclimate_folder, 'raster') # path of the output folder from Step 5
concatene_file_name = "Portet_sur_Garonne.geojson"  # name of the concatenate output file from Step 4
raster_file_name = 'Portet_sur_Garonne_raster.tif' # name of the rasterise output file
width_pixel = 5 #with of each pixel of the rasterization in meter
height_pixel = 5 #height of each pixel of the rasterization in meter

#########################################################################################"

if not os.path.exists(path_geoclimate_raster_folder):
    # creation of the folder for the rasterize file
    os.makedirs(path_geoclimate_raster_folder)

path_concatene_file_name = os.path.join(path_geoclimate_modify_folder, concatene_file_name)
path_raster_file_name = os.path.join(path_geoclimate_raster_folder, raster_file_name)

#computation of the extent of the domain
extent = gpd.read_file(path_concatene_file_name).total_bounds
#returned in the correct format for the QGIS function
EXTENT = f'{extent[0]},{extent[2]},{extent[1]},{extent[3]}'
print("Compute EXTENT =", EXTENT)

#Using the qgis rasterize function
processing.run("gdal:rasterize", {'INPUT': path_concatene_file_name +'|geometrytype=Polygon','FIELD':'N_COVER','BURN':0,'USE_Z':False,'UNITS':1,'WIDTH':width_pixel,'HEIGHT':height_pixel,'EXTENT':EXTENT,'NODATA':0,'OPTIONS':'','DATA_TYPE':5,'INIT':None,'INVERT':False,'EXTRA':'','OUTPUT': path_raster_file_name})
print(f"The following rasterisation file hase been created : '{path_raster_file_name}'")

app.exitQgis()
