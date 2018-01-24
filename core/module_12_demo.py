from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import scipy.io as sio
import os
import inc.module12 as m12
import inc.simens_dadm as smns

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_12_test/'

data = smns.mri_struct().structural_data

data=sio.loadmat(DATASETS_ROOT + 'Imavol.mat')
data = data['Imavol']


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.pushButton = QtWidgets.QPushButton("Click to enable module 12")
        self.setCentralWidget(self.pushButton)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)

    def on_pushButton_clicked(self):
        self.module_12_dialog = m12.main12(data)
        self.module_12_dialog.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()