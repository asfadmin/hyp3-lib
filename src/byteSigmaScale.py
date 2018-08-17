#!/usr/bin/python

import argparse
import saa_func_lib as saa
import numpy as np
from osgeo import gdal

def get2sigmacutoffs(fi):
    (x,y,trans,proj,data) = saa.read_gdal_file(saa.open_gdal_file(fi))
    top = np.percentile(data,99)
    data[data>top]=top
    data[data==0]=np.nan
    stddev = np.nanstd(data)
    mean = np.nanmean(data)
    lo = mean - 2*stddev
    hi = mean + 2*stddev
    return lo,hi

def byteSigmaScale(infile,outfile):
    lo,hi = get2sigmacutoffs(infile)
    print "2-sigma cutoffs are {} {}".format(lo,hi)
    gdal.Translate(outfile,infile,outputType=gdal.GDT_Byte,scaleParams=[[lo,hi,1,255]],resampleAlg="average",noData="0")

    # For some reason, I'm still getting zeros in my byte images eventhough I'm using 1,255 scaling!
    # The following in an attempt to fix that!
    (x,y,trans,proj,data) = saa.read_gdal_file(saa.open_gdal_file(infile))
    mask = (data>0).astype(int)
    (x,y,trans,proj,data) = saa.read_gdal_file(saa.open_gdal_file(outfile))
    mask2 = (data>0).astype(int)
    mask3 = mask ^ mask2
    data = data + mask3
    saa.write_gdal_file_float(outfile,trans,proj,data,nodata=0) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a floating point tiff into a byte tiff using 2-sigma scaling.")
    parser.add_argument("infile",help="Geotiff file to convert")
    parser.add_argument("outfile",help="Name of output file to create")
    args = parser.parse_args()
    byteSigmaScale(args.infile,args.outfile)
    
 
