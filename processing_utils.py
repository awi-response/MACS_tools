# -*- coding: utf-8 -*-
"""
MACS_Processing utils
"""
import os, shutil, rasterio
import numpy as np
import pandas as pd
from pathlib import Path
import geopandas as gpd
from skimage import morphology


def prepare_df_for_mipps2(path_footprints, path_infiles):
    # Load filtered footprints files
    df = gpd.read_file(path_footprints)
    
    flist = list(Path(path_infiles).glob('*/*.macs'))
    flist = [f'"{str(f)}"' for f in flist]
    
    df_full = pd.DataFrame()
    df_full['full_path'] = flist
    df_full['basename'] = pd.DataFrame(df_full['full_path'].apply(lambda x: os.path.basename(x)))
    # return Inner join of lists - create filtered list of filepaths 
    return df.set_index('Basename').join(df_full.set_index('basename'))

def prepare_df_for_mipps(path_footprints, path_infiles):
    # Load filtered footprints files
    df = gpd.read_file(path_footprints)
    
    #flist = glob.glob(path_infiles + '/*/*.macs')
    flist = list(Path(path_infiles).glob('*/*.macs'))
    flist = [str(f) for f in flist]
    
    df_full = pd.DataFrame()
    df_full['full_path'] = flist
    df_full['basename'] = pd.DataFrame(df_full['full_path'].apply(lambda x: os.path.basename(x)))
    # return Inner join of lists - create filtered list of filepaths 
    return df.set_index('Basename').join(df_full.set_index('basename'))

def write_exif(outdir, tag, exifpath):
    s = f'{exifpath} -overwrite_original -Model="{tag}" {outdir}'
    print(s)
    os.system(s)
    
def make_mask(shape, disksize=4864):
    
    dsk = morphology.disk((disksize-1)/2)
    
    diff = np.array(dsk.shape) - np.array(shape)
    r_start = round(diff[0]/2)
    r_end = r_start + shape[0]
    c_start = round(diff[1]/2)
    c_end = c_start + shape[1]
    cropped_dsk = dsk[r_start:r_end, c_start:c_end]
    return cropped_dsk

def mask_and_tag(image, mask, tag=None):
    #mask3 = np.r_[[mask]*n_bands]
    with rasterio.open(image, mode='r+') as src:
        if tag:
            src.update_tags(Model=tag)
            print(src.tags)
        src.profile.update(
            nodata=0,
            compress='lzw')
        data = src.read() * mask
        src.write(data)
    newimage = f'{str(image)[:-4]}_new.tif'
    os.system(f'gdal_translate -a_nodata 0 {str(image)} {str(newimage)}')
    os.remove(str(image))
    shutil.move(str(newimage), str(image))