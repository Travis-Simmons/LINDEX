#!/usr/bin/env python3
"""
Author : Travis Simmons <travissimmons@email.arizona.edu>
Date   : 2/20/2021
Purpose: 
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
                        help='How strict do you want the cloud recognition to be, the lower the more strict',
                        metavar='how_strict',
                        type=float,
                        default=0.7)

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    # Variables

    # Directory containing tar'd or foldered lansat data
    # indir = r'D:\lansat\Bulk Order Large_lansat_8\test'

    # How strict do you want the cloud recognition to be, the lower the more strict
    # how_strict= 0.7


    # # GPS Bounding Box for sampling area, [xmin, xmax, ymin, fymax]
    
    
    # xmin ymin  xmax ymax - gdal 
    
    # xmin ymax xmax ymin

    # x1 = 160785
    # y1 = 3467622
    # x2 = 169515
    # y2 = 3462902

    bb = args.bounding_box

    xmin = int(bb[0])
    ymin = int(bb[1])
    xmax = int(bb[2])
    ymax = int(bb[3])

    #--------------------------------------------------------------------------

    # -Main-


    # If you ahve tars still in the directory, these will grab them and untar them
    
    tars = glob.glob(os.path.join(args.indir ,'*.tar'))
    print('Extracting tar files...')

    # if len(tars) > 1:
    for tar in tars:
        out_file = tar.split('.')[0]


        # making a file for the tars to land
        if not os.path.exists(out_file):
            os.makedirs(out_file)
        one_tar = tarfile.open(tar)
        one_tar.extractall(out_file)
            
            
    # # Function to take a lansat image and crop it to the sample area in Baker County, GA  

    lv1 = glob.glob(os.path.join(args.indir , '*'))
    # print(lv1)
    # print(lv1)

    print('Extraction complete, cropping Lansat images...')
    for folder in lv1:

        if os.path.isdir(folder):
            folder_name = os.path.basename(folder)


            if folder_name.startswith('L'):
                cnt = 1
                # print(os.path.join(folder, '*.TIF'))
                TIFs = glob.glob(os.path.join(folder, '*.TIF'))
                # print(TIFs)

                date = folder.split("_")[-4]

                outdir = os.path.join(args.indir, date)

                while os.path.isdir(outdir):
                    outdir = outdir + f'_{cnt}'
                    cnt += 1

                os.mkdir(outdir)

                # Itterating through the image list
                for im in TIFs:
                    # print(im)

                    split = im.split('_')
                    date = split[-6]
                    band = split[-1]
                    filename = date+'_'+band



            #         print(filename)

                    # Opening each one in GDAL
                    img = gdal.Open(im)

                    # print('translating')
                    # Need to add -a_ullr xmin ymax xmax ymin

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
            
    if not os.path.exists(os.path.join(args.indir, 'NDWI')):
            os.makedirs(os.path.join(args.indir, 'NDWI'))
    
    print('Scanning for cloudcover and running NDWI analysis...')

    for date_folder in lv2:

        if (os.path.isdir(date_folder)):
            date = os.path.basename(date_folder)
            
            
            if not date.startswith('L'):
                band1_imgs = glob.glob(os.path.join(date_folder , '*B1.TIF'))      

                for img in band1_imgs:
                    filename = os.path.basename(img)
    #                     print(img)
    #                     pil_im = Image.open(img)
    #                     display(pil_im)
                    # Open it, histogram mean, sort
                    testing_img = cv2.imread(img)
                    testing_vals = testing_img.mean(axis=2).flatten()
                    testing_mode = statistics.mode(testing_vals)
                    testing_average = statistics.mean(testing_vals)

                    # print('Testing mode: ',testing_mode)
                    # print('Testing Average: ', testing_average)
                    if testing_mode == 0.0:
                        print("Black image")

                    if (len([1 for i in testing_vals if i > testing_mode]) >= len(testing_vals)*args.how_strict) or (testing_average > 35) or (testing_average < 10):
                        # print("Cloudy image")

                        # print(date)
                        try:
                            shutil.move(os.path.join(args.indir, date), os.path.join(args.indir, 'cloudy'))
                        except:
                            continue
                    else:
                        # print("Clear image")
                        # print(date)

                        # do NDWI Then move



                        # Here we can take flags for any index

                        # Calculation
                        # NDWI = (3 - 5)/(3 + 5)
                        date_folder
                        band3 = glob.glob(os.path.join(date_folder, '*B3.TIF'))
                        band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
                        b3 = rio.open(band3[0])
                        b5 = rio.open(band5[0])
                        green = b3.read()
                        nir = b5.read()
                        ndwi = (nir.astype(float)-green.astype(float))/(nir+green)
                        print(type(ndwi))




                        # Plotting
                        fig, ax = plt.subplots(1, figsize=(12, 10))
                        show(ndwi, ax=ax, cmap="coolwarm_r")
                        # testing
                        plt.axis('off')

                        plt.savefig(os.path.join(date_folder, date + '_NDWI.TIF'), bbox_inches = 'tight')
                        plt.savefig(os.path.join(args.indir, 'NDWI' , date + '_NDWI.TIF'), bbox_inches = 'tight')
                        
                        b3.close()
                        b5.close()

                        try:
                            shutil.move(os.path.join(args.indir,  date), os.path.join(args.indir, 'clear'))
                        except:
                            continue


    ndwi_TIFs = glob.glob(os.path.join(args.indir, 'NDWI', '*.TIF'))

   
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
    clip.write_gif(os.path.join(args.indir, 'NDWI', 'final.gif'))


    print(f'Finished analysis, find NDWI outputs at {os.path.join(args.indir,"NDWI")}.')

# --------------------------------------------------
if __name__ == '__main__':
    main()
