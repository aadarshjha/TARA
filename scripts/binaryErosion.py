'''
Params: Input file name, Output file name, radius
File Description: Performs Binary Erosion, erodes white regions with black
Ex Input: medianFilter.py 1000_3.nii.gz 1000_3_erosion.nii.gz 5
'''

import sys
import itk

#Make sure input is selected
if len(sys.argv) != 4:
    print("Usage: " + sys.argv[0] + " <inputImage> <outputImage> <radius>")
    sys.exit(1)

#Inputting the variables
inputImage = "../data/input" + sys.argv[1]
outputImage = "../data/results" + sys.argv[2]
radius = int(sys.argv[3])

PixelType = itk.UC
dims = 3

ImageType = itk.Image[PixelType, dims]

#set up a reader
ReaderType = itk.ImageFileReader[ImageType]
reader = ReaderType.New()
reader.SetFileName(inputImage)

#set kernal shape
StructuringElementType = itk.FlatStructuringElement[dims]
structuringElement = StructuringElementType.Ball(radius)

#create erosion filter
ErodeFilterType = itk.BinaryErodeImageFilter[ImageType,
                                             ImageType,
                                             StructuringElementType]
erodeFilter = ErodeFilterType.New()
erodeFilter.SetInput(reader.GetOutput())
erodeFilter.SetKernel(structuringElement)
erodeFilter.SetForegroundValue(255) # Intensity value to erode
erodeFilter.SetBackgroundValue(0)   # Replacement value for eroded voxels

WriterType = itk.ImageFileWriter[ImageType]
writer = WriterType.New(FileName=outputImage, Input=erodeFilter.GetOutput())

writer.Update()
