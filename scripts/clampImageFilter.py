'''
Input Params: Data file name, lowerBound, upperBound
Output Params: Result File name
File Description: Used to rescale the output image to meet a certain bounds
Ex Input: clampImageFilter.py 1000_3_gaussianSmoothing.nii.gz 1000_3_gaussianSmoothing_clamped.nii.gz 0 5000
'''

import sys
import itk

def arg_func(args):
    #Make sure input is selected
    if len(sys.argv) != 5:
        print("Usage: " + sys.argv[0] + " <inputImage> <outputImage> <lowerBoundOutput> <UpperBoundOutput")
        sys.exit(1)

    #Inputting the variables
    inputImage = "../data/results/" + sys.argv[1]
    outputImage = "../data/results/" + sys.argv[2]
    lowerBound = int(sys.argv[3])
    upperBound = int(sys.argv[4])

    #set up a reader
    reader = itk.ImageFileReader.New(FileName=inputImage)

    #Create clamp filter and perform filtering
    clampFilter = itk.ClampImageFilter.New(Input=reader.GetOutput(), Bounds=(lowerBound, upperBound))

    #Write the file to an output image
    writer = itk.ImageFileWriter.New(FileName=outputImage, Input=clampFilter.GetOutput())

    #Actually write out the file
    writer.Update()

if __name__ == '__main__':
    arg_func(sys.argv)
