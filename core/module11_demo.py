from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import scipy.io as sio
import inc.module11 as module11
import inc.simens_dadm as smns
import os


# Data location in ROOT
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_11_test/'
segmentation = sio.loadmat(DATASETS_ROOT + 'testSegmentation.mat')
segmentation = segmentation['mri_segMask']
#segmentation = sio.loadmat(DATASETS_ROOT + 'segmentationMask.mat')
#segmentation = segmentation['imageMaskFull']
#segmentation = sio.loadmat(DATASETS_ROOT + 'segmentationMask2.mat')
#segmentation = segmentation['imageMaskFull']

struct = smns.mri_struct()
struct.segmentation = segmentation


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.pushButton = QtWidgets.QPushButton("Click to enable module 11")
        self.setCentralWidget(self.pushButton)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)

    def on_pushButton_clicked(self):
        self.module_11_dialog = module11.main11(struct)
        self.module_11_dialog.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()