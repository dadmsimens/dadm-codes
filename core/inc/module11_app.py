from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from . import module11_ui as ui
from . import module11_model3D as model3D



class Brain3D_App(QtWidgets.QMainWindow):
    def __init__(self, mri_data = None):
        super().__init__()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_action()
        self.model3D = model3D.Model3D(mri_data)
        self.model3D.setup_render_window(self.ui.frame, self.ui.frame_layout)

    def set_action(self):
        self.ui.actionHelp.triggered.connect(self.show_help)
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.button_model.clicked.connect(self.preview_model)
        self.ui.button_clipper.clicked.connect(self.clip_model)
        self.ui.button_clipper_plane.clicked.connect(self.clip_model_plane)


    def show_help(self):
        '''information about program in help'''
        message = "This module enable to visualization od three-dimensional model of cortex basing on segementation output. \n \nTo preview elected cross-section of 3d model, choose CLIP MODEL and select the plane intersection by holding middle mouse button. \n \nVisualization of intersection plane is possible by pressing CLIP MODEL AND SHOW PLANE."
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Help")
        msg.exec()


    def exit(self):
        '''confirmation of the exit'''
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.close()


    def preview_model(self):
        '''Return to model view'''
        self.ui.statusbar.showMessage("Return to model view.")
        self.model3D.reset_window()
        self.model3D.preview_model()



    def clip_model(self):
        '''Enable clipping model'''
        self.ui.statusbar.showMessage("You are in clipping mode. To set intersection plane  use middle mouse button.")
        self.model3D.reset_window()
        self.model3D.cut_model()



    def clip_model_plane(self):
        '''Enable clipping model and displaying intersection plane '''
        self.ui.statusbar.showMessage("You are in clipping mode with displaying intersection plane. To set intersection plane  use middle mouse button.")
        self.model3D.reset_window()
        self.model3D.cut_model(plane_mode=True)

