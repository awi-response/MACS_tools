# MACS_tools
Tools for handling DLR MACS (Modular Aerial Camera System) data

## MACS Processing Step-by-Step
_Version: 2021-04-27 Authors: Tabea Rettelbach, Jennika Hammar, Ingmar Nitze_

### Part 0: Setup

1. Make sure you have the following programs installed:
    1. Python 3
    2. Anaconda
    3. QGIS
    4. Pix4Dmapper (commercial licence required)
    5. DLR MACS box (Mosaica, MIPPS)
    6. Git
2. Clone `MACS_tools` git repository:
    1. In Windows Explorer: browse to folder where you will be doing the processing
    > TIP: You should do all processing on a local drive, preferably an SSD. It's therefore best to organize you entire project here. Do not attempt processing on a shared network. The overhead will make processing way too slow.
    2. Right click in explorer &gt; Git Bash Here
    3. In bash, type: git clone [https://github.com/awi-response/MACS\_tools.git](https://github.com/awi-response/MACS_tools.git)
    4. In explorer: unzip `processing_folder_structure_template.zip` to where you'll do your processing. Folder structure should look like this:  
    ![folder_structure_zip](https://user-images.githubusercontent.com/40014163/116421567-3d502280-a83f-11eb-84d0-3f3622d237d2.png)


### Part 1: Prepare your study area

1. Start QGIS &gt; Open new empty project
2. Drag and drop flight footprints into QGIS (should be located within the `raw_data` folder of each flight)  
![macs_image_location](https://user-images.githubusercontent.com/40014163/116421635-4f31c580-a83f-11eb-9d22-225feed75d2c.png)

3. OPTIONAL: Add basemap, for better visualization:
    1. Make sure QuickMapServices PlugIn is installed in QGIS (Plugins &gt; Manage and Install Plugins &gt; Search for QuickMapServices &gt; Install Plugin)
    2. In toolbar: QuickMapServices &gt; Settings  
    ![quickmapservices_qgis](https://user-images.githubusercontent.com/40014163/116421676-5b1d8780-a83f-11eb-8e10-868515ff4ed3.png)
    3. More services tab &gt; Get contributed pack &gt; Save
    4. In toolbar: QuickMapServices &gt; ESRI &gt; ESRI Satellite (or whichever basemap you prefer)
4. Make study area shapefile
    1. Layer &gt; Create layer &gt; New Shapefile Layer
    2. File name: `path/to/your/file/02_studysites/your_study_area`
    3. Geometry type: Polygon
    4. Ok
    5. In toolbar: Add Polygon Feature (Ctrl + .) &gt; start drawing polygon of your desired study area &gt; finish polygon with right click
    6. In toolbar: Save layer edits
5. Select footprints that are in study area
    1. Vector &gt; Research tools &gt; Select by location
    2. Select features from: `your_footprint_layer`
    3. Where the features: check intersect
    4. By comparing to the features from: `your_study_area`
    5. Modify current selection by: creating new selection
    6. Run
    7. Close
    > TIP: Don't select study areas that are too large. ca. 5000 images are already _a lot!_ Processing steps at later stages grow exponentially (?) in computing time. So, if your study area is too large, you&#39;ll need to subset it when processing in Pix4D and then later stitch them back together.
6. Save footprint selection:
    1. Right click footprints &gt; Export &gt; Save Features As…
    2. Format: ESRI Shapefile
    3. File name: `path/to/your/file/02_studysites/my_study_area_footprints`
    4. Check: Save only selected features
    5. Check: Add saved file to map
    6. Ok

1. Remove the footprint layer with all image footprints:
    1. Right click all footprints &gt; Remove Layer… &gt; OK
2. Save GIS project in `05_gis` (of the unzipped folder structure template)

### Part 2: move all necessary MACS images to the local drive

1. Open Anaconda Prompt (anaconda3)
2. Browse to `MACS_tools` repo:
    1. `d:` (or whatever drive you're on)
    2. `cd your_path_here\MACS_tools`
3. Install and activate the virtual python environment
    1. `conda env list` (if `macs_tools` is already listed, then skip to step 3c)
    2. `conda env install -n macs_tools -f environment_geopandas.yml` (only necessary the first time, might take a while)
    3. `conda activate macs_tools`
4. move the MACS images of interest:
    1. Launch Jupyter Notebook with: `jupyter notebook` (still in Anaconda Prompt)
    2. Select `move_MACS_files.ipynb`
    3. Adapt paths:
        - `path_footprints` (path to the subset of the MACS image footprints located only in your study area)
        - `path_infiles` (the directory with all the MACS images from this flight)
        - `path_outfiles` (local drive where to store the relevant images: suggestion: 01\_raw-data from the folder structure template)
    4. Run all notebook cells &gt; wait (this can take several hours; depending on the copy locations and the number of images in your study area).
    > This step has crashed in the past (error so far unknown). You might need to rerun the last cell of the notebook to restart the copying process. The function checks, if the current file is already at the destination, so it will only retry copying those that it had missed previously (saves time by only copying each file once, even if it crashes).

### Part 3: Prepare camera and navigation files in Mosaica

1. Get the corrected navigation files corresponding to your flight:
    1. `N:/response/Restricted_Airborne/MACs/Alaska/ThawTrend-Air_2019/MACS_Nav-PP_your_flight`
    2. Unzip the correct folder (they are named after the date of acquisition; the .pptx-file contains an overview of all footprints and dates --> you can check which one you need here)
    3. Copy `date_nav.txt` file to `local_drive\...\03_mosaica`
2. Open Mosaica
    1. Toolbar &gt; DLR MACS-box &gt; Geo &gt; Mosaica  
    ![launch_mosaica](https://user-images.githubusercontent.com/40014163/116421950-94ee8e00-a83f-11eb-87b8-9d1b5f489e1b.png)
3. Add MACS images:
    1. In file browser, navigate to `01_rawdata/macs` (where `move_MACS_files.ipynb` just moved your images)
    2. Select Left, NIR, Right folders
    3. Drag and drop into Mosaica
    4. Wait (or deselect 'Show Images' for faster loading)
4. Save Mosaica project in `local_drive/.../03_mosaica`
5. Adapt the menu bar as follows:  
![mosaica_toolbar](https://user-images.githubusercontent.com/40014163/116421980-9c159c00-a83f-11eb-8529-38327ccc6ae0.png)

6. Import the navigation file:
    1. File &gt; Import NavFiles
    2. Select the text file with the post processed coordinates: `local_drive/.../03_mosaica/_date_Nav.txt`
    3. Apply import to all items? &gt; Yes
    4. Adapt configurations to match the following:  
    ![mosaica_nav_file_import_settings](https://user-images.githubusercontent.com/40014163/116422022-a33caa00-a83f-11eb-98b0-1a16067929e2.png)

    > Note: The number of lines to skip will depend on your exact navigation file. Make sure, it corresponds to the number of header rows in your nav.txt file. According to metadata of the flight, the height reference is actually EGM 2008, but we can only select EGM96.
    5. OK &gt; wait &gt; OK
7. Export MACS images as .tiff images
    1. Right click on file `xxx_MACS-xxx.xml` in Project Tree &gt; Export &gt; TIF Images
    2. Navigate to `local_drive/.../01_rawdata/` &gt; click tif-folder &gt; Select Folder
    3. Wait
8. Export Mosaica nav-file to txt for later processing:
    1. Right click on file `xxx_MACS-xxx.xml` in Project Tree &gt; Export &gt; Nav -&gt; TXT
    2. Navigate to `local_drive/.../03_mosaica/`
    3. File name: `date_Nav_mosaica.txt`
    4. Save &gt; OK
9. Prepare Nav file for Pix4Dmapper
    1. Open Jupyter Home Page (should still be open in your browser from step 2.4)
    2. Double click `correctednav_to_pix4dnav.ipynb` notebook
    3. Adapt `INFILE` and `outfile` variables corresponding to your file locations (suggestions are given)
    4. Specify vertical and horizontal accuracy
    5. Execute all cells consecutively

### Part 4: Processing in Pix4Dmapper

1. Launch Pix4Dmapper (you'll need a licence for this. If you don`t have access yet, contact Ingmar Nitze for more info: [ingmar.nitze@awi.de](mailto:ingmar.nitze@awi.de))
    1. New Project &gt; Name: `your_project_name` &gt; Create in: `.../04_pix4d` &gt; Project Type: New Project &gt; Next
    2. Add Directories &gt; navigate to `.../01_rawdata/macs` &gt; select NIR, Right, or Left folder &gt; Choose (repeat if multiple directories should be added)
    3. Next
    4. ''More than 80% of the image coordinates ... were the same and ... geotags have been discarded'' &gt; OK
    5. Image Geolocation: Geolocation and Orientation: From File... &gt; File Format: Latitude, longitude, Altitude &gt; File: `.../04_pix4d/date_Nav_geo_pix4d.txt` &gt; Open &gt; OK
    6. Selected Camera Model:
        1. This should read: `MACS_Polar18_xxx`
        2. If not: Edit… Camera Model Name: `MACS_Polar18_xxx` &gt; OK
        3. If this option is not available, skip step 4-1f. for now, we'll get to it later.
    7. Next
    8. Output/GCP Coordinate System &gt; Auto Detected: *xxx* &gt; Next
    9. Processing Options Template. Here we select what kind of processing we want Pix4Dmapper to do with our images. Suggestion: Standard &gt; 3D Maps (this creates both DSM and orthomosaics.
    10. Deselect Start Processing Now
    11. Finish
2. Project &gt; Save Project
3. If you skipped step 4-1f previously (because the right option was not available):
    1. In file browser: move camera specs file `.../MACS_Tools/pix4d_CameraDef_MACS_Polar18.xml` to `.../04_pix4d` folder
    2. In Toolbar: Help &gt; Settings…
    3. Camera Database &gt; Import...
    4. Navigate to: `.../04_pix4d/`
    5. Select `pix4d_CameraDef_MACS_Polar18.xml` &gt; Open &gt; OK
    6. In Toolbar: Project &gt; Image Properties Editor…
    7. Continue with step 4-1f &gt; OK
4. Prepare for the actual processing:
    1. Lower left corner: Processing Options &gt; Select which processing steps you'd like to run.
        1. Initial Processing: Here, the program does…
        2. Point Cloud and Mesh: Here, Pix4Dmapper generates a point cloud of the photogrammetrically matched images.
        3. DSM, Orthomosaic and Index: The final digital surface model and orthomosaic of the images are created here.
        > Note: Step 1. Initial Processing is the most compute expensive and will take the longest. This processing step is also the bottleneck for project sizes. So with large projects, it's best to divide the study area into smaller subsets, do the initial processing for all subsets separately and then only combine them afterwards to continue with steps 2. and 3. Info on how to do the subsetting and re-matching can be found here:
    2. You can now do some finetuning of your project settings and select whatever you desire to get in your output (or stick with the default settings).
    > Tip: If you plan on processing multiple datasets, and potentially comparing them in further analysis, we recommend to set the output resolution manually (and to the same values throughout all projects)
    3. If you want, save your settings as template. This way, you can quickly select the same processing settings for the next time:
        1. Finish adapting all settings &gt; Save Template &gt; Create New Template with Current Options... &gt; Enter name &gt; Description: Some keywords on what default you started with and what you adapted maybe?
        2. OK
5. Start processing:
    1. Lower left corner: Processing
    2. Make sure all steps you want to execute are checked (1. Initial Processing, 2. Point Cloud and Mesh, and 3. DSM, Orthomosaic and Index)
    3. Click Start
    4. Wait (for a long time.)
    5. When processing is done, your results should appear in `.../04/_pix4d/_your_project_/3_dsm/_ortho/`
6. Optional: You can get some processing insights, by clicking:
    1. Lower left corner: Log Output
    2. Or: Processing &gt; Output Status…
    3. Might be good to keep an eye on your computer's task manager as well. Some processing steps are ***really*** compute intensive and might block you from doing any other tasks in the meantime.

### Part 5: Interpreting the Quality Report

1. After each of the three major processing steps, a quality report is generated (and displayed in Pix4Dmapper, unless you've actively disabled the automatic display)
2. At the end of the last processing step, a PDF of the quality report will be generated and saved in your `.../04_pix4d/your_project/1_initial/report/` folder.
3. On page 1, you'll find a Quality Check overview. If not all options are green, you might need to adapt some camera/image parameters, or processing settings. However, it's also possible that your data is not sufficient or not good enough.  
![pix4d_quality_check](https://user-images.githubusercontent.com/40014163/116422074-ac2d7b80-a83f-11eb-8fec-4ba2cd8df226.png)

4. For more info on what might have gone wrong, and on the general interpretation of the quality report, check out: [https://support.pix4d.com/hc/en-us/articles/202558689-Quality-Report-Help#label100](https://support.pix4d.com/hc/en-us/articles/202558689-Quality-Report-Help#label100) (there's also a YouTube video)

Where to add mipps steps?

What are the mipps steps to take?
