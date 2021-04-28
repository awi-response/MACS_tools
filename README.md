# MACS_tools
Tools for handling DLR MACS (Modular Aerial Camera System) data

# MACS Processing Step-by-Step

_Version: 2021-04-27 Authors: Tabea Rettelbach, Jennika Hammar, Ingmar Nitze_

# Part 0: Setup

1. Make sure you have the following programs installed:
    1. Python 3
    2. Anaconda
    3. QGIS
    4. Pix4Dmapper (commercial licence required)
    5. DLR MACS box (Mosaica, MIPPS)
    6. Git
2. Clone MACS\_tools git repository:
    1. ![](RackMultipart20210428-4-fh9bg4_html_1d7f3ac495cc8904.gif)
    > TIP: You should do all processing on a local drive, preferably an SSD. It&#39;s therefore best to organize you entire project here. Do not attempt processing on a shared network. The overhead will make processing way too slow.In Windows Explorer: browse to folder where you will be doing the processing
    2. Right click in explorer \&gt; Git Bash Here
    3. In bash, type: git clone [https://github.com/awi-response/MACS\_tools.git](https://github.com/awi-response/MACS_tools.git)
    4. I ![](RackMultipart20210428-4-fh9bg4_html_84af853e31d80588.png)
 n explorer: unzip processing\_folder\_structure\_template.zip to where you&#39;ll do your processing (½!). Folder structure should look like this:

# Part 1: Prepare your study area

1. Start QGIS \&gt; Open new empty project
2. Drag &amp; drop flight footprints into QGIS (should be located within the raw\_data folder of each flight)
3. O ![](RackMultipart20210428-4-fh9bg4_html_7132a1b03546cdb8.png) PTIONAL: Add basemap, for better visualization:
    1. Make sure QuickMapServices PlugIn is installed in QGIS (Plugins \&gt; Manage and Install Plugins \&gt; Search for QuickMapServices \&gt; Install Plugin)
    2. In toolbar: QuickMapServices \&gt; Settings
    3. M ![](RackMultipart20210428-4-fh9bg4_html_ec30f19acd22c1a6.png)
 ore services tab \&gt; Get contributed pack \&gt; Save
    4. In toolbar: QuickMapServices \&gt; ESRI \&gt; ESRI Satellite (or whichever basemap you prefer)
4. Make study area shapefile
    1. Layer \&gt; Create layer \&gt; New Shapefile Layer
    2. File name = _path/to/your/file/02\_studysites/your\_study\_area_
    3. Geometry type = Polygon
    4. Ok
    5. In toolbar: Add Polygon Feature (Ctrl + .) \&gt; start drawing polygon of your desired study area \&gt; finish polygon with right click
    6. In toolbar: Save layer edits
5. Select footprints that are in study area
    1. Vector \&gt; Research tools \&gt; Select by location
    2. Select features from: _your\_footprint\_layer_
    3. Where the features: check intersect
    4. By comparing to the features from: _your\_study\_area_
    5. Modify current selection by: creating new selection
    6. Run
    7. ![](RackMultipart20210428-4-fh9bg4_html_d1fad712311099b8.gif)
    > TIP: Don&#39;t select study areas that are too large. ca. 5000 images are already _a lot!_ Processing steps at later stages grow exponentially (?) in computing time. So, if your study area is too large, you&#39;ll need to subset it when processing in Pix4D and then later stitch them back together.Close
6. Save footprint selection:
    1. Right click footprints \&gt; Export \&gt; Save Features As…

    1. Format: ESRI Shapefile
    2. File name: _path/to/your/file/02\_studysites/my\_study\_area\_footprints_
    3. Check: Save only selected features
    4. Check: Add saved file to map
    5. Ok

1. Remove the footprint layer with all image footprints:
    1. Right click all footprints \&gt; Remove Layer… \&gt; OK
2. Save GIS project in 05\_gis (of the unzipped folder structure template)

# Part 2: move all necessary MACS images to the local drive

1. Open Anaconda Prompt (anaconda3)
2. Browse to MACS\_tools repo:
    1. d: (or whatever drive you&#39;re on)
    2. cd your\_path\_here\MACS\_tools
3. Install and activate the virtual python environment
    1. conda env list (if macs\_tools is already listed, then skip to step 3c)
    2. conda env install -n macs\_tools -f environment\_geopandas.yml (only necessary the first time, might take a while)
    3. conda activate macs\_tools
4. move the MACS images of interest:
    1. Launch Jupyter Notebook with: jupyter notebook (still in Anaconda Prompt)
    2. Select move\_MACS\_files.ipynb
    3. Adapt paths:
        - path\_footprints (path to the subset of the MACS image footprints located only in your study area)
        - path\_infiles (the directory with all the MACS images from this flight)
        - path\_outfiles (local drive where to store the relevant images: suggestion: 01\_raw-data from the folder structure template)
    4. Run all notebook cells \&gt; wait (this can take several hours; depending on the copy locations and the number of images in your study area).
    > This step has crashed in the past (error so far unknown). You might need to rerun the last cell of the notebook to restart the copying process. The function checks, if the current file is already at the destination, so it will only retry copying those that it had missed previously (saves time by only copying each file once, even if it crashes).

# Part 3: Prepare camera and navigation files in Mosaica

1. Get the corrected navigation files corresponding to your flight:
    1. N:\response\Restricted\_Airborne\MACs\Alaska\ThawTrend-Air\_2019\MACS\_Nav-PP\_your\_flight_
    2. Unzip the correct folder (they are named after the date of acquisition; the .pptx-file contains an overview of all footprints and dates  you can check which one you need here)
    3. Copy _date_\_nav.txt file to _local_\__drive_\...\03\_mosaica
2. Open Mosaica
    1. Toolbar \&gt; DLR MACS-box \&gt; Geo \&gt; Mosaica
3. Add MACS images:
    1. In file browser, navigate to 01\_rawdata/macs (where move\_MACS\_files.ipynb just moved your images)
    2. Select Left, NIR, Right folders
    3. Drag and drop into Mosaica
    4. Wait (or deselect &#39;Show Images&#39; for faster loading)
4. Save Mosaica project in _local_\__drive_/.../03\_mosaica
5. ![](RackMultipart20210428-4-fh9bg4_html_68bf2b984b230d93.png)Adapt the menu bar as follows:
6. Import the navigation file:
    1. File \&gt; Import NavFiles
    2. Select the text file with the post processed coordinates: _local\_drive_/.../03\_mosaica/_date_\_Nav.txt
    3. Apply import to all items? \&gt; Yes
    4. Adapt configurations to match the following:
    > Note: The number of lines to skip will depend on your exact navigation file. Make sure, it corresponds to the number of header rows in your nav.txt file. According to metadata of the flight, the height reference is actually EGM 2008, but we can only select EGM96.OK \&gt; wait \&gt; OK
7. Export MACS images as .tiff images
    1. Right click on file xxx\_MACS-xxx.xml in Project Tree \&gt; Export \&gt; TIF Images
    2. Navigate to _local\_drive_/.../01\_rawdata/\&gt; click tif-folder \&gt; Select Folder
    3. Wait
8. Export Mosaica nav-file to txt for later processing:
    1. Right click on file xxx\_MACS-xxx.xml in Project Tree \&gt; Export \&gt; Nav -\&gt; TXT
    2. Navigate to _local\_drive_/.../03\_mosaica/
    3. File name: _date_\_Nav\_mosaica.txt
    4. Save \&gt; OK
9. Prepare Nav file for Pix4Dmapper
    1. Open Jupyter Home Page (should still be open in your browser from step 2.4
    2. Double click correctednav\_to\_pix4dnav.ipynb notebook
    3. Adapt INFILE and outfile variables corresponding to your file locations (suggestions are given)
    4. Specify vertical and horizontal accuracy
    5. Execute all cells consecutively

# Part 4: Processing in Pix4Dmapper

1. Launch Pix4Dmapper (you&#39;ll need a licence for this. If you don&#39;t have access yet, contact Ingmar Nitze for more info: [ingmar.nitze@awi.de](mailto:ingmar.nitze@awi.de))
    1. New Project \&gt; Name: _your\_project\_name_ \&gt; Create in: …/04\_pix4d \&gt; Project Type: New Project \&gt; Next
    2. Add Directories \&gt; navigate to …/01\_rawdata/macs \&gt; select NIR, Right, or Left folder \&gt; Choose (repeat if multiple directories should be added)
    3. Next
    4. &quot;More than 80% of the image coordinates […] were the same and […] geotags have been discarded&quot; \&gt; OK
    5. Image Geolocation: Geolocation and Orientation: From File… \&gt; File Format: Latitude, longitude, Altitude \&gt; File: …/04\_pix4d/_date_\_Nav\_geo\_pix4d.txt \&gt; Open \&gt; OK
    6. Selected Camera Model:
        1. This should read: MACS\_Polar18\__xxx_
        2. If not: Edit… Camera Model Name: MACS\_Polar18\__xxx_ \&gt; OK
        3. If this option is not available, skip step 4\_1f. for now, we&#39;ll get to it later.
    7. Next
    8. Output/GCP Coordinate System \&gt; Auto Detected: _xxx_ \&gt; Next
    9. Processing Options Template. Here we select what kind of processing we want Pix4Dmapper to do with our images. Suggestion: Standard \&gt; 3D Maps (this creates both DSM and orthomosaics.
    10. Deselect Start Processing Now
    11. Finish
2. Project \&gt; Save Project
3. If you skipped step 4\_1f previously (because the right option was not available):
    1. In file browser: move camera specs file …/MACS\_Tools/pix4d\_CameraDef\_MACS\_Polar18.xml to …/04\_pix4d folder
    2. In Toolbar: Help \&gt; Settings…
    3. Camera Database \&gt; Import…
    4. Navigate to: …/04\_pix4d/
    5. Select pix4d\_CameraDef\_MACS\_Polar18.xml \&gt; Open \&gt; OK
    6. In Toolbar: Project \&gt; Image Properties Editor…
    7. Continue with step 4\_1f \&gt; OK
4. Prepare for the actual processing:
    1. Lower left corner: Processing Options \&gt; Select which processing steps you&#39;d like to run.
        1. Initial Processing: Here, the program does…
        2. Point Cloud and Mesh: Here, Pix4Dmapper generates a point cloud of the photogrammetrically matched images.
        3. ![](RackMultipart20210428-4-fh9bg4_html_682d7cf23ea6adc3.gif)
        > Note: Step 1. Initial Processing is the most compute expensive and will take the longest. This processing step is also the bottleneck for project sizes. So with large projects, it&#39;s best to divide the study area into smaller subsets, do the initial processing for all subsets separately and then only combine them afterwards to continue with steps 2. and 3. Info on how to do the subsetting and re-matching can be found here:3. DSM, Orthomosaic and Index: The final digital surface model and orthomosaic of the images are created here.
    2. ![](RackMultipart20210428-4-fh9bg4_html_acbb1259243e97d0.gif)
Tip: If you plan on processing multiple datasets, and potentially comparing them in further analysis, we recommend to set the output resolution manually (and to the same values throughout all projects)You can now do some finetuning of your project settings and select whatever you desire to get in your output (or stick with the default settings).
    3. If you want, save your settings as template. This way, you can quickly select the same processing settings for the next time:
        1. Finish adapting all settings \&gt; Save Template \&gt; Create New Template with Current Options… \&gt; Enter name \&gt; Description: Some keywords on what default you started with and what you adapted maybe?
        2. OK
5. Start processing:
    1. Lower left corner: Processing
    2. Make sure all steps you want to execute are checked (1. Initial Processing, 2. Point Cloud and Mesh, and 3. DSM, Orthomosaic and Index)
    3. Click Start
    4. Wait (for a long time.)
    5. When processing is done, your results should appear in …/04\_pix4d/_your\_project_/3\_dsm\_ortho/
6. Optional: You can get some processing insights, by clicking:
    1. Lower left corner: Log Output
    2. Or: Processing \&gt; Output Status…
    3. Might be good to keep an eye on your computer&#39;s task manager as well. Some processing steps are _ **really** _ compute intensive and might block you from doing any other tasks in the meantime.

# Part 5: Interpreting the Quality Report

1. After each of the three major processing steps, a quality report is generated (and displayed in Pix4Dmapper, unless you&#39;ve actively disabled the automatic display)
2. At the end of the last processing step, a PDF of the quality report will be generated and saved in your …/04\_pix4d/_your\_project_/1\_initial/report/ folder.
3. O ![](RackMultipart20210428-4-fh9bg4_html_31d89ffe91545931.png)
 n page 1, you&#39;ll find a Quality Check overview. If not all options are green, you might need to adapt some camera/image parameters, or processing settings. However, it&#39;s also possible that your data is not sufficient or not good enough.
4. For more info on what might have gone wrong, and on the general interpretation of the quality report, check out: [https://support.pix4d.com/hc/en-us/articles/202558689-Quality-Report-Help#label100](https://support.pix4d.com/hc/en-us/articles/202558689-Quality-Report-Help#label100) (there&#39;s also a YouTube video)

Where to add mipps steps?

What are the mipps steps to take?
