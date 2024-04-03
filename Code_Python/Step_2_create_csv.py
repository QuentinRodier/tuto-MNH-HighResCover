#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 12:59:07 2024

@author: boumendilp
"""

import json
import csv
import os

path_geoclimate_folder = "/home/boumendilp/Documents/GeoClimate/osm_43.49_1.37_43.53_1.45/" # path of the Geoclimate output folder
path_geoclimate_modify_folder = os.path.join(path_geoclimate_folder, 'modify_geojson') # path of the folder from Step 1
name_file_list = ["urban_areas", "vegetation", "water"] # list of the geojson file with define TYPE
path_csv_cover = os.path.join(path_geoclimate_folder, 'csv_cover') #path for the forlder of the cvs files

#######################################################################################################################################

# creation of the folder for the csv file
if not os.path.exists(path_csv_cover ):
    os.makedirs(path_csv_cover )

def geojson_to_csv(input_geojson_path, output_csv_path):
#This function creates a csv with the list of TYPE mentioned in a geojson file
    # Read GeoJSON file
    with open(input_geojson_path, 'r', encoding='utf-8-sig') as geojson_file:
        geojson_data = json.load(geojson_file)

    # Extract unique "TYPE" values
    type_values = set()
    for feature in geojson_data['features']:
        type_value = feature['properties'].get('TYPE')
        type_values.add(type_value)

    # Create CSV file path with the same base name as GeoJSON but with a .csv extension
    output_csv_path = os.path.splitext(output_csv_path)[0] + '.csv'

    # Write unique "TYPE" values to CSV file with header "N_COVER" and "Description" column
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['TYPE', 'N_COVER','Description'])
        for type_value in type_values:
            csv_writer.writerow([type_value,'',''])
            
    print(f"The following CSV file has been created : '{output_csv_path}'")


# use of the function for name_file_list
for name in name_file_list : 
    geojson_to_csv(os.path.join(path_geoclimate_modify_folder,f'{name}.geojson'), os.path.join(path_csv_cover, f'{name}.csv'))

print('You can now fill these CSV files with the cover numbers of your choice according to the Surfex documentation : https://www.umr-cnrm.fr/surfex/spip.php?article219')
print('Then do Step 3')