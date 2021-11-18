#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 02:18:52 2021

@author: carla nicolin
"""
import os
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable

from celluloid import Camera
from netCDF4 import Dataset as netcdf_dataset
import numpy as np

from cartopy import config
import cartopy.crs as ccrs

###############################
print('This python script animates n latlon.nc output files from MPAS! (command line version).')
print('Before executing the script make sure:')
print('      (1) history_date.nc are converted to latlon_date.nc files (see https://github.com/mgduda/convert_mpas)')
print('      (2) latlon.nc files are in one directory whith nothing else in it')  
### get PATH
print('please type path to the directory with latlon.nc files')
input_path = input()

### get FILES and number of files
path, dirs, files = next(os.walk(input_path))
file_count = len(files); files.sort()

### CHECK VARIABLES FITTING (TIME, LAT, LON) DIMENSIONS
dataset = netcdf_dataset(path+'/'+files[0], mode='r')
wanted_vars = []; wanted_longname = []; wanted_units = []

### loop through all variables to find those with fitting dimension for plot
for v in dataset.variables:
  if dataset.variables[v].dimensions == (u'Time', u'latitude', u'longitude'):
    wanted_vars.append(v)
    wanted_units.append(dataset[v].units)
    
    try: 
        long_name_avail = True
        wanted_longname.append(dataset[v].long_name)
    except AttributeError as exception:
        long_name_avail = False

temp_array_vars = []
  
print('your plot options are:')
for i in range(0,len(wanted_vars)):
    print('-------------------------------------')
    print('variable name:   ', wanted_vars[i])
    temp_array_vars.append(wanted_vars[i])
    print('plot-index:', i)
    if long_name_avail==True:
        print('Info:', wanted_longname[i])

print('ARRAY SHORTNAMES', temp_array_vars)
### VARIABLE FOR COLOURPLOT
print('-------------------------------------')
print('choose parameter to plot (type the plot-index from above):')
input_var = int(input())
print(wanted_longname[input_var], 'will be plottet')
print('-------------------------------------')

### GET LAT,LON, INPUT VARIABLE FROM NETCDF LATLON FILE
sim_date_list = []; lats_list = []; lons_list = []; ckey_list = []
ckey_max_list = []; ckey_min_list = []
for m in range(0,file_count):
            ### extract simulation time from latlon for title
            sim_date = str(files[m]).replace('latlon.','')
            sim_date = sim_date.replace('.nc','')
            
            ### IMPORT latitute and longitude
            dataset = netcdf_dataset(path+'/'+files[m], mode='r')
            lats = dataset.variables['latitude'][:]
            lons = dataset.variables['longitude'][:]
            ckey = dataset.variables[wanted_vars[input_var]][0, :, :]
            
            sim_date_list.append(sim_date)
            lats_list.append(lats)
            lons_list.append(lons)
            ckey_list.append(ckey)
            
            ckey_1d = ckey[:]*1
            ckey_max_list.append(np.max(ckey_1d))
            ckey_min_list.append(np.min(ckey_1d))

ckey_max = np.nanmax(ckey_max_list)
ckey_min = np.nanmax(ckey_min_list)
print(ckey[1,1])
# for i in range(0,len(ckey_1d)):
#     ckey[i] = ckey[i-273]

### PLOTTING
print('-------------------------------------')
print('choose plot title:')
input_title = input()

fig = plt.figure()

### PLOT data     
ax = plt.subplot(1,1,1, projection=ccrs.PlateCarree())
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
camera = Camera(fig)
for k in range(0,file_count):
    ax.coastlines(alpha=0.5)

    cplot = ax.contourf(lons_list[k], lats_list[k], ckey_list[k], 60, vmin=ckey_min, vmax=ckey_max,  transform=ccrs.PlateCarree())
    plt.text(-6, 26, 'time:  ' + sim_date_list[k], fontsize=12, weight='bold')
    ax.set_title(input_title + '(' + wanted_longname[input_var] + ')', pad=12.5)

    camera.snap()
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
cbar = plt.colorbar(ScalarMappable(norm=cplot.norm), cmap=cplot.cmap, pad = 0.22) # pad is for extra distance to plot
cbar.set_label(wanted_vars[input_var] + '    [' + wanted_units[input_var] + ']')  
#cbar.set_ticks([ckey_min-273,ckey_max-273])
anim = camera.animate(blit=False, interval=700, repeat=True)
anim.save(input_title+'.gif')
print('Your gif was saved as ', input_title,'.gif')
