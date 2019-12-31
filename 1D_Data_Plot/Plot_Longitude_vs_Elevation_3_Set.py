#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:  Chris Jing 
Email:   zjing@eoas.ubc.ca
For:     UBC EOAS WFRT 
Purpose: this program read in a csv file containing two sets of longtidue 
             vs elevation data, and generate a plot with three types of 
             smoothing schemes: nearest, bilinear, and cubic
             
Created on Wed Jan 31 12:48:00 2018         
"""

import csv 
import matplotlib.pyplot as plt

latitude = 53.92

with open('53.92N_TwoMethodsComparison.csv') as csvfile: 
    readCSV = csv.reader(csvfile, delimiter=',') 

    longitudes = [] # longitudes in degree decimal (DD) format
    elevations_raw = []  # elevations in metres (raw data)
    
    elevations_12_Nearest = [] 
    elevations_12_Bilinear = [] 
    elevations_12_Cubic = [] 

    
    
    reader = csv.reader(csvfile)
    next(reader, None)
   
    for row in readCSV:
        longitude       = float(row[0])
        elevation_raw   = float(row[1])
        

        #elevation_12_Nearest    = float(row[3])
        elevation_12_Bilinear   = float(row[4])
        elevation_12_Cubic      = float(row[5])
        
        longitudes.append(longitude)
        elevations_raw.append(elevation_raw)
        #elevations_12_Nearest.append(elevation_12_Nearest)
        elevations_12_Bilinear.append(elevation_12_Bilinear)
        elevations_12_Cubic.append(elevation_12_Cubic)
        
# Set figure width to 12.0 and height to 4.0
fig_size = plt.rcParams["figure.figsize"] 
fig_size[0] = 16
fig_size[1] = 4
plt.rcParams["figure.figsize"] = fig_size 
    
# Plot the figure 
plt.plot(longitudes, elevations_raw, 'y', label='Topo_30s Raw Data')
#plt.plot(longitudes, elevations_0_444, 'g', label='WPS Smoothed (0.444 km grid size)')
#plt.plot(longitudes, elevations_1_3, 'c', label='WPS Smoothed (1.333 km grid size)')
#plt.plot(longitudes, elevations_12_Nearest, 'k', label='Nrearest Point Method')
plt.plot(longitudes, elevations_12_Bilinear, 'r', label='Bilinear Interpolation')
plt.plot(longitudes, elevations_12_Cubic, 'g', label='Cubic Interpolation')

# add location reference lines 
#plt.vlines(x=-123.25, ymin=0, ymax=2200, linestyle = '-.', color = 'k') # Hudson's Hope
#plt.text(-123.2, 2100, r"Hudson's Hope", fontsize=10)
plt.vlines(x=-122.73, ymin=0, ymax=2200, linestyle = '-.', color = 'k') # Prince George
plt.text(-122.7, 2100, r'Prince George', fontsize=10)
#plt.vlines(x=-123.25, ymin=0, ymax=2200, linestyle = '-.', color = 'k') # UBC
#plt.text(-123.2, 2100, r'UBC Vanocuver', fontsize=10)
"""
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
"""




    
# Now add the legend with some customizations.
legend = plt.legend(loc='upper left', shadow=False)
frame = legend.get_frame()
frame.set_facecolor('0.90')
    
plt.xlabel('Longitude ($^\circ$)')
plt.ylabel('Terrain Elevation (m)')
plt.title('British Columbia %.2f$^\circ$N Terrain Elevation' %latitude)
plt.grid()
plt.savefig('ThreeInterplationMethodsComparison.pdf')
    