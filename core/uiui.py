import sys
import os
import scipy.io as sio
from PyQt5.QtWidgets import QMainWindow, QFileDialog, qApp, QApplication, QWidget, QLabel, QAction, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QStackedWidget, QStatusBar, QSlider, QScrollArea, QDialog
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtGui import QPixmap, QIcon, QCloseEvent, QImage
from PyQt5.QtCore import QTimer, Qt, QCoreApplication, QSize
import inc.simens_dadm as smns
import inc.module11 as mod11
import inc.module12 as mod12
from inc.constants import *
from inc.visualization import visualize
from inc.visualize_6 import visualise6


class ImageDialog(QMainWindow):
    def __init__(self, communicator):
        super().__init__()
        self.setMinimumSize(800,600)
        self.setMaximumSize(1920,1080)
        self.setWindowTitle("SieMRI")
        self.setWindowIcon(QIcon('ikona.jpg'))
        self.TIMER_1 = QTimer()
        self.mri_data = smns.mri_diff
        self.moelo11 = []
        self.moelo12 = []
        self.upsd = QDialog()
        self.init_ui(communicator)

    def closeEvent(self, a0: QCloseEvent):
        QCoreApplication.instance().quit()

    def init_ui(self, communicator):


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
        self.actionTensor.triggered.connect(lambda: self.mb_action_Tensor_triggerd(communicator))

        self.actionSegment.triggered.connect(lambda: self.mb_action_Segment_triggered(communicator))
        self.actionUpsamp.triggered.connect(lambda: self.mb_action_Upsample_triggered(communicator))
        self.action3d.triggered.connect(self.mb_actions_brain3D_triggered)
        self.actionOoqImag.triggered.connect(self.mb_action_OoqImag_triggered)

        actionQuit.triggered.connect(lambda: self.mb_file_exit_trigger(communicator))

        self.TIMER_1.timeout.connect(lambda: self.receive_data(communicator))

        #DO USUNIĘCIA
        self.actionOoqImag.setEnabled(True)
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
        self.upsd.setWindowTitle('Upsampling')
        self.upsd.btn_acc = QPushButton('Accept')
        self.upsd.label = QLabel('Upsample times:')
        self.upsd.times = QSpinBox()
        self.upsd.times.setMinimum(2)
        self.upsd.times.setMaximum(5)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.upsd.label)
        hlayout.addWidget(self.upsd.times)

        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.upsd.btn_acc)
        self.upsd.setLayout(vlayout)
        self.upsd.show()

        self.upsd.btn_acc.clicked.connect(lambda: self.mb_action_Upsample_send(communicator,self.upsd.times.value()))
        self.upsd.setFixedSize(200,100)


    def mb_action_Upsample_send(self,communicator, times):
        self.upsd.close()
        communicator.gui_says.put(smns.simens_msg(MODULE_10_STR, times))
        self.disable_menu()
        self.TIMER_1.start()

    def mb_actions_brain3D_triggered(self):
        def mb_actions_brain3D_triggered(self):
            segmentation = sio.loadmat('../Data/Module_11_test/testSegmentation.mat')
            segmentation = segmentation['mri_segMask']

            struct = smns.mri_struct()
            struct.segmentation = segmentation

            self.moelo11 = mod11.main11(struct)
            self.moelo11.show()

    def mb_action_OoqImag_triggered(self):
        data = self.mri_data.structural_data
        self.moelo12 =  mod12.main12(data)
        self.moelo12.show()

    def receive_data(self, communicator):
        if not communicator.core_says.empty():
            x = communicator.core_says.get()

            if(isinstance(x, smns.simens_msg)):
                self.action_complete()
                self.TIMER_1.stop()
                self.mb_actions.setEnabled(True)
                self.mri_data = x.arguments
                if x.module == 'data':
                    if isinstance(self.mri_data,smns.mri_diff):
                        print('Dyfuzyjne')
                        read = basic_window_diffusive(self.mri_data.diffusion_data.shape[2],self.mri_data.diffusion_data.shape[3], 'read', self.mri_data.diffusion_data)
                        self.actionNonStatLMMSE.setEnabled(True)
                        self.actionNonStatUNLM.setEnabled(True)
                        self.actionOoqImag.setEnabled(True)
                        self.actionIntensity.setEnabled(True)
                    else:
                        read = basic_window(self.mri_data.structural_data.shape[2], 'read', self.mri_data.structural_data)
                        self.actionNonStatLMMSE.setEnabled(True)
                        self.actionNonStatUNLM.setEnabled(True)
                        self.actionUpsamp.setEnabled(True)
                        self.actionOoqImag.setEnabled(True)
                        self.actionIntensity.setEnabled(True)
                    read.btn_skull_strip.clicked.connect(lambda: self.skull_strip_clicked(communicator))
                    self.central.addWidget(read)
                    self.central.setCurrentWidget(read)


                elif x.module == MODULE_2_STR:
                    if isinstance(self.mri_data, smns.mri_diff):
                        print('Dyfuzyjne')
                        intens = basic_window_diffusive(self.mri_data.diffusion_data.shape[2],self.mri_data.diffusion_data.shape[3], 'intens', self.mri_data.diffusion_data)
                        self.actionTensor.setEnabled(True)
                    else:
                        intens = basic_window(self.mri_data.structural_data.shape[2], 'intens', self.mri_data.structural_data)


                    self.actionOoqImag.setEnabled(True)
                    self.central.addWidget(intens)
                    self.central.setCurrentWidget(intens)

                elif x.module == MODULE_4_STR:
                    if isinstance(self.mri_data,smns.mri_diff):
                        print('Dyfuzyjne')
                        LMMSE = basic_window_diffusive(self.mri_data.diffusion_data.shape[2],self.mri_data.diffusion_data.shape[3], 'LMMSE', self.mri_data.diffusion_data)
                    else:
                        LMMSE = basic_window(self.mri_data.structural_data.shape[2],'LMMSE', self.mri_data.structural_data)
                        self.actionUpsamp.setEnabled(True)
                    if self.mri_data.skull_stripping_mask is not []:
                        self.actionIntensity.setEnabled(True)
                    self.actionOoqImag.setEnabled(True)
                    LMMSE.btn_skull_strip.clicked.connect(lambda: self.skull_strip_clicked(communicator))
                    self.central.addWidget(LMMSE)
                    self.central.setCurrentWidget(LMMSE)

                elif x.module == MODULE_5_STR:
                    if isinstance(self.mri_data,smns.mri_diff):
                        print('Dyfuzyjne')
                        UNLM = basic_window_diffusive(self.mri_data.diffusion_data.shape[2],self.mri_data.diffusion_data.shape[3], 'UNLM', self.mri_data.diffusion_data)

                    else:
                        UNLM = basic_window(self.mri_data.structural_data.shape[2], 'ULM', self.mri_data.structural_data)
                        self.actionUpsamp.setEnabled(True)

                    self.actionOoqImag.setEnabled(True)
                    if self.mri_data.skull_stripping_mask is not []:
                        self.actionIntensity.setEnabled(True)
                    UNLM.btn_skull_strip.clicked.connect(lambda: self.skull_strip_clicked(communicator))
                    self.central.addWidget(UNLM)
                    self.central.setCurrentWidget(UNLM)

                elif x.module == MODULE_6_STR:
                    tensor = visualise6(self.mri_data.biomarkes)
                    self.actionOoqImag.setEnabled(True)
                    self.central.addWidget(tensor)
                    self.central.setCurrentWidget(tensor)

                elif x.module == MODULE_8_STR:
                    if isinstance(self.mri_data,smns.mri_diff):
                        pass
                    else:
                        skull = basic_window(self.mri_data.structural_data.shape[2], 'skull',
                                            self.mri_data.structural_data)
                        skull.btn_skull_strip.setEnabled(False)

                        self.central.addWidget(skull)
                        self.central.setCurrentWidget(skull)

                    if self.mri_data.filtering_allowed:
                        self.actionNonStatLMMSE.setEnabled(True)
                        self.actionNonStatUNLM.setEnabled(True)
                    if self.mri_data.inhomogenity_correction_allowed:
                        self.actionIntensity.setEnabled(True)
                        self.actionSegment.setEnabled(True)

                elif x.module == MODULE_9_STR:
                    if isinstance(self.mri_data, smns.mri_diff):
                        pass
                    else:
                        segment = basic_window(self.mri_data.structural_data.shape[2], 'seg', self.mri_data.structural_data)
                        self.central.addWidget(segment)
                        self.central.setCurrentWidget(segment)
                    self.actionOoqImag.setEnabled(True)
                    self.action3d.setEnabled(True)

                elif x.module == MODULE_10_STR:
                    if isinstance(self.mri_data,smns.mri_diff):
                        upsl = basic_window(self.mri_data.structural_data.shape[2], 'ups', self.mri_data.structural_data)
                    else:
                        upsl = basic_window(self.mri_data.structural_data.shape[2], 'ups', self.mri_data.structural_data)
                    self.actionOoqImag.setEnabled(True)
                    self.action3d.setEnabled(True)
                    self.central.addWidget(upsl)
                    self.central.setCurrentWidget(upsl)

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
        # self.action3d.setEnabled(False)
        self.actionOoqImag.setEnabled(False)


class basic_window(QWidget):
    def __init__(self, slices, btnname, data):
        super().__init__()
        self.data = data
        self.init_ui(slices, btnname, data)

    def init_ui(self, slices, btnname, data):
        main_layout = QHBoxLayout()
        self.button_list = []
        left_Vlay = QVBoxLayout()

        self.number = slices

        if data is not None:
            self.main_slice = visualize(data[:,:,0])
        else:
            self.main_slice = QLabel()
        self.main_slice.setMinimumSize(400,400)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(slices)
        self.slider.setSingleStep(1)
        left_Vlay.addWidget(self.main_slice)
        left_Vlay.addWidget(self.slider)
        left_Vlay.setAlignment(Qt.AlignCenter)

        right_Vlay = QVBoxLayout()
        self.btn_skull_strip = QPushButton('Skull Striping')
        self.btn_skull_strip.setFixedSize(200,50)

        slices_viewer = QScrollArea()
        slices_viewer.setMinimumHeight(200)
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
            numero = str(i+1)
            name_tmp.append(numero)
            obj_name = ''.join(name_tmp)
            temp.setObjectName(obj_name)
            if i == 0:
                temp.setEnabled(False)
            self.button_list.append(temp)
            self.button_list[i].clicked.connect(lambda: self.slice_clicked(int(numero)))
            scrollLayout.addWidget(temp)
        slices_viewer.setWidget(scrollContent)
        right_Vlay.addWidget(slices_viewer)
        right_Vlay.addWidget(self.btn_skull_strip)

        main_layout.addSpacing(20)
        main_layout.addLayout(left_Vlay)
        main_layout.addSpacing(20)
        main_layout.addLayout(right_Vlay)
        self.setLayout(main_layout)
        self.slider.valueChanged.connect(lambda: self.slider_change(btnname))


    def slice_clicked(self, number):
        self.enable_all()
        slice_ = self.button_list[number]
        slice_.setEnabled(False)
        self.main_slice = visualize(self.data[:,:,number])
        self.main_slice.repaint()


    def slider_change(self, btnname):
        self.enable_all()
        name_tmp = []
        name_tmp.append(btnname)
        name_tmp.append("{}".format(self.slider.value()))
        obj_name = ''.join(name_tmp)
        slice_ = self.findChild(QPushButton, obj_name)
        slice_.setEnabled(False)
        self.main_slice = visualize(self.data[:,:,(self.slider.value()-1)])
        self.main_slice.repaint()

    def enable_all(self):
        for i in range (0, self.number):
            slice_ = self.button_list[i]
            slice_.setEnabled(True)


class basic_window_diffusive(QWidget):
    def __init__(self, slices, gradients, btnname, data):
        super().__init__()
        self.init_ui(slices, gradients, btnname, data)

    def init_ui(self, slices, gradients, btnname, data):
        self.number = slices
        self.button_list = []
        self.data = data
        main_layout = QHBoxLayout()
        left_Vlay = QVBoxLayout()
        main_widget = QScrollArea()
        main_widget.setMinimumSize(500, 500)
        main_widget.setWidgetResizable(False)
        self.scrollContent = QWidget(main_widget)
        scrollLayout = QHBoxLayout(self.scrollContent)
        scrollLayout.setAlignment(Qt.AlignCenter)
        self.scrollContent.setLayout(scrollLayout)
        for i in range(0, slices):
            new_data = data[:,:,i,0]
            temp = visualize(new_data)
            temp.setMinimumSize(500, 500)
            scrollLayout.addWidget(temp)
        main_widget.setWidget(self.scrollContent)
        left_Vlay.addWidget(main_widget)
        left_Vlay.setAlignment(Qt.AlignCenter)
        right_Vlay = QVBoxLayout()

        self.btn_skull_strip = QPushButton('Skull Striping')
        self.btn_skull_strip.setFixedSize(200, 50)
        #
        self.gradient_viewer = QScrollArea()
        self.gradient_viewer.setMinimumHeight(400)
        self.gradient_viewer.setFixedWidth(200)
        self.gradient_viewer.setWidgetResizable(True)
        sndscrollContent = QWidget(self.gradient_viewer)
        sndscrollLayout = QVBoxLayout(sndscrollContent)
        sndscrollContent.setLayout(sndscrollLayout)
        for i in range(0, gradients):
            tempus = QPushButton()
            tempus.setFixedSize(150, 150)
            name_tmp = []
            name_tmp.append(btnname)
            numero = str(i + 1)
            name_tmp.append(numero)
            obj_name = ''.join(name_tmp)
            tempus.setObjectName(obj_name)
            self.button_list.append(tempus)
            self.button_list[i].clicked.connect(lambda: self.slice_clicked(int(numero)))
            scrollLayout.addWidget(tempus)
            sndscrollLayout.addWidget(tempus)
        self.gradient_viewer.setWidget(sndscrollContent)

        right_Vlay.addWidget(self.gradient_viewer)
        right_Vlay.addWidget(self.btn_skull_strip)

        main_layout.addSpacing(20)
        main_layout.addLayout(left_Vlay)
        main_layout.addSpacing(20)
        main_layout.addLayout(right_Vlay)
        self.setLayout(main_layout)

    def enable_all(self):
        for i in range(0, self.number):
            slice_ = self.button_list[i]
            slice_.setEnabled(True)

    def slice_clicked(self, number):
        self.enable_all()
        slice_ = self.button_list[number]
        slice_.setEnabled(False)
        scrollLayout = QHBoxLayout(self.scrollContent)
        scrollLayout.setAlignment(Qt.AlignCenter)
        self.scrollContent.setLayout(scrollLayout)
        for i in range(0, self.number):
            new_data = self.data[:, :, i, number]
            temp = visualize(new_data)
            temp.setMinimumSize(500, 500)
            scrollLayout.addWidget(temp)
        self.gradient_viewer.setWidget(self.scrollContent)

def launch_gui(communicator):
    app = QApplication(sys.argv)
    window = ImageDialog(communicator)
    sys.exit(app.exec_())