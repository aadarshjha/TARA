'''
Input Params: FixedImage, MovingImage, transform
Output Params: Result File name
File Description: Perform registration through ANTS
Ex Input: registration.py SubjectB_T1.nrrd SubjectA_T1.nrrd SubjectA2B_Syn.nii.gz Affine
'''

import sys
import ants

#Make sure input is selected
if len(sys.argv) != 5:
    print("Usage: " + sys.argv[0] + " <FixedImage> <MovingImage> <outputImage> <transform>")
    sys.exit(1)

fixedImage = "../data/input/" + sys.argv[1]
movingImage = "../data/input/" + sys.argv[2]
outputImage = "../data/results/" + sys.argv[3]
transform = sys.argv[4]

fixImg = ants.image_read(fixedImage)
movImg = ants.image_read(movingImage)
mytx = ants.registration(fixed=fixImg, moving=movImg, type_of_transform=transform)
ants.image_write(mytx['warpedmovout'], outputImage)
