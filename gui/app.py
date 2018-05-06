#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : app.py
# -- Authors    : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Mai 06
# ----------------------------------------------------------------------------
# -- Description: Main window initialisation
# ----------------------------------------------------------------------------

import sys
from PyQt5.Qt import Qt                              # Some relevant constants
from PyQt5.QtCore import QIODevice, QThreadPool, QRect, QThread
from PyQt5.QtWidgets import (QApplication, QMainWindow, QButtonGroup, QLabel,
        QProgressBar)
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

from draw_vinci import Ui_MainWindow
from canvas import MainScene
from terminal import Terminal
from constants import TIMEOUT_STATUS

class AppWindow(QMainWindow):
    '''
    Main Window:
        Where the drawing and menu functionalities take place. Besides, the
        single messages sent to XMC4500 using the promptEdit will be handled
        here too.
    '''
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Tools Group of buttons
        self.toolsButtonGroup = QButtonGroup()
        self.toolsButtonGroup.setExclusive(True)
        self.toolsButtonGroup.addButton(self.ui.eraserButton, 0)
        self.toolsButtonGroup.addButton(self.ui.freehandButton, 1)
        self.toolsButtonGroup.addButton(self.ui.lineButton, 2)
        self.toolsButtonGroup.addButton(self.ui.textButton, 3)
        self.toolsButtonGroup.addButton(self.ui.rectangleButton, 4)
        self.toolsButtonGroup.addButton(self.ui.ellipseButton, 5)
        self.toolsButtonGroup.addButton(self.ui.polygonButton, 6)
        self.toolsButtonGroup.addButton(self.ui.selectButton, 7)

        # Configuring UART Port
        self.port = QSerialPort()
        self.port.setBaudRate(QSerialPort.Baud9600)
        self.port.setDataBits(QSerialPort.Data8)
        self.port.setParity(QSerialPort.NoParity)
        self.port.setStopBits(QSerialPort.OneStop)
        self.port.setFlowControl(QSerialPort.NoFlowControl)

        # Ports refresh
        self.refreshPorts()

        # Connect promptEdit return event to send a single message to XMC4500
        self.ui.promptEdit.returnPressed.connect(self.sendSingleMsg)

        # Configuring statusbar 
        self.drawingProgress = QProgressBar() # Progress of auto sending G-CODE
        self.drawingProgress.setMaximum(100)
        self.drawingProgress.setMinimum(0)
        self.drawingProgress.setValue(0)
        self.drawingProgress.setStyleSheet("QProgressBar {\n"
                "border: 1px solid grey;\n"
                "border-radius: 5px;}\n"
                "QProgressBar::chunk{\n"
                "background-color: #CD96CD;\n"
                "width: 10px;\n"
                "margin: 0.5px;}")
        self.drawingProgress.setMaximumHeight(15)
        self.drawingProgress.setVisible(False)
        self.artworkLabel = QLabel()    # Name of image being edited
        self.artworkLabel.setAlignment(Qt.AlignLeft)
        self.artworkLabel.setTextFormat(Qt.RichText)
        self.artworkLabel.setText("UNKNOWN_FILE")
        self.toolLabel = QLabel()       # Icon of tool last used
        self.toolLabel.setAlignment(Qt.AlignLeft)
        self.toolLabel.setTextFormat(Qt.RichText)
        self.connectionLabel = QLabel() # connection state: online - offline
        self.connectionLabel.setAlignment(Qt.AlignHCenter)
        self.connectionLabel.setTextFormat(Qt.RichText)
        self.ui.statusbar.addPermanentWidget(self.drawingProgress)
        self.ui.statusbar.addPermanentWidget(self.artworkLabel)
        self.ui.statusbar.addPermanentWidget(self.toolLabel)
        self.ui.statusbar.addPermanentWidget(self.connectionLabel)

        # Write OFFLINE to connectionStatus - statusbar
        self.connectionLabel.setText('<html><head/><body><p align="center">\
                <span style=" font-weight:600; color:#cc0000;">OFFLINE\
                </span></p></body></html>')

        # Creating canvas
        self.scene = MainScene(self.toolsButtonGroup, self.toolLabel)
        self.ui.canvas.setScene(self.scene)
        self.scene.view = self.ui.canvas
        self.ui.canvas.show()

        # Menus Initialisation
        self.ui.actionQuit.triggered.connect(self.close) # Quit

        # Buttons Initialisation
        self.ui.connectButton.clicked.connect(self.connectPort)    # connect
        self.ui.refreshButton.clicked.connect(self.refreshPorts)   # refresh
        self.ui.playButton.toggled.connect(self.playIt)            # play
        self.ui.stopButton.clicked.connect(self.stopIt)            # stop
        self.ui.pauseButton.clicked.connect(self.pauseIt)          # pause
        self.ui.slowDownButton.clicked.connect(self.slowItDown)    # slow down
        self.ui.speedUpButton.clicked.connect(self.speedItUp)      # speed up

        # Thread for permanent communication with XMC4500
        self.terminalThread = Terminal(self.drawingProgress, self.ui.termEdit)

        # Connect finishing of thread with stopButton
        self.terminalThread.finished.connect(self.ui.stopButton.toggle)

        self.show()

    def refreshPorts(self):
        ''' Callback of refreshButton:
                refreshing the list of available serial ports to connect.
        '''
        self.ui.portsBox.clear()
        self.ui.portsBox.addItem("Custom")
        apt_ports = QSerialPortInfo.availablePorts()
        for port in apt_ports:
            self.ui.portsBox.addItem(port.portName())

        self.port.setPortName(self.ui.portsBox.currentText())

    def connectPort(self):
        ''' Callback of connectButton:
                trying to connect to the port chosen.
        '''
        self.port.close()
        self.port.setPortName(self.ui.portsBox.currentText())
        if not self.port.open(QIODevice.ReadWrite):
            self.connectionLabel.setText('<html><head/><body><p align="center">\
                    <span style=" font-weight:600; color:#cc0000;">OFFLINE\
                    </span></p></body></html>')
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("ERROR: {0:2d} - vide docs!".format(self.port.error())), TIMEOUT_STATUS)
        else:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Successfuly Connected"), TIMEOUT_STATUS)
            self.connectionLabel.setText('<html><head/><body><p align="center">\
                    <span style=" font-weight:600; color:#008000;">ONLINE</span>\
                    </p></body></html>')

    def sendSingleMsg(self):
        if self.port.isOpen():
            ret = self.port.writeData(bytes(self.ui.promptEdit.text(), 'utf-8'))
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("{0} characters sent!".format(ret)), TIMEOUT_STATUS)
        else:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Not Connected!"), TIMEOUT_STATUS)

    def playIt(self, isChecked):
        '''
        Initialise permanent communication with XMC4500; i.e. if in manual
        the directional buttons will drive the plotter, and if in auto mode,
        the image on canvas will be translated in G-CODE and sent to XMC4500.
        '''
        if isChecked:
            self.terminalThread.start(QThread.HighestPriority)

    def stopIt(self):
        pass

    def pauseIt(self):
        pass

    def slowItDown(self):
        pass

    def speedItUp(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AppWindow()

    sys.exit(app.exec_())

