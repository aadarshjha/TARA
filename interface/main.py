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

        # viewport = [
        #     [ 0.67, 0.0, 1.0, 0.5 ],
        #     [ 0.67, 0.5, 1.0, 1.0 ],
        #     [ 0.0, 0.0, 0.67, 1.0 ],
        # ]

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

if __name__ == "__main__":
 
    app = QtWidgets.QApplication(sys.argv)
 
    window = MainWindow()
 
    sys.exit(app.exec_())