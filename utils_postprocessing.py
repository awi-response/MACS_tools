import numpy as np
import os
import pandas as pd
import rasterio


def flist_to_df(filelist):
    """
    Create pandas DataFrame with information parsed from filelist

    Parameters
    ----------
    filelist : list
        file list of MACS Orthomosaic Output files

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    sensors = []
    rows = []
    cols = []
    for f in filelist:
        sensor, row, col = f.name[:-4].split('_')[-3:]
        sensors.append(sensor)
        rows.append(row)
        cols.append(col)

    df = pd.DataFrame(columns=['filename', 'sensor', 'row', 'col'])
    df['filename'] = filelist
    df['sensor'] = sensors
    df['row'] = rows 
    df['col'] = cols 
    return df

# create more specific vrt files for each run to avoid duplicates on parallel run
def stack_output(outmosaic, rgbfile, nirfile, remove_temporary_files=True):
    """
    Function to stack together RGB and NIR images
    Input: 
        4 Band RGB (RGB-A)
        2 Band NIR (NIR-A)
    """

    basename_rgb = rgbfile.name[:-4]
    basename_nir = nirfile.name[:-4]
    
    b1 = f'{basename_rgb}_1.vrt'
    b2 = f'{basename_rgb}_2.vrt'
    b3 = f'{basename_rgb}_3.vrt'
    b_nir = f'{basename_nir}_1.vrt'
    mos = f'{basename_rgb}.vrt'
    
    for band in [1,2,3]:
        s = f'gdalbuildvrt -b {band} {basename_rgb}_{band}.vrt {rgbfile}'
        os.system(s)

    for band in [1]:
        s = f'gdalbuildvrt -b {band} {basename_nir}_{band}.vrt {nirfile}'
        os.system(s)

    s = f'gdalbuildvrt -separate {mos} {b3} {b2} {b1} {b_nir}'
    os.system(s)

    s = f'gdal_translate -a_nodata 0 -co COMPRESS=DEFLATE -co BIGTIFF=YES {mos} {outmosaic}'
    os.system(s)
    if remove_temporary_files:
        for file in [b1, b2, b3, b_nir, mos]:
            os.remove(file)
            

def calculate_pyramids(rasterfile):
    """
    Function to calculate pyramids

    Parameters
    ----------
    rasterfile : Path
        file for which to create pyramids

    Returns
    -------
    None.

    """
    addo = f'gdaladdo -ro --config COMPRESS_OVERVIEW DEFLATE --config GDAL_NUM_THREADS ALL_CPUS {rasterfile}'
    os.system(addo)


def mask_and_name_bands(mosaic_file):
    """
    Function to mask incomplete spectral data (e.g. with only NIR data and no RGB and vice versa)
    Add names to Bands
    """
    with rasterio.open(mosaic_file, 'r+') as src:
        src.profile['nodata'] = 0
        data = src.read()
        newmask = ~(data == 0).any(axis=0)
        newmask_write = np.r_[src.count * [newmask]]
        data_masked = data * newmask_write
        src.set_band_description(1, 'MACS Blue Band')
        src.set_band_description(2, 'MACS Green Band')
        src.set_band_description(3, 'MACS Red Band')
        src.set_band_description(4, 'MACS NIR Band')
        src.write(data_masked)


def full_postprocessing_optical(df, tile_id, rgb_name='group1', nir_name='nir'):
    """
    Wrapper function to sequentially run

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    tile_id : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    subset = df[df['tile_id'] == tile_id]
    rgbfile = subset.query(f'sensor=="{rgb_name}"').filename.values[0]
    nirfile = subset.query(f'sensor=="{nir_name}"').filename.values[0]
    outmosaic = rgbfile.parent / f'mosaic_{tile_id}.tif'
    stack_output(outmosaic, rgbfile, nirfile, remove_temporary_files=True)
    calculate_pyramids(outmosaic)
    mask_and_name_bands(outmosaic)