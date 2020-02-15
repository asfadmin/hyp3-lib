#!/usr/bin/python3

import argparse
from argparse import RawTextHelpFormatter
import os
import sys
from osgeo import gdal, ogr, osr
import netCDF4 as nc
from asf_geometry import data2geotiff
from asf_time_series import nc2meta, getNetcdfGranule


def time_series2data(ncFile, granuleList=None):
  if granuleList == None:
    granuleList = getNetcdfGranule(ncFile)
  ### Read granule list
  image = ncFile.variables['image'][:]
  granules = ncFile.variables['granule'][:]
  granules = list(nc.chartostring(granules, encoding='utf-8'))

  geotiff_list = []
  for granule in granuleList:
    t = granules.index(granule)
    data = image[t]
    geotiff_list.append(data)
  print("geotiff_list")
  print(geotiff_list)
  return geotiff_list




def time_series2geotiff(ncFilePath, listFile, outDir):
  ### Read granule list
  granuleList = [line.rstrip() for line in open(listFile)]

  ### Read time series data
  print('Reading time series file ({0}) ...'.format(ncFile))
  dataset = nc.Dataset(ncFilePath, 'r')
  SOMETHING = time_series2data(dataset, granuleList=granuleList)
  dataset.close()

  ### Read time series metadata and
  meta = nc2meta(ncFilePath)
  spatialRef = osr.SpatialReference()
  spatialRef.ImportFromEPSG(meta['epsg'])
  geoTrans = ( meta['minX'], meta['pixelSize'], 0, meta['maxY'], 0, -meta['pixelSize'])

  ### Go through granules
  if not os.path.exists(outDir):
    os.makedirs(outDir)
  for line in lines:
    ## Determine index of the granule in the time series
    t = granules.index(line)
    data = image[t,:,:]
    outFile = os.path.join(outDir, line+'_time_series.tif')

    ## Save time series layers into GeoTIFF files
    print('Saving result to GeoTIFF file ({0})'.format(outFile))
    data2geotiff(data, geoTrans, spatialRef, 'FLOAT', 0, outFile)


if __name__ == '__main__':

  parser = argparse.ArgumentParser(prog='time_series2geotiff',
    description='extracts time series layers and stores them in GeoTIFF format',
    formatter_class=RawTextHelpFormatter)
  parser.add_argument('inFile', metavar='<input file>',
    help='name of the netCDF time series file')
  parser.add_argument('listFile', metavar='<granule list>',
    help='name of the granule list file')
  parser.add_argument('outDir', metavar='<output directory>',
    help='name of the output directory')
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  args = parser.parse_args()

  if not os.path.exists(args.inFile):
    print('netCDF file (%s) does not exist!' % args.inFile)
    sys.exit(1)

  # time_series2geotiff(args.inFile, args.listFile, args.outDir)
  time_series2data(args.inFile)