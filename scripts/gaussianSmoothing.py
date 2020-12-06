'''
Input Params: Data file name, sigma
Output Params: Result File name
File Description: Gaussian Smoothing on input image with given sigma
Ex Input: gaussianSmoothing.py 1000_3.nii.gz 1000_3_gaussianSmoothing.nii.gz 2.5
'''

import sys
import itk

def arg_func(args):
    #Make sure input is selected
    if len(args) != 4:
        print("Usage: " + args[0] + " <inputImage> <outputImage> <sigma>")
        sys.exit(1)

    #Inputting the variables
    inputImage = args[1]
    outputImage = args[2]
    sigma = float(args[3])

    #set up a reader
    reader = itk.ImageFileReader.New(FileName=inputImage)

    #Create gaussian filter and perform filtering
    smoothFilter = itk.SmoothingRecursiveGaussianImageFilter.New(Input=reader.GetOutput(), Sigma=sigma)

    #Write the file to an output image
    writer = itk.ImageFileWriter.New(FileName=outputImage, Input=smoothFilter.GetOutput())

    #Actually write out the file
    writer.Update()

if __name__ == '__main__':
    arg_func(sys.argv)
