'''
Input Params: FixedImage, MovingImage, transform
Output Params: Result File name
File Description: Perform registration through ANTS
Ex Input: registration.py SubjectB_T1.nrrd SubjectA_T1.nrrd SubjectA2B_Syn.nii.gz Affine
'''

import sys
import ants

def arg_func(args):
    #Make sure input is selected
    if len(args) != 5:
        print("Usage: " + args[0] + " <FixedImage> <MovingImage> <outputImage> <transform>")
        sys.exit(1)

    fixedImage = "../data/input/" + args[1]
    movingImage = "../data/input/" + args[2]
    outputImage = "../data/results/" + args[3]
    transform = args[4]

    fixImg = ants.image_read(fixedImage)
    movImg = ants.image_read(movingImage)
    mytx = ants.registration(fixed=fixImg, moving=movImg, type_of_transform=transform)
    ants.image_write(mytx['warpedmovout'], outputImage)

if __name__ == '__main__':
    arg_func(sys.argv)
