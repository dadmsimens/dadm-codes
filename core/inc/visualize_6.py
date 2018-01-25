from PyQt5.QtWidgets import QWidget,QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

class visualise6(QWidget):
    def __init__(self, data):
        super().__init__()

        self.data = data
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas = FigureCanvas(self.figure)
        self.button = QPushButton('Change plot', self)
        self.button.clicked.connect(self.plot)
        self.axes = None

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.plot()

    def plot(self):
        ''' plot some random stuff '''
        self.figure.clf()
        if type(self.axes)!=list:
            plot_dict = {
                    221: ['MD', 'MD (Mean Diffusivity)'],
                    222: ['RA', 'RA (Relative Anisotropy)'],
                    223: ['FA', 'FA (Fractional Anisotropy)'],
                    224: ['VR', 'VR (Volume Ratio)']
                }
            self.axes = [None]*4
            self.figure.suptitle('Diffusion tensor biomarkers')
            i = 0
            for key, value in plot_dict.items():
                    self.axes[i] = self.figure.add_subplot(key)
                    self.axes[i].imshow(np.squeeze(self.data[value[0]]), cmap='gray')
                    self.axes[i].axis('off')
                    self.axes[i].title.set_text(value[1])
                    i+=1
        else:
            self.figure.suptitle('Fractional Anisotropy Colormap')
            self.axes = self.figure.add_subplot(111)
            self.axes.title.set_text('FA (Fractional Anisotropy)')
            self.axes.imshow(np.squeeze(self.data['FA_rgb']))
            self.axes.axis('off')
            self.axes.text(-30,20,'Right-Left',bbox={'facecolor': 'red','pad':8})
            self.axes.text(-30,33,' Front-Back   ',bbox={'facecolor': 'green','pad':8})
            self.axes.text(-30,46,' Up-Down   ',bbox=dict(facecolor='blue',pad=8))
        self.canvas.draw()


