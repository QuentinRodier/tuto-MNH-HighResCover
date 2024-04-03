#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:27:30 2024

@author: ChatGPT et boumendilp
"""
import rasterio
from pyproj import Proj, transform
import csv
import os
import geopandas as gpd
import re

#This code uses the rasterio library to read a raster file (rasterized image) and convert
#its pixels to geographic coordinates (latitude and longitude) using the Universal Transverse Mercator (UTM) projection system.
#The code then creates a CSV file to save this data.
 
path_geoclimate_folder = "/home/boumendilp/Documents/GeoClimate/osm_43.49_1.37_43.53_1.45/" # path of the Geoclimate output folder
path_geoclimate_modify_folder = os.path.join(path_geoclimate_folder, 'modify_geojson') # path of the folder from Step 1
path_geoclimate_raster_folder = os.path.join(path_geoclimate_folder, 'raster') # path of the output folder from Step 5
raster_file_name = 'Portet_sur_Garonne_raster.tif'  # name of the rasterise output file from Step 5
concatene_file_name = "Portet_sur_Garonne.geojson" # name of the concatenate output file from Step 4
csv_file_name = 'Portet_sur_Garonne_ECOCLIMAP.csv' # name of the csv output file

####################################################################################################################

path_concatene_file_name = os.path.join(path_geoclimate_modify_folder, concatene_file_name)

gdf = gpd.read_file(path_concatene_file_name)

# Get Projection information
crs = gdf.crs
print("Projection:", crs)

# Print the projection
if crs is not None:
    print("Projection chaine:", crs.to_wkt())

    projection_string = crs.to_wkt()
    
# Extract UTM zone number
zone_utm_match = re.search(r'UTM zone (\d+)', projection_string)
if zone_utm_match:
    zone_utm = zone_utm_match.group(1)
    print("Zone UTM:", zone_utm)
else:
    print("Zone UTM non trouvée dans la chaîne de projection.")

# Define the projection 
# Coordinate UTM (Universal Transverse Mercator coordinate system)
#World Geodetic System 1984 (WGS84)
utm_proj = Proj(proj='utm', zone=zone_utm, ellps='WGS84') 

#####################################################################################################################

path_raster_file_name = os.path.join(path_geoclimate_raster_folder, raster_file_name)
path_csv_file_name = os.path.join(path_geoclimate_raster_folder, csv_file_name)

#Open the rasterize file
with rasterio.open(path_raster_file_name) as src:
    
    # we store the pixel values in the variable raster_data
    raster_data = src.read(1)
    # extracts transform matrix from the raster file
    transform = src.transform
    print(transform)
    
    # Create a CSV file
    with open(path_csv_file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ')
        
        # header of the CSV file
        csv_writer.writerow(['Latitude [deg]', 'Longitude [deg]', 'N_COVER [-]'])
        
        # Parcourir tous les pixels et récupérer leurs valeurs
        for j in range(src.height):
            for i in range(src.width):
                # Converts the pixel coordinates in the spatial reference system to geographic coordinates
                # We add 0.5 to be at the center of the pixel
                # we multiply by transform to convert in UTM coordinate
                x_coord, y_coord = transform * (i + 0.5, j + 0.5)
                # we then convert to latitude longitude in degre
                lon, lat = utm_proj(x_coord, y_coord, inverse=True)
                
                # we recover the value of the pixel (cover number)
                pixel_value = raster_data[j, i]
                
                # save data in the csv file
                csv_writer.writerow([lat, lon, int(pixel_value)])
                #print(f"Coordonnées ({lat}, {lon}), N_COVER : {pixel_value}")

print(f"The following csv file hase been created : '{path_csv_file_name}'")



