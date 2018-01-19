from PyQt5 import QtCore, QtGui, QtWidgets
from  PyQt5.QtWidgets import QMessageBox
from . import module11_ui as Ui
from . import module11_model3D as model3D
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

import sys

class Brain3D_App(QtWidgets.QMainWindow):
    def __init__(self, mri_data = None):
        super().__init__()
        self.ui = Ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_action()
        self.model3D = model3D.model3D(mri_data, self.ui.frame, self.ui.frame_layout)


    def exit(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            QtCore.QCoreApplication.instance().quit()

    def set_action(self):
        self.ui.actionHelp.triggered.connect(self.show_help)
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.button_model.clicked.connect(self.previewModel)
        self.ui.button_clipper.clicked.connect(self.clip_model)
        self.ui.button_clipper_plane.clicked.connect(self.clip_model_plane)

    def previewModel(self):
        self.model3D.preview_model()

    def show_help(self):
        '''information about program in help'''
        message = "#TODO"
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Help")
        msg.exec()

    def clip_model(self):
        self.model3D.cut_model()

    def clip_model_plane(self):
        self.model3D.cut_model(plane_mode=True)

