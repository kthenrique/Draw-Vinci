#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : terminal.py
# -- Author     : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Jun 05
# ----------------------------------------------------------------------------
# -- Description: Thread responsible for communicating with the plotter
# ----------------------------------------------------------------------------

import os
import serial
from sys import platform as _platform

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QIODevice, QWaitCondition, QMutex

from constants import *
from parser import getElements

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

        self.nav = QWaitCondition()
        self.mutex = QMutex()

        self.scale = QUARTER_STEP[0]
        self.path  = None
        self.port  = None
        self.com = 0
        self.fileLines = []

        self.flag = False

    def __del__(self):
        self.wait()

    @pyqtSlot()
    def run(self):
        self.fileLines = []
        getElements(self.path, writeCode = True, toScale = False, RESOLUTION=self.scale)
        self.path = self.path.replace('.svg', '.gcode')
        file_size = os.path.getsize(self.path)
        with open(self.path) as code:
            if _platform == "win32" or _platform == "win64":
                self.port = 'COM1'
            else:
                self.port = '/dev/'+self.port
            with serial.Serial(self.port) as ser:
                while file_size > code.tell():
                    self.msleep(300)
                    try:
                        self.fileLines.append(code.tell())
                        command = code.readline()
                        command = command.replace('\n','')
                        if ser.is_open:
                            ret = ser.write(bytes(command, 'utf-8'))
                            print('{0} char sent -> msg: {1}'.format(ret, command))
                            # Update Progress Bar
                            self.drawingProgress.setValue(100*(code.tell()/file_size))
                        else:
                            self.statusbar.showMessage(self.statusbar.tr("Serial port disconnected!"), TIMEOUT_STATUS)
                            print('serial port problem')
                            break
                    except:
                        print('EXCEPT')
                        break
                    if self.isInterruptionRequested():
                        print("thread interrupted")
                        break
                    while self.pauseButton.isChecked():
                        print("thread paused")
                        self.mutex.lock()
                        self.nav.wait(self.mutex)
                        if self.com == 1:
                            self.com = 0
                            print("next command")
                            self.fileLines.append(code.tell())
                            command = code.readline()
                            if command:
                                command = command.replace('\n','')
                                if ser.is_open:
                                    ret = ser.write(bytes(command, 'utf-8'))
                                    print('{0} char sent -> msg: {1}'.format(ret, command))
                                    # Update Progress Bar
                                    self.drawingProgress.setValue(100*(code.tell()/file_size))
                                else:
                                    self.statusbar.showMessage(self.statusbar.tr("Serial port disconnected!"), TIMEOUT_STATUS)
                                    print('serial port problem')
                                    break
                            else:
                                break
                        elif self.com == -1:
                            print("previous command")
                            if self.fileLines:
                                code.seek(self.fileLines.pop())
                                command = code.readline()
                                command = command.replace('\n','')
                                if ser.is_open:
                                    ret = ser.write(bytes(command, 'utf-8'))
                                    print('{0} char sent -> msg: {1}'.format(ret, command))
                                    # Update Progress Bar
                                    self.drawingProgress.setValue(100*(code.tell()/file_size))
                                else:
                                    self.statusbar.showMessage(self.statusbar.tr("Serial port disconnected!"), TIMEOUT_STATUS)
                                    print('serial port problem')
                                    break
                            else:
                                self.statusbar.showMessage(self.statusbar.tr("Already at first G-CODE!"), TIMEOUT_STATUS)
                            self.com = 0
                        self.mutex.unlock()

        os.remove(self.path)
        self.exit()
