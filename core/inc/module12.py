from . import module12_ui as m12ui
from PyQt5 import QtWidgets
import sys

def main12(mri_data):

    app = QtWidgets.QApplication(sys.argv)
    myapp = m12ui.Window(mri_data)
    myapp.show()

    sys.exit(app.exec_())