import sys
import numpy as np
from array import array

from astropy.io import fits

import ROOT

from skp2avg import procHDUL, getProcHeaderVals


def main():
	""" Place fits info into a root Tree """
	raw_file = sys.argv[1]
	with fits.open(raw_file) as raw_hdul:
		#avg_hdul, rms_hdul = procHDUL(raw_hdul)

		aTree = fitsHeader2Tree(raw_hdul)
		#root_file = ROOT.TFile('root_example.root', 'examp')
		#aTree = fitsImage2Tree(avg_hdul, rms_hdul)




def fitsHeader2Tree(hdul):
	""" Place header information in ROOT TTree"""
	# Define Header Tree
	headTree = ROOT.TTree("header", "header")

	#val = array('c', 'N') # B is unsigned char and b is signed char
	#val = np.array('bye', dtype=str)

	"""
	char_array = array('B') #bytearray(21)
	char_array.frombytes('happybirthday'.encode())
	print(char_array)
	print( len(char_array))

	headTree.Branch('char_array', char_array.tobytes(), 'char_array/C') # C is chararacter in ROOT_C++
	headTree.Fill()
	"""

	
	for hdu in hdul:
		if hdu.data is None: continue

		strings = ROOT.vector('string')()
		
		# sring addresses to put into branches
		key_address = bytearray(21)
		val_address = bytearray(21)

		# Branches
		headTree.Branch('key_address', key_address, "key_address[21]/C")
		headTree.Branch('val_address', val_address, "val_address[21]/C")

		for key, val in hdu.header.items():

			# place key and val values in address
			key_address[:21] = key.ljust(20).encode()
			val_address[:21] = str(val).ljust(20).encode()

			#print(key_address, '->', val_address)
			headTree.Fill()

			# place the values in the Tree

			"""
			del val[:] #clear the byte array
			val2 = hdu.header[key]
			val.frombytes( str(val2).encode()  )
			headTree.Branch(key, val.tobytes(), "key/C")
			headTree.Fill()
			"""
			#add2Head(headTree, key, val)
			#headTree.Fill()
		break
	headTree.Scan()
	return headTree


def add2Head(tree, branchname, val):
	val_address = array('B', val.encode()) # intitialize byte array

	tree.Branch(branchname, val_address.tobytes(), branchname+'/C')
	
	return 0 






def fitsImage2Tree(avg_hdul, rms_hdul):
	""" Place averaged and rms HDUList pixel values into a ROOT TTree"""
	# Define Tree
	skpTree = ROOT.TTree("skpTree", "skpTree")

	# Dfine variables that will go into Branches
	row    = array('I',[0])    # row
	col    = array('I',[0])    # col
	ohdu = array('I',[0])    # quadrant
	pix  = array('f',[0])    # average pixel value
	rms  = array('f',[0])    # standard deviation in pixel value

	# Generate branches for Tree
	skpTree.Branch("row", row, "row/I")
	skpTree.Branch("col", col, "col/I")
	skpTree.Branch("ohdu", ohdu, "ohdu/I")
	skpTree.Branch("pix", pix, "pix/F")
	skpTree.Branch("rms", rms, "rms/F")


	# Iterate through HDUList (different quadratns of LTA)
	for quad, (avg_hdu, rms_hdu) in enumerate(zip(avg_hdul, rms_hdul)):
		if avg_hdu.data is None: continue # Primary unit has no information

		# get the number of rows and columns in the image
		nrow, ncol, _ = getProcHeaderVals(avg_hdu.header)

		for x in range(ncol):
			for y in range(nrow):
				
				row[0] = x
				col[0] = y
				ohdu[0] = quad
				pix[0] = avg_hdu.data[y, x]
				rms[0] = rms_hdu.data[y, x]

				# Fill the branch with the values defined in the 3 for loops
				skpTree.Fill()

	return skpTree

main()