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

with open('50.12_Cubic_Interp_Complete_Set.csv') as csvfile: 
    readCSV = csv.reader(csvfile, delimiter=',') 

    longitudes = [] # longitudes in degree decimal (DD) format
    elevations_raw = []  # elevations in metres (raw data)
    
    elevations_0_444 = [] # elevations in metres (grid size = 0.444 km)
    elevations_1_3 = [] # elevations in metres (grid size = 1.3km)
    elevations_4 = [] # elevations in metres (grid size = 4 km)
    elevations_9 = [] # elevations in metres (grid size = 9 km)
    elevations_12 = [] # elevations in metres (grid size = 12 km)
    elevations_27 = [] # elevations in metres (grid size = 27 km)
    elevations_36 = [] # elevations in metres (grid size = 36 km)
    elevations_108 = [] # elevations in metres (grid size = 108 km)
    
    
    reader = csv.reader(csvfile)
    next(reader, None)
   
    for row in readCSV:
        longitude       = float(row[0])
        elevation_raw   = float(row[1])
        
        elevation_0_444 = float(row[3])
        elevation_1_3   = float(row[4])
        elevation_4     = float(row[5])
        elevation_9     = float(row[6])
        elevation_12    = float(row[7])
        elevation_27    = float(row[8])
        elevation_36    = float(row[9])
        elevation_108   = float(row[10])
        
        longitudes.append(longitude)
        elevations_raw.append(elevation_raw)
        elevations_0_444.append(elevation_0_444)
        elevations_1_3.append(elevation_1_3)
        elevations_4.append(elevation_4)
        elevations_9.append(elevation_9)
        elevations_12.append(elevation_12)
        elevations_27.append(elevation_27)
        elevations_36.append(elevation_36)
        elevations_108.append(elevation_108)
        
# Set figure width to 12.0 and height to 4.0
fig_size = plt.rcParams["figure.figsize"] 
fig_size[0] = 16
fig_size[1] = 4
plt.rcParams["figure.figsize"] = fig_size 
    
# Plot the figure 
plt.plot(longitudes, elevations_raw, 'b', label='Topo_30s Raw Data')
#plt.plot(longitudes, elevations_0_444, 'g', label='WPS Smoothed (0.444 km grid size)')
#plt.plot(longitudes, elevations_1_3, 'c', label='WPS Smoothed (1.333 km grid size)')
plt.plot(longitudes, elevations_4, 'r', label='WPS Smoothed (4 km grid size)')
plt.plot(longitudes, elevations_9, 'c', label='WPS Smoothed (9 km grid size)')
plt.plot(longitudes, elevations_12, 'm', label='WPS Smoothed (12 km grid size)')
plt.plot(longitudes, elevations_27, 'y', label='WPS Smoothed (27 km grid size)')
plt.plot(longitudes, elevations_36, 'k', label='WPS Smoothed (36 km grid size)')
plt.plot(longitudes, elevations_108, 'g', label='WPS Smoothed (108 km grid size)')

# add location reference lines 
plt.vlines(x=-127.379, ymin=0, ymax=3000, linestyle = '-.', color = 'k') # Kyuquot 
plt.vlines(x=-125.273, ymin=0, ymax=3000, linestyle = '--', color = 'k') # Campbell River 
plt.vlines(x=-122.957, ymin=0, ymax=3000, linestyle = '--', color = 'k') # Whistler S
plt.vlines(x=-120.9, ymin=0, ymax=3000, linestyle = '--', color = 'k') # Merrit S 
plt.vlines(x=-119.496, ymin=0, ymax=3000, linestyle = '--', color = 'k') # Kelowna - Vernon
plt.vlines(x=-115.769, ymin=0, ymax=3000, linestyle = '--', color = 'k') # Cranbook N
plt.vlines(x=-114.66, ymin=0, ymax=3000, linestyle = '-.', color = 'k') # BC/AB border
plt.vlines(x=-112.842, ymin=0, ymax=3000, linestyle = '--', color = 'k') # Lethbridge N 
plt.vlines(x=-110.676, ymin=0, ymax=3000, linestyle = '--', color = 'k') # Medicine Hat S

plt.text(-127.32, 2800, r'Kyuquot', fontsize=10)
plt.text(-125.2, 2800, r'Campbell River', fontsize=10)
plt.text(-125.2, 2800, r'Campbell River', fontsize=10)
plt.text(-122.9, 2800, r'Whistler S', fontsize=10)
plt.text(-120.72, 2800, r'Merritt S', fontsize=10)
plt.text(-119.4, 2800, r'Kelowna', fontsize=10)
plt.text(-117.1, 2800, r'Cranbrook', fontsize=10)
plt.text(-115.325, 2800, r'<-BC', fontsize=10)
plt.text(-114.60, 2800, r'AB->', fontsize=10)
plt.text(-112.8, 2800, r'Lethbridge N', fontsize=10)
plt.text(-110.62, 2800, r'Medicine Hat', fontsize=10)

plt.text(-127.32, 50, r'2 m', fontsize=10)
plt.text(-125.2, 50, r'24 m', fontsize=10)
plt.text(-122.9, 50, r'670 m', fontsize=10)
plt.text(-120.85, 50, r'605 m', fontsize=10)
plt.text(-119.4, 50, r'344 m', fontsize=10)
plt.text(-115.75, 50, r'921 m', fontsize=10)
plt.text(-114.60, 50, r'2754 m', fontsize=10)
plt.text(-112.8, 50, r'910 m', fontsize=10)
plt.text(-110.62, 50, r'690 m', fontsize=10)


# Now add the legend with some customizations.
legend = plt.legend(loc='upper left', shadow=False)
frame = legend.get_frame()
frame.set_facecolor('0.90')
    
plt.xlabel('Longitude ($^\circ$)')
plt.ylabel('Terrain Elevation (m)')
plt.title('British Columbia %.2f$^\circ$N Terrain Elevation' %latitude)
plt.grid()
plt.savefig('Elevation Raw vs WPS Cubic Interpolation.pdf')
    