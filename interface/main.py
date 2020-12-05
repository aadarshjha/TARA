import sys
import vtk
from PyQt5 import QtCore, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QFileDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.renderers = []
        self.frame = QtWidgets.QFrame()
        self.setFixedHeight(520)
        self.setFixedWidth(900)
 
        self.main_layout = QtWidgets.QHBoxLayout()

        # Add menu widgets
        self.menu_layout = QtWidgets.QVBoxLayout()
        self.button1 = QtWidgets.QPushButton('Open NIFTI', self)
        self.button2 = QtWidgets.QPushButton('Button2', self)
        self.button1.clicked.connect(lambda: self.openFileNameDialog())
        self.button2.clicked.connect(lambda: self.printOut(self.button2.text()))

        self.menu_layout.addWidget(self.button1)
        self.menu_layout.addWidget(self.button2)


        self.main_layout.addLayout(self.menu_layout)

        # VTK Widget
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.main_layout.addWidget(self.vtkWidget)
 
        ren = vtk.vtkRenderer()
        self.renderers.append(ren)
        self.vtkWidget.GetRenderWindow().AddRenderer(ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
 
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

        scalarRange = reader.GetOutput().GetScalarRange()
        extent = reader.GetOutput().GetExtent()
        viewport = [[0.67, 0.0, 1.0, 0.5],
                    [0.67, 0.5, 1.0, 1.0],
                    [0.0, 0.0, 0.67, 1.0]]

        for ren in self.renderers:
            self.vtkWidget.GetRenderWindow().RemoveRenderer(ren)

        for i in range(3):
            mapper = vtk.vtkImageSliceMapper()
            mapper.SetInputConnection(reader.GetOutputPort())
            mapper.SetOrientation(i % 3)
            mapper.SliceAtFocalPointOn()

            image = vtk.vtkImageSlice()
            image.SetMapper(mapper)
            image.GetProperty().SetColorWindow(scalarRange[1] - scalarRange[0])
            image.GetProperty().SetColorLevel(0.5 * (scalarRange[0] + scalarRange[1]))

            renderer = vtk.vtkRenderer()
            renderer.AddActor(image)
            renderer.SetBackground(0, 0, 0)
            self.vtkWidget.GetRenderWindow().AddRenderer(renderer)
            self.renderers.append(renderer)

            

        self.iren.Initialize()

if __name__ == "__main__":
 
    app = QtWidgets.QApplication(sys.argv)
 
    window = MainWindow()
 
    sys.exit(app.exec_())