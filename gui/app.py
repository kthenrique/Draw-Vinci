#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : app.py
# -- Authors    : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Apr 28
# ----------------------------------------------------------------------------
# -- Description: Main window initialisation
# ----------------------------------------------------------------------------

import sys
from PyQt5.Qt import Qt                              # Some relevant constants
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QLabel

from draw_vinci import Ui_MainWindow
from canvas import MainScene

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Tools Group of buttons
        self.toolsButtonGroup = QButtonGroup()
        self.toolsButtonGroup.setExclusive(True)
        self.toolsButtonGroup.addButton(self.ui.eraserButton, 1)
        self.toolsButtonGroup.addButton(self.ui.freehandButton, 2)
        self.toolsButtonGroup.addButton(self.ui.lineButton, 3)
        self.toolsButtonGroup.addButton(self.ui.textButton, 4)
        self.toolsButtonGroup.addButton(self.ui.rectangleButton, 5)
        self.toolsButtonGroup.addButton(self.ui.ellipseButton, 6)
        self.toolsButtonGroup.addButton(self.ui.polygonButton, 7)

        # Creating canvas
        self.scene = MainScene(self.toolsButtonGroup)
        self.ui.canvas.setScene(self.scene)
        self.ui.canvas.show()

        # Configuring UART Port
        self.port = QSerialPort()
        self.port.setBaudRate(QSerialPort.Baud9600)
        self.port.setDataBits(QSerialPort.Data8)
        self.port.setParity(QSerialPort.NoParity)
        self.port.setStopBits(QSerialPort.OneStop)
        self.port.setFlowControl(QSerialPort.NoFlowControl)

        # Ports refresh
        self.refresh_ports()

        # Menus Initialisation
        self.ui.actionQuit.triggered.connect(self.close) # Quit

        # Buttons Initialisation
        self.ui.connectButton.clicked.connect(self.connect_port)   # connect
        self.ui.refreshButton.clicked.connect(self.refresh_ports)  # refresh

        # Configuring statusbar 
        self.connectionStatus = QLabel() # connection state: online - offline
        self.connectionStatus.setAlignment(Qt.AlignHCenter)
        self.connectionStatus.setTextFormat(Qt.RichText)
        self.artworkStatus = QLabel()    # Name of image being edited
        self.ui.statusbar.addPermanentWidget(self.connectionStatus)
        self.ui.statusbar.addPermanentWidget(self.artworkStatus)

        # Write OFFLINE to connectionStatus - statusbar
        self.connectionStatus.setText('<html><head/><body><p align="center">\
                <span style=" font-weight:600; color:#cc0000;">OFFLINE\
                </span></p></body></html>')

        self.show()

    def refresh_ports(self):
        ''' Callback of refreshButton:
                refreshing the list of available serial ports to connect.
        '''
        self.ui.portsBox.clear()
        self.ui.portsBox.addItem("Custom")
        apt_ports = QSerialPortInfo.availablePorts()
        for port in apt_ports:
            self.ui.portsBox.addItem(port.portName())

        self.port.setPortName(self.ui.portsBox.currentText())

    def connect_port(self):
        ''' Callback of connectButton:
                trying to connect to the port chosen.
        '''
        self.port.setPortName(self.ui.portsBox.currentText())
        if not self.port.open(QIODevice.ReadWrite):
            self.ui.statusbar.showMessage("ERROR: {0:2d} - vide docs!".format(self.port.error()), 900)
        else:
            self.connectionStatus.setText('<html><head/><body><p align="center">\
                    <span style=" font-weight:600; color:#73d216;">ONLINE</span>\
                    </p></body></html>')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AppWindow()

    sys.exit(app.exec_())

