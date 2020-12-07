'''
Input Params: Data file name
Output Params: Result File name
File Description: sobel Edge Detection (Not setup for wrapper function, so must give dimension 3 image)
Ex Input: sobelEdgeDetection.py 1000_3.nii.gz 1000_3_sobelEdgeDetection.nii.gz
'''

import sys
import itk

def arg_func(args):
    #Make sure input is selected
    if len(args) != 3:
        print("Usage: " + args[0] + " <inputImage> <outputImage> ")
        sys.exit(1)

    #Inputting the variables
    inputImage = args[1]
    outputImage = args[2]

    InputPixelType = itk.F
    OutputPixelType = itk.UC
    Dimension = 3

    InputImageType = itk.Image[InputPixelType, Dimension]
    OutputImageType = itk.Image[OutputPixelType, Dimension]

    reader = itk.ImageFileReader[InputImageType].New()
    reader.SetFileName(inputImage)

    sobelEdgeDetection = itk.SobelEdgeDetectionImageFilter[
        InputImageType,
        InputImageType].New()
    sobelEdgeDetection.SetInput(reader.GetOutput())

    rescaler = itk.RescaleIntensityImageFilter[
        InputImageType,
        OutputImageType].New()
    rescaler.SetInput(sobelEdgeDetection.GetOutput())
    rescaler.SetOutputMinimum(0)
    rescaler.SetOutputMaximum(255)

    writer = itk.ImageFileWriter[OutputImageType].New()
    writer.SetFileName(outputImage)
    writer.SetInput(rescaler.GetOutput())

    writer.Update()

if __name__ == '__main__':
    arg_func(sys.argv)
