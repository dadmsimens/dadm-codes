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
        self.mri_data = mri_data
        self.ui = Ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_action()
        self.layout = QtWidgets.QHBoxLayout()
        self.model3D = model3D.model3D(self.mri_data, self.ui.frame, self.layout)
        #self.ui.actionReturn.setEnabled(False)

    def exit(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            QtCore.QCoreApplication.instance().quit()

    def set_action(self):
        self.ui.actionHelp.triggered.connect(self.show_help)
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionClip.triggered.connect(self.cut_mode_enable)
        self.ui.actionReturn.triggered.connect(self.undo)


    def undo(self):
        self.model3D.change_mode(0)
        self.ui.actionReturn.setEnabled(False)
        self.ui.actionClip.setEnabled(True)

    def show_help(self):
        '''information about program in help'''
        message = "#TODO"
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Help")
        msg.exec()


    def cut_mode_enable(self):
        self.ui.actionReturn.setEnabled(True)
        self.model3D.change_mode(1)
        self.model3D.cut_model()
