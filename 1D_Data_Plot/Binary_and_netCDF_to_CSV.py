#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:  Chris Jing 
Email:   zjing@eoas.ubc.ca
For:     UBC EOAS WFRT 
Purpose: this program read in four geogrid topo_30s tiles, 
         eight netCDF files with different grid sizes and 
         generate a csv file to store the elevation data along a latitude

Created on Tues Jan 30 14:42:00 2018
"""

import sys
import csv 
import os
import numpy as np
import struct  
from netCDF4 import Dataset
from wrf import to_np, getvar, latlon_coords
from scipy.interpolate import griddata 

# User change the following parameters 
latitude = float(sys.argv[1]) # options include any float between 40 and 60 exclusive
method = str(sys.argv[2]) # options include 'nearest', 'linear', 'cubic'


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


# This function reads two 2D arrays and fuse them into one single 2D array side by side
# Inputs: arrW, arrE (two 2D arrays)
# Output: arrFinal, a 2D array composed of elements from arrW on the left 
#         and elements from arrE on the right
# Requires: both arrays must all be square arrays witht same size 
def fuseTwoArray(arrW, arrE):
    size = len(arrW)
    listWE =[]
    for i in range(0, size):
        row_i = np.concatenate([arrW[i], arrE[i]]) 
        listWE.append(row_i)
    
    arrFinal = np.asarray(listWE) 
    return arrFinal 


# This function merge two arrays of latitudes and longitudes into one single array of coordinates
# Inputs: lats, a 2D array that stores the latitudes of several points 
#         lons, a 2D array that stores the longitudes of several points 
# Outputs: a 2D array of points made by merging lats and lons 
# Requires: lats and lons must have the same shapes (dimensions) 
    
def mergeLatsLons(lats, lons):
    points = np.zeros(shape=(len(lats) * len(lats[0]), 2))
    num = 0
    for row in range(0, len(lats)):
        for col in range(0, len(lats[0])):
            points[num][0] = lats[row][col]
            points[num][1] = lons[row][col]
            num += 1
    return points 


"""
START OF PROGRAM
"""

## Assign file path and directory for the binary tile files 
main_dir = '/Users/JZC/Desktop/EOAS_Research_Assistant/Project_2/tifReader/Pacific_Northwest_Files'
tile_NE = '07201-08400.16801-18000' # Pacific Northwest Region Tile Northeast (-120 - -110, 50-60)
tile_SE = '07201-08400.15601-16800' # Pacific Northwest Region Tile Southeast (-120 - -110, 40-50)
tile_NW = '06001-07200.16801-18000' # Pacific Northwest Region Tile Northwest (-130 - -120, 50-60)
tile_SW = '06001-07200.15601-16800' # Pacific Northwest Region Tile Southwest (-130 - -120, 40-50)

# create four 2D arrays from the four tiles 
file_path_NE = os.path.join(main_dir, tile_NE) 
file_path_SE = os.path.join(main_dir, tile_SE) 
file_path_NW = os.path.join(main_dir, tile_NW) 
file_path_SW = os.path.join(main_dir, tile_SW) 

arrNE = binaryTo2DArray(file_path_NE)
arrSE = binaryTo2DArray(file_path_SE)
arrNW = binaryTo2DArray(file_path_NW)
arrSW = binaryTo2DArray(file_path_SW)

arrN = fuseTwoArray(arrNW, arrNE) 
arrS = fuseTwoArray(arrSW, arrSE) 

if (latitude >= 50):
    arr = arrN
    rowSelected = int(((latitude - 50.0) / 10.0)* 1200.0 + 3.0)
else:
    arr = arrS 
    rowSelected = int(((50.0 - latitude) / 10.0)* 1200.0 + 3.0)

x0 = -130 # Longitude to start at 
xN = -110 # Longitude to end at
dx = 10.0/1200.0 # displacement between adjacent elevation data points 
col0 = 3 #(130 degree W)
colN = 1206 * 2 - 3 #(130 degree W)


plot_pts = np.zeros(shape=(2400, 2)) 
for i in range(0, 2400):
    plot_pts[i][0] = latitude 
    plot_pts[i][1] = x0 + i * dx

## read the netcdf file for Pacific Northwest Region 
## Assign file path and directory for the wrfout file 
main_dir = '/Users/JZC/Desktop/EOAS_Research_Assistant/Project_2/netcdfReader/geogrid_files_mc'
grid_size = np.array(['0.444', '1.333','4', '9', '12', '27', '36', '108']) 
# grid sizes (in km) available to interpolate 


wrf_file = dict()
for i in range(0, len(grid_size)):
    wrf_file[i] = ('geo_em.%s.nc' % grid_size[i]) 

interpElev = dict()
for i in range(0, len(grid_size)):
    nc = Dataset(os.path.join(main_dir,wrf_file[i]),'r') # nc is a python datatype
 
    # Model terrain height (from wrf-python)
    hgt = getvar(nc, 'ter') 
    # 2D array for the terrain height data 
    elevArray = to_np(hgt).ravel() 
    # Get latitude and longitude points
    lats, lons = latlon_coords(hgt, as_np=True) 
    # Merge latitudes and longitudes to get coordinates 
    points = mergeLatsLons(lats, lons) 

    interpElev[i] = griddata(points, elevArray, plot_pts, method=method)

headerStr = 'WPS %s km grid size Height (m)'

with open('InterpTable.csv', 'w') as csvfile: 
    fieldnames = ['Longitude (degree)', 
                  'geotiff Topo_30s Raw Height (m)',
                  headerStr % grid_size[0], 
                  headerStr % grid_size[1],
                  headerStr % grid_size[2],
                  headerStr % grid_size[3],
                  headerStr % grid_size[4],
                  headerStr % grid_size[5],
                  headerStr % grid_size[6],
                  headerStr % grid_size[7]]
    elevWriter = csv.DictWriter(csvfile, fieldnames=fieldnames) 
    elevWriter.writeheader() 
    
    for j in range(0, 1200):
        longitude = plot_pts[j][1] 

        elevWriter.writerow({'Longitude (degree)': longitude, 
                             'geotiff Topo_30s Raw Height (m)': arr[rowSelected][j+3],  
                             headerStr % grid_size[0] : interpElev[0][j], 
                             headerStr % grid_size[1] : interpElev[1][j], 
                             headerStr % grid_size[2] : interpElev[2][j], 
                             headerStr % grid_size[3] : interpElev[3][j], 
                             headerStr % grid_size[4] : interpElev[4][j], 
                             headerStr % grid_size[5] : interpElev[5][j], 
                             headerStr % grid_size[6] : interpElev[6][j], 
                             headerStr % grid_size[7] : interpElev[7][j]}) 
        print("Longitude = ", longitude)
        print("Heights = ", interpElev[0][j], interpElev[1][j], interpElev[2][j], interpElev[3][j],
                            interpElev[4][j], interpElev[5][j], interpElev[6][j], interpElev[7][j]) 
        print() 
        
    for j in range(1200, 2400):
        longitude = plot_pts[j][1] 

        elevWriter.writerow({'Longitude (degree)': longitude, 
                             'geotiff Topo_30s Raw Height (m)': arr[rowSelected][j+9],  
                             headerStr % grid_size[0] : interpElev[0][j], 
                             headerStr % grid_size[1] : interpElev[1][j], 
                             headerStr % grid_size[2] : interpElev[2][j], 
                             headerStr % grid_size[3] : interpElev[3][j], 
                             headerStr % grid_size[4] : interpElev[4][j], 
                             headerStr % grid_size[5] : interpElev[5][j], 
                             headerStr % grid_size[6] : interpElev[6][j], 
                             headerStr % grid_size[7] : interpElev[7][j]}) 
        print("Longitude = ", longitude)
        print("Heights = ", interpElev[0][j], interpElev[1][j], interpElev[2][j], interpElev[3][j],
                            interpElev[4][j], interpElev[5][j], interpElev[6][j], interpElev[7][j]) 
        print() 
