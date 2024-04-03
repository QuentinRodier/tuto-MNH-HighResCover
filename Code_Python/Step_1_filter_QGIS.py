#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 16:45:39 2024

@author: boumendilp
"""

import sys
from qgis.core import QgsApplication
import os
import shutil

# Starts the qgis application without the graphical user interface
gui_flag = False
app = QgsApplication([], gui_flag)
app.initQgis()

sys.path.append('/usr/share/qgis/python/plugins/')

import processing

from processing.core.Processing import Processing
Processing.initialize()


path_geoclimate_folder = "/home/boumendilp/Documents/GeoClimate/osm_43.49_1.37_43.53_1.45/" #path of the Geoclimate output folder
path_geoclimate_modify_folder = os.path.join(path_geoclimate_folder, 'modify_geojson') #path of the output folder from Step 1
name_file_list = ["urban_areas", "vegetation", "water"] #list of the geojson file with define TYPE
target_geojson = 'rsu_utrf_floor_area' #geojson file with all the polygones
output_geojson = 'unknown_areas' #name of the output filter geojson


#######################################################################################################################################
#creation of the folder
if not os.path.exists(path_geoclimate_modify_folder):
    os.makedirs(path_geoclimate_modify_folder)


input_geojson = os.path.join(path_geoclimate_folder, f'{target_geojson}.geojson')

# Loop through name_file_list to remove polygons from target_geojson
for name_file in name_file_list:
    input_path = os.path.join(path_geoclimate_folder, f'{name_file}.geojson')
    shutil.copy2(input_path, path_geoclimate_modify_folder)
    output_path = os.path.join(path_geoclimate_modify_folder, f'{target_geojson}_{name_file}.geojson')

    # Using the qgis difference function for each file
    processing.run("native:difference", {'INPUT': input_geojson, 'OVERLAY': input_path, 'OUTPUT': output_path})

    # The output of the current process becomes the input for the next one
    input_geojson = output_path

# Rename the last output file as output_geojson
path_output_geojson = os.path.join(path_geoclimate_modify_folder, f'{output_geojson}.geojson')
os.rename(output_path, path_output_geojson)

print('The file ' + f'{path_output_geojson}' + ' have been create')
print('You can now proced to Step 2')