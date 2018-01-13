#import simens_dadm as smns
from . import module11_app as m11_app
from PyQt5 import QtWidgets
import sys

def main11(mri_input):
    data = mri_input.segmentation
    app = QtWidgets.QApplication(sys.argv)
    myApp = m11_app.Brain3D_App(data)
    myApp.mri_data
    myApp.show()
    sys.exit(app.exec_())
