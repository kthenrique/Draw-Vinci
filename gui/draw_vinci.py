# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Draw-Vinci.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(409, 561)
        MainWindow.setMinimumSize(QtCore.QSize(409, 558))
        MainWindow.setStyleSheet("")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.canvas = QtWidgets.QGraphicsView(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(10, 40, 390, 310))
        self.canvas.setMinimumSize(QtCore.QSize(390, 310))
        self.canvas.setMaximumSize(QtCore.QSize(390, 310))
        self.canvas.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.canvas.setObjectName("canvas")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 360, 390, 151))
        self.tabWidget.setMinimumSize(QtCore.QSize(390, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(390, 16777215))
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.lineButton = QtWidgets.QPushButton(self.tab)
        self.lineButton.setGeometry(QtCore.QRect(50, 10, 27, 27))
        self.lineButton.setObjectName("lineButton")
        self.ellipseButton = QtWidgets.QPushButton(self.tab)
        self.ellipseButton.setGeometry(QtCore.QRect(50, 50, 27, 27))
        self.ellipseButton.setObjectName("ellipseButton")
        self.rectangleButton = QtWidgets.QPushButton(self.tab)
        self.rectangleButton.setGeometry(QtCore.QRect(50, 90, 27, 27))
        self.rectangleButton.setObjectName("rectangleButton")
        self.pushButton_15 = QtWidgets.QPushButton(self.tab)
        self.pushButton_15.setGeometry(QtCore.QRect(170, 10, 27, 27))
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_16 = QtWidgets.QPushButton(self.tab)
        self.pushButton_16.setGeometry(QtCore.QRect(170, 50, 27, 27))
        self.pushButton_16.setObjectName("pushButton_16")
        self.pushButton_17 = QtWidgets.QPushButton(self.tab)
        self.pushButton_17.setGeometry(QtCore.QRect(170, 90, 27, 27))
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(self.tab)
        self.pushButton_18.setGeometry(QtCore.QRect(300, 10, 27, 27))
        self.pushButton_18.setObjectName("pushButton_18")
        self.pushButton_19 = QtWidgets.QPushButton(self.tab)
        self.pushButton_19.setGeometry(QtCore.QRect(300, 50, 27, 27))
        self.pushButton_19.setObjectName("pushButton_19")
        self.pushButton_20 = QtWidgets.QPushButton(self.tab)
        self.pushButton_20.setGeometry(QtCore.QRect(300, 90, 27, 27))
        self.pushButton_20.setObjectName("pushButton_20")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.upButton = QtWidgets.QPushButton(self.tab_2)
        self.upButton.setGeometry(QtCore.QRect(40, 10, 31, 21))
        self.upButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/up.png) 0 ;\n"
"}\n"
"\n"
" QPushButton:hover {\n"
"    border-image: url(./img/up_hover.png) 0;\n"
" }\n"
"\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/up_click.png) 0;\n"
" }")
        self.upButton.setText("")
        self.upButton.setObjectName("upButton")
        self.leftButton = QtWidgets.QPushButton(self.tab_2)
        self.leftButton.setGeometry(QtCore.QRect(20, 30, 21, 31))
        self.leftButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/left.png) -1;\n"
" }\n"
"\n"
" QPushButton:hover {\n"
"    border-image: url(./img/left_hover.png) 0;\n"
" }\n"
"\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/left_click.png) 0;\n"
" }")
        self.leftButton.setText("")
        self.leftButton.setObjectName("leftButton")
        self.rightButton = QtWidgets.QPushButton(self.tab_2)
        self.rightButton.setGeometry(QtCore.QRect(70, 30, 21, 31))
        self.rightButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/right.png) -1;\n"
" }\n"
"\n"
" QPushButton:hover {\n"
"    border-image: url(./img/right_hover.png) 0;\n"
" }\n"
"\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/right_click.png) 0;\n"
" }")
        self.rightButton.setText("")
        self.rightButton.setObjectName("rightButton")
        self.downButton = QtWidgets.QPushButton(self.tab_2)
        self.downButton.setGeometry(QtCore.QRect(40, 60, 31, 21))
        self.downButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/down.png) -1;\n"
" }\n"
"\n"
" QPushButton:hover {\n"
"    border-image: url(./img/down_hover.png) 0;\n"
" }\n"
"\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/down_click.png) 0;\n"
" }")
        self.downButton.setText("")
        self.downButton.setObjectName("downButton")
        self.penButton = QtWidgets.QPushButton(self.tab_2)
        self.penButton.setGeometry(QtCore.QRect(40, 30, 31, 31))
        self.penButton.setAutoFillBackground(False)
        self.penButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/pen_off.png) 0 ;\n"
"}\n"
" QPushButton:hover {\n"
"    border-image: url(./img/pen_off_hover.png) 0;\n"
" }\n"
"\n"
" QPushButton:on  {\n"
"    border-image: url(./img/pen_on.png) 0;\n"
" }")
        self.penButton.setText("")
        self.penButton.setCheckable(True)
        self.penButton.setDefault(False)
        self.penButton.setFlat(False)
        self.penButton.setObjectName("penButton")
        self.termEdit = QtWidgets.QTextEdit(self.tab_2)
        self.termEdit.setGeometry(QtCore.QRect(260, 10, 121, 101))
        self.termEdit.setStyleSheet(" QTextEdit{\n"
"    background-color: rgb(76, 76, 76);\n"
"    border-radius: 1px;\n"
" }")
        self.termEdit.setObjectName("termEdit")
        self.portsBox = QtWidgets.QComboBox(self.tab_2)
        self.portsBox.setGeometry(QtCore.QRect(140, 10, 111, 27))
        self.portsBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.portsBox.setObjectName("portsBox")
        self.connectButton = QtWidgets.QPushButton(self.tab_2)
        self.connectButton.setGeometry(QtCore.QRect(140, 40, 71, 27))
        self.connectButton.setObjectName("connectButton")
        self.promptEdit = QtWidgets.QLineEdit(self.tab_2)
        self.promptEdit.setGeometry(QtCore.QRect(140, 80, 113, 27))
        self.promptEdit.setStyleSheet("QLineEdit {\n"
"background-color: rgb(255, 255, 255);\n"
" }")
        self.promptEdit.setObjectName("promptEdit")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(9, 90, 101, 21))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.stopButton = QtWidgets.QPushButton(self.groupBox_2)
        self.stopButton.setGeometry(QtCore.QRect(60, 0, 21, 21))
        self.stopButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/stop.png) -1;\n"
" }\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/stop_pressed.png) 0;\n"
" }")
        self.stopButton.setText("")
        self.stopButton.setCheckable(True)
        self.stopButton.setChecked(True)
        self.stopButton.setAutoExclusive(True)
        self.stopButton.setObjectName("stopButton")
        self.speedUpButton = QtWidgets.QPushButton(self.groupBox_2)
        self.speedUpButton.setGeometry(QtCore.QRect(80, 0, 21, 21))
        self.speedUpButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/speed_up.png) -1;\n"
" }\n"
" QPushButton::hover {\n"
" }\n"
"\n"
" QPushButton:pressed {\n"
"\n"
" }\n"
"\n"
"")
        self.speedUpButton.setText("")
        self.speedUpButton.setCheckable(False)
        self.speedUpButton.setObjectName("speedUpButton")
        self.playButton = QtWidgets.QPushButton(self.groupBox_2)
        self.playButton.setGeometry(QtCore.QRect(40, 0, 21, 21))
        self.playButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/play.png) -1;\n"
" }\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/play_pressed.png) 0;\n"
" }")
        self.playButton.setText("")
        self.playButton.setCheckable(True)
        self.playButton.setAutoExclusive(True)
        self.playButton.setObjectName("playButton")
        self.pauseButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pauseButton.setGeometry(QtCore.QRect(20, 0, 21, 21))
        self.pauseButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/pause.png) -1;\n"
" }\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/pause_pressed.png) 0;\n"
" }")
        self.pauseButton.setText("")
        self.pauseButton.setCheckable(True)
        self.pauseButton.setAutoExclusive(True)
        self.pauseButton.setObjectName("pauseButton")
        self.slowDownButton = QtWidgets.QPushButton(self.groupBox_2)
        self.slowDownButton.setGeometry(QtCore.QRect(0, 0, 21, 21))
        self.slowDownButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/slow_down.png) -1;\n"
" }\n"
"\n"
" QPushButton::hover {\n"
" }\n"
"\n"
" QPushButton:pressed {\n"
"\n"
" }\n"
"\n"
"")
        self.slowDownButton.setText("")
        self.slowDownButton.setObjectName("slowDownButton")
        self.refreshButton = QtWidgets.QPushButton(self.tab_2)
        self.refreshButton.setGeometry(QtCore.QRect(220, 40, 31, 27))
        self.refreshButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/port_refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon)
        self.refreshButton.setObjectName("refreshButton")
        self.groupBox_2.raise_()
        self.upButton.raise_()
        self.leftButton.raise_()
        self.rightButton.raise_()
        self.downButton.raise_()
        self.penButton.raise_()
        self.termEdit.raise_()
        self.portsBox.raise_()
        self.connectButton.raise_()
        self.promptEdit.raise_()
        self.refreshButton.raise_()
        self.tabWidget.addTab(self.tab_2, "")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 161, 21))
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName("groupBox")
        self.manualButton = QtWidgets.QPushButton(self.groupBox)
        self.manualButton.setGeometry(QtCore.QRect(90, 0, 71, 21))
        self.manualButton.setMinimumSize(QtCore.QSize(0, 0))
        self.manualButton.setStyleSheet("")
        self.manualButton.setCheckable(True)
        self.manualButton.setAutoExclusive(True)
        self.manualButton.setObjectName("manualButton")
        self.autoButton = QtWidgets.QPushButton(self.groupBox)
        self.autoButton.setGeometry(QtCore.QRect(0, 0, 71, 21))
        self.autoButton.setMinimumSize(QtCore.QSize(10, 0))
        self.autoButton.setStyleSheet("")
        self.autoButton.setCheckable(True)
        self.autoButton.setChecked(True)
        self.autoButton.setAutoExclusive(True)
        self.autoButton.setObjectName("autoButton")
        self.groupBox.raise_()
        self.canvas.raise_()
        self.tabWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 409, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSetup = QtWidgets.QMenu(self.menubar)
        self.menuSetup.setObjectName("menuSetup")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionLicense = QtWidgets.QAction(MainWindow)
        self.actionLicense.setObjectName("actionLicense")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuSetup.addAction(self.actionPreferences)
        self.menuAbout.addAction(self.actionLicense)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetup.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Draw-Vinci"))
        self.lineButton.setText(_translate("MainWindow", "PushButton"))
        self.ellipseButton.setText(_translate("MainWindow", "PushButton"))
        self.rectangleButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_15.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_16.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_17.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_18.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_19.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_20.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Draw"))
        self.penButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Pen Up</span></p></body></html>"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.refreshButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Refresh Ports</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Control"))
        self.manualButton.setText(_translate("MainWindow", "Manual"))
        self.autoButton.setText(_translate("MainWindow", "Auto"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSetup.setTitle(_translate("MainWindow", "Settings"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As ..."))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionLicense.setText(_translate("MainWindow", "License"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))

