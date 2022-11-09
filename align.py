"""
    
""" 

from astropy.io import fits
from astropy.wcs import WCS
from reproject import reproject_adaptive
import numpy as np
import sys


# this function assumes that file1 has size greater than or equal to file2
def reproject(file1, file2):
    print('reprojecting ', file1, file2)
    hdul1 = fits.open(file1)
    hdul2 = fits.open(file2)

    data1 = hdul1['SCI'].data
    wcs1 = WCS(hdul1['SCI'].header)
    wcs2 = WCS(hdul2['Primary'].header)
    cols = hdul2['Primary'].header['NAXIS1']
    rows = hdul2['Primary'].header['NAXIS2']

    result_gaussian, _ = reproject_adaptive((data1, wcs1),
                                            wcs2, shape_out=(rows, cols),
                                            kernel='gaussian')

    filename = file1.split('.')
    filename[0] += '_match'
    fits.writeto('.'.join(filename), result_gaussian, hdul2['Primary'].header, overwrite=True)

    hdul1.close()
    hdul2.close()
    print('done')



cosmic_cliffs = [ 
    'jw02731-o001_t017_nircam_clear-f090w_i2d.fits', 
    'jw02731-o001_t017_nircam_clear-f187n_i2d.fits',
    'jw02731-o001_t017_nircam_clear-f200w_i2d.fits',
    'jw02731-o001_t017_nircam_clear-f335m_i2d.fits',
    'jw02731-o001_t017_nircam_clear-f444w_i2d.fits',
    'jw02731-o001_t017_nircam_f444w-f470n_i2d.fits'
]

cosmic_files = ['cosmic_cliffs/' + file for file in cosmic_cliffs]

southern_ring = [
    'jw02733-o001_t001_nircam_clear-f090w_i2d.fits',
    'jw02733-o001_t001_nircam_clear-f187n_i2d.fits',
    'jw02733-o001_t001_nircam_clear-f212n_i2d.fits',
    'jw02733-o001_t001_nircam_clear-f356w_i2d.fits',
    'jw02733-o001_t001_nircam_f405n-f444w_i2d.fits',
    'jw02733-o001_t001_nircam_f444w-f470n_i2d.fits'
]

southern_ring = ['southern_ring/' + file for file in southern_ring]


basefile = 'southern_ring/jw02733-o001_t001_nircam_f444w-f470n_i2d.fits'

desired_rows = 1170
desired_cols = 1977

for file in southern_ring:
    reproject(file, basefile)

