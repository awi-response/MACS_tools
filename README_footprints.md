# MACS_tools
Tools for handling DLR MACS (Modular Aerial Camera System) data

## MACS footprints from raw flight data
_Version: 2021-08-09 Author: Ingmar Nitze, Simon Schaeffler

### Part 0: Export navigation files, KML files and Mosaica project files

1. Open raw flight data:
    1. Select flight folder in `01_raw_data`
    2. Drag and drop into Mosaica
2. Export navigation file:
	1. Right click on file xxx_MACS-xxx.xml in Project Tree > Export > Nav-> TXT
    2. Navigate to `local_drive/.../01_raw_data/` > click flight folder
	3. File name: `“flight folder_footprints_nav.txt”`
3. Export RGB-KML-file:
	1. Select Left and Right (RGB-files) in Project Tree
	2. Right click on selected files in Project Tree > Export > KML Footprints
	3. Navigate to `local_drive/.../01_raw_data/` > click flight folder
	4. File name: `“flight folder_footprints_RGB.kml”`
4. Export NIR-KML-file:
	1. Select NIR in Project Tree
	2. Right click on selected files in Project Tree > Export > KML Footprints
	3. Navigate to `local_drive/.../01_raw_data/` > click flight folder
	4. File name: `“flight folder_footprints_NIR.kml”`
5. Export Mosaica project file (.mxd)
	1. File > Save File As 
	2. Navigate to `local_drive/.../01_raw_data/` > click flight folder
	3. File name: `“flight folder.mxd”`
6. Proposals to review:
	1. Search folder for “_nav”., “_mxd”, “_footprints_NIR”, “footprints_RGB”. “ :  number of results should be how you expect it
	2. Search folder for common mistakes like “footprint_”, “m_RGB”. etc.

### Part 1: Generating footprint file

1. Make sure you have the following programs installed:
    1. Python 3
    2. Anaconda
2. Make sure you have the following packages installed:
	1. notebook
	2. geopandas
	3. pytz
	4. fiona
	5. pandas
	6. glob2
	7. glob
	8. os

3. Download ![MACS_tools](https://github.com/awi-response/MACS_tools)
 and open fill_footprints.ipynb) in Jupyter Notebook from Anaconda
4. In [2] change DATADIR -path  to specific /01_raw_data
5. In [14] change “2019” to specific year
6. In [61] change “49”  to specific folder number
7. Select all > run
