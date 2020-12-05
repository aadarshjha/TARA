'''
Input Params: Data file name
Output Params: Result File name
File Description: Perform Atropos-style six tissue segmentation using deep learning.
Ex Input: brainExtraction.py SubjectA_T1.nrrd SubjectA_T1_deepAtroposSegmentation.nrrd
SubjectA_T1_deepAtroposBackground.nrrd SubjectA_T1_deepAtroposCSF.nrrd SubjectA_T1_deepAtroposGM.nrrd
SubjectA_T1_deepAtroposWM.nrrd SubjectA_T1_deepAtroposDeepGM.nrrd SubjectA_T1_deepAtroposBrainStem.nrrd
SubjectA_T1_deepAtroposCerebellum.nrrd
'''

import sys
import ants
import antspynet

#Make sure input is selected
if len(sys.argv) != 10:
    print("Usage: " + sys.argv[0] + " <inputImage> <Segmentation>"
          "<BackgroundOutput> <CSFOutput> <GMOutput> <WMOutput> <DeepGMOutput> <BrainStem> <Cerebellum>")
    sys.exit(1)

inputImage = "../data/input/" + sys.argv[1]
segmentationOutput = "../data/results/" + sys.argv[2]
BackgroundOutput = "../data/results/" + sys.argv[3]
CSFOutput = "../data/results/" + sys.argv[4]
GMOutput = "../data/results/" + sys.argv[5]
WMOutput = "../data/results/" + sys.argv[6]
DeepGMOutput = "../data/results/" + sys.argv[7]
BrainStemOutput = "../data/results/" + sys.argv[8]
CerebellumOutput = "../data/results/" + sys.argv[9]

image = ants.image_read(inputImage)
flash = antspynet.utilities.deep_atropos(image, do_preprocessing=True, verbose=True)
ants.image_write(flash['segmentation_image'], segmentationOutput)
probability = flash['probability_images']
ants.image_write(probability[0], BackgroundOutput)
ants.image_write(probability[1], CSFOutput)
ants.image_write(probability[2], GMOutput)
ants.image_write(probability[3], WMOutput)
ants.image_write(probability[4], DeepGMOutput)
ants.image_write(probability[5], BrainStemOutput)
ants.image_write(probability[6], CerebellumOutput)
