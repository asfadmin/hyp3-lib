import os
from execute import execute

def reproject(in_image, out_image, epsg):
    if not ('.png' in out_image or '.tif' in out_image):
        print(out_image)
        raise Exception("JPG not yet implemented for Mercator browses")

    try:
        reprojection_cmd = "gdalwarp -t_srs EPSG:{0} {1} {2}".format(epsg, in_image, out_image)
        print("")
        execute(reprojection_cmd)

        return True
    except Exception as e:
        print('Geocoded browse generation failed.')
        print(e)

        return False
