#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 17:46:35 2024

@author: boumendilp
"""

import json
import pandas as pd
import os
import random

path_geoclimate_folder = "/home/boumendilp/Documents/GeoClimate/osm_43.49_1.37_43.53_1.45/" # path of the Geoclimate output folder
path_csv_cover = os.path.join(path_geoclimate_folder, 'csv_cover') #path for the forlder of the cvs files from Step 2
path_geoclimate_modify_folder = os.path.join(path_geoclimate_folder, 'modify_geojson') # path of the folder from Step 1
name_file_list = ["urban_areas","vegetation","water"] # list of the geojson and csv
unknown_file_name = 'unknown_areas.geojson' #name off the geojson output file from Step 1
unknown_N_COVER = 87 # cover number to applied in the unknown_file
# 87 = N-America semiarid continental Open Shrubland

#######################################################################################################################################

def add_N_COVER(input_geojson_path, csv_file_path ,output_geojson_path):
#This function adds an N_COVER properties to a geojson file according to its TYPE and according to the equivalence from a cvs file    
    csv_data = pd.read_csv(csv_file_path)
    
    #opening the geojson
    with open(input_geojson_path, 'r') as geojson_file:
        geojson_data = json.load(geojson_file)
    
    # Create a mapping from "TYPE" to "N_COVER" from the csv
    type_to_ncover_mapping = dict(zip(csv_data['TYPE'], csv_data['N_COVER']))
    
    # For eatch feature of the GeoJSON 
    for feature in geojson_data['features']:
        #found the TYPE
        type_value = feature['properties']['TYPE']
        #found the equivalent N_COVER from the csv
        n_cover_value = type_to_ncover_mapping.get(type_value)
        
        #Add it to the properties of the features (polygone)
        if n_cover_value is not None:
            feature['properties']['N_COVER'] = n_cover_value
        else:
            print(f'No N_COVER value found for TYPE: {type_value}')
    
    #Updating geojson with modifications
    with open(output_geojson_path, 'w') as updated_geojson_file:
        json.dump(geojson_data, updated_geojson_file, indent=2)
        
    print(f"The following GeoJSON file has been modify : '{output_geojson_path}'")

# use of the function for name_file_list
for name in name_file_list : 
    add_N_COVER(os.path.join(path_geoclimate_folder,f'{name}.geojson'), os.path.join(path_csv_cover, f'{name}.csv'),os.path.join(path_geoclimate_modify_folder, f'{name}.geojson'))
    

#########################################################################################

# This part of the code allows to add a unique N_COVER for all the features from the unknown_file created in Step 1

geojson_file_path = os.path.join(path_geoclimate_modify_folder, unknown_file_name)

with open(geojson_file_path, 'r') as geojson_file:
    geojson_data = json.load(geojson_file)

# Add to GeoJSON features a the unknown_N_COVER
for feature in geojson_data['features']:
        feature['properties']['N_COVER'] = unknown_N_COVER 
        
   
# Save the updated GeoJSON file
with open(geojson_file_path, 'w') as geojson_file_path:
    json.dump(geojson_data, geojson_file_path, indent=2)

print('All GeoJSON files updated successfully.')

#########################################################################################

# This part of the code creates a csv file with the cover numbers ordered in ascending order
# and associates a color and a description which will be used later to create the legend 
# of the map after the PREP_PGD step of Meso-NH

# Create a dictionary to store the DataFrames
dfs = {}

# create DataFrames
for name in name_file_list : 
    dfs[name] = pd.read_csv(os.path.join(path_csv_cover, f'{name}.csv'))
    
# Merge DataFrames 
merged_df = pd.concat(dfs.values(), ignore_index=False)


def format_n_cover(n_cover):
    return f'COVER{n_cover:03d}'

# add a NAME column with the COVER000 format
merged_df['NAME'] = merged_df['N_COVER'].apply(format_n_cover)

# Delete the “TYPE” column
merged_df = merged_df.drop(columns=['TYPE'])

# Remove duplicates row that have the same "N_COVER"
merged_df = merged_df.drop_duplicates(subset=['N_COVER'])

# Sort by column "N_COVER" in ascending order
merged_df= merged_df.sort_values(by='N_COVER')

# List of default color names
color_names = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown", "grey"]

# add a color column with randam color names
merged_df['color'] = [random.choice(color_names) for _ in range(len(merged_df))]

print(merged_df)
merged_csv_path = os.path.join(path_csv_cover, 'cover_color_legend.csv')

# Write in a new CSV file
merged_df.to_csv(merged_csv_path, index=False)

print(f"The following csv file has been created : '{merged_csv_path}'")
print("You can edit it to change the default caption colors for each COVER")
print('You can now do Step 4')