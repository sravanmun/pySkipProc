#!/usr/local/bin/python3
import sys, getopt

from skp2avg import rawFits2procHDUL
try:
    from skp2root import hdul2Root
except:
    pass


def main():
    # check to see if the options and arguments are correct format
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help', 'rms', 'avg', 'noroot' 'outfile='])
        if len(args) == 0: raise Exception("Expecting fits file as argument")
        for a in args:
            if not a.split('.')[-1] in ('fits', 'fz'): raise Exception("Expecting fits file as argument")
    except Exception as e: 
        usage(e)
    
    # get options
    print_avg, print_rms, print_root, root_file_name = False, False, True, False
    for o, a in opts:
        if o in ("-h", "--help"): usage()
        if o=="--avg": print_avg = True
        if o=="--rms": print_rms = True
        if o=="--noroot":  print_root = False
        if o=="--outfile": root_file_name = a


    # iterate through all the input fits files
    for raw_file in args:
        # get the average and rms HDUList
        avg_hdul, rms_hdul = rawFits2procHDUL(raw_file)

        # save the average fits file
        if print_avg:
            avg_file = new_name(raw_file, "avg")
            print("saving average data to {0}".format(avg_file))
            avg_hdul.writeto(avg_file)

        # save the rms fits file
        if print_rms:
            rms_file = new_name(raw_file, "rms")
            print("saving rms data to {0}".format(raw_file))
            avg_hdul.writeto(rms_file)

        # save data to a root file
        if print_root:
            if not root_file_name:
                root_file_name = change_ext(raw_file, 'root')
            print("saving data to root file called {0}".format(raw_file))
            try:
                hdul2Root(root_file_name, avg_hdul, raw_hdul)
            except:
                print("Error: Cannot save file to root. pyRoot is probably not installed properly")

    return 0


def new_name(name, suffix):
    """ Change file name from name.fits -> name_suffix.fits """
    name_split = name.split('.')
    new_name = name_split[0] + '_' + suffix + '.' + name_split[-1]

    return new_name


def change_ext(name, ext):
    name_split = name.split('.')
    name_split.pop()
    name_split.append(ext)

    return '.'.join(name_split)


def usage(error=""):
    """ Print Error Message and Proper way of using code """
    if error: print("Error: {0}".format(error))

    out = """
    This script takes a raw skipper fits file. 
    It calculates the average and rms value of each pixel and saves it to a root Tree.
    Optionally, we can produce a average and rms compressed fits (fz) files.

    Options to do more stuff
    ========================
        ./{0} --opt1 --opt2 -o  --opt3=arg <fits_file1> <fits_file2> .... <fits_filen>
            <fits_filei> = a *.fits or *.fz files
                          need atleast 1 fits files, can input as many fits files as you want
        Options:
            -h, --help   : tells user how to use function
            --avg        : geneartes an average fits file
            --rms        : generates an rms fits
            --nroot      : do not generate a root file
            --outfile    : specify a root file name. Default name is the same as the gi

    """.format(sys.argv[0])
    
    print(out)
    sys.exit()


if __name__=="__main__":
    main()

