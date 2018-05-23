#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : app.py
# -- Authors    : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Mai 23
# ----------------------------------------------------------------------------
# -- Description: Main window initialisation
# ----------------------------------------------------------------------------

import sys
from PyQt5.Qt import Qt                              # Some relevant constants
from PyQt5.QtCore import QIODevice, QThreadPool, QRect, QThread, QSize
from PyQt5.QtGui import QIntValidator, QPainter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QButtonGroup, QLabel,
        QProgressBar, QFileDialog, QMessageBox)
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtSvg import QSvgGenerator

from pyudev import Context, Monitor
from pyudev.pyqt5 import MonitorObserver

from draw_vinci import Ui_MainWindow
from parser import parser
from canvas import MainScene
from terminal import Terminal
from constants import TIMEOUT_STATUS, FONT_SIZES

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

        # Monitoring IO Ports
        context = Context()
        monitor = Monitor.from_netlink(context)
        monitor.filter_by('COM') # WINDOWS
        monitor.filter_by('tty') # LINUX
        self.observer = MonitorObserver(monitor)
        self.observer.deviceEvent.connect(self.updateConnection)
        monitor.start()

        # Fill fontSizeBox
        self.ui.fontSizeBox.addItems([str(size) for size in FONT_SIZES])
        self.ui.fontSizeBox.setValidator(QIntValidator())

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
        self.toolsButtonGroup.addButton(self.ui.magnifierButton, 8)
        self.toolsButtonGroup.addButton(self.ui.circleButton, 9)
        self.toolsButtonGroup.addButton(self.ui.squareButton, 10)
        self.toolsButtonGroup.addButton(self.ui.importButton, 11)

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
        self.ui.promptEdit.returnPressed.connect(lambda: self.sendSingleMsg(self.ui.promptEdit.text()))

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

        # Creating and initialising canvas
        self.scene = MainScene(self.toolsButtonGroup, self.toolLabel)
        self.ui.canvas.setScene(self.scene)
        self.scene.view = self.ui.canvas
        self.scene.setIconTool(self.ui.eraserButton)
        self.scene.textTools = (self.ui.fontBox, self.ui.fontSizeBox,\
                self.ui.italicButton, self.ui.underlineButton)
        self.scene.changed.connect(self.updateFileState)
        self.ui.canvas.show()

        # Menus Initialisation
        self.ui.actionNew.triggered.connect(self.newFile)         # New
        self.ui.actionOpen.triggered.connect(self.openFile)       # Open
        self.ui.actionSave.triggered.connect(self.saveFile)       # Save
        self.ui.actionSave_As.triggered.connect(self.saveFileAs)  # Save as
        self.ui.actionAbout.triggered.connect(self.about)         # About
        self.ui.actionQuit.triggered.connect(self.close)          # Quit

        # Control Buttons Initialisation
        self.ui.connectButton.clicked.connect(self.connectPort)    # connect
        self.ui.playButton.toggled.connect(self.playIt)            # play
        self.ui.stopButton.clicked.connect(self.stopIt)            # stop
        self.ui.pauseButton.clicked.connect(self.pauseIt)          # pause
        self.ui.slowDownButton.clicked.connect(self.slowItDown)    # slow down
        self.ui.speedUpButton.clicked.connect(self.speedItUp)      # speed up

        # Directional Buttons Initialisation
        self.ui.upButton.clicked.connect(self.goUp)                # up
        self.ui.downButton.clicked.connect(self.goDown)            # down
        self.ui.leftButton.clicked.connect(self.goLeft)            # left
        self.ui.rightButton.clicked.connect(self.goRight)          # right
        self.ui.penButton.toggled.connect(self.togglePen)          # pen

        # Listening to incoming messages
        self.port.readyRead.connect(self.updateTerm)
        #self.port.bytesWritten.connect(self.updateTerm)

        # Thread for permanent communication with XMC4500
        self.terminalThread = Terminal(self.drawingProgress, self.ui.pauseButton)

        # Connect thread signals
        self.terminalThread.finished.connect(self.prepFini)
        self.terminalThread.started.connect(self.prepInit)

        # Connect finishing of thread with toggling of stopButton
        self.terminalThread.finished.connect(self.ui.stopButton.toggle)

        # File state variables
        self.isPlotting = False
        self.isSaved    = False
        self.hasChanged = False
        self.path       = None

        self.parser     = parser()

        self.show()

    def updateConnection(self, device):
        self.refreshPorts()
        if self.port.isOpen():
            self.port.close()
            if not self.port.open(QIODevice.ReadWrite):
                self.connectionLabel.setText('<html><head/><body><p align="center">\
                        <span style=" font-weight:600; color:#cc0000;">OFFLINE\
                        </span></p></body></html>')
                self.ui.statusbar.showMessage(self.ui.statusbar.tr("ERROR: {0:2d} - vide docs!".format(self.port.error())), TIMEOUT_STATUS)
                self.ui.stopButton.setChecked(True)
                self.isPlotting = False

    def refreshPorts(self):
        '''
        Callback of refreshButton:
        refreshing the list of available serial ports to connect.
        '''
        self.ui.portsBox.clear()
        apt_ports = QSerialPortInfo.availablePorts()
        for port in apt_ports:
            self.ui.portsBox.addItem(port.portName())

        self.port.setPortName(self.ui.portsBox.currentText())
        if self.ui.portsBox.count() == 0:
            self.ui.portsBox.addItem("Custom")
            self.ui.portsBox.setEditable(True)
        else:
            self.ui.portsBox.setEditable(False)

    def connectPort(self):
        '''
        Callback of connectButton:
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

    def sendSingleMsg(self, text):
        '''
        Sends one single text message to xmc4500, returning True if it was
        successful and False otherwise
        '''
        if self.port.isOpen():
            ret = self.port.writeData(bytes(text, 'utf-8'))
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("{0} characters sent!".format(ret)), TIMEOUT_STATUS)
            self.ui.termEdit.append('>' + text)
            return True
        else:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Not Connected!"), TIMEOUT_STATUS)
            return False

    def playIt(self, isChecked):
        '''
        Initialise permanent communication with XMC4500; i.e. if in manual
        the directional buttons will drive the plotter, and if in auto mode,
        the image on canvas will be translated in G-CODE and sent to XMC4500.
        '''
        if isChecked and not self.terminalThread.isRunning():
            if self.port.isOpen():
                self.ui.autoButton.setEnabled(False)
                self.ui.manualButton.setEnabled(False)
                if self.ui.autoButton.isChecked():                 # AUTO MODE
                    if self.isSaved:
                        self.port.close()
                        g_code_path = self.path.replace('.svg', '.gcode')
                        self.terminalThread.path = g_code_path
                        self.terminalThread.port = self.ui.portsBox.currentText()
                        self.terminalThread.start(QThread.HighestPriority)
                    else:
                        self.ui.statusbar.showMessage(self.ui.statusbar.tr("Save canvas before plotting!"), TIMEOUT_STATUS)
                        self.ui.stopButton.setChecked(True)
                        self.ui.autoButton.setEnabled(True)
                        self.ui.manualButton.setEnabled(True)
                elif not self.isPlotting:                          # MANUAL MODE
                    self.isPlotting = True
                    self.sendSingleMsg("#G91$")                      # set relative positioning
                    if self.ui.penButton.isChecked():
                        self.sendSingleMsg('#G01:Z1$')
                    else:
                        self.sendSingleMsg('#G01:Z0$')
            else:
                self.ui.statusbar.showMessage(self.ui.statusbar.tr("Not Connected!"), TIMEOUT_STATUS)
                self.ui.stopButton.setChecked(True)

    def stopIt(self):
        '''
        Interrupt terminal thread when it is running
        '''
        self.isPlotting = False
        self.ui.autoButton.setEnabled(True)
        self.ui.manualButton.setEnabled(True)
        if self.terminalThread.isRunning():
            print("trying to interrupt thread")
            self.terminalThread.requestInterruption()

    def pauseIt(self):
        if self.ui.autoButton.isChecked() and not self.terminalThread.isRunning():
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Nothing's being plotted ..."), TIMEOUT_STATUS)
            self.ui.stopButton.setChecked(True)

    def slowItDown(self):
        '''
        send G-CODE to slow the plotter motors down
        '''
        self.sendSingleMsg("G-CODE to slow down")

    def speedItUp(self):
        '''
        send G-CODE to speed the plotter motors up
        '''
        self.sendSingleMsg("G-CODE to slow down")

    def prepInit(self):
        '''
        Everything that should be done before starting terminalThread
        '''
        print("thread started")
        self.drawingProgress.setVisible(True)

    def prepFini(self):
        '''
        Everything that should be done right before finishing terminalThread
        '''
        print("thread finished")
        self.ui.statusbar.showMessage("Plotting finished or interrupted", TIMEOUT_STATUS)
        self.isPlotting = False
        self.drawingProgress.setValue(0)
        self.drawingProgress.setVisible(False)
        self.ui.autoButton.setEnabled(True)
        self.ui.manualButton.setEnabled(True)
        self.connectPort()

    def goUp(self):
        if self.ui.playButton.isChecked():
            self.sendSingleMsg('#G01:Y1000$')
        else:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Plotter not listening! Press play ..."), TIMEOUT_STATUS)

    def goDown(self):
        if self.ui.playButton.isChecked():
            self.sendSingleMsg('#G01:Y-1000$')
        else:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Plotter not listening! Press play ..."), TIMEOUT_STATUS)

    def goLeft(self):
        if self.ui.playButton.isChecked():
            self.sendSingleMsg('#G01:X-1000$')
        else:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Plotter not listening! Press play ..."), TIMEOUT_STATUS)

    def goRight(self):
        if self.ui.playButton.isChecked():
            self.sendSingleMsg('#G01:X1000$')
        else:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Plotter not listening! Press play ..."), TIMEOUT_STATUS)

    def togglePen(self):
        if self.ui.playButton.isChecked():
            if self.ui.penButton.isChecked():
                self.sendSingleMsg('#G01:Z1$')
            else:
                self.sendSingleMsg('#G01:Z0$')
        else:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Plotter not listening! Press play ..."), TIMEOUT_STATUS)

    def checkCanvas(self):
        print("checkCanvas")
        if len(self.ui.canvas.items()) == 0:                   # a blank canvas
            pass
        elif not self.isSaved:                                 # a not-saved filled canvas
            ret = QMessageBox(QMessageBox.Warning, 'Eita Caramba!',\
                    'There is work not saved in canvas.\n'+\
                    'Are you sure you want to discard it?\n',\
                    QMessageBox.Yes | QMessageBox.Cancel).exec()
            if ret == QMessageBox.Cancel:
                return False
        elif self.hasChanged:                                  # a saved but aftwrwards altered canvas
            ret = QMessageBox(QMessageBox.Warning, 'Eita Caramba!',\
                    'The canvas has changed since last save..\n'+\
                    'Are you sure you want to discard it?\n',\
                    QMessageBox.Yes | QMessageBox.Cancel).exec()
            if ret == QMessageBox.Cancel:
                return False

        self.scene.resetTools()
        self.scene.clear()
        self.path = None
        return True

    def newFile(self):
        if self.checkCanvas():
            self.hasChanged = False
            self.artworkLabel.setText("UNKNOWN_FILE")

    def openFile(self):
        if self.checkCanvas():

            path = QFileDialog.getOpenFileName(self, "Open SVG Image", '', "SVG files (*.svg)")
            self.path = str(path[0])

            parsed = self.parser.getElements(self.path)
            if parsed:
                self.isSaved = True
                self.artworkLabel.setText(((self.path.replace('/', ' ')).replace('\\', ' ')).split()[-1])
                for element in parsed:
                    self.scene.addItem(element)
                    self.hasChanged = False

    def saveFile(self):
        try:
            self.scene.removeItem(self.scene.tools[7])
        except:
            print('no selection to remove')
        if self.isSaved:
            generator = QSvgGenerator()
            generator.setFileName(str(self.path))
            generator.setSize(QSize(self.scene.width(), self.scene.height()))
            generator.setViewBox(QRect(0, 0, self.scene.width(), self.scene.height()))
            generator.setTitle("Title for SVG file")
            generator.setDescription("Description for SVG file");

            painter = QPainter()
            painter.begin(generator)
            self.scene.render(painter)
            painter.end()

            self.hasChanged = False
            self.parser.getElements(self.path, 0)      # generate g-code
        else:
            self.saveFileAs()

    def saveFileAs(self):
            path = QFileDialog.getSaveFileName(self, 'Save File', '', "SVG files (*.svg)")

            if not path:
                print(path)
                print("Smth went wrong")
                return

            self.path = str(path[0])

            generator = QSvgGenerator()
            generator.setFileName(self.path)
            generator.setSize(QSize(self.scene.width(), self.scene.height()))
            generator.setViewBox(QRect(0, 0, self.scene.width(), self.scene.height()))
            generator.setTitle("Title for SVG file")
            generator.setDescription("Description for SVG file");

            painter = QPainter()
            painter.begin(generator)
            self.scene.render(painter)
            painter.end()
            self.artworkLabel.setText(((self.path.replace('/', ' ')).replace('\\', ' ')).split()[-1])

            self.parser.getElements(self.path, 0)      # generate g-code
            self.hasChanged = False
            self.isSaved = True

    def about(self):
        pass

    def updateFileState(self):
        if self.hasChanged:
            self.hasChanged = False
        else:
            self.hasChanged = True

    def updateTerm(self):#, by):
        '''
        It is signaled every time there's incoming message from uC
        '''
        if self.port.isOpen():
            wasRead = self.port.readAll()
            self.ui.termEdit.append((wasRead.data()).decode('utf-8'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AppWindow()

    sys.exit(app.exec_())

