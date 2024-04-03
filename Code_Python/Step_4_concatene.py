#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 13:47:14 2024

@author: boumendilp
"""

import json
import os


path_geoclimate_folder = "/home/boumendilp/Documents/GeoClimate/osm_43.49_1.37_43.53_1.45/"# path of the Geoclimate output folder
path_geoclimate_modify_folder = os.path.join(path_geoclimate_folder, 'modify_geojson') # path of the folder from Step 1
name_file_list = ["vegetation.geojson", "urban_areas.geojson", "water.geojson","unknown_areas.geojson"]  # list of the geojson files that must be concatenate
concatene_file_name = "Portet_sur_Garonne.geojson" # name of the concatenate output file


#Found the "name" for the EPSG
with open(os.path.join(path_geoclimate_modify_folder, name_file_list[0])) as f:
    data = json.load(f)
name_EPSG = data["crs"]["properties"]["name"]

print("name_EPSG = ",name_EPSG)

# Initialize the GeoJSON dictionary containing the oncatenate features
geojson_concatene = {
    "type": "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {
            "name": name_EPSG
        }
    },
    "features": []
}

# For eath geojson from name_file_list
for name in name_file_list : 
    path = os.path.join(path_geoclimate_modify_folder, name)
    
    # We concatenate with the dictionary define previously 
    with open(path, "r") as f:
        data = json.load(f)
        geojson_concatene["features"].extend(data["features"])
    
path_concatene_file_name = os.path.join(path_geoclimate_modify_folder, concatene_file_name)

# Save the concatenated GeoJSON file with the specify name
with open(path_concatene_file_name, "w") as f:
    json.dump(geojson_concatene, f)


print(f"The following concatenet file hase been created : '{path_concatene_file_name}'")
    
