'''
Input Params: Data file name, lower Threshold, upper Threshold, outside Value, inside Value
Output Params: Result File name
File Description: Code has been modularized to be data type agnostic wherein the file name will be threshold according to input parameters 
Ex Input: binaryThreshold.py 1000_3.nii.gz 1000_3_threshold.nii.gz 600 1500 0 1
'''

import sys
import itk

def arg_func(): 
    #Make sure input is selected
    if len(sys.argv) != 7:
        print("Usage: " + sys.argv[0] + " <inputImage> <outputImage> "
            "<lowerThreshold> <upperThreshold> <outsideValue> <insideValue>")
        sys.exit(1)

    #Inputting the variables
    inputImage = "../data/input/" + sys.argv[1]
    outputImage = "../data/results/" + sys.argv[2]
    lowerThreshold = int(sys.argv[3])
    upperThreshold = int(sys.argv[4])
    outsideValue = int(sys.argv[5])
    insideValue = int(sys.argv[6])

    #set up a reader
    reader = itk.ImageFileReader.New(FileName=inputImage)

    #Create threshold filter
    thresholdFilter = itk.BinaryThresholdImageFilter.New(Input=reader.GetOutput(),
                                                        LowerThreshold=lowerThreshold,
                                                        UpperThreshold=upperThreshold,
                                                        OutsideValue=outsideValue,
                                                        InsideValue=insideValue)

    #Write the file to an output image
    writer = itk.ImageFileWriter.New(FileName=outputImage, Input=thresholdFilter.GetOutput())

    #Actually write out the file
    writer.Update()

if __name__ == '__main__':
    arg_func()
