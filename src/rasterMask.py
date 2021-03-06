#!/usr/bin/python3

import argparse
import sys
import numpy as np
from osgeo import gdal
from asf_geometry import geotiff2data, data2geotiff
from asf_time_series import vector_meta


def applyRasterMask(inFile, maskFile, outFile):

  (data, dataGeoTrans, dataProj, dataEPSG, dataDtype, dataNoData) = \
    geotiff2data(inFile)
  (mask, maskGeoTrans, maskProj, maskEPSG, maskDtype, maskNoData) = \
    geotiff2data(maskFile)

  data = data.astype(np.float32)
  mask = mask.astype(np.float32)
  (dataRows, dataCols) = data.shape
  dataOriginX = dataGeoTrans[0]
  dataOriginY = dataGeoTrans[3]
  dataPixelSize = dataGeoTrans[1]
  (maskRows, maskCols) = mask.shape
  maskOriginX = maskGeoTrans[0]
  maskOriginY = maskGeoTrans[3]
  maskPixelSize = maskGeoTrans[1]
  offsetX = int(np.rint((maskOriginX - dataOriginX)/maskPixelSize))
  offsetY = int(np.rint((dataOriginY - maskOriginY)/maskPixelSize))
  data = data[offsetY:maskRows+offsetY,offsetX:maskCols+offsetX]
  data *= mask

  data2geotiff(data, dataGeoTrans, dataProj, 'FLOAT', np.nan, outFile)


def rasterMask(inFile, maskFile, aoiFile, maskAoiFile, outFile):

  ### Extract relevant metadata from AOI shapefile
  (fields, proj, extent, features) = vector_meta(aoiFile)
  pixelSize = features[0]['pixSize']
  epsg = features[0]['epsg']
  proj = ('EPSG:{0}'.format(epsg))
  coords = (extent[0], extent[2], extent[1], extent[3])

  ### Generate raster mask
  gdal.Warp(maskAoiFile, maskFile, format='GTiff', dstSRS=proj, xRes=pixelSize,
    yRes=pixelSize, resampleAlg='cubic', outputBounds=coords,
    outputType=gdal.GDT_Byte, creationOptions=['COMPRESS=LZW'])

  ### Apply raster mask to image
  applyRasterMask(inFile, maskAoiFile, outFile)


if __name__ == '__main__':

  parser = argparse.ArgumentParser(prog='rasterMask',
    description='Generate an AOI mask and apply it')
  parser.add_argument('inFile', help='name of the file to be masked')
  parser.add_argument('maskFile', help='name of the external mask file')
  parser.add_argument('aoiFile', help='name of the AOI polygon file')
  parser.add_argument('maskAoiFile', help='name of the AOI mask file')
  parser.add_argument('outFile', help='name of the masked file')
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  args = parser.parse_args()

  rasterMask(args.inFile, args.maskFile, args.aoiFile, args.maskAoiFile,
    args.outFile)
