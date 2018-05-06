#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : terminal.py
# -- Author     : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Mai 06
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
    def __init__(self, drawingProgress):
        super().__init__()
        self.setObjectName("DrawVinci")
        self.drawingProgress = drawingProgress
        self.statusbar = self.drawingProgress.parentWidget()

        # Connect signals
        self.finished.connect(self.prepFini)
        self.started.connect(self.prepInit)

        # Set a timer
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateProgress)

        self.flag = False

    @pyqtSlot()
    def run(self):
        while self.drawingProgress.value() != 10:
            pass
        print("END OF THREAD")
        self.exit()

    def updateProgress(self):
        print(self.drawingProgress.value() + 1)
        self.drawingProgress.setValue(self.drawingProgress.value() + 1)

    def prepInit(self):
        ''' Everything that should be done before starting this thread '''
        self.drawingProgress.setVisible(True)
        self.timer.start()

    def prepFini(self):
        ''' Everything that should be done right before finishing this thread '''
        self.statusbar.showMessage("Thread Finished", TIMEOUT_STATUS)
        self.timer.stop()
        self.drawingProgress.setValue(0)
        self.drawingProgress.setVisible(False)

