#!/usr/bin/python

import argparse
from argparse import RawTextHelpFormatter
import os
import sys
from resample_geotiff import resample_geotiff
import saa_func_lib as saa

def makeAsfBrowse(geotiff, baseName, use_nn=False):
    kmzName = baseName + ".kmz"
    pngName = baseName + ".png"
    lrgName = baseName + "_large.png"
    x1,y1,trans1,proj1 = saa.read_gdal_file_geo(saa.open_gdal_file(geotiff))
    if (x1 < 2048):
        print("Warning: width exceeds image dimension - using actual value")
        resample_geotiff(geotiff,x1,"KML",kmzName,use_nn)
        if x1 < 1024:      
            resample_geotiff(geotiff,x1,"PNG",pngName,use_nn)
        else:
            resample_geotiff(geotiff,1024,"PNG",pngName,use_nn)
        resample_geotiff(geotiff,x1,"PNG",lrgName,use_nn)
    else:
        resample_geotiff(geotiff,2048,"KML",kmzName,use_nn)
        resample_geotiff(geotiff,1024,"PNG",pngName,use_nn)
        resample_geotiff(geotiff,2048,"PNG",lrgName,use_nn)

if __name__ == '__main__':

  parser = argparse.ArgumentParser(prog='makeAsfBrowse',
    description='Resamples a GeoTIFF file and saves it in a number of formats',
    formatter_class=RawTextHelpFormatter)
  parser.add_argument('geotiff', help='name of GeoTIFF file (input)')
  parser.add_argument('basename', help='base name of output file (output)')
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  args = parser.parse_args()

  if not os.path.exists(args.geotiff):
    print('GeoTIFF file (%s) does not exist!' % args.geotiff)
    sys.exit(1)
  if len(os.path.splitext(args.basename)[1]) != 0:
    print('Output file (%s) has an extension!' % args.basename)
    sys.exit(1)

  makeAsfBrowse(args.geotiff, args.basename)
