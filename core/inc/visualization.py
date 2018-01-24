import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtWidgets import QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import scipy.io

class visualize(QWidget):
    def __init__(self, data):
        super().__init__()
        if data is not None:
            print(data.shape)
            self.data = data

            self.figure = plt.figure()

            self.canvas = FigureCanvas(self.figure)

            self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.canvas.updateGeometry()

            self.axes = self.figure.add_subplot(111)
            # set the layout
            layout = QVBoxLayout()
            layout.addWidget(self.canvas)

            self.setLayout(layout)
            print('mam layout')
            self.im1 = self.axes.imshow(self.data,cmap='gray', interpolation='nearest', vmin=None, vmax=255)
            print('prawie wyświetlam')
            self.axes.axis('off')

            self.canvas.draw()

if __name__ == '__main__':
    mat = scipy.io.loadmat('C:/Users/Maciej/Desktop/MRI/recon_T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat')
    data = mat['SENSE_LSE']

    app = QApplication(sys.argv)

    main = visualize(data)
    main.show()

    sys.exit(app.exec_())
