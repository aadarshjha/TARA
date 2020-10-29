'''
Input Params: Data file name, lower Threshold, upper Threshold, outside Value, inside Value
Output Params: Result File name
File Description: Code has been modularized to be data type agnostic wherein the file name will be threshold according to input parameters 
Ex Input: binaryThreshold.py 1000_3.nii.gz 1000_3_threshold.nii.gz 600 1500 0 1
'''

import sys
import itk

if len(sys.argv) != 7:
    print("Usage: " + sys.argv[0] + " <inputImage> <outputImage> "
          "<lowerThreshold> <upperThreshold> <outsideValue> <insideValue>")
    sys.exit(1)

inputImage = "../data/input/" + sys.argv[1]
outputImage = "../data/results/" + sys.argv[2]
lowerThreshold = int(sys.argv[3])
upperThreshold = int(sys.argv[4])
outsideValue = int(sys.argv[5])
insideValue = int(sys.argv[6])

reader = itk.ImageFileReader.New(FileName=inputImage)

thresholdFilter = itk.BinaryThresholdImageFilter.New(Input=reader.GetOutput())

thresholdFilter.SetLowerThreshold(lowerThreshold)
thresholdFilter.SetUpperThreshold(upperThreshold)
thresholdFilter.SetOutsideValue(outsideValue)
thresholdFilter.SetInsideValue(insideValue)

writer = itk.ImageFileWriter.New(FileName=outputImage, Input=thresholdFilter.GetOutput())

writer.Update()



