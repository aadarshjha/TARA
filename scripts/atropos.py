'''
Input Params: Data file name
Output Params: Result File name
File Description: atropos three tissue segmentation using deep learning.
Ex Input: atropos.py SubjectA_T1.nrrd SubjectA_T1_atroposSegmentation.nrrd SubjectA_T1_atroposCSF.nrrd
SubjectA_T1_atroposGM.nrrd SubjectA_T1_atroposWM.nrrd
'''

import sys
import ants

#Make sure input is selected
if len(sys.argv) != 6:
    print("Usage: " + sys.argv[0] + " <inputImage> <outputImage> <outputImage> <outputImage> <outputImage>")
    sys.exit(1)

inputImage = "../data/input/" + sys.argv[1]
segmentationOutput = "../data/results/" + sys.argv[2]
CSFOutput = "../data/results/" + sys.argv[3]
GMOutput = "../data/results/" + sys.argv[4]
WMOutput = "../data/results/" + sys.argv[5]

img = ants.image_read(inputImage)
mask = ants.get_mask(img)
flash = ants.atropos(a = img, x = mask, i='Kmeans[3]', m='[0.3, 1x1x1]')
ants.image_write(flash['segmentation'], segmentationOutput)
probability = flash['probabilityimages']
ants.image_write(probability[0], CSFOutput)
ants.image_write(probability[1], GMOutput)
ants.image_write(probability[2], WMOutput)
