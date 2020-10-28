import sys
import vtk
from PyQt5 import QtCore, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
 
        self.frame = QtWidgets.QFrame()
        self.setFixedHeight(520)
        self.setFixedWidth(900)
 
        self.main_layout = QtWidgets.QHBoxLayout()

        # Add menu widgets
        self.menu_layout = QtWidgets.QVBoxLayout()
        self.button1 = QtWidgets.QPushButton('Button1', self)
        self.button2 = QtWidgets.QPushButton('Button2', self)
        self.button1.clicked.connect(lambda: self.printOut(self.button1.text()))
        self.button2.clicked.connect(lambda: self.printOut(self.button2.text()))

        self.menu_layout.addWidget(self.button1)
        self.menu_layout.addWidget(self.button2)


        self.main_layout.addLayout(self.menu_layout)

        # VTK Widget
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.main_layout.addWidget(self.vtkWidget)
 
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
 
        # Create source
        source = vtk.vtkSphereSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(5.0)
 
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
 
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
 
        self.ren.AddActor(actor)
 
        self.ren.ResetCamera()
 
        self.frame.setLayout(self.main_layout)
        self.setCentralWidget(self.frame)

        self.show()
        self.iren.Initialize()

    def printOut(self, msg):
        print(msg)
 
if __name__ == "__main__":
 
    app = QtWidgets.QApplication(sys.argv)
 
    window = MainWindow()
 
    sys.exit(app.exec_())