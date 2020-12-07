'''
Input Params: Data file name, lower Threshold, upper Threshold, outside Value, inside Value
Output Params: Result File name
File Description: Code has been modularized to be data type agnostic wherein the file name will be threshold according to input parameters 
Ex Input: binaryThreshold.py 1000_3.nii.gz 1000_3_threshold.nii.gz 600 1500 0 1
'''

import sys
import itk

def arg_func(args): 
    #Make sure input is selected
    if len(args) != 7:
        print("Usage: " + args[0] + " <inputImage> <outputImage> " + 
            "<lowerThreshold> <upperThreshold> <outsideValue> <insideValue>")
        sys.exit(1)

    #Inputting the variables
    # inputImage = "../data/input/" + args[1]
    # outputImage = "../data/results/" + args[2]

    inputImage = args[1]
    outputImage =  args[2]

    lowerThreshold = int(args[3])
    upperThreshold = int(args[4])
    outsideValue = int(args[5])
    insideValue = int(args[6])

    print("HELLLO")
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
    arg_func(sys.argv)
