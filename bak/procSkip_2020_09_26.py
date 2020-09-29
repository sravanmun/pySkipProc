#!/usr/local/bin/python3
import sys, getopt
import numpy as np
from astropy.io import fits


def main():
    # check to see if the options and arguments are correct format
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help', 'rms', 'avg'])
        if len(args) == 0: raise Exception("Expecting fits file as argument")
        for a in args:
            if not a.split('.')[-1] in ('fits', 'fz'): raise Exception("Expecting fits file as argument")
    except Exception as e: 
        usage(e)
    
    # get options
    print_avg, print_rms = False, False 
    for o, a in opts:
        if o in ("-h", "--help"): usage()
        if o=="--avg": print_avg = True
        if o=="--rms": print_rms = True


    for raw_file in args:
        with fits.open(raw_file) as raw_hdul:
            avg_hdul, rms_hdul = procHDUL(raw_hdul)

        if print_avg:
            print(avg_hdul)
            avg_file = new_name(raw_file, "avg")
            avg_hdul.writeto(avg_file)

        if print_rms:
            rms_file = new_name(raw_file, "rms")
            avg_hdul.writeto(rms_file)

    return 0


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


def new_name(name, suffix):
    """ Change file name from name.fits -> name_suffix.fits """
    name_split = name.split('.')
    new_name = name_split[0] + '_' + suffix + '.' + name_split[-1]
    return new_name


def usage(error=""):
    """ Print Error Message and Proper way of using code """
    if error: print("Error: {0}".format(error))

    out = """
    This script takes a raw skipper fits file and generates an average and rms files.
    
    Options to do more stuff
    ========================
        ./{0} --opt1 --opt2 -o  --opt3=arg <fits>
    or
        ./{0} <fits> --opt1 --opt2 -o --opt3=arg
            <fits> = a *.fits or *.fz files
        Options:
            -h, --help   : tells user how to use function
            --avg        : geneartes an average fits file
            --rms        : generates an rms fits
    """.format(sys.argv[0])
    
    print(out)
    sys.exit()


if __name__=="__main__":
    main()

