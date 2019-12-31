#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Chris Jing 
Email: zjing@eoas.ubc.ca
For: UBC EOAS WFRT 
Created on Tues Jan 30 14:42:00 2018
Description: this program read in two geogrid topo_30s tiles, and generate 
             a csv file to store the elevation data along a latitude line 
             
"""

import csv 
import os
import numpy as np
import struct  
from netCDF4 import Dataset
from wrf import to_np, getvar, latlon_coords
from math import radians, cos, sin, asin, sqrt

# This function reads a binary file, converts into a 2D array of signed integers
# Inputs: str, the path of the binary file 
# Output: arr, a 2D square array of signed int
def binaryTo2DArray(file_path):
    with open(file_path, "rb") as binary_file: 
        data = binary_file.read() 
    
    byte_order = ">"              # represent the big-endian bypte order
    elem_count = str(1206 * 1206) # represent the number of elements in the tile 
    format_char = "h"             # represent short int of size 2 bytes

    arr_1d = struct.unpack(byte_order + elem_count + format_char, data) 
    arr_2d = np.reshape(arr_1d, (1206, 1206))
    return arr_2d 

        
# This function calculate the great circle distance between twop points on Earth
# (specified in decimal degrees) 
# Inputs: lat1, latitude of point 1
#         lon1, longitude of point 1
#         lat2, latitude of point 2  
#         lon2, longitude of point 2
# Output: distance between point 1 and 2 in km
def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # haversie formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2 
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of Earth in km 
    return c * r 

# This function returns the indice where the coordinate is 
# closest to the given latitude and longitude
# Inputs: lats2D, a 2D array that stores the latitudes of several points 
#          lons2D, a 2D array that stores the longitudes of several points 
#          lat, the latitude of the point to compare against
#          lon, the longitude of the point to compare against
# Outputs: the index that holds the closest distance 
# Requires: lats2D and lons2D must have the same dimension (shape)
def closestIndex(lats, lons, lat, lon): 
    dists = np.zeros((len(lats), len(lats[0])))
    for row in range(0, len(lats)): 
        for col in range(0, len(lats[0])):
            dist = haversine(lats[row][col], lons[row][col],lat, lon)
            dists[row][col] = dist
    return np.where(dists == dists.min())

"""
START OF PROGRAM
"""

## Assign file path and directory for the binary tile files 
main_dir = '/Users/JZC/Desktop/EOAS_Research_Assistant/Project_2/tifReader/Pacific_Northwest_Files'

tile_NW = '06001-07200.16801-18000' # Pacific Northwest Region Tile Northwest (-130 - -120, 50-60)

file_path_NW = os.path.join(main_dir, tile_NW) 
arrNW = binaryTo2DArray(file_path_NW)

x0 = -130 # Longitude to start at 
xN = -120 # Longitude to end at
dx = 10.0/1200.0 # displacement between adjacent elevation data points 
rowSelected = 3 # correspond to 50 N latitude line 
latitude = 50 
col0 = 3 #(130 degree W)
colN = 1206 - 3 #(130 degree W)

## read the netcdf file for Pacific Northwest Region (4 km grid size domain)
## Assign file path and directory for the wrfout file 
main_dir = '/Users/JZC/Desktop/EOAS_Research_Assistant/Project_2/netcdfReader/geogrid_files_mc'
wrf_file = 'geo_em.1.333.nc'
nc = Dataset(os.path.join(main_dir,wrf_file),'r') # nc is a python datatype
 
# Model terrain height (from wrf-python)
hgt = getvar(nc, 'ter') 
# 2D array for the errain height data 
elevArray = to_np(hgt)
# Get latitude and longitude points
lats, lons = latlon_coords(hgt, as_np=True) 

with open('50_N_Terrain_Height_Table.csv', 'w') as csvfile: 
    fieldnames = ['Longitude (degree)', 'geotiff Topo_30s Raw Height (m)', 'netCDF WPS 1.333 km grid size Smoothed Height (m)']
    elevWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    elevWriter.writeheader() 
    
    for i in range(col0, colN):
        longitude = round(x0 + dx * (i - col0), 3)
        
        if (longitude >= (lons[rowSelected][0]).item()) & (longitude <= (lons[rowSelected][len(lons[rowSelected]) - 1]).item()):
            closest = closestIndex(lats, lons, latitude, longitude)
        
            smoothedHgt = elevArray[(closest[0][0])][(closest[1][0])] 

            elevWriter.writerow({'Longitude (degree)': longitude, \
                                 'geotiff Topo_30s Raw Height (m)': arrNW[rowSelected][i], \
                                 'netCDF WPS 1.333 km grid size Smoothed Height (m)': smoothedHgt}) 
            print("Longitude = ", longitude)
            print("Height =", smoothedHgt) 
            print() 