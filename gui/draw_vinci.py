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
        MainWindow.resize(575, 678)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(575, 678))
        MainWindow.setMaximumSize(QtCore.QSize(575, 678))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("svg/logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTip("")
        MainWindow.setStyleSheet("")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.canvas = QtWidgets.QGraphicsView(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(10, 0, 555, 477))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setMinimumSize(QtCore.QSize(555, 477))
        self.canvas.setMaximumSize(QtCore.QSize(555, 477))
        self.canvas.setMouseTracking(True)
        self.canvas.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.canvas.setToolTip("")
        self.canvas.setAutoFillBackground(True)
        self.canvas.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.canvas.setFrameShape(QtWidgets.QFrame.Box)
        self.canvas.setFrameShadow(QtWidgets.QFrame.Plain)
        self.canvas.setLineWidth(1)
        self.canvas.setMidLineWidth(0)
        self.canvas.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.canvas.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.canvas.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.canvas.setSceneRect(QtCore.QRectF(0.0, 0.0, 390.0, 310.0))
        self.canvas.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.canvas.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.canvas.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.canvas.setObjectName("canvas")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 487, 555, 141))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(18)
        sizePolicy.setVerticalStretch(12)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(555, 141))
        self.tabWidget.setMaximumSize(QtCore.QSize(555, 141))
        self.tabWidget.setStyleSheet("QTabWidget::pane { /* The tab widget frame */\n"
"    border-top: 2px solid #C2C7CB;\n"
"    border-left: 2px solid #C2C7CB;\n"
"    border-right: 2px solid #C2C7CB;\n"
" border-bottom: 2px solid #C2C7CB;\n"
"\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    left: 1px; /* move to the right by 5px */\n"
"}\n"
"\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"    border: 2px solid #C4C4C3;\n"
"    border-bottom-color: #C2C7CB; /* same as the pane color */\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 6ex;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,\n"
"                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    border-color: #9B9B9B;\n"
"    border-bottom-color: #C2C7CB; /* same as pane color */\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; /* make non-selected tabs look smaller */\n"
"}\n"
"\n"
"/* make use of negative margins for overlapping tabs */\n"
"QTabBar::tab:selected {\n"
"    /* expand/overlap to the left and right by 4px */\n"
"    margin-left: -4px;\n"
"    margin-right: -4px;\n"
"}\n"
"\n"
"QTabBar::tab:first:selected {\n"
"    margin-left: 0; /* the first selected tab has nothing to overlap with on the left */\n"
"}\n"
"\n"
"QTabBar::tab:last:selected {\n"
"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"}\n"
"\n"
"QTabBar::tab:only-one {\n"
"    margin: 1; /* if there is only one tab, we don\'t want overlapping margins */\n"
"}")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.drawTab = QtWidgets.QWidget()
        self.drawTab.setObjectName("drawTab")
        self.textButton = QtWidgets.QPushButton(self.drawTab)
        self.textButton.setGeometry(QtCore.QRect(110, 60, 41, 41))
        self.textButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/text.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.textButton.setIcon(icon1)
        self.textButton.setCheckable(True)
        self.textButton.setAutoExclusive(True)
        self.textButton.setObjectName("textButton")
        self.selectButton = QtWidgets.QPushButton(self.drawTab)
        self.selectButton.setGeometry(QtCore.QRect(10, 60, 41, 41))
        self.selectButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/select.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.selectButton.setIcon(icon2)
        self.selectButton.setCheckable(True)
        self.selectButton.setAutoExclusive(True)
        self.selectButton.setObjectName("selectButton")
        self.lineButton = QtWidgets.QPushButton(self.drawTab)
        self.lineButton.setGeometry(QtCore.QRect(110, 10, 41, 41))
        self.lineButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lineButton.setIcon(icon3)
        self.lineButton.setCheckable(True)
        self.lineButton.setAutoExclusive(True)
        self.lineButton.setObjectName("lineButton")
        self.polygonButton = QtWidgets.QPushButton(self.drawTab)
        self.polygonButton.setGeometry(QtCore.QRect(260, 10, 41, 41))
        self.polygonButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("img/polygon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.polygonButton.setIcon(icon4)
        self.polygonButton.setCheckable(True)
        self.polygonButton.setAutoExclusive(True)
        self.polygonButton.setObjectName("polygonButton")
        self.eraserButton = QtWidgets.QPushButton(self.drawTab)
        self.eraserButton.setGeometry(QtCore.QRect(10, 10, 41, 41))
        self.eraserButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("img/eraser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.eraserButton.setIcon(icon5)
        self.eraserButton.setCheckable(True)
        self.eraserButton.setChecked(True)
        self.eraserButton.setAutoExclusive(True)
        self.eraserButton.setObjectName("eraserButton")
        self.ellipseButton = QtWidgets.QPushButton(self.drawTab)
        self.ellipseButton.setGeometry(QtCore.QRect(210, 60, 41, 41))
        self.ellipseButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("img/ellipse.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ellipseButton.setIcon(icon6)
        self.ellipseButton.setCheckable(True)
        self.ellipseButton.setAutoExclusive(True)
        self.ellipseButton.setObjectName("ellipseButton")
        self.rectangleButton = QtWidgets.QPushButton(self.drawTab)
        self.rectangleButton.setGeometry(QtCore.QRect(210, 10, 41, 41))
        self.rectangleButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("img/rectangle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rectangleButton.setIcon(icon7)
        self.rectangleButton.setCheckable(True)
        self.rectangleButton.setAutoExclusive(True)
        self.rectangleButton.setObjectName("rectangleButton")
        self.freehandButton = QtWidgets.QPushButton(self.drawTab)
        self.freehandButton.setGeometry(QtCore.QRect(60, 10, 41, 41))
        self.freehandButton.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("img/freehand.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.freehandButton.setIcon(icon8)
        self.freehandButton.setCheckable(True)
        self.freehandButton.setAutoExclusive(True)
        self.freehandButton.setObjectName("freehandButton")
        self.fontBox = QtWidgets.QFontComboBox(self.drawTab)
        self.fontBox.setGeometry(QtCore.QRect(415, 10, 131, 25))
        self.fontBox.setEditable(False)
        self.fontBox.setFrame(True)
        self.fontBox.setObjectName("fontBox")
        self.fontSizeBox = QtWidgets.QComboBox(self.drawTab)
        self.fontSizeBox.setGeometry(QtCore.QRect(415, 40, 55, 25))
        self.fontSizeBox.setMinimumSize(QtCore.QSize(55, 25))
        self.fontSizeBox.setMaximumSize(QtCore.QSize(55, 25))
        self.fontSizeBox.setStyleSheet("QComboBox {\n"
"    border: 1.5px solid gray;\n"
"    border-radius: 5px;\n"
"    min-width: 3em;\n"
"     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 3px;\n"
"}\n"
"")
        self.fontSizeBox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.fontSizeBox.setEditable(True)
        self.fontSizeBox.setObjectName("fontSizeBox")
        self.underlineButton = QtWidgets.QPushButton(self.drawTab)
        self.underlineButton.setGeometry(QtCore.QRect(490, 40, 25, 25))
        self.underlineButton.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("img/underline.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.underlineButton.setIcon(icon9)
        self.underlineButton.setCheckable(True)
        self.underlineButton.setObjectName("underlineButton")
        self.italicButton = QtWidgets.QPushButton(self.drawTab)
        self.italicButton.setGeometry(QtCore.QRect(520, 40, 25, 25))
        self.italicButton.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("img/italic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.italicButton.setIcon(icon10)
        self.italicButton.setCheckable(True)
        self.italicButton.setObjectName("italicButton")
        self.magnifierButton = QtWidgets.QPushButton(self.drawTab)
        self.magnifierButton.setGeometry(QtCore.QRect(60, 60, 41, 41))
        self.magnifierButton.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("img/magnifier.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.magnifierButton.setIcon(icon11)
        self.magnifierButton.setCheckable(True)
        self.magnifierButton.setAutoExclusive(True)
        self.magnifierButton.setObjectName("magnifierButton")
        self.circleButton = QtWidgets.QPushButton(self.drawTab)
        self.circleButton.setGeometry(QtCore.QRect(160, 60, 41, 41))
        self.circleButton.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("img/circle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.circleButton.setIcon(icon12)
        self.circleButton.setCheckable(True)
        self.circleButton.setAutoExclusive(True)
        self.circleButton.setObjectName("circleButton")
        self.squareButton = QtWidgets.QPushButton(self.drawTab)
        self.squareButton.setGeometry(QtCore.QRect(160, 10, 41, 41))
        self.squareButton.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("img/square.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.squareButton.setIcon(icon13)
        self.squareButton.setCheckable(True)
        self.squareButton.setAutoExclusive(True)
        self.squareButton.setObjectName("squareButton")
        self.nextSVGButton = QtWidgets.QPushButton(self.drawTab)
        self.nextSVGButton.setGeometry(QtCore.QRect(310, 10, 91, 91))
        self.nextSVGButton.setText("")
        self.nextSVGButton.setIconSize(QtCore.QSize(50, 50))
        self.nextSVGButton.setObjectName("nextSVGButton")
        self.importButton = QtWidgets.QPushButton(self.drawTab)
        self.importButton.setGeometry(QtCore.QRect(260, 60, 41, 41))
        self.importButton.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("img/import.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.importButton.setIcon(icon14)
        self.importButton.setCheckable(True)
        self.importButton.setAutoExclusive(True)
        self.importButton.setObjectName("importButton")
        self.line_2 = QtWidgets.QFrame(self.drawTab)
        self.line_2.setGeometry(QtCore.QRect(400, 8, 16, 100))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.tabWidget.addTab(self.drawTab, "")
        self.controlTab = QtWidgets.QWidget()
        self.controlTab.setObjectName("controlTab")
        self.upButton = QtWidgets.QPushButton(self.controlTab)
        self.upButton.setGeometry(QtCore.QRect(37, 7, 41, 31))
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
        self.leftButton = QtWidgets.QPushButton(self.controlTab)
        self.leftButton.setGeometry(QtCore.QRect(7, 37, 31, 41))
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
        self.rightButton = QtWidgets.QPushButton(self.controlTab)
        self.rightButton.setGeometry(QtCore.QRect(77, 37, 31, 41))
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
        self.downButton = QtWidgets.QPushButton(self.controlTab)
        self.downButton.setGeometry(QtCore.QRect(37, 77, 41, 31))
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
        self.penButton = QtWidgets.QPushButton(self.controlTab)
        self.penButton.setGeometry(QtCore.QRect(37, 37, 41, 41))
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
        self.termEdit = QtWidgets.QTextEdit(self.controlTab)
        self.termEdit.setGeometry(QtCore.QRect(397, 10, 148, 96))
        font = QtGui.QFont()
        font.setFamily("Tlwg Typewriter")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.termEdit.setFont(font)
        self.termEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.termEdit.setStyleSheet(" QTextEdit{\n"
"    background-color:rgb(0, 17, 44);\n"
"    color: rgb(252, 255, 74);\n"
"    border-radius: 1px;\n"
" }\n"
"\n"
"QScrollBar:vertical {           \n"
"       border: 1px solid #999999;\n"
"   background:white;\n"
"  width:7px;    \n"
"  margin: 0px 0px 0px 0px;\n"
" }\n"
"    QScrollBar::handle:vertical {\n"
"       background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"      stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));\n"
"      min-height: 0px;\n"
"    }\n"
"    QScrollBar::add-line:vertical {\n"
"        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"       stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));\n"
"      height: 0px;\n"
"      subcontrol-position: bottom;\n"
"      subcontrol-origin: margin;\n"
"   }\n"
"    QScrollBar::sub-line:vertical {\n"
"       background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"      stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));\n"
"       height: 0 px;\n"
"       subcontrol-position: top;\n"
"      subcontrol-origin: margin;\n"
"    }\n"
"\n"
"\n"
"")
        self.termEdit.setReadOnly(True)
        self.termEdit.setObjectName("termEdit")
        self.portsBox = QtWidgets.QComboBox(self.controlTab)
        self.portsBox.setGeometry(QtCore.QRect(280, 10, 111, 27))
        self.portsBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.portsBox.setObjectName("portsBox")
        self.connectButton = QtWidgets.QPushButton(self.controlTab)
        self.connectButton.setGeometry(QtCore.QRect(280, 40, 71, 27))
        self.connectButton.setObjectName("connectButton")
        self.promptEdit = QtWidgets.QLineEdit(self.controlTab)
        self.promptEdit.setGeometry(QtCore.QRect(280, 80, 113, 27))
        self.promptEdit.setStyleSheet("QLineEdit {\n"
"background-color: rgb(255, 255, 255);\n"
" }")
        self.promptEdit.setCursorPosition(0)
        self.promptEdit.setClearButtonEnabled(True)
        self.promptEdit.setObjectName("promptEdit")
        self.playButton = QtWidgets.QPushButton(self.controlTab)
        self.playButton.setGeometry(QtCore.QRect(177, 70, 31, 31))
        self.playButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/play_off.svg) 0;\n"
" }\n"
"\n"
" QPushButton:hover {\n"
"    border-image: url(./img/play_hover.svg) 0;\n"
" }\n"
"\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/play_on.svg) 0;\n"
" }\n"
"\n"
" QPushButton:on  {\n"
"    border-image: url(./img/play_on.svg) 0;\n"
" }\n"
"")
        self.playButton.setText("")
        self.playButton.setCheckable(True)
        self.playButton.setAutoExclusive(True)
        self.playButton.setObjectName("playButton")
        self.stopButton = QtWidgets.QPushButton(self.controlTab)
        self.stopButton.setGeometry(QtCore.QRect(207, 70, 31, 31))
        self.stopButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/stop_off.svg) 0;\n"
" }\n"
"\n"
" QPushButton:hover {\n"
"    border-image: url(./img/stop_hover.svg) 0;\n"
" }\n"
"\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/stop_on.svg) 0;\n"
" }\n"
"\n"
" QPushButton:on  {\n"
"    border-image: url(./img/stop_on.svg) 0;\n"
" }\n"
"")
        self.stopButton.setText("")
        self.stopButton.setCheckable(True)
        self.stopButton.setChecked(True)
        self.stopButton.setAutoExclusive(True)
        self.stopButton.setObjectName("stopButton")
        self.nextComButton = QtWidgets.QPushButton(self.controlTab)
        self.nextComButton.setGeometry(QtCore.QRect(237, 70, 31, 31))
        self.nextComButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/speed_up.svg) 0;\n"
" }\n"
"\n"
" QPushButton:hover {\n"
"    border-image: url(./img/speed_up_hover.svg) 0;\n"
" }\n"
"\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/speed_up_pressed.svg) 0;\n"
" }")
        self.nextComButton.setText("")
        self.nextComButton.setCheckable(False)
        self.nextComButton.setObjectName("nextComButton")
        self.pauseButton = QtWidgets.QPushButton(self.controlTab)
        self.pauseButton.setGeometry(QtCore.QRect(147, 70, 31, 31))
        self.pauseButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/pause_off.svg) 0;\n"
" }\n"
"\n"
" QPushButton:hover {\n"
"    border-image: url(./img/pause_hover.svg) 0;\n"
" }\n"
"\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/pause_on.svg) 0;\n"
" }\n"
"\n"
" QPushButton:on  {\n"
"    border-image: url(./img/pause_on.svg) 0;\n"
" }\n"
"")
        self.pauseButton.setText("")
        self.pauseButton.setCheckable(True)
        self.pauseButton.setAutoExclusive(True)
        self.pauseButton.setObjectName("pauseButton")
        self.prevComButton = QtWidgets.QPushButton(self.controlTab)
        self.prevComButton.setGeometry(QtCore.QRect(117, 70, 31, 31))
        self.prevComButton.setStyleSheet(" QPushButton {\n"
"    border-image:url(./img/slow_down.svg) 0;\n"
" }\n"
"\n"
" QPushButton:hover {\n"
"    border-image: url(./img/slow_down_hover.svg) 0;\n"
" }\n"
"\n"
" QPushButton:pressed  {\n"
"    border-image: url(./img/slow_down_pressed.svg) 0;\n"
" }\n"
"\n"
"")
        self.prevComButton.setText("")
        self.prevComButton.setObjectName("prevComButton")
        self.clearTermButton = QtWidgets.QPushButton(self.controlTab)
        self.clearTermButton.setGeometry(QtCore.QRect(360, 40, 31, 27))
        self.clearTermButton.setText("")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("img/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearTermButton.setIcon(icon15)
        self.clearTermButton.setObjectName("clearTermButton")
        self.line = QtWidgets.QFrame(self.controlTab)
        self.line.setGeometry(QtCore.QRect(117, 50, 151, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.autoButton = QtWidgets.QPushButton(self.controlTab)
        self.autoButton.setGeometry(QtCore.QRect(117, 10, 70, 27))
        self.autoButton.setMinimumSize(QtCore.QSize(10, 0))
        self.autoButton.setStyleSheet("")
        self.autoButton.setCheckable(True)
        self.autoButton.setChecked(True)
        self.autoButton.setAutoExclusive(True)
        self.autoButton.setObjectName("autoButton")
        self.manualButton = QtWidgets.QPushButton(self.controlTab)
        self.manualButton.setGeometry(QtCore.QRect(198, 10, 70, 27))
        self.manualButton.setMinimumSize(QtCore.QSize(0, 0))
        self.manualButton.setStyleSheet("")
        self.manualButton.setCheckable(True)
        self.manualButton.setAutoExclusive(True)
        self.manualButton.setObjectName("manualButton")
        self.tabWidget.addTab(self.controlTab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 575, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSetup = QtWidgets.QMenu(self.menubar)
        self.menuSetup.setObjectName("menuSetup")
        self.menuStep_Motor = QtWidgets.QMenu(self.menuSetup)
        self.menuStep_Motor.setObjectName("menuStep_Motor")
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
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionDocs = QtWidgets.QAction(MainWindow)
        self.actionDocs.setObjectName("actionDocs")
        self.actionSetSvgDir = QtWidgets.QAction(MainWindow)
        self.actionSetSvgDir.setObjectName("actionSetSvgDir")
        self.actionFullStep = QtWidgets.QAction(MainWindow)
        self.actionFullStep.setCheckable(True)
        self.actionFullStep.setObjectName("actionFullStep")
        self.actionHalfStep = QtWidgets.QAction(MainWindow)
        self.actionHalfStep.setCheckable(True)
        self.actionHalfStep.setChecked(True)
        self.actionHalfStep.setObjectName("actionHalfStep")
        self.actionQuarterStep = QtWidgets.QAction(MainWindow)
        self.actionQuarterStep.setCheckable(True)
        self.actionQuarterStep.setObjectName("actionQuarterStep")
        self.actionEighthStep = QtWidgets.QAction(MainWindow)
        self.actionEighthStep.setCheckable(True)
        self.actionEighthStep.setObjectName("actionEighthStep")
        self.actionSixteenthStep = QtWidgets.QAction(MainWindow)
        self.actionSixteenthStep.setCheckable(True)
        self.actionSixteenthStep.setObjectName("actionSixteenthStep")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuStep_Motor.addAction(self.actionFullStep)
        self.menuStep_Motor.addAction(self.actionHalfStep)
        self.menuStep_Motor.addAction(self.actionQuarterStep)
        self.menuStep_Motor.addAction(self.actionEighthStep)
        self.menuStep_Motor.addAction(self.actionSixteenthStep)
        self.menuSetup.addAction(self.actionSetSvgDir)
        self.menuSetup.addAction(self.menuStep_Motor.menuAction())
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
        self.textButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">text</p></body></html>"))
        self.selectButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">select</p></body></html>"))
        self.lineButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">line</p></body></html>"))
        self.polygonButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">polygon</p></body></html>"))
        self.eraserButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">eraser</p></body></html>"))
        self.ellipseButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">ellipse</p></body></html>"))
        self.rectangleButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">rectangle</p></body></html>"))
        self.freehandButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">freehand</p></body></html>"))
        self.magnifierButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">magnifier</p></body></html>"))
        self.circleButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">circle</p></body></html>"))
        self.squareButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">square</p></body></html>"))
        self.importButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">import</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.drawTab), _translate("MainWindow", "Draw"))
        self.penButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">Pen</p></body></html>"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.clearTermButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">clear terminal</p></body></html>"))
        self.autoButton.setText(_translate("MainWindow", "Auto"))
        self.manualButton.setText(_translate("MainWindow", "Manual"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.controlTab), _translate("MainWindow", "Control"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuSetup.setTitle(_translate("MainWindow", "Setti&ngs"))
        self.menuStep_Motor.setTitle(_translate("MainWindow", "Step Motor"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.actionNew.setText(_translate("MainWindow", "&New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionSave.setText(_translate("MainWindow", "&Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_As.setText(_translate("MainWindow", "Sa&ve As ..."))
        self.actionSave_As.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionLicense.setText(_translate("MainWindow", "&License"))
        self.actionAbout.setText(_translate("MainWindow", "&About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+?"))
        self.actionPreferences.setText(_translate("MainWindow", "&Preferences"))
        self.actionOpen.setText(_translate("MainWindow", "Open ..."))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionDocs.setText(_translate("MainWindow", "Docs"))
        self.actionSetSvgDir.setText(_translate("MainWindow", "SVG Directory"))
        self.actionFullStep.setText(_translate("MainWindow", "Full Step"))
        self.actionHalfStep.setText(_translate("MainWindow", "Half Step"))
        self.actionQuarterStep.setText(_translate("MainWindow", "Quarter Step"))
        self.actionEighthStep.setText(_translate("MainWindow", "Eighth Step"))
        self.actionSixteenthStep.setText(_translate("MainWindow", "Sixteenth Step"))

