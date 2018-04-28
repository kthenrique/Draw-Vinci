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
        MainWindow.resize(409, 558)
        MainWindow.setMinimumSize(QtCore.QSize(409, 558))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 30, 390, 310))
        self.graphicsView.setMinimumSize(QtCore.QSize(390, 310))
        self.graphicsView.setMaximumSize(QtCore.QSize(390, 310))
        self.graphicsView.setObjectName("graphicsView")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 350, 391, 151))
        self.groupBox.setObjectName("groupBox")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 390, 151))
        self.tabWidget.setMinimumSize(QtCore.QSize(390, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(390, 16777215))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_12 = QtWidgets.QPushButton(self.tab)
        self.pushButton_12.setGeometry(QtCore.QRect(50, 10, 27, 27))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_13 = QtWidgets.QPushButton(self.tab)
        self.pushButton_13.setGeometry(QtCore.QRect(50, 50, 27, 27))
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_14 = QtWidgets.QPushButton(self.tab)
        self.pushButton_14.setGeometry(QtCore.QRect(50, 90, 27, 27))
        self.pushButton_14.setObjectName("pushButton_14")
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
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 10, 31, 21))
        self.pushButton_3.setStyleSheet(" QPushButton {\n"
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
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 30, 21, 31))
        self.pushButton_4.setStyleSheet(" QPushButton {\n"
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
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_5.setGeometry(QtCore.QRect(70, 30, 21, 31))
        self.pushButton_5.setStyleSheet(" QPushButton {\n"
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
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_6.setGeometry(QtCore.QRect(40, 60, 31, 21))
        self.pushButton_6.setStyleSheet(" QPushButton {\n"
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
        self.pushButton_6.setText("")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_7.setGeometry(QtCore.QRect(40, 30, 31, 31))
        self.pushButton_7.setAutoFillBackground(False)
        self.pushButton_7.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/pen_off.png) 0 ;\n"
"}\n"
" QPushButton:hover {\n"
"    border-image: url(./img/pen_off_hover.png) 0;\n"
" }\n"
"\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/pen_on.png) 0;\n"
" }")
        self.pushButton_7.setText("")
        self.pushButton_7.setDefault(False)
        self.pushButton_7.setFlat(False)
        self.pushButton_7.setObjectName("pushButton_7")
        self.textEdit = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit.setGeometry(QtCore.QRect(260, 10, 121, 101))
        self.textEdit.setObjectName("textEdit")
        self.comboBox = QtWidgets.QComboBox(self.tab_2)
        self.comboBox.setGeometry(QtCore.QRect(140, 10, 111, 27))
        self.comboBox.setObjectName("comboBox")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_8.setGeometry(QtCore.QRect(140, 40, 111, 27))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_9.setGeometry(QtCore.QRect(30, 90, 21, 21))
        self.pushButton_9.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/pause.png) -1;\n"
" }\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/pause_pressed.png) 0;\n"
" }")
        self.pushButton_9.setText("")
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_10.setGeometry(QtCore.QRect(50, 90, 21, 21))
        self.pushButton_10.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/play.png) -1;\n"
" }\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/play_pressed.png) 0;\n"
" }")
        self.pushButton_10.setText("")
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_11.setGeometry(QtCore.QRect(70, 90, 21, 21))
        self.pushButton_11.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/stop.png) -1;\n"
" }\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/stop_pressed.png) 0;\n"
" }")
        self.pushButton_11.setText("")
        self.pushButton_11.setObjectName("pushButton_11")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit.setGeometry(QtCore.QRect(140, 80, 113, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_21 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_21.setGeometry(QtCore.QRect(10, 90, 21, 21))
        self.pushButton_21.setStyleSheet(" QPushButton {\n"
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
        self.pushButton_21.setText("")
        self.pushButton_21.setObjectName("pushButton_21")
        self.pushButton_22 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_22.setGeometry(QtCore.QRect(90, 90, 21, 21))
        self.pushButton_22.setStyleSheet(" QPushButton {\n"
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
        self.pushButton_22.setText("")
        self.pushButton_22.setObjectName("pushButton_22")
        self.tabWidget.addTab(self.tab_2, "")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 0, 201, 31))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 0, 85, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 85, 27))
        self.pushButton.setObjectName("pushButton")
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
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton_12.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_13.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_14.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_15.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_16.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_17.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_18.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_19.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_20.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Draw"))
        self.pushButton_7.setToolTip(_translate("MainWindow", "<html><head/><body><p>Pen Up</p></body></html>"))
        self.pushButton_8.setText(_translate("MainWindow", "Connect"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Control"))
        self.groupBox_2.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton_2.setText(_translate("MainWindow", "Manual"))
        self.pushButton.setText(_translate("MainWindow", "Auto"))
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

