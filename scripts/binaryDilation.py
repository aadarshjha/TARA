'''
Params: Input file name, Output file name, radius
File Description: Performs Binary Dilation, expands white regions
Ex Input: medianFilter.py 1000_3.nii.gz 1000_3_dilation.nii.gz 5
'''

import sys
import itk


def arg_func(args):
    #Make sure input is selected
    if len(args) != 4:
        print("Usage: " + args[0] + " <inputImage> <outputImage> <radius>")
        sys.exit(1)


    #Inputting the variables
    inputImage = args[1]
    outputImage = args[2]
    radius = int(args[3])

    PixelType = itk.UC
    dims = 3

    ImageType = itk.Image[PixelType, dims]

    #set up a reader
    ReaderType = itk.ImageFileReader[ImageType]
    reader = ReaderType.New()
    reader.SetFileName(inputImage)

    #set kernal shape
    StructuringElementType = itk.FlatStructuringElement[dims]
    structuringElement = StructuringElementType.Ball(radiusValue)

    #create dilation filter
    DilateFilterType = itk.BinaryDilateImageFilter[ImageType,
                                                   ImageType,
                                                   StructuringElementType]
    dilateFilter = DilateFilterType.New()
    dilateFilter.SetInput(reader.GetOutput())
    dilateFilter.SetKernel(structuringElement)
    dilateFilter.SetForegroundValue(255)

    WriterType = itk.ImageFileWriter[ImageType]
    writer = WriterType.New(FileName=outputImage, Input=dilateFilter.GetOutput())

    writer.Update()

if __name__ == '__main__':
    arg_func(sys.argv)
