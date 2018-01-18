from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from . import module12_core as m12core
import numpy as np


class Window(QtWidgets.QDialog):
    def __init__(self, mri_data = None):
        super().__init__()

        self.mri_data = mri_data
        self.xx = []
        self.yy = []
        self.zz = []
        self.rev = False

        self.figure = Figure()
        self.figure2 = Figure()

        self.canvas = FigureCanvas(self.figure)
        self.canvas2 = FigureCanvas(self.figure2)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.button = QtWidgets.QPushButton('Get Oblique Image')
        self.button.clicked.connect(self.getobliqueimage)

        # self.revb = QtWidgets.QPushButton('Grid to opposite corner')
        # self.revb.clicked.connect(self.revf)

        self.labelx = QtWidgets.QLabel("Rotation X")
        self.sliderx = QtWidgets.QSlider(Qt.Horizontal)
        self.sliderx.setFocusPolicy(Qt.StrongFocus)
        self.sliderx.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderx.setMaximum(360)
        self.sliderx.setMinimum(0)
        self.sliderx.setTickInterval(10)
        self.sliderx.setSingleStep(1)
        self.sliderx.setValue(0)
        self.sliderx.valueChanged.connect(self.plot)

        self.labely = QtWidgets.QLabel("Rotation Y")
        self.slidery = QtWidgets.QSlider(Qt.Horizontal)
        self.slidery.setFocusPolicy(Qt.StrongFocus)
        self.slidery.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slidery.setMaximum(360)
        self.slidery.setMinimum(0)
        self.slidery.setTickInterval(10)
        self.slidery.setSingleStep(1)
        self.slidery.setValue(0)
        self.slidery.valueChanged.connect(self.plot)

        self.labelz = QtWidgets.QLabel("Rotation Z")
        self.sliderz = QtWidgets.QSlider(Qt.Horizontal)
        self.sliderz.setFocusPolicy(Qt.StrongFocus)
        self.sliderz.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderz.setMaximum(360)
        self.sliderz.setMinimum(0)
        self.sliderz.setTickInterval(10)
        self.sliderz.setSingleStep(1)
        self.sliderz.setValue(0)
        self.sliderz.valueChanged.connect(self.plot)

        self.labeltransx = QtWidgets.QLabel("Translation x")
        self.transsliderx = QtWidgets.QSlider(Qt.Horizontal)
        self.transsliderx.setFocusPolicy(Qt.StrongFocus)
        self.transsliderx.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.transsliderx.setMaximum(1000)
        self.transsliderx.setMinimum(-1000)
        self.transsliderx.setTickInterval(100)
        self.transsliderx.setSingleStep(1)
        self.transsliderx.setValue(0)
        self.transsliderx.valueChanged.connect(self.plot)

        self.labeltransy = QtWidgets.QLabel("Translation y")
        self.transslidery = QtWidgets.QSlider(Qt.Horizontal)
        self.transslidery.setFocusPolicy(Qt.StrongFocus)
        self.transslidery.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.transslidery.setMaximum(1000)
        self.transslidery.setMinimum(-1000)
        self.transslidery.setTickInterval(100)
        self.transslidery.setSingleStep(1)
        self.transslidery.setValue(0)
        self.transslidery.valueChanged.connect(self.plot)

        self.labeltransz = QtWidgets.QLabel("Translation z")
        self.transsliderz = QtWidgets.QSlider(Qt.Horizontal)
        self.transsliderz.setFocusPolicy(Qt.StrongFocus)
        self.transsliderz.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.transsliderz.setMaximum(1000)
        self.transsliderz.setMinimum(-1000)
        self.transsliderz.setTickInterval(100)
        self.transsliderz.setSingleStep(1)
        self.transsliderz.setValue(0)
        self.transsliderz.valueChanged.connect(self.plot)

        # self.transbox = QtWidgets.QSpinBox()
        # self.transbox.setMaximum(10000)
        # self.transbox.setMinimum(-10000)
        # self.transbox.setValue(0)
        # self.transbox.valueChanged.connect(self.plot)

        self.resetbutton = QtWidgets.QPushButton('Reset values')
        self.resetbutton.clicked.connect(self.resetvalues)

        # set the layout
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.canvas)
        layout.addWidget(self.canvas2)
        layout.addWidget(self.button)

        layout.addWidget(self.labelx)
        layout.addWidget(self.sliderx)
        layout.addWidget(self.labely)
        layout.addWidget(self.slidery)
        layout.addWidget(self.labelz)
        layout.addWidget(self.sliderz)
        # layout.addWidget(self.transbox)
        layout.addWidget(self.labeltransx)
        layout.addWidget(self.transsliderx)
        layout.addWidget(self.labeltransy)
        layout.addWidget(self.transslidery)
        layout.addWidget(self.labeltransz)
        layout.addWidget(self.transsliderz)
        # layout.addWidget(self.revb)
        layout.addWidget(self.resetbutton)

        self.setLayout(layout)
        self.plot()

    def plot(self):
        ''' plot some random stuff '''
        # random data
        sliderxval = self.sliderx.value()
        slideryval = self.slidery.value()
        sliderzval = self.sliderz.value()
        transboxvalx = self.transsliderx.value()
        transboxvaly = self.transslidery.value()
        transboxvalz = self.transsliderz.value()

        self.xx, self.yy, self.zz = m12core.transrotateplane(self.mri_data, sliderxval, slideryval, sliderzval, transboxvalx, transboxvaly, transboxvalz, self.rev)

        self.figure.clear()
        # create an axis
        ax = self.figure.gca(projection='3d')

        # plot data
        ax.plot_surface(self.xx, self.yy, self.zz)

        x = [x for x in range(self.mri_data.shape[0])]
        y = [y for y in range(self.mri_data.shape[1])]
        z = [z for z in range(self.mri_data.shape[2])]

        ax.plot(x, [0]*len(x), 'red')
        ax.plot([max(x)] * len(y), y, 'red')
        ax.plot([0] * len(y), y, 'red')
        ax.plot(x, [max(y)]*len(x), 'red')

        ax.plot(x, [0] * len(x), [max(z)]*len(x), 'red')
        ax.plot([max(x)] * len(y), y, [max(z)]*len(y), 'red')
        start_time = time.time()
        ax.plot([0] * len(y), y, [max(z)]*len(y), 'red')
        ax.plot(x, [max(y)] * len(x), [max(z)]*len(x), 'red')

        ax.plot([0] * len(z), [0] * len(z), z, 'red')
        ax.plot([max(x)] * len(z), [0] * len(z), z, 'red')
        ax.plot([0] * len(z), [max(y)] * len(z), z, 'red')
        ax.plot([max(x)] * len(z), [max(y)] * len(z), z, 'red')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        # refresh canvas
        self.canvas.draw()

    def getobliqueimage(self):
        QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
        interpolatedimage = m12core.interpolatemri(self.mri_data, self.xx, self.yy, self.zz)
        QtWidgets.QApplication.restoreOverrideCursor()
        self.figure2.clear()
        ax2 = self.figure2.add_subplot(111)
        ax2.set_xticks([])
        ax2.set_yticks([])
        ax2.imshow(interpolatedimage,cmap='gray', aspect='equal')

        self.canvas2.draw()

    def resetvalues(self):
        self.sliderx.setValue(0)
        self.slidery.setValue(0)
        self.sliderz.setValue(0)
        self.transslider.setValue(0)
        self.rev = False

    def revf(self):
        self.rev = not self.rev
        self.plot()

