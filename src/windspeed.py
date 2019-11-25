#!/usr/bin/python3

import argparse
import os, sys
import numpy as np
from osgeo import gdal, ogr, osr
from asf_geometry import raster_meta, geotiff2data, data2geotiff


def calcNRCS(v, phi, theta, type):

  ### v - wind velocity [m/s]
  ### phi - angle [degrees] between azimuth and wind direction
  ### theta - incidence angle [degrees]

  ### A. Verhoef, M. Portabella, A. Stoffelen and H. Hersbach, 2008.
  ### CMOD5.n - the CMOD5 GMF for neutral winds
  ### Technical Note: SAF/OSI/CDOP/KNMI/TEC/TN/165
  cmod5 = [ 0, -0.688, -0.793, 0.338, -0.173, 0.0, 0.004, 0.111, 0.0162, 6.34,
    2.57, -2.18, 0.4, -0.6, 0.045, 0.007, 0.33, 0.012, 22.0, 1.95, 3.0, 8.39,
    -3.44, 1.36, 5.35, 1.99, 0.29, 3.80, 1.53 ]
  cmod5n = [ 0, -0.6878, -0.7957, 0.338, -0.1728, 0.0, 0.004, 0.1103, 0.0159,
    6.7329, 2.7713, -2.2885, 0.4971, -0.725, 0.045, 0.0066, 0.3222, 0.012,
    22.7, 2.0813, 3.0, 8.3659, -3.3428, 1.3236, 6.2437, 2.3893, 0.3249, 4.159,
    1.693 ]
  if type == 'CMOD5':
    c = cmod5
  elif type == 'CMOD5N':
    c = cmod5n

  thetm = 40.0
  thethr = 25.0
  zpow = 1.6

  y0 = c[19]
  n = c[20]
  a = y0 - (y0 - 1)/n
  b = 1 / (n * np.power(y0 -1, n -1))

  cosPhi = np.cos(np.radians(phi))
  x = (theta - thetm)/thethr
  xx = x*x
  a0 = c[1] + c[2]*x + c[3]*xx + c[4]*xx*x
  a1 = c[5] + c[6]*x
  a2 = c[7] + c[8]*x
  gamma = c[9] + c[10]*x + c[11]*xx
  s0 = c[12] + c[13]*x
  s = a2*v
  a3 = 1.0 / (1.0 + np.exp(-np.maximum(s, s0)))
  if [s < s0]:
    a3 = a3*np.power((s/s0), s0*(1.0 - a3))

  b0 = np.power(a3, gamma)*np.power(10.0, a0 + a1*v)
  b1 = c[15]*v*(0.5 + x - np.tanh(4.0*(x+c[16]+c[17]*v)))
  b1 = (c[14]*(1.0 + x) - b1)/(np.exp(0.34*(v-c[18])) + 1)
  v0 = c[21] + c[22]*x + c[23]*xx
  d1 = c[24] + c[25]*x + c[26]*xx
  d2 = c[27] + c[28]*x
  v2 = v/v0 + 1.0
  if [v2 < y0]:
    v2 = a + b*np.power(v2 - 1.0, n)
  b2 = (-d1 + d2*v2)*np.exp(-v2)

  return b0*np.power(1.0 + b1*cosPhi + b2*(2.0*cosPhi*cosPhi - 1.0), zpow)


def cmod5_forward(sigmaFile, incidFile, type, outFile):

  print('Reading sigma0 and incidence angle files ...')
  (sigma0_vv, geoTrans, proj, epsg, dtype, noData) = geotiff2data(sigmaFile)
  sigma0_vv[sigma0_vv<0.0001] = 0.0001
  (theta, geoTrans, proj, epsg, dtype, noData) = geotiff2data(incidFile)
  windspeed = 10.0*np.ones_like(theta) # [m/s]
  phi = 45.0*np.ones_like(theta) # [degrees]

  print('Calculating normalized radar cross section ...')
  ncrs = calcNRCS(windspeed, phi, theta, type)

  print('Calculating normalized backscatter ...')
  normalized_backscatter = sigma0_vv/ncrs

  print('Writing to GeoTIFF file ({0})'.format(os.path.basename(outFile)))
  data2geotiff(normalized_backscatter, geoTrans, proj, dtype, noData, outFile)


def cmod5_inverse(sigmaFile, incidFile, type, outFile):

  print('Reading sigma0 and incidence angle files ...')
  (sigma0_obs, geoTrans, proj, epsg, dtype, noData) = geotiff2data(sigmaFile)
  sigma0_obs[sigma0_obs<0.0001] = 0.0001
  (theta, geoTrans, proj, epsg, dtype, noData) = geotiff2data(incidFile)

  print('Calculating windspeed ...')
  windspeed = 10.0*np.ones_like(theta) # [m/s]
  phi = 45.0*np.ones_like(theta) # [degrees]
  step = 10.0
  iterations = 10

  for ii in range(iterations):
    print('Iteration {0} ...'.format(ii+1))
    sigma0_calc = calcNRCS(windspeed, phi, theta, type)
    ind = sigma0_calc - sigma0_obs > 0
    windspeed += step
    windspeed[ind] -= 2*step
    step /= 2

  print('Writing to GeoTIFF file ({0})'.format(os.path.basename(outFile)))
  data2geotiff(windspeed, geoTrans, proj, dtype, noData, outFile)


if __name__ == '__main__':

  parser = argparse.ArgumentParser(prog='windspeed',
    description='Conversion using the CMOD5(N)')
  parser.add_argument('sigmaFile', help='name of the sigma VV file')
  parser.add_argument('incidFile', help='name of the incidence file')
  parser.add_argument('dir', help='direction of the transformation: forward, '\
    'inverse')
  parser.add_argument('type', help='model type: CMOD5, CMOD5N')
  parser.add_argument('outFile', help='name of the output file')
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  args = parser.parse_args()
  type = args.type.upper()

  if args.dir.upper() == 'FORWARD':
    cmod5_forward(args.sigmaFile, args.incidFile, type, args.outFile)
  elif args.dir.upper() == 'INVERSE':
    cmod5_inverse(args.sigmaFile, args.incidFile, type, args.outFile)
