import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QFileDialog, qApp, QApplication, QLabel
from PyQt5.QtGui import QPixmap



class ImageDialog(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.ui = loadUi("mainwindow.ui")

        self.ui.show()


        #image into
        self.ui.diffusive_if.setPixmap(QPixmap('diff_no.png'))
        self.ui.diffusive_if.setScaledContents(True)
        self.ui.view_mini.setPixmap(QPixmap('Structural_MRI_animation1.jpg'))
        self.ui.view_mini.setScaledContents(True)
        pixmap1 = QPixmap('Structural_MRI_animation1.jpg')
        pixmap2 = QPixmap('Structural_MRI_animation2.jpg')
        pixmap3 = QPixmap('Structural_MRI_animation3.jpg')
        pixmap = [pixmap1, pixmap2, pixmap3]
        self.ui.view_image.setPixmap(pixmap1)
        self.ui.view_image.setScaledContents(True)
        #self.ui.view_image.setAlignment(AlignCenter)
       # self.ui.view_upper_left.setPixmap(pixmap(0))
       # self.ui.view_upper_right.setPixmap(pixmap(1))
       # self.ui.view_lower_right_3.setPixmap(pixmap(2))
       # self.ui.view_lower_left_3.setPixmap(pixmap(0))

        # Events
        self.ui.actionNew_patient.triggered.connect(self.mb_file_new_trigger)
        self.ui.actionQuit.triggered.connect(self.mb_file_exit_trigger)
        #self.ui.start_btn.clicked.connect(self.action_complete)



    ##Menu functionality:
    def mb_file_new_trigger(self):
        open_image = QFileDialog()
        filename = open_image.getOpenFileName(self, 'Choose image', os.getenv('HOME'),
                                              'MRI Files *.mat')
        with open(filename[0], 'r') as image:
            current_mri = image.read()

    def mb_file_exit_trigger(self):
        qApp.quit()
        ##

    def action_complete(self):
        self.ui.statusBar.showMessage('Witojże', 200)

    def change_pixmap(self):
        pass

app = QApplication(sys.argv)
window = ImageDialog()

sys.exit(app.exec_())
