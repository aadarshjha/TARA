'''
Input Params: Data file name, variance, lowerThreshold, upperThreshold
Output Params: Result File name
File Description: canny Edge Detection (Not setup for wrapper function, so must give dimension 3 image)
Ex Input: cannyEdgeDetection.py 1000_3.nii.gz 1000_3_cannyEdgeDetection.nii.gz 0.5 50 200
'''

import sys
import itk

def arg_func(args):
    #Make sure input is selected
    if len(args) != 6:
        print("Usage: " + args[0] + " <InputImage> <OutputImage> "
              "<Variance> <LowerThreshold> <UpperThreshold>")
        sys.exit(1)

    #Inputting the variables
    inputImage = args[1]
    outputImage = args[2]
    variance = float(args[3])
    lowerThreshold = float(args[4])
    upperThreshold = float(args[5])

    InputPixelType = itk.F
    OutputPixelType = itk.UC
    Dimension = 3

    InputImageType = itk.Image[InputPixelType, Dimension]
    OutputImageType = itk.Image[OutputPixelType, Dimension]

    reader = itk.ImageFileReader[InputImageType].New()
    reader.SetFileName(inputImage)

    cannyFilter = itk.CannyEdgeDetectionImageFilter[
        InputImageType,
        InputImageType].New()
    cannyFilter.SetInput(reader.GetOutput())
    cannyFilter.SetVariance(variance)
    cannyFilter.SetLowerThreshold(lowerThreshold)
    cannyFilter.SetUpperThreshold(upperThreshold)

    rescaler = itk.RescaleIntensityImageFilter[
        InputImageType,
        OutputImageType].New()
    rescaler.SetInput(cannyFilter.GetOutput())
    rescaler.SetOutputMinimum(0)
    rescaler.SetOutputMaximum(255)

    writer = itk.ImageFileWriter[OutputImageType].New()
    writer.SetFileName(outputImage)
    writer.SetInput(rescaler.GetOutput())

    writer.Update()

if __name__ == '__main__':
    arg_func(sys.argv)
