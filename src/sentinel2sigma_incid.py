#!/usr/bin/python3

import argparse
import os, sys
import shutil
import numpy as np
import datetime


def sentinel2sigma_incid(inFile, sigmaFile, incidFile):

  ### Create temporary directory
  tmpDir = 'windspeed_' + datetime.datetime.utcnow().isoformat()
  os.makedirs(tmpDir)

  ### Import Sentinel-1 into ASF internal format
  print('Importing Sentinel-1 data ...')
  importFile = os.path.join(tmpDir, 'import')
  cmd = ('asf_import -format sentinel -sigma {0} {1}'.format(inFile,
    importFile))
  os.system(cmd)

  ### Geocode ASF internal Sentinel-1 VV and incidence angle
  print('Gecoding Sentinel-1 bands ...')
  geocode_vv = os.path.join(tmpDir, 'geocode_vv')
  geocode_incid = os.path.join(tmpDir, 'geocode_incid')
  cmd = ('asf_geocode -pixel-size 50 -p utm -force -band VV {0} {1}' \
    .format(importFile, geocode_vv))
  os.system(cmd)
  cmd = ('asf_geocode -pixel-size 50 -p utm -force -band INCID {0} {1}' \
    .format(importFile, geocode_incid))
  os.system(cmd)

  ### Export files to GeoTIFF
  print('Exporting bands to GeoTIFF ...')
  geotiff_vv = os.path.join(tmpDir, 'geotiff_vv.tif')
  geotiff_incid = os.path.join(tmpDir, 'geotiff_incid.tif')
  cmd = ('asf_export {0} {1}'.format(geocode_vv, sigmaFile))
  os.system(cmd)
  cmd = ('asf_export {0} {1}'.format(geocode_incid, incidFile))
  os.system(cmd)

  shutil.rmtree(tmpDir)


if __name__ == '__main__':

  parser = argparse.ArgumentParser(prog='sentinel2sigma_incid',
    description='Conversion of Sentinel-1 data to geocoded sigma0 and ' \
    'incidence angle')
  parser.add_argument('inFile', metavar='<manifest.safe>',
    help='name of the manifest file')
  parser.add_argument('sigmaFile', metavar='<sigma0>',
    help='name of the sigma0 GeoTIFF file')
  parser.add_argument('incidFile', metavar='<incidence angle>',
    help='name of the incidence angle GeoTIFF file')
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  args = parser.parse_args()

  sentinel2sigma_incid(args.inFile, args.sigmaFile, args.incidFile)