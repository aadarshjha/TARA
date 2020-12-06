import vtk

from PyQt5 import QtCore, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
import subprocess
import sys 

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../scripts/')
import binaryThreshold

# Just importing all. 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.renderers = []
        self.frame = QtWidgets.QFrame()
        self.setFixedHeight(520)
        self.setFixedWidth(900)
 
        self.main_layout = QtWidgets.QVBoxLayout()

        # Adding some text here: 
        self.label= QLabel("TARA")
        self.label.setFont(QFont('Arial', 30)) 

        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.label)

        # Add menu widgets
        self.menu_layout = QtWidgets.QHBoxLayout()
        self.button1 = QtWidgets.QPushButton('Open NIFTI', self)
        self.button2 = QtWidgets.QPushButton('Save NIFTI', self)
        self.button3 = QtWidgets.QPushButton('Help', self); 
        self.button1.clicked.connect(lambda: self.openFileNameDialog())
        self.button2.clicked.connect(lambda: self.printOut(self.button2.text()))
        self.button2.clicked.connect(lambda: self.printOut(self.button3.text()))

        self.menu_layout.addWidget(self.button1)
        self.menu_layout.addWidget(self.button2)
        self.menu_layout.addWidget(self.button3)

        self.main_layout.addLayout(self.menu_layout)

        # VTK Widget, split the view. 
        self.overall_layout = QtWidgets.QHBoxLayout(); 
        self.options_layout = QtWidgets.QVBoxLayout()
        self.sub_menu_options = QtWidgets.QHBoxLayout()

        # getting optoins from the user: 
        # we allow for access of: 

        # creating a qt form: 

        self.cb = QComboBox()
        self.cb.addItem("Select Image Processing Algorithm")
        self.cb.addItem("Binary Threshold")  
        self.cb.addItem("Canny Edge Detection")  
        self.cb.addItem("Clamp Image Filter")  
        self.cb.addItem("Gaussian Smoothing")  
        self.cb.addItem("Median Filter")  
        self.cb.addItem("Otsu Threshold")  
        self.cb.addItem("Sobel Edge Detection")
        self.cb.addItem("Registration")
        self.cb.addItem("Segmentation")     
        self.cb.addItem("Brain Extraction")
        self.cb.addItem("Deep Segmentation")
        self.cb.addItem("Super Resolution")
        self.options_layout.addWidget(self.cb)
        self.options_layout.addWidget(self.button1)

        # call back function: 
        self.cb.currentTextChanged.connect(self.pickBackend)

        

        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
      
        self.overall_layout.addLayout(self.options_layout)
        self.main_layout.addLayout(self.overall_layout)
        self.options_layout.addLayout(self.sub_menu_options)

        self.overall_layout.addWidget(self.vtkWidget)
 
        ren = vtk.vtkRenderer()

        self.renderers.append(ren)
        self.vtkWidget.GetRenderWindow().AddRenderer(ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
 
        style = vtk.vtkInteractorStyleImage()
        style.SetInteractionModeToImage3D()
        self.iren.SetInteractorStyle(style)

        ren.ResetCamera()
 
        self.frame.setLayout(self.main_layout)
        self.setCentralWidget(self.frame)

        self.show()
        self.iren.Initialize()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, 
            "QFileDialog.getOpenFileName()", 
            "","NIFTI files (*.nii, *.nii.gz)", 
            options=options)

        if file_name:
            print(file_name)
            self.openImage(file_name)

    def printOut(self, msg):
        print(msg)

    def openImage(self, file_name):
        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileName(file_name)
        reader.Update()

        matrix = vtk.vtkMatrix4x4()

        if (reader.GetQFormMatrix()):
            matrix.DeepCopy(reader.GetQFormMatrix())
            matrix.Invert()
        elif (reader.GetSFormMatrix()):
            matrix.DeepCopy(reader.GetSFormMatrix())
            matrix.Invert()

        reslice = vtk.vtkImageReslice()
        reslice.SetInputConnection(reader.GetOutputPort())
        reslice.SetResliceAxes(matrix)
        reslice.SetInterpolationModeToLinear()
        reslice.Update()

        scalarRange = [0.0, 0.0]
        extent = [0, 0, 0, 0, 0, 0]
        scalarRange = reslice.GetOutput().GetScalarRange()
        extent = reslice.GetOutput().GetExtent()

    
        viewport = [[0.0, 0.0, 0.33, 1.0],
                    [0.33, 0.0, 0.67, 1.0],
                    [0.67, 0.0, 1.0, 1.0]]

        imageIs3D = (extent[5] > extent[4])

        for i in range(2 * (imageIs3D == 0), 3):
            imageMapper = vtk.vtkImageSliceMapper()

            if (i < 3):
                imageMapper.SetInputConnection(reslice.GetOutputPort())

            imageMapper.SetOrientation(i % 3)
            imageMapper.SliceAtFocalPointOn()

            image = vtk.vtkImageSlice()
            image.SetMapper(imageMapper)

            image.GetProperty().SetColorWindow(scalarRange[1] - scalarRange[0])
            image.GetProperty().SetColorLevel(0.5*(scalarRange[0] + scalarRange[1]))
            image.GetProperty().SetInterpolationTypeToNearest()

            renderer = vtk.vtkRenderer()
            self.renderers.append(renderer)

            renderer.AddViewProp(image)
            renderer.SetBackground(0.0, 0.0, 0.0)
            if imageIs3D:
                renderer.SetViewport(viewport[i])

            renWin = self.vtkWidget.GetRenderWindow()
            renWin.AddRenderer(renderer)

            bounds = imageMapper.GetBounds()
            point = [0,0,0]
            point[0] = 0.5*(bounds[0] + bounds[1])
            point[1] = 0.5*(bounds[2] + bounds[3])
            point[2] = 0.5*(bounds[4] + bounds[5])
            maxdim = 0.0

            for j in range(3):
                s = 0.5*(bounds[2*j+1] - bounds[2*j])
                maxdim = s if s > maxdim else maxdim

            camera = renderer.GetActiveCamera()
            camera.SetFocalPoint(point)
            if imageMapper.GetOrientation() == 2:
                point[imageMapper.GetOrientation()] -= 500.0
                camera.SetViewUp(0.0, +1.0, 0.0)
            else:
                point[imageMapper.GetOrientation()] += 500.0
                camera.SetViewUp(0.0, 0.0, +1.0)

            camera.SetPosition(point)
            camera.ParallelProjectionOn()
            camera.SetParallelScale(maxdim)

        if (imageIs3D):
            renWin.SetSize(850, 500)
        else:
            renWin.SetSize(400, 400)

        renWin.Render()
        self.iren.Start()
            

        self.iren.Initialize()
    
    def pickBackend(self, type):
        # we display a particular screen depending on the type of 
        # values that the user will give to us. 

        # for instance, in the case of binary thres, we take
        # Ex Input: binaryThreshold.py 1000_3.nii.gz 1000_3_threshold.nii.gz 600 1500 0 1
        # according to ashwin. 

        ## clearing the view: 
        
        while self.sub_menu_options.count():
            child = self.sub_menu_options.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if type == "Binary Threshold":
            # we pull up a different UI to the user, this will have configurable views 

            # file path "../scripts/binaryThreshold.py"

            # running the file. 

            # self.button1 = QtWidgets.QPushButton('Open NIFTI', self)
            # self.button2 = QtWidgets.QPushButton('Save NIFTI', self)
            self.button3 = QtWidgets.QPushButton('Run Binary Threshold', self); 
            # self.button1.clicked.connect(lambda: self.openFileNameDialog())
            # self.button2.clicked.connect(lambda: self.printOut(self.button2.text()))
            # binaryThreshold.py 1000_3.nii.gz 1000_3_threshold.nii.gz 600 1500 0 1
            self.button3.clicked.connect(lambda: self.getBinThres("1000_3.nii.gz", "1000_3_threshold_test.nii.gz", 600, 1500, 0, 1))

            self.sub_menu_options.addWidget(self.button1)
            self.sub_menu_options.addWidget(self.button2)
            self.sub_menu_options.addWidget(self.button3)
        elif type == "Canny Edge Detection":
            self.button1 = QtWidgets.QPushButton('Open TESTS', self)
            self.button2 = QtWidgets.QPushButton('Save NIFTI', self)
            self.button3 = QtWidgets.QPushButton('Help', self); 
            self.button1.clicked.connect(lambda: self.openFileNameDialog())
            self.button2.clicked.connect(lambda: self.printOut(self.button2.text()))
            self.button2.clicked.connect(lambda: self.printOut(self.button3.text()))

            self.sub_menu_options.addWidget(self.button1)
            self.sub_menu_options.addWidget(self.button2)
            self.sub_menu_options.addWidget(self.button3)





        return type 


    #    print("Usage: " + sys.argv[0] + " <inputImage> <outputImage> "
    #         "<lowerThreshold> <upperThreshold> <outsideValue> <insideValue>")
    #     sys.exit(1)

    def getBinThres(self, inputImage, outputImage, lowerThres, upperThres,
                    outsideValue, insideValue):
        # actually calling the script. 
        # print("is this working?")
        # subprocess.run(["python3","../scripts/binaryThreshold.py", 
        #     str(inputImage), str(outputImage), str(lowerThres), str(upperThres), str(outsideValue), str(insideValue)], 
        #     shell=True, check=True, capture_output=True)

        print("is this working?")
        binaryThreshold.arg_func(["../scripts/binaryThreshold.py", 
            str(inputImage), str(outputImage), str(lowerThres), str(upperThres), str(outsideValue), str(insideValue)])


if __name__ == "__main__":
 
    app = QtWidgets.QApplication(sys.argv)
 
    window = MainWindow()
 
    sys.exit(app.exec_())