#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 10:42:48 2021

@author: ijuszak
"""
# --------------------------------------------------
# Loads TIFF of MACS NIR images to define an offset for the MIPPS tool
# --------------------------------------------------
# 1) File paths, file names and parameters
# 2) Load images
# 3) Calculate general statistics
# 4) Estimate offsets based on 'no water median'
# 5) Add statistics to output file
# 6) Plot histograms
# 7) Check 'no water saturated fraction' vs. 'no water median' vs. offset
# --------------------------------------------------
#
# Previous step: export tiffs using standard devignetting in MOSAICA
#
# Next step: run the MIPPS tool on all images with the estimated offset
#
# takes roughly 11hours to run for 15406 NIR images
#
# IG 04/2021

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
# from scipy import stats
from os import listdir
import time

# --------------------------------------------------
# 1) File paths, file names and parameters
# --------------------------------------------------
# test with few images of process all of the TVC folder?
onlytest = False

fp = ['blabladbad',
      'D:/00_orga/12_MACS_processing/01_anaktuvuk_chuck/01_rawdata/tif/20190606 MACS-Polar18/NIR 33552/',
      'D:/00_orga/12_MACS_processing/01_anaktuvuk_chuck/01_rawdata']
# output file name
filename = fp[2] + 'NIR_image_offset.csv'

# separation between water and tundra and saturated pixels
P1 = 15720448  # total number of pixels: len(imdataframe)
P2 = 65500  # threshold to define saturation
P3 = 20000  # image contains <= P5 saturated pixels: everything below 20000 is water
P4 = 30000  # image contains > P5 saturated pixels: everything below 30000 is water
P5 = 0.1

# defining offsets for different image brightness
N1 = 40000
M1 = -5000  # 'no water median' < 40000 :      offset = -5000
N2 = 45000
M2 = 0  # 'no water median' 40000..45000 : offset = -5000..0 (linear)
# 'no water median' 45000..55000 : offset = 0
N3 = 55000  # 'no water median' 55000..60000 : offset = 0..5000 (linear)
N4 = 60000
M3 = 5000  # 'no water median' >= 60000 :     offset = 5000

# sample images
fname = ['09338_014657056_1800.tif', '08730_014153058_1800.tif', '12436_021246043_1800.tif', '16855_024935525_1800.tif', \
         '18958_030707017_1800.tif', '13574_022215038_1800.tif', '19014_030735017_1800.tif', '02449_004932583_1800.tif',
         '33614_050914957_1800.tif', '18032_025924021_1800.tif']
ftitles = ['Dark image', 'Normal image', 'Saturated image (with water)', 'Saturated image (no water)', \
           '18958_030707017_1800.tif', '13574_022215038_1800.tif', '19014_030735017_1800.tif',
           '02449_004932583_1800.tif', '33614_050914957_1800.tif', '18032_025924021_1800.tif']
# Dark image: 09338_014657056_1800.tif
# Normal image: 08730_014153058_1800.tif
# Saturated image (with water): 12436_021246043_1800.tif
# Saturated image (no water): 16855_024935525_1800.tif
# saturated:            18958_030707017_1800.tif 13574_022215038_1800.tif
# saturated with water: 19014_030735017_1800.tif
# dark:                 02449_004932583_1800.tif 33614_050914957_1800.tif
# normal:               18032_025924021_1800.tif

print('Starting processing: ' + time.strftime('%H:%M'))
st = time.time()

# --------------------------------------------------
# 2) Load images
# --------------------------------------------------
if onlytest:
    allfiles = fname
    n = len(fname)  # nr of images to load at once
else:
    allfiles = listdir(fp[1])
    allfiles = [s for s in allfiles if '.tif' in s]
    allfiles.sort()
    n = 1
    # nr of images to load at once:
    # benchmark 32 images: n= 1 : 1.38 min
    #                      n= 2 : 2.41 min
    #                      n= 5 : 3.82 min
    #                      n=10 : 6.06 min
    #                      n=20 : 9.72 min

i = 0
i1 = i + n
i2 = len(allfiles)

while i < i2:
    i1 = i + n
    if i1 > i2:
        i1 = i2

    if onlytest:
        my_dpi = 96
        fig = plt.figure(figsize=(3000 / my_dpi, 1500 / my_dpi), dpi=my_dpi)

    k = 0
    ftitles = allfiles[i:i1]
    for j in ftitles:
        im = Image.open(fp[1] + j)
        if onlytest:
            ax = fig.add_subplot(3, 4, k + 1)
            # im.show()
            ax.imshow(im)
        if k == 0:
            tmp = np.array(im)
            imvector = np.zeros((np.size(tmp, 0) * np.size(tmp, 1), len(ftitles)))
        imvector[:, k] = np.hstack(np.array(im))
        k += 1

    imdataframe = pd.DataFrame(imvector, columns=ftitles)

    # --------------------------------------------------
    # 3) Calculate general statistics
    # --------------------------------------------------
    imagestats = pd.DataFrame(np.nan, columns=['median', 'mean'], index=ftitles)
    imagestats.loc[:, 'median'] = imdataframe.median()
    imagestats.loc[:, 'mean'] = imdataframe.mean()

    ### Propper estimation of the separation water - tundra in a loop through all images
    # for i in range(len(ftitles)):
    #     tmpseries = imdataframe.iloc[:,i].copy()
    #     # water pixel value
    #     tmp = tmpseries.copy()
    #     tmp.loc[tmp>N1] = np.nan
    #     imagestats.loc[ftitles[i],'lowmodal'] =  stats.mode(tmp,nan_policy='omit')[0]
    #     # tundra pixel value
    #     tmp = tmpseries.copy()
    #     tmp.loc[tmp<N1] = np.nan
    #     imagestats.loc[ftitles[i],'highmodal'] =  stats.mode(tmp,nan_policy='omit')[0]
    #     # separation between water and tundra
    #     tmp = tmpseries.copy()
    #     tmp.loc[(tmp<imagestats.loc[ftitles[i],'lowmodal'])|(tmp>imagestats.loc[ftitles[i],'highmodal'])] = np.nan
    #     imagestats.loc[ftitles[i],'minimum between classes'] = tmp.value_counts().index[-1]
    #     if imagestats.loc[ftitles[i],'minimum between classes'] == imagestats.loc[ftitles[i],'lowmodal']:
    #         imagestats.loc[ftitles[i],'minimum between classes'] = 0
    #     # make water pixels nan
    #     tmpseries.loc[tmpseries<imagestats.loc[ftitles[i],'minimum between classes']] = np.nan
    #     imagestats.loc[ftitles[i],'no water median'] = tmpseries.median()
    #     imagestats.loc[ftitles[i],'no water mean'] = tmpseries.mean()
    #     # percentage saturated
    #     imagestats.loc[ftitles[i],'no water saturated fraction'] = sum(tmpseries>N2)/sum(~np.isnan(tmpseries))

    # total saturated fraction
    tmp = imdataframe.copy()
    tmp[tmp < P2] = np.nan
    imagestats.loc[:, 'total saturated fraction'] = tmp.count() / P1

    # water fraction
    tmp = imdataframe.copy()
    tmp[tmp < P3] = np.nan
    tmp2 = imagestats.loc[:, 'total saturated fraction'] > P5
    tmp[tmp.loc[:, tmp2[tmp2].index.tolist()] < P4] = np.nan
    imagestats.loc[:, 'water fraction'] = (P1 - tmp.count()) / P1
    imagestats.loc[:, 'no water median'] = tmp.median()

    # no water saturated fraction
    imagestats.loc[:, 'no water saturated fraction'] = (P1 * imagestats.loc[:, 'total saturated fraction']) / (
                P1 * (1 - imagestats.loc[:, 'water fraction']))

    # --------------------------------------------------
    # 4) Estimate offsets based on 'no water median'
    # --------------------------------------------------
    imagestats.loc[:, 'offset'] = 0
    imagestats.loc[imagestats.loc[:, 'no water median'] < N1, 'offset'] = M1

    tmp = (imagestats.loc[:, 'no water median'] >= N1) & (imagestats.loc[:, 'no water median'] < N2)
    imagestats.loc[tmp, 'offset'] = M1 + (imagestats.loc[tmp, 'no water median'] - N1) / (N2 - N1) * (M2 - M1)

    tmp = (imagestats.loc[:, 'no water median'] >= N3) & (imagestats.loc[:, 'no water median'] < N4)
    imagestats.loc[tmp, 'offset'] = M2 + (imagestats.loc[tmp, 'no water median'] - N3) / (N4 - N3) * (M3 - M2)

    imagestats.loc[imagestats.loc[:, 'no water median'] >= N4, 'offset'] = M3

    # --------------------------------------------------
    # 5) Add statistics to output file
    # --------------------------------------------------
    if not onlytest:
        if i == 0:
            with open(filename, 'w') as file:
                imagestats.to_csv(file, header=True, index=True, index_label='NirImage', na_rep='NaN')
        else:
            with open(filename, 'a') as file:
                imagestats.to_csv(file, header=False, index=True, index_label='NirImage', na_rep='NaN')
    i = i1

# --------------------------------------------------
# 6) Plot histograms
# --------------------------------------------------
if onlytest:
    fig = plt.figure(figsize=(3000 / my_dpi, 1500 / my_dpi), dpi=my_dpi)
    fig.suptitle('Histogram with auto bins', fontsize=14)
    for j in range(len(ftitles)):
        ax = fig.add_subplot(3, 4, j + 1)
        plt.hist(imvector[:, j], bins='auto')
        ax.set_xlabel('Value')
        ax.set_ylabel(ftitles[j])

# --------------------------------------------------
# 7) Check 'no water saturated fraction' vs. 'no water median' vs. offset
# --------------------------------------------------
if onlytest:
    fig = plt.figure(figsize=(3000 / my_dpi, 1500 / my_dpi), dpi=my_dpi)
    fig.suptitle('compare variables', fontsize=14)
    ax = fig.add_subplot(2, 2, 1)
    ax.scatter(imagestats.loc[:, 'no water median'], imagestats.loc[:, 'no water saturated fraction'])
    ax.set_xlabel('no water median')
    ax.set_ylabel('no water saturated fraction')
    ax = fig.add_subplot(2, 2, 2)
    ax.scatter(imagestats.loc[:, 'no water median'], imagestats.loc[:, 'offset'])
    ax.set_xlabel('no water median')
    ax.set_ylabel('offset')
    ax = fig.add_subplot(2, 2, 3)
    ax.scatter(imagestats.loc[:, 'no water saturated fraction'], imagestats.loc[:, 'offset'])
    ax.set_xlabel('no water saturated fraction')
    ax.set_ylabel('offset')

print('Finished processing: ' + time.strftime('%H:%M') + ', after ' + str((time.time() - st) / 60) + ' min')

plt.show()




















