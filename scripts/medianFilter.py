'''
Input Params: Data file name, lower Threshold, upper Threshold, outside Value, inside Value
Output Params: Result File name
File Description: Median Filter on input image with given radius
Ex Input: medianFilter.py 1000_3.nii.gz 1000_3_medianFilter.nii.gz 5
'''

import sys
import itk

#Make sure input is selected
if len(sys.argv) != 4:
    print("Usage: " + sys.argv[0] + " <inputImage> <outputImage> <radius>")
    sys.exit(1)

#Inputting the variables
inputImage = "../data/input/" + sys.argv[1]
outputImage = "../data/results/" + sys.argv[2]
radius = int(sys.argv[3])

#set up a reader
reader = itk.ImageFileReader.New(FileName=inputImage)

#Create median filter and perform filtering
medianFilter = itk.MedianImageFilter.New(Input=reader.GetOutput())
medianFilter.SetRadius(radius)

#Write the file to an output image
writer = itk.ImageFileWriter.New(FileName=outputImage, Input=medianFilter.GetOutput())

#Actually write out the file
writer.Update()