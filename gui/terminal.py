#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : terminal.py
# -- Author     : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Mai 07
# ----------------------------------------------------------------------------
# -- Description: Thread responsible for communicating with the plotter
# ----------------------------------------------------------------------------

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer

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

    updateTerm = pyqtSignal(str) # when the terminal should be written

    def __init__(self, drawingProgress, termEdit):
        super().__init__()
        self.setTerminationEnabled(True)
        self.setObjectName("DrawVinci")
        self.drawingProgress = drawingProgress
        self.termEdit  = termEdit
        self.statusbar = self.drawingProgress.parentWidget()

        # Connect signals
        self.updateTerm.connect(self.updateTermEdit)

        # Set a timer
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateProgress)

        self.flag = False

    def __del__(self):
        self.wait()

    @pyqtSlot()
    def run(self):
        while self.drawingProgress.value() != 10:
            if self.isInterruptionRequested():
                print("thread interrupted")
                break
        self.exit()

    def updateProgress(self):
        print(self.drawingProgress.value() + 1)
        self.drawingProgress.setValue(self.drawingProgress.value() + 1)

    def updateTermEdit(self, text):
        self.termEdit.append(text)

