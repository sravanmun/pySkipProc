#!/usr/local/bin/python3
from array import array
from astropy.io import fits
import ROOT

from skp2avg import getProcHeaderVals



def hdul2Root(out_file_name, avg_hdul, rms_hdul):
	""" Given a average and rms HDUList, producea  root file """
	# create a root file instance
	root_file = ROOT.TFile(out_file_name, "RECREATE")

	# generate a header Tree and average/rms tree
	header_tree = fitsHeader2Tree(raw_hdul)
	image_tree = fitsImage2Tree(avg_hdul, rms_hdul)

	# write the trees to the root file intance
	header_tree.Write()
	image_tree.Write()

	# save the rootfile
	out_file.Close()


def fitsHeader2Tree(hdul):
	""" Place header information in ROOT TTree"""
	# Define Header Tree
	tree = ROOT.TTree("header", "header")
	
	key_array = ROOT.vector('string')()
	val_array = ROOT.vector('string')()
	
	# Branches
	tree.Branch('key', key_array)
	tree.Branch('val', val_array)
	
	for hdu in hdul:
		if hdu.data is None:
			continue
		
		for key, val in hdu.header.items():
			key_array.push_back(key)
			val_array.push_back(str(val))

		break
	tree.Fill()
	return tree


def fitsImage2Tree(avg_hdul, rms_hdul):
	""" Place averaged and rms HDUList pixel values into a ROOT TTree"""
	# Define Tree
	tree = ROOT.TTree("skpTree", "skpTree")

	# Dfine variables that will go into Branches
	row    = array('I',[0])    # row
	col    = array('I',[0])    # col
	ohdu = array('I',[0])    # quadrant
	pix  = array('f',[0])    # average pixel value
	rms  = array('f',[0])    # standard deviation in pixel value

	# Generate branches for Tree
	tree.Branch("row", row, "row/I")
	tree.Branch("col", col, "col/I")
	tree.Branch("ohdu", ohdu, "ohdu/I")
	tree.Branch("pix", pix, "pix/F")
	tree.Branch("rms", rms, "rms/F")


	# Iterate through HDUList (different quadratns of LTA)
	for quad, (avg_hdu, rms_hdu) in enumerate(zip(avg_hdul, rms_hdul)):
		if avg_hdu.data is None: continue # Primary unit has no information

		# get the number of rows and columns in the image
		nrow, ncol, _ = getProcHeaderVals(avg_hdu.header)

		# iterate through rows
		for x in range(ncol):
			for y in range(nrow):
				
				# declare value to address
				row[0] = x
				col[0] = y
				ohdu[0] = quad
				pix[0] = avg_hdu.data[y, x]
				rms[0] = rms_hdu.data[y, x]

				# Fill the branch with the values defined in the 3 for loops
				tree.Fill()

	return tree
