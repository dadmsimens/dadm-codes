from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import Qt
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import module12_core as m12

class Window(QtWidgets.QDialog):
    def __init__(self, parent=None, mri_data = None):
        super(Window, self).__init__(parent)

        self.mri_data = mri_data
        self.xx = []
        self.yy = []
        self.zz = []
        self.rev = False

        # a figure instance to plot on
        self.figure = Figure()
        self.figure2 = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.canvas2 = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtWidgets.QPushButton('Get Oblique Image')
        self.button.clicked.connect(self.plot)

        self.button = QtWidgets.QPushButton('Grid to ooposite end')
        self.button.clicked.connect(self.revf)

        self.sliderx = QtWidgets.QSlider(Qt.Horizontal)
        self.sliderx.setFocusPolicy(Qt.StrongFocus)
        self.sliderx.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderx.setMaximum(360)
        self.sliderx.setMinimum(0)
        self.sliderx.setTickInterval(10)
        self.sliderx.setSingleStep(1)
        self.sliderx.setValue(0)
        self.sliderx.valueChanged.connect(self.plot)

        self.slidery = QtWidgets.QSlider(Qt.Horizontal)
        self.slidery.setFocusPolicy(Qt.StrongFocus)
        self.slidery.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slidery.setMaximum(360)
        self.slidery.setMinimum(0)
        self.slidery.setTickInterval(10)
        self.slidery.setSingleStep(1)
        self.slidery.setValue(0)
        self.slidery.valueChanged.connect(self.plot)

        self.sliderz = QtWidgets.QSlider(Qt.Horizontal)
        self.sliderz.setFocusPolicy(Qt.StrongFocus)
        self.sliderz.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderz.setMaximum(360)
        self.sliderz.setMinimum(0)
        self.sliderz.setTickInterval(10)
        self.sliderz.setSingleStep(1)
        self.sliderz.setValue(0)
        self.sliderz.valueChanged.connect(self.plot)

        self.transbox = QtWidgets.QSpinBox()
        self.transbox.setMaximum(10000)
        self.transbox.setMinimum(-10000)
        self.transbox.setValue(0)
        self.transbox.valueChanged.connect(self.plot)

        # set the layout
        layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.canvas2)
        layout.addWidget(self.button)
        layout.addWidget(self.sliderx)
        layout.addWidget(self.slidery)
        layout.addWidget(self.sliderz)
        layout.addWidget(self.transbox)

        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        sliderxval = self.sliderx.value()
        slideryval = self.slidery.value()
        sliderzval = self.sliderz.value()
        transboxval = self.transbox.value()

        self.xx, self.yy, self.zz = m12.transrotateplane(self.mri_data, sliderxval, slideryval, sliderzval, 0)

        # create an axis
        ax = self.figure.gca(projection='3d', azim=250)

        # discards the old graph
        ax.clear()

        # plot data
        ax.plot_surface(self.xx, self.yy, self.zz)

        # refresh canvas
        self.canvas.draw()

    def getobliqueimage(self):
        interpolatedimage = m12.interpolatemri(self.mri_data, self.xx, self.yy, self.zz)
        ax.imshow(interpolatedimage)
        # splotować

    def revf(self):
        self.rev = ~self.rev

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())