#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : app.py
# -- Authors    : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Apr 28
# ----------------------------------------------------------------------------
# -- Description: 
# ----------------------------------------------------------------------------

import sys
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import QApplication, QMainWindow
from draw_vinci import Ui_MainWindow

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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

        self.show()

    def refresh_ports(self):
        self.ui.portsBox.clear()
        self.ui.portsBox.addItem("Custom")
        apt_ports = QSerialPortInfo.availablePorts()
        for port in apt_ports:
            self.ui.portsBox.addItem(port.portName())

        self.port.setPortName(self.ui.portsBox.currentText())

    def connect_port(self):
        self.port.setPortName(self.ui.portsBox.currentText())
        self.port.open(QIODevice.ReadWrite);


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AppWindow()
    sys.exit(app.exec_())

