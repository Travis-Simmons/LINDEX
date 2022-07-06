# LINDEX

LINDEX is a containerized Landsat 8 processing tool for timeseries index analysis.

## Inputs

A directory containing compressed Landsat 8 data, and corner cordinates for your region of interest.


## Outputs

The origional Landast 8 data cropped to your region of interest and sorted by cloudcover as well as the results of the selected analysis for each non-cloudy day.

## Arguments and Flags
* **Positional Arguments:**
    * **Directory containing compressed Landsat 8 data:** 'indir'
* **Required Arguments:**
    * **Corner cordinates of GPS bounding box for your region of intrest in UTM:** '-b', '--bounding_box'
    * **Index you would like to run (options below):** '-in', '--index'
* **Optional Arguments:**
    * **Strictness of cloud detection:** '-c', '--how_strict', default = 0.7 (the lower the value the more strict)

## Workflow for finding GPS bounding cordinates.

1. Download the Earth Explorer Bulk Download Application 
    * https://dds.cr.usgs.gov/bulk
2. Use the Bulk Download Application and the Earth Eplorer Website in order to bulk download compressed Lansat-8 data in your region of intrest
3. Uncompress one TAR
4. Use QGIS to visualize one band
5. Zoom into your ROI
6. Use the QGIS 'Lat Lon Tools' plugin to copy the canvas coordinates (modify plugin setting to take coordinates in UTM with spaces separating)
7. Run the container

## Example Deployment
singularity build lindex.img docker://travissimmons/lindex:all_indices

singularity run lindex.img {PATH TO COMPRESSED DATA} -b {PASTE CORNER COORDINATES} -in {index name}


| Index Name                                     | Formula                                         | 
|------------------------------------------------|-------------------------------------------------|
| Normalized Difference Water Index (NDWI)       | (NIR-SWIR)/(NIR+SIWR)                           |
| Normalized Differencce Vegetation Index (NDVI) | (NIR-RED)/(NIR+RED)                             |
| Enhanced Vegetation Index (EVI)                | G*((NIR-RED)/(NIR+C1*R-C2*BLUE+L))              |
| Advanced Vegetation Index (AVI)                | (NIR*(1-RED)*(NIR-RED))^(1/3)                   |
| Soil Adjusted Vegetation IndexSAVI             | ((NIR-RED)/(NIR+RED+L))*(1+L)                   |
| NDMI                                           | (NIR-SWIR)/(NIR+SWIR)                           |
| MSI                                            | MidIR/NIR                                       |
| GCI                                            | (NIR)/(GREEN)-1                                 |
| NBRI                                           | (NIR-SWIR)/(NIR+SWIR)                           |
| BSI                                            | ((RED+SWIR)-(NIR+BLUE))/((RED+SWIR)+(NIR+BLUE)) |
| NDSI                                           | (GREEN-SWIR)/(GREEN+SWIR)                       |
| NDGI                                           | (NIR-GREEN)/(NIR+GREEN)                         |


## Custom Indices

Refer to the index template function in lindex.py in order to add your own custom index.


DOI: 10.1002/essoar.10511799.1
