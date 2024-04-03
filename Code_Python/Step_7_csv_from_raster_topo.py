#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:27:30 2024

@author: ChatGPT et boumendilp
"""
import rasterio
import csv
import os


path_topo_folder = "/home/boumendilp/Documents/Topography/Opentopography/Portet3" # path of the topographie folder
raster_file_name = 'output_AW3D30.tif'  # name of the rasterise file from OpenTopography
csv_file_name = 'AW3D30.txt' # name of the csv output file

#Open the rasterize file
with rasterio.open(os.path.join(path_topo_folder, raster_file_name)) as src:
    # we store the pixel values in the variable raster_data
    raster_data = src.read(1)
    
    # extracts transform matrix from the raster file
    transform = src.transform
    
    # Créer un fichier CSV pour enregistrer les données
    path_csv_file_name = os.path.join(path_topo_folder, csv_file_name)
    with open(path_csv_file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ')
        
        # Ajouter l'en-tête du fichier CSV
        csv_writer.writerow(['Latitude [deg]', 'Longitude [deg]', 'Topo [m]'])
        
        # Parcourir tous les pixels et récupérer leurs valeurs
        for j in range(src.height):
            for i in range(src.width):
                # We add 0.5 to be at the center of the pixel
                # we multiply by transform to convert in UTM coordinate
                lon, lat = transform * (i + 0.5, j + 0.5)
                
                # Valeur du pixel
                pixel_value = raster_data[j, i]
                # save data in the csv file
                csv_writer.writerow([lat, lon, pixel_value])
                #print(f"Coordonnées ({lat}, {lon}), Topo : {pixel_value}")

print(f"The following csv file hase been created : '{path_csv_file_name}'")