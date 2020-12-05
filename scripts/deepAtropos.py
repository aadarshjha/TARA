'''
Input Params: Data file name
Output Params: Result File name
File Description: Perform Atropos-style six tissue segmentation using deep learning.
Ex Input: brainExtraction.py SubjectA_T1.nrrd SubjectA_T1_atropos.nrrd
'''

import sys
import ants
import antspynet

#Make sure input is selected
if len(sys.argv) != 3:
    print("Usage: " + sys.argv[0] + " <inputImage> <outputImage>")
    sys.exit(1)

inputImage = "../data/input/" + sys.argv[1]
outputImage = "../data/results/" + sys.argv[2]

image = ants.image_read(inputImage)
#preprocessed_image = antspynet.utilities.preprocess_brain_image(image, do_brain_extraction=False)
flash = antspynet.utilities.deep_atropos(image, do_preprocessing=True, verbose=True)
ants.image_write(flash, outputImage)
