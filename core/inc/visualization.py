import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtWidgets import QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import scipy.io

class visualize(QWidget):
    def __init__(self):
        super().__init__()
    
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)            
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.canvas.updateGeometry()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
    def set_active(self, data):
        if data is not None:
            self.figure.clf
            self.axes = self.figure.add_subplot(111)
            self.figure.subplots_adjust(0, 0, 1, 1)
            # set the layout
            self.figure.set_facecolor('black')
            self.im1 = self.axes.imshow(data,cmap='gray', interpolation='nearest', vmin=None)
            self.axes.axis('off')

            self.canvas.draw()

            
if __name__ == '__main__':
    mat = scipy.io.loadmat('C:/Users/Maciej/Desktop/MRI/recon_T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat')
    data = mat['SENSE_LSE']

    app = QApplication(sys.argv)

    main = visualize(data)
    main.show()

    sys.exit(app.exec_())
