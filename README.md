# Skipper CCD fits (fz) Processor
This code will take a raw fits (fz) file from the LTA or LEACH DAQ systems and calculate the average and rms (standard deviation) of each pixel. This information can then be saved to either two fits files or to the a root file.

This script takes a raw skipper fits file. 
It calculates the average and rms value of each pixel and saves it to a root Tree.
Optionally, we can produce a average and rms compressed fits (fz) files.

Options to do more stuff
```shell
    ./procSkip --opt1 --opt2 -o  --opt3=arg <fits_file1> <fits_file2> .... <fits_filen>
        <fits_filei> = a *.fits or *.fz files
                      need atleast 1 fits files, can input as many fits files as you want
    Options:
        -h, --help   : tells user how to use function
        --avg        : geneartes an average fits file
        --rms        : generates an rms fits
        --nroot      : do not generate a root file
        --outfile    : specify a root file name. Default name is the same as the 
```

# Examples on how to use script
To save data to a root file only.
```shell
./procSkip.py path/to/file/file1.fz
```

To save data as average and rms fits files and not a root file
```shell
./procSkip.py --avg --rms --noroot path/to/file/file1.fz
```

Specify the output root file name. ( Default name is the input file name with the extention replaced to root.)
```shell
./procSkip.py --outfile=name_you_want.root /path/to/file/file1.fz
```
