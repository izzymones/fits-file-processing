from astropy.io import fits
from astropy.wcs import WCS
from reproject import reproject_adaptive
import numpy as np
import sys, math

"""
    Produce a new fits file whose size is a percent of original file
"""
def downsize(file, percent):

    hdul = fits.open(file)
    data = hdul['SCI'].data               # image data
    wcs = WCS(hdul['SCI'].header)         # world coordinate system for image
    cols = hdul['SCI'].header['NAXIS1']   # dimensions of image data array
    rows = hdul['SCI'].header['NAXIS2']

    # create a new world coordinate system for the new fits file
    newcols = math.floor(cols * percent) # new array dimensions
    newrows = math.floor(rows * percent)
    newwcs = wcs.deepcopy()              # start with a copy of the old wcs

    # crpix is the pixel position of the reference point crval  
    # we need to translate it to the new pixel grid
    newwcs.wcs.crpix = [ wcs.wcs.crpix[0] * newcols / cols, wcs.wcs.crpix[1] * newrows / rows ]

    # cdelt is the real world distance between pixels
    # we need to adjust it to the new grid
    newwcs.wcs.cdelt = [ wcs.wcs.cdelt[0] * cols / newcols, wcs.wcs.cdelt[1] * rows / newrows ]

    # finally set new size of the data array
    newwcs.array_shape = (newrows, newcols)

    # now we just do a check to see that the distance covered by both images is the same
    old_width = wcs.wcs.cdelt[0] * cols
    old_height = wcs.wcs.cdelt[1] * rows
    new_width = newwcs.wcs.cdelt[0] * newcols
    new_height = newwcs.wcs.cdelt[1] * newrows

    if (not old_width == new_width or not old_height == new_height):
        print('image distances do not match')
        quit()


    # finally we project the old data onto the new grid
    result_gaussian, _ = reproject_adaptive((data, wcs),
                                            newwcs, shape_out=(newrows, newcols),
                                            kernel='gaussian')

    fits.writeto('cc_basefile.fits', result_gaussian, newwcs.to_header(), overwrite=True)

    hdul.close()




basefile = 'cosmic_cliffs/jw02731-o001_t017_nircam_clear-f335m_i2d.fits'
    
downsize(basefile, 0.3)

