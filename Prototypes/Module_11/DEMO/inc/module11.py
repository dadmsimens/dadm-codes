#import simens_dadm as smns
from . import module11_app as m11_app
from PyQt5 import QtWidgets
import sys

def main11(mri_input):
    data = mri_input.segmentation
    #model_3D = visualization.generate_model3D(data)
    app = QtWidgets.QApplication(sys.argv)
    myApp = m11_app.Brain3D_App(data)
    myApp.mri_data
    myApp.show()
    #myApp.showFullScreen()
    sys.exit(app.exec_())
