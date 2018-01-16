# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inc/module11_gui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(760, 505)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 760, 25))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionSagittal = QtWidgets.QAction(MainWindow)
        self.actionSagittal.setObjectName("actionSagittal")
        self.actionAxial = QtWidgets.QAction(MainWindow)
        self.actionAxial.setObjectName("actionAxial")
        self.actionCoronal = QtWidgets.QAction(MainWindow)
        self.actionCoronal.setObjectName("actionCoronal")
        self.actionReturn = QtWidgets.QAction(MainWindow)
        self.actionReturn.setObjectName("actionReturn")
        self.actionClip = QtWidgets.QAction(MainWindow)
        self.actionClip.setObjectName("actionClip")
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionReturn)
        self.menuMenu.addAction(self.actionClip)
        self.menuMenu.addAction(self.actionHelp)
        self.menuMenu.addAction(self.actionExit)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BRAIN 3D"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionSagittal.setText(_translate("MainWindow", "Sagittal"))
        self.actionAxial.setText(_translate("MainWindow", "Axial"))
        self.actionCoronal.setText(_translate("MainWindow", "Coronal"))
        self.actionReturn.setText(_translate("MainWindow", "Return to model view"))
        self.actionClip.setText(_translate("MainWindow", "Clip model"))

