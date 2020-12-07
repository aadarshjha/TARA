'''
Input Params: Data file name
Output Params: Result File name
File Description: Generate probabilistic map using ants
Ex Input: brainExtraction.py SubjectA_T1.nrrd SubjectA_T1_brainExtraction.nrrd
'''

import sys
import ants
import antspynet

def arg_func(args):
    #Make sure input is selected
    if len(args) != 3:
        print("Usage: " + args[0] + " <inputImage> <outputImage>")
        sys.exit(1)

    inputImage = args[1]
    outputImage = args[2]

    brain_image = ants.image_read(inputImage)
    probability_brain_mask = antspynet.utilities.brain_extraction(brain_image, modality="t1")
    ants.image_write(probability_brain_mask,outputImage)

if __name__ == '__main__':
    arg_func(sys.argv)
