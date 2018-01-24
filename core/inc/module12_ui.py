from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import Qt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
        self.interpolatedimage = []

        self.figure = Figure()
        self.figure2 = Figure()

        self.canvas = FigureCanvas(self.figure)
        self.canvas2 = FigureCanvas(self.figure2)

        self.buttonobl = QtWidgets.QPushButton('Get Oblique Image')
        self.buttonobl.clicked.connect(self.getobliqueimage)

        self.buttonrotl = QtWidgets.QPushButton('Rotate image left')
        self.buttonrotl.clicked.connect(self.imagerotleft)

        self.buttonrotr = QtWidgets.QPushButton('Rotate image right')
        self.buttonrotr.clicked.connect(self.imagerotright)

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
        self.sliderx.valueChanged.connect(self.setxbox)

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
        self.slidery.valueChanged.connect(self.setybox)

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
        self.sliderz.valueChanged.connect(self.setzbox)

        self.labeltransx = QtWidgets.QLabel("Translation x")
        self.transsliderx = QtWidgets.QSlider(Qt.Horizontal)
        self.transsliderx.setFocusPolicy(Qt.StrongFocus)
        self.transsliderx.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.transsliderx.setMaximum(2.5*max(mri_data.shape))
        self.transsliderx.setMinimum(-2.5*max(mri_data.shape))
        self.transsliderx.setTickInterval(100)
        self.transsliderx.setSingleStep(1)
        self.transsliderx.setValue(0)
        self.transsliderx.valueChanged.connect(self.plot)

        self.labeltransy = QtWidgets.QLabel("Translation y")
        self.transslidery = QtWidgets.QSlider(Qt.Horizontal)
        self.transslidery.setFocusPolicy(Qt.StrongFocus)
        self.transslidery.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.transslidery.setMaximum(2.5*max(mri_data.shape))
        self.transslidery.setMinimum(-2.5*max(mri_data.shape))
        self.transslidery.setTickInterval(100)
        self.transslidery.setSingleStep(1)
        self.transslidery.setValue(0)
        self.transslidery.valueChanged.connect(self.plot)

        self.labeltransz = QtWidgets.QLabel("Translation z")
        self.transsliderz = QtWidgets.QSlider(Qt.Horizontal)
        self.transsliderz.setFocusPolicy(Qt.StrongFocus)
        self.transsliderz.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.transsliderz.setMaximum(2.5*max(mri_data.shape))
        self.transsliderz.setMinimum(-2.5*max(mri_data.shape))
        self.transsliderz.setTickInterval(100)
        self.transsliderz.setSingleStep(1)
        self.transsliderz.setValue(0)
        self.transsliderz.valueChanged.connect(self.plot)

        self.xbox = QtWidgets.QSpinBox()
        self.xbox.setValue(0)
        self.xbox.setMaximum(360)
        self.xbox.valueChanged.connect(self.setxslider)

        self.ybox = QtWidgets.QSpinBox()
        self.ybox.setValue(0)
        self.ybox.setMaximum(360)
        self.ybox.valueChanged.connect(self.setyslider)

        self.zbox = QtWidgets.QSpinBox()
        self.zbox.setValue(0)
        self.zbox.setMaximum(360)
        self.zbox.valueChanged.connect(self.setzslider)

        self.resetbutton = QtWidgets.QPushButton('Reset values')
        self.resetbutton.clicked.connect(self.resetvalues)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.canvas, 0, 0, 4, 4)
        layout.addWidget(self.canvas2, 4, 0, 4, 4)
        layout.addWidget(self.buttonobl, 8, 0, 1, 4)
        layout.addWidget(self.buttonrotl, 9, 0, 1, 2)
        layout.addWidget(self.buttonrotr, 9, 2, 1, 2)
        layout.addWidget(self.labelx, 10, 0, 1, 4)
        layout.addWidget(self.sliderx, 11, 0, 1, 3)
        layout.addWidget(self.xbox, 11, 3, 1, 1)
        layout.addWidget(self.labely, 12, 0, 1, 4)
        layout.addWidget(self.slidery, 13, 0, 1, 3)
        layout.addWidget(self.ybox, 13, 3, 1, 1)
        layout.addWidget(self.labelz, 14, 0, 1, 4)
        layout.addWidget(self.sliderz, 15, 0, 1, 3)
        layout.addWidget(self.zbox, 15, 3, 1, 1)
        layout.addWidget(self.labeltransx, 16, 0, 1, 4)
        layout.addWidget(self.transsliderx, 17, 0, 1, 4)
        layout.addWidget(self.labeltransy, 18, 0, 1, 4)
        layout.addWidget(self.transslidery, 19, 0, 1, 4)
        layout.addWidget(self.labeltransz, 20, 0, 1, 4)
        layout.addWidget(self.transsliderz, 21, 0, 1, 4)
        layout.addWidget(self.resetbutton, 22, 0, 1, 4)

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

        self.xx, self.yy, self.zz = m12core.transrotateplane(self.mri_data, sliderxval, slideryval, sliderzval, transboxvalx, transboxvaly, transboxvalz)

        self.figure.clear()
        # create an axis
        ax = self.figure.gca(projection='3d')

        # plot data
        ax.plot_surface(self.xx, self.yy, self.zz)

        x = [x for x in range(self.mri_data.shape[0])]
        y = [y for y in range(self.mri_data.shape[1])]
        z = [z for z in range(self.mri_data.shape[2])]

        ax.plot(x, [0]*len(x), 'red')
        ax.plot([max(x)] * len(y), y, 'yellow')
        ax.plot([0] * len(y), y, 'red')
        ax.plot(x, [max(y)]*len(x), 'red')

        ax.plot(x, [0] * len(x), [max(z)]*len(x), 'red')
        ax.plot([max(x)] * len(y), y, [max(z)]*len(y), 'yellow')
        ax.plot([0] * len(y), y, [max(z)]*len(y), 'red')
        ax.plot(x, [max(y)] * len(x), [max(z)]*len(x), 'red')

        ax.plot([0] * len(z), [0] * len(z), z, 'red')
        ax.plot([max(x)] * len(z), [0] * len(z), z, 'yellow')
        ax.plot([0] * len(z), [max(y)] * len(z), z, 'red')
        ax.plot([max(x)] * len(z), [max(y)] * len(z), z, 'yellow')

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        # refresh canvas
        self.canvas.draw()

    def plotimage(self):
        self.figure2.clear()
        ax2 = self.figure2.add_subplot(111)
        ax2.set_xticks([])
        ax2.set_yticks([])
        ax2.imshow(self.interpolatedimage, cmap='gray', aspect='equal')
        self.canvas2.draw()

    def getobliqueimage(self):
        QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
        self.interpolatedimage = m12core.interpolatemri(self.mri_data, self.xx, self.yy, self.zz)
        QtWidgets.QApplication.restoreOverrideCursor()
        self.plotimage()

    def resetvalues(self):
        self.sliderx.setValue(0)
        self.slidery.setValue(0)
        self.sliderz.setValue(0)
        self.xbox.setValue(0)
        self.ybox.setValue(0)
        self.zbox.setValue(0)
        self.transsliderx.setValue(0)
        self.transslidery.setValue(0)
        self.transsliderz.setValue(0)

    def imagerotright(self):
        self.interpolatedimage = m12core.rotimageright(self.interpolatedimage)
        self.plotimage()

    def imagerotleft(self):
        self.interpolatedimage = m12core.rotimageleft(self.interpolatedimage)
        self.plotimage()

    def setxslider(self):
        self.sliderx.setValue(self.xbox.value())

    def setyslider(self):
        self.slidery.setValue(self.ybox.value())

    def setzslider(self):
        self.sliderz.setValue(self.zbox.value())

    def setxbox(self):
        self.xbox.setValue(self.sliderx.value())

    def setybox(self):
        self.ybox.setValue(self.slidery.value())

    def setzbox(self):
        self.zbox.setValue(self.sliderz.value())
