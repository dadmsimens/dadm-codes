#import simens_dadm as smns
from . import module11_app as m11_app
from PyQt5 import QtWidgets
import sys
import numpy as np
def main11(mri_input):
    segmentation = mri_input.segmentation
    segmentation_np = np.asarray(segmentation)
    cortex_mask = segmentation_np != 3 
    segmentation_np[cortex_mask] = 0
    #print(segmentation_np[50][50])
    data = mri_input.structural_data
    data[cortex_mask] = 0
    #print (data[50][50])
    app = QtWidgets.QApplication(sys.argv)
    myApp = m11_app.Brain3D_App(data)
    myApp.mri_data
    myApp.show()
    sys.exit(app.exec_())
