'''
Input Params: Data file name, histogram, thresholds, offset
Output Params: Result File name
File Description: otsuThreshold
Ex Input: otsuThreshold.py 1000_3.nii.gz 1000_3_otsuThreshold.nii.gz 10 2 2
'''

import sys
import itk

def arg_func(args):
    #Make sure input is selected
    if len(args) != 6:
        print("Usage: " + args[0] + " <inputImage> <outputImage> "
              "<numberOfHistogramBins> <numberOfThresholds> <labelOffset>")
        sys.exit(1)

    #Inputting the variables
    inputImage = "../data/input/" + args[1]
    outputImage = "../data/results/" + args[2]
    numberOfHistogramBins = int(args[3])
    numberOfThresholds = int(args[4])
    labelOffset = int(args[5])

    #set up a reader
    reader = itk.ImageFileReader.New(FileName=inputImage)

    #Create otsu filter
    otsuFilter = itk.OtsuMultipleThresholdsImageFilter.New(Input=reader.GetOutput(),
                                                           NumberOfHistogramBins=numberOfHistogramBins,
                                                           NumberOfThresholds=numberOfThresholds,
                                                           LabelOffset=labelOffset)

    rescaleFilter = itk.RescaleIntensityImageFilter.New(Input=otsuFilter.GetOutput(),
                                                        OutputMinimum=0,
                                                        OutputMaximum=255)

    #Write the file to an output image
    writer = itk.ImageFileWriter.New(FileName=outputImage, Input=rescaleFilter.GetOutput())

    #Actually write out the file
    writer.Update()

if __name__ == '__main__':
    arg_func(sys.argv)
