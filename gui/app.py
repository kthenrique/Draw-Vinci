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
from PyQt5.QtWidgets import QApplication, QMainWindow
from draw_vinci import Ui_MainWindow

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

app = QApplication(sys.argv)
win = AppWindow()
sys.exit(app.exec_())

