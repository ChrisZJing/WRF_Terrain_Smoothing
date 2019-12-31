#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:  Chris Jing 
Email:   zjing@eoas.ubc.ca
For:     UBC EOAS WFRT 
Purpose: this program read in a csv file containing two sets of longtidue 
         vs elevation data, and generate a plot 
             
Created on Wed Jan 31 12:48:00 2018
             
             
"""

import csv 
import matplotlib.pyplot as plt

latitude = 50.12

with open('50.12_Bilinear_Interp_Complete_Set.csv') as csvfile: 
    readCSV = csv.reader(csvfile, delimiter=',') 

    longitudes = [] # longitudes in degree decimal (DD) format
    elevations_raw = []  # elevations in metres (raw data)
    
    
    longitudes_0_444 = []
    longitudes_1_3 = []
    
    elevations_0_444 = [] # elevations in metres (grid size = 0.444 km)
    elevations_1_3 = [] # elevations in metres (grid size = 1.3km)
    
    reader = csv.reader(csvfile)
    next(reader, None)
   
    for row in readCSV:
        longitude       = float(row[0])
        longitudes.append(longitude)
        elevation_raw   = float(row[1])
        elevations_raw.append(elevation_raw)
        
        if str(row[3]) != "nan" :
            
            elevation_0_444 = float(row[3])
            elevations_0_444.append(elevation_0_444)
            longitudes_0_444.append(longitude)
            
        if str(row[4]) != "nan" :
            elevation_1_3   = float(row[4])
            elevations_1_3.append(elevation_1_3)
            longitudes_1_3.append(longitude)

      
# Set figure width to 16.0 and height to 4.0
fig_size = plt.rcParams["figure.figsize"] 
fig_size[0] = 16
fig_size[1] = 4
plt.rcParams["figure.figsize"] = fig_size 
    
# Plot the figure 
plt.plot(longitudes, elevations_raw, 'b', label='Topo_30s Raw Data')
plt.plot(longitudes_0_444, elevations_0_444, 'g', label='WPS Smoothed (0.444 km grid size)')
plt.plot(longitudes_1_3, elevations_1_3, 'r', label='WPS Smoothed (1.333 km grid size)')
#plt.plot(longitudes, elevations_4, 'r', label='WPS Smoothed (4 km grid size)')
#plt.plot(longitudes, elevations_12, 'm', label='WPS Smoothed (12 km grid size)')
#plt.plot(longitudes, elevations_27, 'y', label='WPS Smoothed (27 km grid size)')
#plt.plot(longitudes, elevations_36, 'k', label='WPS Smoothed (36 km grid size)')
#plt.plot(longitudes, elevations_108, 'g', label='WPS Smoothed (108 km grid size)')

# add location reference lines 
plt.vlines(x=-124.0, ymin=0, ymax=2500, linestyle = '--', color = 'k') # Jervis Inlet
plt.vlines(x=-122.9, ymin=0, ymax=2500, linestyle = '--', color = 'k') # Whistler S

plt.text(-125.42, 1700, r'Jervis Inlet', fontsize=10)
plt.text(-122.85, 2400, r'Whistler S', fontsize=10)

plt.text(-124.5, 50, r'0 m', fontsize=10)
plt.text(-122.85, 50, r'670 m', fontsize=10)

# Now add the legend with some customizations.
legend = plt.legend(loc='upper left', shadow=False)
frame = legend.get_frame()
frame.set_facecolor('0.90')
    
plt.xlabel('Longitude ($^\circ$)')
plt.ylabel('Terrain Elevation (m)')
plt.title('British Columbia %.2f$^\circ$N Terrain Elevation' %latitude)
plt.grid()
plt.savefig('BC Terrain Elevation Raw and Smoothed Comparison.pdf')
    