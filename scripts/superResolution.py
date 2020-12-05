'''
Input Params: Data file name
Output Params: Result File name
File Description: MRI Super Resolution
Ex Input: superResolution.py 1000_3.nii.gz 1000_3_superResolution.nii.gz
'''

import sys
import ants
import antspynet

#Make sure input is selected
if len(sys.argv) != 3:
    print("Usage: " + sys.argv[0] + " <inputImage> <OutputImage>")
    sys.exit(1)

inputImage = "../data/input/" + sys.argv[1]
outputImage = "../data/results/" + sys.argv[2]

image = ants.image_read(inputImage)
superRes = antspynet.utilities.mri_super_resolution(image)
ants.image_write(superRes, outputImage)

