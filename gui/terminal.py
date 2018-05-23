#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : terminal.py
# -- Author     : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Mai 23
# ----------------------------------------------------------------------------
# -- Description: Thread responsible for communicating with the plotter
# ----------------------------------------------------------------------------

import os
import shutil

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QIODevice
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

from constants import TIMEOUT_STATUS

class Terminal(QThread):
    '''
    Terminal Thread:
    It is called whenever the user presses the play button on control tab.
    In Manual Mode, it will listen for directions and pen position (keyboard
    and mouse events) commandd, translate it in G-Code and send it to XMC4500.
    In Auto Mode, it will translate the image in canvas into G-Code and send
    it to XMC4500.
    '''

    def __init__(self, drawingProgress, pauseButton):
        super().__init__()
        self.setTerminationEnabled(True)
        self.setObjectName("DrawVinci")
        self.drawingProgress = drawingProgress
        self.statusbar = self.drawingProgress.parentWidget()
        self.pauseButton = pauseButton

        self.path  = None
        self.port  = None

        self.flag = False

    def __del__(self):
        self.wait()

    @pyqtSlot()
    def run(self):
        self.path = shutil.copy(self.path, self.path.replace(os.path.basename(self.path), 'toPlotTemp'))
        file_size = os.path.getsize(self.path)
        with open(self.path) as code:
            port = QSerialPort()
            port.setPortName(self.port)
            port.setBaudRate(QSerialPort.Baud9600)
            port.setDataBits(QSerialPort.Data8)
            port.setParity(QSerialPort.NoParity)
            port.setStopBits(QSerialPort.OneStop)
            port.setFlowControl(QSerialPort.NoFlowControl)
            if not port.open(QIODevice.ReadWrite):
                print('NOT CONNECTED')
            while file_size > code.tell():
                self.sleep(1)
                try:
                    command = code.readline()
                    command = command.replace('\n','')
                    if port.isOpen():
                        ret = port.writeData(bytes(command, 'utf-8'))
                        print('{0} char sent -> msg: {1}'.format(ret, command))
                        # Update Progress Bar
                        self.drawingProgress.setValue(100*(code.tell()/file_size))
                    else:
                        self.statusbar.showMessage(self.statusbar.tr("Auto sending interrupted!"), TIMEOUT_STATUS)
                        print('port problem')
                        break
                except:
                    print('EXCEPT')
                    break
                if self.isInterruptionRequested():
                    print("thread interrupted")
                    break
                while self.pauseButton.isChecked():
                    print("thread paused")
                    self.sleep(5)
        os.remove(self.path)
        self.exit()
