from astropy.io import fits
import sys

m74 = [
    'jw02107-o039_t018_miri_f1000w_i2d.fits',
    'jw02107-o039_t018_miri_f1130w_i2d.fits',
    'jw02107-o039_t018_miri_f2100w_i2d.fits',
    'jw02107-o039_t018_miri_f770w_i2d.fits'
]

m74_files = ['m74/' + file for file in m74]

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


"""
    This function opens a 2d fits image file that was downloaded from the MAST archive
    and pulls out the 'SCI' image and writes it to a new fits file.  The resulting file
    is much smaller than the original archive file.
"""
def pullSciImage(files):

    for file in files:
        print('processing ' + file)
        hdul = fits.open(file)

        # now lets get the main image data
        img_data = hdul['SCI'].data
        img_header = hdul['SCI'].header

        # now we'll create a new fits file with just the SCI image
        filename = file.split('.')
        filename[0] += '_sci'
        fits.writeto('.'.join(filename), img_data, img_header, overwrite=True)

        hdul.close()
        print('done')

# pullSciImage(cosmic_files)
# pullSciImage(m74_files)
pullSciImage(southern_ring)