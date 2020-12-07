'''
Input Params: Data file name, radius
Output Params: Result File name
File Description: Median Filter on input image with given radius
Ex Input: medianFilter.py 1000_3.nii.gz 1000_3_medianFilter.nii.gz 5
'''

import sys
import itk

def arg_func(args):
    #Make sure input is selected
    if len(args) != 4:
        print("Usage: " + args[0] + " <inputImage> <outputImage> <radius>")
        sys.exit(1)

    #Inputting the variables
    inputImage = "../data/input/" + args[1]
    outputImage = "../data/results/" + args[2]
    radius = int(args[3])

    #set up a reader
    reader = itk.ImageFileReader.New(FileName=inputImage)

    #Create median filter and perform filtering
    medianFilter = itk.MedianImageFilter.New(Input=reader.GetOutput(), Radius=radius)

    #Write the file to an output image
    writer = itk.ImageFileWriter.New(FileName=outputImage, Input=medianFilter.GetOutput())

    #Actually write out the file
    writer.Update()

if __name__ == '__main__':
    arg_func(sys.argv)
