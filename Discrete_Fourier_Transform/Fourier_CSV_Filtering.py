#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:  Chris Jing 
Email:   zjing@eoas.ubc.ca
For:     UBC EOAS WFRT 
Purpose: This Program read in a csv file containing latitude, longitude and elevation 
         data for a list of locations and plot a diagram of elevations vs longitudes,
         both the original and a filtered version. 
         Note that all locations in the csv file has the same latitude 

Created on Sun Jan 14 11:47:33 2018

"""

import csv 
import numpy as np
import math 
import matplotlib.pyplot as plt

# This function carrys out a discrete Fourier transform (DFT)
# Inputs: samples    (array),    the sample points for DFT
# Output: the real part of the DFT (array of size len(samples))
def realDFT(samples):
    N = len(samples)
    realComp = np.zeros(N) 
    
    for k in range(N):
        sum = 0
        for n in range(N):
            sum += samples[n] * math.cos(2 * math.pi * k * n / N)
        realComp[k] = sum / N
    
    return realComp
            
# This function carrys out a discrete Fourier transform (DFT)
# Inputs: samples    (array),    the sample points for DFT
# Output: the imaginary part of the DFT (array of size len(samples))
def imagDFT(samples):
    N = len(samples)
    imagComp = np.zeros(N) 
    
    for k in range(N):
        sum = 0
        for n in range(N):
            sum += samples[n] * math.sin(2 * math.pi * k * n / N)
        imagComp[k] =  - 1.0 * sum / N 
    
    return imagComp

# This function computes the variance spectrum of a DFT
# Inputs: reals (array), the real components of the DFT
#         imags (array), the imaginary component of the DFT
# Output: the variance spectrum of the DFT (array)
# Requires: length of reals must equals length of imags
def spectrum(reals, imags):
    nyquist = len(reals) / 2
    spec = np.zeros(nyquist + 1)
    
    for i in range(nyquist + 1):
        spec[i] = reals[i]**2 + imags[i]**2 
    return spec

# This function filters the variance spectrum of a DFT
# Inputs: reals (array), the real components of the DFT
#         imags (array), the imaginary component of the DFT
#         threshold (int), assign zero filter weights to all wavenumbers 
#                          below this threshold
# Output: the filtered variance spectrum of the DFT (array)
# Requires: length of reals must equals length of imags
#           threshold <= len(reals)
def filterSpectrum(reals, imags, threshold):
    filteredSpec = np.zeros(len(reals) + 1)
    
    for i in range(threshold):
        filteredSpec[i] = reals[i]**2 + imags[i]**2 
    return filteredSpec
        
# This function carrys out an inverse discrete Fourier transform (IDFT)
# Inputs: reals (array), the real components of the DFT
#         imags (array), the imaginary component of the DFT
#         threshold (int), assign zero filter weights to all wavenumbers 
#                          below this threshold
# Outputs: the filtered space series (array of size(threshold + 1))
def inverseDFT(reals, imags, threshold):
    N = len(reals)
    filteredReals = np.zeros(threshold + 1)
    filteredImags = np.zeros(threshold + 1)
    filteredSeries = np.zeros(N)
    
    for i in range(threshold + 1):
        filteredReals[i] = reals[i]
        filteredImags[i] = imags[i]
        
    for n in range(N):
        sum = 0;
        for k in range(threshold + 1): 
            sum += filteredReals[k] * math.cos(2 * math.pi * k * n / N)
            sum -= filteredImags[k] * math.sin(2 * math.pi * k * n / N)
        filteredSeries[n] = sum

    return filteredSeries 


"""
START OF PROGRAM

"""

with open('BC_Elevation_Longitude_124-122.csv') as csvfile: 
    readCSV = csv.reader(csvfile, delimiter=',') 

    longitudes = [] # longitudes in degree decimal (DD) format
    elevations = [] # elevations in metres 
    
    for row in readCSV:
        latitude  = float(row[0])
        longitude = float(row[1])
        elevation = float(row[2])
        
        longitudes.append(longitude)
        elevations.append(elevation)


    reals = realDFT(elevations)
    imags = imagDFT(elevations)
    threshold = 10;
    filtered = inverseDFT(reals, imags, threshold)
    
    # Set figure width to 12.0 and height to 4.0
    fig_size = plt.rcParams["figure.figsize"] 
    fig_size[0] = 12
    fig_size[1] = 4
    plt.rcParams["figure.figsize"] = fig_size
    
    # Plot the figure 
    plt.plot(longitudes, elevations, 'b')
    plt.plot(longitudes, filtered, 'r')
    
    plt.xlabel('Longitude ($^\circ$)')
    plt.ylabel('Terrain Elevation (m)')
    plt.title('British Columbia %.2f$^\circ$N Terrain Elevation' %latitude)
    plt.grid()
    plt.savefig('BC Terrain Elevation.pdf')
    
    for i in range(len(reals)):
        print("number: %d" %i)
        print("real component: %f" %reals[i]) 
        print("imaginary component: %f" %imags[i])
        print("\n") 
    