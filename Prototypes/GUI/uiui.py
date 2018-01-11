import sys
import os
import scipy.io as sio
from PyQt5.QtWidgets import QMainWindow, QFileDialog, qApp, QApplication, QWidget, QLabel, QAction, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy, QStackedWidget, QStatusBar, QSlider, QScrollArea
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer,Qt, QSize


class ImageDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1024,768)
        self.setMaximumSize(1920,1080)
        self.setWindowTitle("SieMRI")
        self.setWindowIcon(QIcon('ikona.jpg'))
        self.init_ui()

    def init_ui(self):


        self.TIMER_1 = QTimer()

        self.central = QStackedWidget()
        self.setCentralWidget(self.central)

        self.fool = basic_window(0)
        self.basic = basic_window(10)
        self.central.addWidget(self.fool)


        #Create Menu Bar
        self.menu_bar = self.menuBar()

        #Create Root Menus
        self.mb_file = self.menu_bar.addMenu('&File')
        self.mb_actions = self.menu_bar.addMenu('&Procedures')
        mb_actions_NonStat = self.mb_actions.addMenu('&Nonstationary noise filtration')

        #Create Actions for menus
        actionNew_patient = QAction('&New patient', self)
        actionNew_patient.setShortcut("Ctrl+N")

        actionQuit = QAction('&Quit',self)
        actionQuit.setShortcut("Ctrl+Q")
        actionQuit.setStatusTip('Leave The App')

        actionSqlStrip = QAction('Scull Stripping', self)
        actionUpsamp  = QAction('&Upsampling', self)

        actionNonStatLMMSE = QAction('LMMSE', self)
        actionNonStatUNLM  = QAction('UNLM', self)


        actionIntensity  = QAction('&Intensity inhomogeneity correction', self)
        actionTensor = QAction('&Diffusion tensor imaging', self)
        actionSegment = QAction('&Segmentation',self)
        action3d =  QAction('&Visualisation 3D', self)
        actionOoqImag = QAction('&Oblique imaging', self)

        #Add actions to menus
        self.mb_file.addAction(actionNew_patient)
        self.mb_file.addSeparator()
        self.mb_file.addAction(actionQuit)

        mb_actions_NonStat.addAction(actionNonStatLMMSE)
        mb_actions_NonStat.addAction(actionNonStatUNLM)
        self.mb_actions.addAction(actionIntensity)
        self.mb_actions.addAction(actionSegment)
        self.mb_actions.addAction(actionUpsamp)
        self.mb_actions.addAction(actionTensor)
        self.mb_actions.addSeparator()
        self.mb_actions.addAction(action3d)
        self.mb_actions.addAction(actionOoqImag)

        #Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Waiting for data...')

        #image into

        # Events
        actionNew_patient.triggered.connect(self.mb_file_new_trigger)
        actionQuit.triggered.connect(self.mb_file_exit_trigger)
        self.TIMER_1.timeout.connect(self.receive_data)

    ##Menu functionality:
    def mb_file_new_trigger(self):
        open_file = QFileDialog()
        filename = open_file.getOpenFileName(self, 'Choose image', os.getenv('HOME'),
                                              'MRI Files *.mat')
        return filename
       # if filename:
        # with open(filename, 'r') as file:
         #   current_mri = file.read()

    def mb_file_exit_trigger(self):
        qApp.quit()
        ##

    def receive_data(self):
        received = 'yes'
        self.action_complete()
        print(received)
        self.TIMER_1.stop()
        self.mb_actions.setEnabled(True)
        self.central.addWidget(self.basic)
        self.central.setCurrentWidget(self.basic)

    def action_complete(self):
        self.statusBar.showMessage('Data is ready!')

    def change_pixmap(self):
        pass


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500,400)
        self.setWindowIcon(QIcon('ikona.jpg'))
        self.setWindowTitle('SieMRI')
        self.init_ui()

    def init_ui(self):
        self.btn_open_file= QPushButton('Open file')
        self.btn_open_file.setMinimumHeight(50)
        self.btn_open_file.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Fixed
        )

        self.lab_welcome = QLabel('<h1 align = "center">Welcome to SieMRI!</h1>')
        self.lab_new_patient = QLabel('<h3 align = "center">'
                                      'Open MRI file for new patient'
                                      '</h3>')

        vbox_layout = QVBoxLayout()
        vbox_layout.addSpacing(50)
        vbox_layout.addWidget(self.lab_welcome)
       # vbox_layout.addSpacing(100)
        vbox_layout.addWidget(self.lab_new_patient)
        vbox_layout.addWidget(self.btn_open_file)
        vbox_layout.addSpacing(110)

        hbox_layout = QHBoxLayout()
        hbox_layout.addSpacing(100)
        hbox_layout.addLayout(vbox_layout)
        hbox_layout.addSpacing(100)

        self.setLayout(hbox_layout)

        self.main_window = ImageDialog()

        self.show()

        self.btn_open_file.clicked.connect(lambda: self.open_first_file(self.main_window))



    def open_first_file(self, window):
        filename = window.mb_file_new_trigger()

        window.TIMER_1.start(5000)
        window.mb_actions.setEnabled(False)

        self.main_window.show()
        self.close()
        return filename

    def open_file(self):
        open_file = QFileDialog()
        filename = open_file.getOpenFileName(self, 'Choose image', os.getenv('HOME'),
                                             'MRI Files *.jpg')
        return filename


class basic_window(QWidget):
    def __init__(self,slices):
        super().__init__()
        self.init_ui(slices)

    def init_ui(self, slices):
        main_layout = QHBoxLayout()

        left_Vlay = QVBoxLayout()

        self.main_slice = QLabel()
        self.main_slice.setScaledContents(True)
        self.main_slice.setMinimumSize(500,650)
        if slices > 0:
            self.main_slice.setPixmap(QPixmap("tmp_images\slice_1"))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(slices)
        self.slider.setSingleStep(1)

        left_Vlay.addWidget(self.main_slice)
        left_Vlay.addWidget(self.slider)
        left_Vlay.setAlignment(Qt.AlignCenter)

        right_Vlay = QVBoxLayout()

        btn_skull_strip = QPushButton('Skull Striping')
        btn_skull_strip.setFixedSize(200,50)

        slices_viewer = QScrollArea()
        slices_viewer.setMinimumHeight(550)
        slices_viewer.setFixedWidth(200)
        slices_viewer.setWidgetResizable(True)
        scrollContent = QWidget(slices_viewer)
        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)
        for i in range (0,slices):
            temp = QPushButton()
            temp.setFixedSize(150,150)
            name_tmp = []
            name_tmp.append('tmp_images\slice_')
            name_tmp.append(str(i+1))
            obj_name = ''.join(name_tmp)
            temp.setObjectName(obj_name)
            if i == 0:
                temp.setEnabled(False)
            #path_tmp = []
            #path_tmp.append('tmp_images\slice_')
            #path_tmp.append(str(i+1))
            #path = ''.join(path_tmp)
            current_slice = QPixmap(obj_name)
            temp.setIcon(QIcon(current_slice))
            temp.setIconSize(QSize(150,150))
            scrollLayout.addWidget(temp)
        slices_viewer.setWidget(scrollContent)

        right_Vlay.addWidget(slices_viewer)
        right_Vlay.addWidget(btn_skull_strip)

        main_layout.addSpacing(20)
        main_layout.addLayout(left_Vlay)
        main_layout.addSpacing(20)
        main_layout.addLayout(right_Vlay)
        self.setLayout(main_layout)

        for i in range (0,slices):
            slice_ = self.findChild(QPushButton,"tmp_images\slice_{}".format(i+1))
            slice_.clicked.connect(lambda: self.slice_clicked(slice_.objectName()))

        self.slider.valueChanged.connect(self.slider_change)

    def slice_clicked(self, name):
        self.enable_all()
        slice_ = self.findChild(QPushButton, name)
        slice_.setEnabled(False)
        self.main_slice.setPixmap(QPixmap(name))

    def slider_change(self):
        self.enable_all()
        name = "tmp_images\slice_{}".format(self.slider.value())
        slice_ = self.findChild(QPushButton, name)
        slice_.setEnabled(False)
        self.main_slice.setPixmap(QPixmap(name))

    def enable_all(self):
        for i in range (0,10):
            name = "tmp_images\slice_{}".format(i+1)
            slice_ = self.findChild(QPushButton, name)
            slice_.setEnabled(True)




app = QApplication(sys.argv)
window = StartWindow()
sys.exit(app.exec_())