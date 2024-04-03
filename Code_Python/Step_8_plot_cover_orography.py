#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 11:11:45 2024

@author: boumendilp
"""

import numpy as np
import netCDF4 as nc 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.colors import ListedColormap
import os
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches


ncfile_list = []
path_PGD_folder = '/home/boumendilp/Documents/Resultats/Meso_NH/Realiste/007_16janvier_EOL40_ADR/PGD/'
ncfile_list = ["16JAN98_1km.nc","16JAN98_3km.nc","16JAN98_9km.nc"]
ncfile_list_titre = ["Domaine 4","Domaine 3","Domaine 2"]

# Load CSV file with colors
csv_color = '/home/boumendilp/Documents/GeoClimate/Lewes_v2/csv_full/csv_fusion_color.csv'
df_colors = pd.read_csv(csv_color)

eol = False #if you have a wind turbine in your simulation and you want to plot it

#########################################################################################"

if eol == True :
    farm_file = path_PGD_folder +"data_farm.csv"
    farm_Data = pd.read_csv(farm_file)
    Lat = farm_Data.values[:,0]
    Long = farm_Data.values[:,1]


p = 0
for filename in ncfile_list:
    
    print('Hello' + filename)
    nc_file = os.path.join(path_PGD_folder, filename)
    
    latitude = nc.Dataset(nc_file).variables['latitude'][1:,1:]
    longitude = nc.Dataset(nc_file).variables['longitude'][1:,1:]
    ZS = nc.Dataset(nc_file).variables['ZS'][1:-1,1:-1]
    
    # Open the netCDF
    dataset = nc.Dataset(nc_file)
    
    # Get list of variable names
    liste_variables = dataset.variables.keys()
    
    # Filter variables starting with 'COVER' and exclude 'COVER_LIST' and 'COVER_PACKED'
    liste_cover = [var for var in liste_variables if var.startswith('COVER') and var not in ['COVER_LIST', 'COVER_PACKED']]
    liste_matrice_cover = [nc.Dataset(nc_file).variables[matrice][1:-1, 1:-1] for matrice in liste_cover]

    n_x = np.size(longitude[0,:])-1
    n_y = np.size(latitude[:,0])-1
    carte = np.zeros((n_x, n_y))
    
    colors_liste = []
    legend_list = []
    
    # Loop over the domaine to find the most present cover for eatch mesh cel
    for i in range(n_x):
        for j in range(n_y): 
            max_value = 0
            
            # Loop over the cover
            k = 0
            for matrice in liste_matrice_cover: 
                k = k + 1
                if matrice[i,j]>max_value:
                    max_value = np.max(matrice[i,j])
                    N_COVER_value = k
                    
            # We save a new matrix with the index of the most present COVER
            carte[i,j] = N_COVER_value
    
    
    #Loop over the cover list to made the legend label and color
    k = 0   
    for matrice in liste_matrice_cover:
            ligne_correspondante = df_colors[df_colors['NAME'] == liste_cover[k]]
            print('k=')
            print(ligne_correspondante)
            colors_liste.append(ligne_correspondante['color'].values[0])
            legend_list.append(liste_cover[k] +' : ' + ligne_correspondante['Description'].values[0])
            k = k + 1
      
        
    # Figure COVER
    projection = ccrs.PlateCarree()
    fig, ax = plt.subplots(subplot_kw={'projection': projection}, figsize=(10, 8))
    
    # Add coastlines and political borders
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    # Create a list of legend handles and labels
    legend_handles = [mpatches.Patch(color=c) for c in colors_liste]

    #Plot map
    cmap = plt.cm.get_cmap(ListedColormap(colors_liste))
    ax.pcolormesh(longitude, latitude, carte, cmap=cmap, alpha=1)
    
    #Plot legend and axes
    ax.legend(legend_handles, legend_list, loc='center right', bbox_to_anchor=(1.65, 0.5))
    ax.set_xticks(np.linspace(longitude.min(), longitude.max(),5))
    ax.set_yticks(np.linspace(latitude.min(), latitude.max(),5))
    
    if eol == True :
        x, y = ax.projection.transform_point(Long, Lat, ccrs.PlateCarree())
        ax.plot(x, y, 'rx', markersize=15, label='Eolienne')
     
    # Add a general title to the figure
    fig.suptitle(ncfile_list_titre[p], fontsize=20)
    p = p + 1
    
    # Close netCDF
    dataset.close()
    
    plt.show()
 
    # Figure OROGRAPHY
    projection = ccrs.PlateCarree()

    fig, ax = plt.subplots(subplot_kw={'projection': projection}, figsize=(10, 8))

    # Add coastlines and political borders
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    
    # plot ZS
    pcm = ax.pcolormesh(longitude, latitude, ZS, transform=ccrs.PlateCarree(), cmap="terrain", shading='auto')

    cbar = plt.colorbar(pcm, ax=ax, orientation='vertical', pad=0.05)
    cbar.set_label('ZS')

    ax.set_xlabel('Longitude', fontsize=15)
    ax.set_ylabel('Latidude', fontsize=15)
    ax.set_title('Orography', fontsize=15)
    
    ax.set_xticks(np.linspace(longitude.min(), longitude.max(),5))
    ax.set_yticks(np.linspace(latitude.min(), latitude.max(),5))
    
    plt.show()
   

  
        
        
       
