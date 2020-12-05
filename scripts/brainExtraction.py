'''
Input Params: Data file name
Output Params: Result File name
File Description: Generate probabilistic map using ants
Ex Input: brainExtraction.py SubjectA_T1.nrrd SubjectA_T1_brainExtraction.nrrd
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

brain_image = ants.image_read(inputImage)
probability_brain_mask = antspynet.utilities.brain_extraction(brain_image, modality="t1")
ants.image_write(probability_brain_mask,outputImage)
