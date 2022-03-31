import pandas as pd
import os
#from pathlib import Path


def flist_to_df(filelist):
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
    addo = f'gdaladdo -ro --config COMPRESS_OVERVIEW DEFLATE --config GDAL_NUM_THREADS ALL_CPUS {rasterfile}'
    os.system(addo)


def full_postprocessing(df, tile_id):
    subset = df[df['tile_id'] == tile_id]
    rgbfile = subset.query('sensor=="group1"').filename.values[0]
    nirfile = subset.query('sensor=="nir"').filename.values[0]
    outmosaic = rgbfile.parent / f'mosaic_{tile_id}.tif'
    stack_output(outmosaic, rgbfile, nirfile, remove_temporary_files=True)
    calculate_pyramids(outmosaic)