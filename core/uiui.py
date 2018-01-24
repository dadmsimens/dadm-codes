import sys
import os
import scipy.io as sio
from PyQt5.QtWidgets import QMainWindow, QFileDialog, qApp, QApplication, QWidget, QLabel, QAction, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QStackedWidget, QStatusBar, QSlider, QScrollArea, QDialog
from PyQt5.QtGui import QPixmap, QIcon, QCloseEvent
from PyQt5.QtCore import QTimer, Qt, QSize, QCoreApplication
import inc.simens_dadm as smns
import inc.module11 as mod11
import inc.module12_ui as mod12
from inc.constants import *
from inc.visualization import visualize


class ImageDialog(QMainWindow):
    def __init__(self, communicator):
        super().__init__()
        self.setMinimumSize(1024,768)
        self.setMaximumSize(1920,1080)
        self.setWindowTitle("SieMRI")
        self.setWindowIcon(QIcon('ikona.jpg'))
        self.init_ui(communicator)

    def closeEvent(self, a0: QCloseEvent):
        QCoreApplication.instance().quit()

    def init_ui(self, communicator):
        self.TIMER_1 = QTimer()
        self.mri_data = []
        self.moelo11 = []
        self.moelo12 = []
        self.ups = []

        self.central = QStackedWidget()
        self.setCentralWidget(self.central)

        self.fool = basic_window(0,'fool', None)
        self.central.addWidget(self.fool)

        #Create Menu Bar
        self.menu_bar = self.menuBar()

        #Create Root Menus
        self.mb_file = self.menu_bar.addMenu('&File')
        self.mb_actions = self.menu_bar.addMenu('&Procedures')
        self.mb_actions_NonStat = self.mb_actions.addMenu('&Nonstationary noise filtration')

        #Create Actions for menus
        self.actionNew_patient = QAction('&New patient', self)
        self.actionNew_patient.setShortcut("Ctrl+N")

        actionQuit = QAction('&Quit',self)
        actionQuit.setShortcut("Ctrl+Q")
        actionQuit.setStatusTip('Leave The App')
        self.actionUpsamp  = QAction('&Upsampling', self)

        self.actionNonStatLMMSE = QAction('LMMSE', self)
        self.actionNonStatUNLM  = QAction('UNLM', self)


        self.actionIntensity  = QAction('&Intensity inhomogeneity correction', self)
        self.actionTensor = QAction('&Diffusion tensor imaging', self)
        self.actionSegment = QAction('&Segmentation',self)
        self.action3d =  QAction('&Visualisation 3D', self)
        self.actionOoqImag = QAction('&Oblique imaging', self)

        #Add actions to menus
        self.mb_file.addAction(self.actionNew_patient)
        self.mb_file.addSeparator()
        self.mb_file.addAction(actionQuit)

        self.mb_actions_NonStat.addAction(self.actionNonStatLMMSE)
        self.mb_actions_NonStat.addAction(self.actionNonStatUNLM)
        self.mb_actions.addAction(self.actionIntensity)
        self.mb_actions.addAction(self.actionSegment)
        self.mb_actions.addAction(self.actionUpsamp)
        self.mb_actions.addAction(self.actionTensor)
        self.mb_actions.addSeparator()
        self.mb_actions.addAction(self.action3d)
        self.mb_actions.addAction(self.actionOoqImag)
        self.disable_menu()

        #Create status bar
        self.statusBar = QStatusBar()
        self.statusMsg = QLabel()
        self.statusBar.addWidget(self.statusMsg)
        self.setStatusBar(self.statusBar)
        self.statusMsg.setText('Load data to start')

        #image into

        # Events
        self.actionNew_patient.triggered.connect(lambda: self.mb_file_new_trigger(communicator))
        self.actionIntensity.triggered.connect(lambda: self.mb_actions_Intesity_triggered(communicator))
        self.actionNonStatLMMSE.triggered.connect(lambda: self.mb_actions_LMSE_triggered(communicator))
        self.actionNonStatUNLM.triggered.connect(lambda: self.mb_actions_UNLM_triggered(communicator))

        self.actionUpsamp.triggered.connect(lambda: self.mb_action_Upsample_triggered(communicator))
        self.action3d.triggered.connect(self.mb_actions_brain3D_triggered)
        self.actionOoqImag.triggered.connect(self.mb_action_OoqImag_triggered)

        actionQuit.triggered.connect(lambda: self.mb_file_exit_trigger(communicator))


        self.TIMER_1.timeout.connect(lambda: self.receive_data(communicator))

        #DO USUNIĘCIA
        self.action3d.setEnabled(True)
        self.actionOoqImag.setEnabled(True)
        self.actionUpsamp.setEnabled(True)
        ##First showing of the window
        self.show()

    ##Menu functionality:
    def mb_file_new_trigger(self, communicator):
        open_file = QFileDialog()
        filename = open_file.getOpenFileName(self, 'Choose image', os.getenv('HOME'),
                                              'MRI Files *.mat')
        if filename[0] is not "":
            # print(filename[0])
            communicator.gui_says.put(smns.simens_msg('read', filename[0]))
            self.TIMER_1.start()
            self.central.setCurrentWidget(self.fool)

    def mb_file_exit_trigger(self, communicator):
        communicator.exit_event.set()
        qApp.quit()

        ##
    def mb_actions_Intesity_triggered(self, communicator):
        communicator.gui_says.put(smns.simens_msg(MODULE_2_STR, None))
        self.disable_menu()
        self.TIMER_1.start()

    def mb_actions_LMSE_triggered(self, communicator):
        communicator.gui_says.put(smns.simens_msg(MODULE_4_STR, None))
        self.disable_menu()
        self.TIMER_1.start()

    def mb_actions_UNLM_triggered(self, communicator):
        communicator.gui_says.put(smns.simens_msg(MODULE_5_STR, None))
        self.disable_menu()
        self.TIMER_1.start()

    def mb_action_Tensor_triggerd(self, communicator):
        communicator.gui_says.put(smns.simens_msg(MODULE_6_STR, None))
        self.disable_menu()
        self.TIMER_1.start()

    def skull_strip_clicked(self, communicator):
        communicator.gui_says.put(smns.simens_msg(MODULE_8_STR, None))
        self.disable_menu()
        self.TIMER_1.start()

    def mb_action_Segment_triggered(self, communicator):
        communicator.gui_says.put(smns.simens_msg(MODULE_9_STR, None))
        self.disable_menu()
        self.TIMER_1.start()

    def mb_action_Upsample_triggered(self, communicator):

        self.ups = Upsample_dialog()
        self.ups.show()
       # ups.btn_acc.clicked.connect(lambda: self.mb_action_Upsample_send(communicator,2))


    def mb_action_Upsample_send(self,communicator, times):
        communicator.gui_says(smns.simens_msg(MODULE_10_STR,times))
        self.disable_menu()
        self.TIMER_1.start()

    def mb_actions_brain3D_triggered(self):
        #do usunięcia - potrzba danych -
        print('line 174: ustaw sobie swoją scieżkę')
        segmentation = sio.loadmat('C:/Users/Maciej/Desktop/MRI/segmentationMask.mat')
        segmentation = segmentation['imageMaskFull']

        struct = smns.mri_struct()
        struct.segmentation = segmentation

        self.moelo11 = mod11.main11(struct)
        self.moelo11.show()

    def mb_action_OoqImag_triggered(self):
        print('line 185: ustaw sobie swoją scieżkę')
        data = sio.loadmat('C:/Users/Maciej/Desktop/MRI/Imavol.mat')

        Imavol = data['Imavol']

        self.moelo12 =  mod12.Window(Imavol)

    def receive_data(self, communicator):
        if not communicator.core_says.empty():
            x = communicator.core_says.get()

            if(isinstance(x, smns.simens_msg)):
                self.action_complete()
                self.TIMER_1.stop()
                self.mb_actions.setEnabled(True)
                self.statusMsg.setText('Data is ready')
                self.mri_data = x.arguments
                if x.module == 'data':
                    if isinstance(self.mri_data,smns.mri_diff):
                        print('Dyfuzyjne')
                        read = basic_window(self.mri_data.structural_data.shape[2], 'read', self.mri_data.structural_data)
                    else:
                        read = basic_window(self.mri_data.structural_data.shape[2], 'read', self.mri_data.structural_data)
                        self.actionNonStatLMMSE.setEnabled(True)
                        self.actionNonStatUNLM.setEnabled(True)
                        self.actionUpsamp.setEnabled(True)
                        self.actionOoqImag.setEnabled(True)
                        self.actionIntensity.setEnabled(True)
                        self.action3d.setEnabled(True)
                        #
                    self.central.addWidget(read)
                    self.central.setCurrentWidget(read)

                elif x.module == MODULE_2_STR:
                    if isinstance(self.mri_data, smns.mri_diff):
                        print('Dyfuzyjne')
                        intens = basic_window(self.mri_data.structural_data.shape[2], 'intens', self.mri_data.structural_data)
                    else:
                        #intens = QLabel()
                        intens = basic_window(self.mri_data.structural_data.shape[2], 'intens', self.mri_data.structural_data)
                        self.actionOoqImag.setEnabled(True)
                        self.action3d.setEnabled(True)
                    self.central.addWidget(intens)
                    self.central.setCurrentWidget(intens)

                elif x.module == MODULE_4_STR:
                    LMMSE = basic_window(self.mri_data.structural_data.shape[2],'LMMSE', self.mri_data.structural_data)
                    self.actionUpsamp.setEnabled(True)
                    self.actionIntensity.setEnabled(True)
                    self.actionOoqImag.setEnabled(True)
                    self.central.addWidget(LMMSE)
                    self.central.setCurrentWidget(LMMSE)

                elif x.module == MODULE_5_STR:
                    UNLM = basic_window(self.mri_data.structural_data.shape[2], 'ULM', self.mri_data.structural_data)
                    self.actionUpsamp.setEnabled(True)
                    self.actionIntensity.setEnabled(True)
                    self.actionOoqImag.setEnabled(True)
                    self.central.addWidget(UNLM)
                    self.central.setCurrentWidget(UNLM)

                elif x.module == MODULE_6_STR:
                    print('Dyfuzyjne DTI')
                elif x.module == MODULE_8_STR:
                    pass
                elif x.module == MODULE_9_STR:
                     pass
                elif x.module == MODULE_10_STR:
                     pass

            elif (isinstance(x,str)):
                if x == READ_ERROR:
                    self.statusMsg.setText(x)
                    self.TIMER_1.stop()
                else:
                    print(x)
                    self.statusMsg.setText(x)
            # self.central.addWidget(self.basic)
            # self.central.setCurrentWidget(self.basic)

    def action_complete(self):
        self.statusBar.showMessage('Data is ready!')

    def disable_menu(self):
        self.actionNonStatUNLM.setEnabled(False)
        self.actionNonStatLMMSE.setEnabled(False)
        self.actionIntensity.setEnabled(False)
        self.actionSegment.setEnabled(False)
        self.actionUpsamp.setEnabled(False)
        self.actionTensor.setEnabled(False)
        self.action3d.setEnabled(False)
        self.actionOoqImag.setEnabled(False)

    def change_pixmap(self):
        pass


class basic_window(QWidget):
    def __init__(self, slices, btnname, data):
        super().__init__()
        self.init_ui(slices, btnname, data)

    def init_ui(self, slices, btnname, data):
        main_layout = QHBoxLayout()

        left_Vlay = QVBoxLayout()

        self.number = slices
        if data is not None:
            print(data.shape)
            data = data[:,:,0]
            self.main_slice = visualize(data)

        else:
            self.main_slice = QLabel()
        self.main_slice.setMinimumSize(500,650)
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
            name_tmp.append(btnname)
            name_tmp.append(str(i+1))
            obj_name = ''.join(name_tmp)
            print(obj_name)
            temp.setObjectName(obj_name)
            if i == 0:
                temp.setEnabled(False)
            #path_tmp = []
            #path_tmp.append('tmp_images\slice_')
            #path_tmp.append(str(i+1))
            #path = ''.join(path_tmp)
            # current_slice = QPixmap(obj_name)
            # temp.setIcon(QIcon(current_slice))
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
        # self.slider.valueChanged.connect(lambda: self.slider_change(btnname))


    def slice_clicked(self, name):
        self.enable_all()
        slice_ = self.findChild(QPushButton, name)
        slice_.setEnabled(False)
        self.main_slice.setPixmap(QPixmap(name))

    def slider_change(self, btnname):
        self.enable_all(btnname)
        name_tmp = []
        name_tmp.append(btnname)
        name_tmp.append("{}".format(self.slider.value()))
        obj_name = ''.join(name_tmp)
        slice_ = self.findChild(QPushButton, obj_name)
        slice_.setEnabled(False)
        # self.main_slice.setPixmap(QPixmap(obj_name))

    def enable_all(self, btnname):
        for i in range (0, self.number):
            name_tmp = []
            name_tmp.append(btnname)
            name_tmp.append("{}".format(i+1))
            obj_name = ''.join(name_tmp)
            slice_ = self.findChild(QPushButton, obj_name)
            slice_.setEnabled(True)

# class basic_window_diffusive(basic_window):
#     def __init__(self,slices):
#         super().__init__()
#         self.init_ui(slices)
#
#     def init_ui(self, slices):
#         main_layout = QHBoxLayout()
#
#         left_Vlay = QVBoxLayout()
#
#         self.main_slice = QLabel()
#         self.main_slice.setScaledContents(True)
#         self.main_slice.setMinimumSize(500,650)
#         if slices > 0:
#             self.main_slice.setPixmap(QPixmap("tmp_images\slice_1"))
#
#         self.slider = QSlider(Qt.Horizontal)
#         self.slider.setMinimum(1)
#         self.slider.setMaximum(slices)
#         self.slider.setSingleStep(1)
#
#         left_Vlay.addWidget(self.main_slice)
#         left_Vlay.addWidget(self.slider)
#         left_Vlay.setAlignment(Qt.AlignCenter)
#
#         right_Vlay = QVBoxLayout()
#
#         btn_skull_strip = QPushButton('Skull Striping')
#         btn_skull_strip.setFixedSize(200,50)
#
#         slices_viewer = QScrollArea()
#         slices_viewer.setMinimumHeight(550)
#         slices_viewer.setFixedWidth(200)
#         slices_viewer.setWidgetResizable(True)
#         scrollContent = QWidget(slices_viewer)
#         scrollLayout = QVBoxLayout(scrollContent)
#         scrollContent.setLayout(scrollLayout)
#         for i in range (0,slices):
#             temp = QPushButton()
#             temp.setFixedSize(150,150)
#             name_tmp = []
#             name_tmp.append('tmp_images\slice_')
#             name_tmp.append(str(i+1))
#             obj_name = ''.join(name_tmp)
#             temp.setObjectName(obj_name)
#             if i == 0:
#                 temp.setEnabled(False)
#             #path_tmp = []
#             #path_tmp.append('tmp_images\slice_')
#             #path_tmp.append(str(i+1))
#             #path = ''.join(path_tmp)
#             print(obj_name)
#             current_slice = QPixmap(obj_name)
#             temp.setIcon(QIcon(current_slice))
#             temp.setIconSize(QSize(150,150))
#             scrollLayout.addWidget(temp)
#         slices_viewer.setWidget(scrollContent)
#
#         right_Vlay.addWidget(slices_viewer)
#         right_Vlay.addWidget(btn_skull_strip)
#
#         main_layout.addSpacing(20)
#         main_layout.addLayout(left_Vlay)
#         main_layout.addSpacing(20)
#         main_layout.addLayout(right_Vlay)
#         self.setLayout(main_layout)
#
#         for i in range (0,slices):
#             slice_ = self.findChild(QPushButton,"tmp_images\slice_{}".format(i+1))
#             slice_.clicked.connect(lambda: self.slice_clicked(slice_.objectName()))
#
#         self.slider.valueChanged.connect(self.slider_change)


class segmented_window(basic_window):

    def __int__(self, slices, btnname):
        super.__init__()
        self.init_ui(slices,btnname)

    def init_ui(self, slices, btnname):
        pass


class Upsample_dialog(QDialog):
    def __int__(self):
        super().__init__()
        main_widget = QWidget()
        self.btn_acc = QPushButton('Accept')
        print(self.btn_acc)
        vlayout = QVBoxLayout()
        main_widget.addWidget(self.btn_acc)
        vlayout.addWidget(main_widget)
        self.setLayout(vlayout)

def launch_gui(communicator):
    app = QApplication(sys.argv)
    window = ImageDialog(communicator)
    sys.exit(app.exec_())