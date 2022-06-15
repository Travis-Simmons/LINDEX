#!/usr/bin/env python3
"""
Author : Travis Simmons <920117874@student.ccga.edu>
Date   : 2/20/2021
Purpose: Automatically run index timeseries analysis
"""

import argparse
import os
import sys
import cv2
import glob
import tarfile
from osgeo import gdal
import shutil
import statistics
import rasterio as rio
import matplotlib.pyplot as plt
from rasterio.plot import show
from moviepy.editor import ImageSequenceClip

# singularity run test.simg ~/data/landsat -b 444596.16110394 3437984.92577712 472974.60807573 3453852.93907577


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('indir',
                        metavar='indir',
                        type = str,
                        help="Directory containing tar'd or foldered lansat data")



    parser.add_argument('-b',
                        '--bounding_box',
                        help='GPS Bounding Box for sampling area, [xmin, ymin, xmax, ymax]. We recommend leveraging the QGIS plugin "lat lon tools" copy canvas bounding box function. ',
                        metavar='bounding_box',
                        type= float,
                        nargs = '+',
                        required = True
                        )

    parser.add_argument('-c',
                        '--how_strict',
                        help='How strict do you want the cloud recognition to be, the lower the more strict, 999 turns it off, suggested is 0.7',
                        metavar='how_strict',
                        type=float,
                        default=999)

    parser.add_argument('-in',
                        '--index',
                        help='What index to run',
                        metavar='index',
                        type=str,
                        default='ndwi')

    return parser.parse_args()


# ------- Functions --------
def do_ndwi(date_folder):

    band3 = glob.glob(os.path.join(date_folder, '*B3.TIF'))
    band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
    b3 = rio.open(band3[0])
    b5 = rio.open(band5[0])
    green = b3.read()
    nir = b5.read()
    green = green.astype(float)
    nir = nir.astype(float)
    ndwi = (nir-green)/(nir+green)
    b3.close()
    b5.close()
    return ndwi

def do_ndvi(date_folder):
    band4 = glob.glob(os.path.join(date_folder, '*B4.TIF'))
    band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
    b4 = rio.open(band4[0])
    b5 = rio.open(band5[0])
    red = b4.read()
    nir = b5.read()
    red = red.astype(float)
    nir = nir.astype(float)
    ndvi = (nir-red)/(nir+red)
    b4.close()
    b5.close()
    return ndvi

def do_evi(date_folder):
    band2 = glob.glob(os.path.join(date_folder, '*B2.TIF'))
    band4 = glob.glob(os.path.join(date_folder, '*B4.TIF'))
    band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
    b2 = rio.open(band2[0])
    b4 = rio.open(band4[0])
    b5 = rio.open(band5[0])
    blue = b2.read()
    red = b4.read()
    nir = b5.read()
    blue = blue.astype(float)
    red = red.astype(float)
    nir = nir.astype(float)
    g = 2.5
    c1 = 6
    c2 = 7.5
    l = 1
    
    evi =g*((nir-red)/(nir+c1*red-c2*blue+l)) 
    b2.close()
    b4.close()
    b5.close()
    return evi

def do_avi(date_folder):
    band4 = glob.glob(os.path.join(date_folder, '*B4.TIF'))
    band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
    b4 = rio.open(band4[0])
    b5 = rio.open(band5[0])
    red = b4.read()
    nir = b5.read()
    red = red.astype(float)
    nir = nir.astype(float)
    avi = (nir*(1-red)*(nir-red))**(1/3)
    b4.close()
    b5.close()
    return avi

def do_savi(date_folder):
    band4 = glob.glob(os.path.join(date_folder, '*B4.TIF'))
    band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
    b4 = rio.open(band4[0])
    b5 = rio.open(band5[0])
    red = b4.read()
    nir = b5.read()
    red = red.astype(float)
    nir = nir.astype(float)
    l = .5
    savi = ((nir-red)/(nir+red+l))*(1+l)
    b4.close()
    b5.close()
    return savi

def do_ndmi(date_folder):
    band6 = glob.glob(os.path.join(date_folder, '*B6.TIF'))
    band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
    b6 = rio.open(band6[0])
    b5 = rio.open(band5[0])
    swir = b6.read()
    nir = b5.read()
    swir = swir.astype(float)
    nir = nir.astype(float)
    ndmi = (nir-swir)/(nir+swir)
    b6.close()
    b5.close()
    return ndmi

def do_msi(date_folder):
    band6 = glob.glob(os.path.join(date_folder, '*B6.TIF'))
    band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
    b6 = rio.open(band6[0])
    b5 = rio.open(band5[0])
    swir = b6.read()
    nir = b5.read()
    swir = swir.astype(float)
    nir = nir.astype(float)
    msi = swir/nir
    b6.close()
    b5.close()
    return msi

def do_gci(date_folder):
    band6 = glob.glob(os.path.join(date_folder, '*B6.TIF'))
    band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
    b6 = rio.open(band6[0])
    b5 = rio.open(band5[0])
    swir = b6.read()
    nir = b5.read()
    swir = swir.astype(float)
    nir = nir.astype(float)
    msi = swir/nir
    b6.close()
    b5.close()
    return gci

def do_gci(date_folder):

    band3 = glob.glob(os.path.join(date_folder, '*B3.TIF'))
    band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
    b3 = rio.open(band3[0])
    b5 = rio.open(band5[0])
    green = b3.read()
    nir = b5.read()
    green = green.astype(float)
    nir = nir.astype(float)
    gci = (nir/green)-1
    b3.close()
    b5.close()
    return gci

def do_nbri(date_folder):
    band7 = glob.glob(os.path.join(date_folder, '*B7.TIF'))
    band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
    b7 = rio.open(band7[0])
    b5 = rio.open(band5[0])
    swir = b7.read()
    nir = b5.read()
    swir = swir.astype(float)
    nir = nir.astype(float)
    nbri = (nir-swir)/(nir+swir)
    b7.close()
    b5.close()
    return nbri

def do_bsi(date_folder):
    band2 = glob.glob(os.path.join(date_folder, '*B2.TIF'))
    band4 = glob.glob(os.path.join(date_folder, '*B4.TIF'))
    band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
    band6 = glob.glob(os.path.join(date_folder, '*B6.TIF'))
    b2 = rio.open(band2[0])
    b4 = rio.open(band4[0])
    b5 = rio.open(band5[0])
    b6 = rio.open(band6[0])
    blue = b2.read()
    red = b4.read()
    nir = b5.read()
    swir = b6.read()
    blue = blue.astype(float)
    red = red.astype(float)
    nir = nir.astype(float)
    swir = swir.astype(float)
    
    bsi = ((red+swir)-(nir+blue))/((red+swir) + (nir+blue))
    b2.close()
    b4.close()
    b5.close()
    b6.close()
    return bsi

def do_ndsi(date_folder):

    band3 = glob.glob(os.path.join(date_folder, '*B3.TIF'))
    band6 = glob.glob(os.path.join(date_folder, '*B6.TIF'))
    b3 = rio.open(band3[0])
    b6 = rio.open(band6[0])
    green = b3.read()
    swir = b6.read()
    green = green.astype(float)
    swir = swir.astype(float)
    ndsi = (green-swir) / (green-swir)
    b3.close()
    b6.close()
    return ndsi


def do_ndgi(date_folder):

    band3 = glob.glob(os.path.join(date_folder, '*B3.TIF'))
    band4 = glob.glob(os.path.join(date_folder, '*B4.TIF'))
    b3 = rio.open(band3[0])
    b4 = rio.open(band4[0])
    nir = b3.read()
    green = b4.read()
    green = green.astype(float)
    nir = nir.astype(float)
    ndgi = (nir-green)/(nir+green)
    b3.close()
    b4.close()
    return ndgi


def index_template(date_folder):

    # replace the underscores with the band you need, repeat as necissary
    band_ = glob.glob(os.path.join(date_folder, '*B_.TIF'))
    b_ = rio.open(band_[0])

    # After adding in each band you will be using, rename then as their common name eg: nir, red, green ...
    # replace occurances of that below
    green = b_.read()
    green = green.astype(float)

    # Replace index name with your index
    # do the raster math with the common names
    ndgi = (nir-green)/(nir+green)

    # Close all the bands, repeat as necissary
    b_.close()

    # Scroll down and find 'index dict' to add your index to the options before running



def check_cloudy(img):
    # Open it, histogram mean, sort
    testing_img = cv2.imread(img)
    testing_vals = testing_img.mean(axis=2).flatten()
    testing_mode = statistics.mode(testing_vals)
    testing_average = statistics.mean(testing_vals)

    
    # Here we are looking for unusable dates
    # first we look for black images, this indicates that although your roi was in the area of the scan, it was outside the imaged area
    # Then we use a series of statements to test for how variable the pixel intensities are
    # If they are highly variable they are likely cloudy
    if testing_mode == 0.0:
        print("Black image")
    
    # checking for heterogeneity of pixel intensities
    if (len([1 for i in testing_vals if i > testing_mode]) >= len(testing_vals)*args.how_strict):
        return True
    
    # testing for a super bright image (mostly clouds but homogenious so it wont get caught in cloud detection)
    elif testing_average > 35:
        return True

    # testing for super dark image
    elif testing_average < 10:
        return True
        
    else:
        return False




# --------------------------------------------------
def main():
    global args
    args = get_args()

    index_dict = {
    'ndwi': do_ndwi, # working
    'ndvi': do_ndvi, # working
    'evi' : do_evi,# working
    'avi' : do_avi,# working
    'savi' : do_savi, # working
    'ndmi' : do_ndmi,# working
    'msi' : do_msi,# working
    'gci' : do_gci,# working
    'nbri' : do_nbri,# working
    'bsi' : do_bsi,# working
    'ndsi' : do_ndsi, # working
    'ndgi' : do_ndgi, # add your custom index here

    }

    # we want to use the band names for landsat8 for all calcs
    # format = landsat8 band : new band
    # In development
    bands_dict = {
        'landsat_8_9':{
            'B1':'B1',
            'B2':'B2',
            'B3':'B3',
            'B4':'B4',
            'B5':'B5',
            'B6':'B6',
            'B7':'B7',
            'B8':'B8',
            'B9':'B9',
            'B10':'B10',
            'B11':'B11'
        },
        # add in warning for bands
        'landsat_7':{
            'B2':'B1',
            'B3':'B2',
            'B4':'B3',
            'B5':'B4',
            'B6':'B5',
            'B7':'B7',
            'B8':'B8',
            'B10':'B6'
        },

        'landsat_4_5':{

        },

        'landsat_1_5':{

        }

    }








    bb = args.bounding_box

    xmin = int(bb[0])
    ymin = int(bb[1])
    xmax = int(bb[2])
    ymax = int(bb[3])


    index_name = args.index

    # If you ahve tars still in the directory, these will grab them and untar them
    
    tars = glob.glob(os.path.join(args.indir ,'*.tar'))
    print('Extracting tar files...')

    for tar in tars:
        out_file = tar.split('.')[0]

        # making a file for the tars to land
        if not os.path.exists(out_file):
            os.makedirs(out_file)
        one_tar = tarfile.open(tar)
        one_tar.extractall(out_file)

    lv1 = glob.glob(os.path.join(args.indir , '*'))

    print('Extraction complete, cropping Lansat images...')
    for folder in lv1:

        if os.path.isdir(folder):
            folder_name = os.path.basename(folder)


            if folder_name.startswith('L'):
                cnt = 1
                TIFs = glob.glob(os.path.join(folder, '*.TIF'))

                date = folder.split("_")[-4]

                outdir = os.path.join(args.indir, date)

                while os.path.isdir(outdir):
                    outdir = outdir + f'_{cnt}'
                    cnt += 1

                os.mkdir(outdir)

                # Itterating through the image list
                for im in TIFs:
                    split = im.split('_')
                    date = split[-6]
                    band = split[-1]
                    filename = date+'_'+band

                    # Opening each one in GDAL
                    img = gdal.Open(im)

                    # large extent
                    # 160894,3459609,173729,3468590
                    # QGIS copy seems to be in xmin ymin xmax ymax
                    # We need to change the input to reflect that for ease of use
                    gdal.Translate(os.path.join(outdir, filename), img, projWin = [xmin, ymax, xmax, ymin])

    lv2 = glob.glob(os.path.join(args.indir, '*'))

    print('Creating cloudy and clear directories for sorting...')

    if not os.path.exists(os.path.join(args.indir, 'cloudy')):
            os.makedirs(os.path.join(args.indir, 'cloudy'))

    if not os.path.exists(os.path.join(args.indir, 'clear')):
            os.makedirs(os.path.join(args.indir, 'clear'))
            
    if not os.path.exists(os.path.join(args.indir, index_name)):
            os.makedirs(os.path.join(args.indir, index_name))
    

# Raw
    if not os.path.exists(os.path.join(args.indir, index_name, 'raw')):
            os.makedirs(os.path.join(args.indir, index_name, 'raw'))

# Visualizations
    if not os.path.exists(os.path.join(args.indir, index_name, 'visualizations')):
            os.makedirs(os.path.join(args.indir, index_name, 'visualizations'))

    print(f'Scanning for cloudcover and running {index_name} analysis...')

    for date_folder in lv2:

        if (os.path.isdir(date_folder)):
            date = os.path.basename(date_folder)
            
            
            if not date.startswith('L'):
                band1_imgs = glob.glob(os.path.join(date_folder , '*B1.TIF'))      

                for img in band1_imgs:
                    filename = os.path.basename(img)



                    # Check if the user wants to check for clouds
                    if not args.how_strict == 999:
                        is_cloudy = check_cloudy(img)

                    else:
                        is_cloudy = False

                    if is_cloudy == True:
    
                        try:
                            shutil.move(os.path.join(args.indir, date), os.path.join(args.indir, 'cloudy'))
                        except:
                            continue
                    else:
                        
                        # Do index then move the images

                        # Here we can take flags for any index
                        index_eval = index_dict[args.index](date_folder)

# https://gis.stackexchange.com/questions/290776/how-to-create-a-tiff-file-using-gdal-from-a-numpy-array-and-specifying-nodata-va
                        ds = gdal.Open(img)
                        cols = ds.RasterXSize
                        rows = ds.RasterYSize
                        myarray = index_eval
                        trans = ds.GetGeoTransform()
                        # create the output image
                        driver = ds.GetDriver()
                        outDs = driver.Create(os.path.join(args.indir, index_name ,'raw', date + f'_{index_name}.TIF'), cols, rows, 1, gdal.GDT_Float32)
                        outBand = outDs.GetRasterBand(1)
                        # outBand.SetNoDataValue()
                        outBand.WriteArray(myarray[0])
                        outDs.SetGeoTransform(trans)





                        # Plotting
                        fig, ax = plt.subplots(1, figsize=(12, 10))
                        show(index_eval, ax=ax, cmap="coolwarm_r")
                        plt.axis('off')

                        plt.savefig(os.path.join(date_folder, date + f'_{index_name}.TIF'), bbox_inches = 'tight')
                        plt.savefig(os.path.join(args.indir, index_name, 'visualizations' , date + f'_{index_name}.TIF'), bbox_inches = 'tight')
                        

                        try:
                            shutil.move(os.path.join(args.indir,  date), os.path.join(args.indir, 'clear'))
                        except:
                            continue


    ndwi_TIFs = glob.glob(os.path.join(args.indir, index_name, 'visualizations', '*.TIF'))




    for i in ndwi_TIFs:
        # Add coordinates
        img = gdal.Open(i)
        gdal.Translate(i.replace('.TIF', '_reprojected.TIF'), img, outputBounds = [xmin, ymax, xmax, ymin])

        # Labeling
        # pic_name = os.path.basename(i)
        # pic_name = pic_name.replace('.TIF', '')
        # img = cv2.imread(i)
        # height, width, channels = img.shape
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(img,pic_name,(int(width/2),height, font, 1,(0,0,0),2))
        # cv2.imwrite(i.replace('.TIF', '_labeled.TIF'), img)

    # ndwi_TIFs_labeled = glob.glob(os.path.join(args.indir, 'NDWI', '*labeled.TIF'))
    clip = ImageSequenceClip(ndwi_TIFs,fps=.20)
    clip.write_gif(os.path.join(args.indir, index_name, 'visualizations', 'final.gif'))


    print(f'Finished analysis, find {index_name} outputs at {os.path.join(args.indir,index_name)}.')

# --------------------------------------------------
if __name__ == '__main__':
    main()
