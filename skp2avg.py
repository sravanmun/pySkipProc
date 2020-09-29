#!/usr/local/bin/python3
import numpy as np
from astropy.io import fits



def rawFits2procHDUL(raw_fits_file):
    """ Given a raw fits file, Return an RMS and AVG HDUList """
    with fits.open(raw_file) as raw_hdul:
        avg_hdul, rms_hdul = procHDUL(raw_hdul)

    return avg_hdul, rms_hdul


def procHDUL(raw_hdul):
    """ Process a HDUList of raw Skipper images into and average and rms HDUList """
    # Initalize the processed hdulist
    avg_hdul = fits.HDUList()
    rms_hdul = fits.HDUList()
    
    # Iterate through different headers (quadrants)
    for raw_hdu in raw_hdul:
        if raw_hdu.data is None: continue # if the header file is empty, do nothing
        
        # Get number of rows, columns samples for LTA or LEACH automatically
        nrow, ncol, N = getProcHeaderVals(raw_hdu.header)
        
        # define processed hdu with all values of data zero, and same header
        avg_hdu = fits.CompImageHDU(data=np.zeros((nrow, ncol)) ,header=raw_hdu.header)
        rms_hdu = fits.CompImageHDU(data=np.zeros((nrow, ncol)) ,header=raw_hdu.header)
        
        # Iterate through elements of newly defined images
        for row in range(nrow):
            for col in range(ncol):
                # Caluclate average pixel value and rms pixel value
                avg_hdu.data[row, col] = raw_hdu.data[row, N*col:N*col+N].mean()
                rms_hdu.data[row, col] = raw_hdu.data[row, N*col:N*col+N].std()

        # avg_hdu = fits.CompImageHDU(data=avg_image)
        avg_hdul.append(avg_hdu)
        rms_hdul.append(rms_hdu)


    return avg_hdul, rms_hdul 


def getProcHeaderVals(hdr):
    """ Input header of Leach of LTA. return nrow, ncol, nsamp"""
    
    if 'NROW' in hdr.keys(): # means that it is LTA
        nrow = int(hdr['NROW'])
        ncol = int(hdr['NCOL'])
        nsamp =    int(hdr['NSAMP'])
    elif 'NAXIS1' in hdr.keys():
        nrow = int(hdr['NAXIS2'])
        ncol = int(hdr['NAXIS1']/hdr['NDCMS'])
        nsamp = int(hdr['NDCMS'])

    return nrow, ncol, nsamp
