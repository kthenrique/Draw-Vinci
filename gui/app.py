#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : app.py
# -- Authors    : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Jun 05
# ----------------------------------------------------------------------------
# -- Description: Main window initialisation
# ----------------------------------------------------------------------------

import sys
from PyQt5.Qt import Qt                              # Some relevant constants
from PyQt5.QtCore import QIODevice, QThreadPool, QRect, QThread, QSize
from PyQt5.QtGui import QIntValidator, QPainter, QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QButtonGroup, QLabel,
        QProgressBar, QFileDialog, QMessageBox, QWidget, QActionGroup)
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtSvg import QSvgGenerator

from pyudev import Context, Monitor
from pyudev.pyqt5 import MonitorObserver

from draw_vinci import Ui_MainWindow
from parser import getElements
from canvas import MainScene
from terminal import Terminal
from constants import *


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

        # Draw Buttons
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

        # Initialise import tool
        self.svg = SVG
        self.svg_index = 0
        self.ui.nextSVGButton.clicked.connect(self.nextSVG)

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
        self.scene = MainScene(self.toolsButtonGroup, self.toolLabel, self.svg_index)
        self.ui.canvas.setScene(self.scene)
        self.scene.view = self.ui.canvas
        self.scene.setIconTool(self.ui.eraserButton)
        self.scene.textTools = (self.ui.fontBox, self.ui.fontSizeBox,\
                self.ui.italicButton, self.ui.underlineButton)
        self.scene.changed.connect(self.updateFileState)
        self.ui.canvas.setSceneRect(self.scene.sceneRect())
        self.ui.canvas.show()

        self.nextSVG()

        # Menus Initialisation
        self.ui.actionNew.triggered.connect(self.newFile)         # New
        self.ui.actionOpen.triggered.connect(self.openFile)       # Open
        self.ui.actionSave.triggered.connect(self.saveFile)       # Save
        self.ui.actionSave_As.triggered.connect(self.saveFileAs)  # Save as
        self.ui.actionAbout.triggered.connect(self.about)         # About
        self.ui.actionQuit.triggered.connect(self.close)          # Quit
        self.ui.actionSetSvgDir.triggered.connect(self.setSVGDir) # Set SVG dir

        # Step motor config
        self.StepConfig = QActionGroup(self)
        self.StepConfig.addAction(self.ui.actionFullStep)
        self.StepConfig.addAction(self.ui.actionHalfStep)
        self.StepConfig.addAction(self.ui.actionQuarterStep)
        self.StepConfig.addAction(self.ui.actionEighthStep)
        self.StepConfig.addAction(self.ui.actionSixteenthStep)
        self.ui.actionQuarterStep.setChecked(True)

        self.StepConfig.triggered.connect(self.updateStepConfig)

        # Control Buttons Initialisation
        self.controlButtonGroup = QButtonGroup()
        self.controlButtonGroup.setExclusive(True)
        self.controlButtonGroup.addButton(self.ui.pauseButton, 0)
        self.controlButtonGroup.addButton(self.ui.playButton, 1)
        self.controlButtonGroup.addButton(self.ui.stopButton, 2)
        self.ui.connectButton.clicked.connect(self.connectPort)    # connect
        self.ui.clearTermButton.clicked.connect(self.clearTerm)    # clear terminal
        self.ui.playButton.toggled.connect(self.playIt)            # play
        self.ui.stopButton.clicked.connect(self.stopIt)            # stop
        self.ui.pauseButton.toggled.connect(self.pauseIt)          # pause
        self.ui.prevComButton.clicked.connect(self.prevCom)        # previous command
        self.ui.nextComButton.clicked.connect(self.nextCom)        # next command

        # Directional Buttons Initialisation
        self.ui.upButton.clicked.connect(self.goUp)                # up
        self.ui.downButton.clicked.connect(self.goDown)            # down
        self.ui.leftButton.clicked.connect(self.goLeft)            # left
        self.ui.rightButton.clicked.connect(self.goRight)          # right
        self.ui.penButton.toggled.connect(self.togglePen)          # pen

        self.manualResolution = str(int(QUARTER_STEP[0]/50))+'$'

        # Listening to incoming messages
        self.port.readyRead.connect(self.updateTerm)

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

    def clearTerm(self):
        self.ui.termEdit.clear()

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
                        self.terminalThread.path = self.path
                        self.terminalThread.port = self.ui.portsBox.currentText()
                        self.terminalThread.start(QThread.HighestPriority)
                    else:
                        self.ui.statusbar.showMessage(self.ui.statusbar.tr("Save canvas before plotting!"), TIMEOUT_STATUS)
                        self.ui.stopButton.setChecked(True)
                        self.ui.autoButton.setEnabled(True)
                        self.ui.manualButton.setEnabled(True)
                elif not self.isPlotting:                          # MANUAL MODE
                    self.isPlotting = True
                    self.sendSingleMsg("#G28$")                      # housing plotter
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

    def pauseIt(self, isChecked):
        '''
        Button Pause action when toggled
        '''
        if self.ui.autoButton.isChecked() and not self.terminalThread.isRunning() and isChecked:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Nothing's being plotted ..."), TIMEOUT_STATUS)
            self.ui.stopButton.setChecked(True)
        elif self.terminalThread.isRunning() and not isChecked:
            self.terminalThread.com = 0
            self.terminalThread.nav.wakeOne()

    def prevCom(self):
        '''
        Wake terminal thread to read previous line of g-code
        '''
        if self.terminalThread.isRunning() and self.ui.pauseButton.isChecked():
            self.terminalThread.com = -1
            self.terminalThread.nav.wakeOne()

    def nextCom(self):
        '''
        Wake terminal thread to read next line of g-code
        '''
        if self.terminalThread.isRunning() and self.ui.pauseButton.isChecked():
            self.terminalThread.com = 1
            self.terminalThread.nav.wakeOne()

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
            self.sendSingleMsg(GOUP+self.manualResolution)
        else:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Plotter not listening! Press play ..."), TIMEOUT_STATUS)

    def goDown(self):
        if self.ui.playButton.isChecked():
            self.sendSingleMsg(GODOWN+self.manualResolution)
        else:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Plotter not listening! Press play ..."), TIMEOUT_STATUS)

    def goLeft(self):
        if self.ui.playButton.isChecked():
            self.sendSingleMsg(GOLEFT+self.manualResolution)
        else:
            self.ui.statusbar.showMessage(self.ui.statusbar.tr("Plotter not listening! Press play ..."), TIMEOUT_STATUS)

    def goRight(self):
        if self.ui.playButton.isChecked():
            self.sendSingleMsg(GORIGHT+self.manualResolution)
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
        '''
        Checking to avoid loss of data
        '''
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
            self.isSaved    = False
            self.artworkLabel.setText("UNKNOWN_FILE")

    def openFile(self):
        if self.checkCanvas():
            path = QFileDialog.getOpenFileName(self, "Open SVG Image", '', "SVG files (*.svg)")
            self.path = str(path[0])

            parsed = getElements(self.path, toScale = True)
            if parsed:
                self.isSaved = True
                self.artworkLabel.setText(((self.path.replace('/', ' ')).replace('\\', ' ')).split()[-1])
                for element in parsed:
                    self.scene.addItem(element)
                    self.hasChanged = False

    def saveFile(self):
        if self.scene.tools[7]:
            self.scene.removeItem(self.scene.tools[7])
        if self.isSaved:
            generator = QSvgGenerator()
            generator.setFileName(self.path)
            generator.setSize(QSize(self.scene.width(), self.scene.height()))
            generator.setViewBox((self.scene.itemsBoundingRect()).toRect())
            generator.setTitle("Title for SVG file")
            generator.setDescription("Description for SVG file");

            painter = QPainter()
            painter.begin(generator)
            self.scene.render(painter)
            painter.end()

            self.hasChanged = False
        else:
            self.saveFileAs()

    def saveFileAs(self):
            path = QFileDialog.getSaveFileName(self, 'Save File', '', "SVG files (*.svg)")

            if not path[0]:
                print("NOT SAVED!")
                return

            self.path = str(path[0])

            generator = QSvgGenerator()
            generator.setFileName(self.path)
            generator.setSize(QSize(self.scene.width(), self.scene.height()))
            generator.setViewBox((self.scene.itemsBoundingRect()).toRect())
            generator.setTitle("Title for SVG file")
            generator.setDescription("Description for SVG file");

            painter = QPainter()
            painter.begin(generator)
            self.scene.render(painter)
            painter.end()
            self.artworkLabel.setText(((self.path.replace('/', ' ')).replace('\\', ' ')).split()[-1])

            self.hasChanged = False
            self.isSaved = True

    def about(self):
        ret = QMessageBox(QMessageBox.NoIcon, 'Draw-Vinci',\
                '<html><head/><body><p align="center"><span style=" font-size:16pt; font-weight:600;">Draw-Vinci</span></p><p align="center"><span style="\
                font-size:16pt; font-weight:600;">V0.1</span></p><p align="center"><span style=" font-size:10pt;">A drawing tool to edit and create SVG files and\
                generate its G-Code.</span></p><p align="center"><span style=" font-size:10pt;">It is supposed to be used with a plotter.</span></p><p\
                align="center"><span style=" font-style:italic; color:#0c5099;">© </span><a href="andreas.hofschweiger@technikum-wien.at"><span style="\
                text-decoration: underline; color:#0000ff;">Andreas Hofschweiger</span></a></p><p align="center"><span style=" font-style:italic; color:#0c5099;">©\
                </span><a href="kelvehenrique@pm.me"><span style=" text-decoration: underline; color:#0000ff;">Kelve T. Henrique</span></a></p><p\
                align="center"><span style=" font-size:7pt; font-style:italic; color:#582f34;">This program comes with absolutely no warranty.</span></p><p\
                align="center"><a href="http://www.gnu.org/licenses/old-licenses/gpl-2.0.html"><span style=" font-size:7pt; text-decoration: underline;\
                color:#582f34;">See the GNU General Public License</span></a><span style=" font-size:7pt; font-style:italic; color:#582f34;">, version 2 or later\
                for details.</span></p></body></html>',
                QMessageBox.Close).exec()

    def updateFileState(self):
        '''
        Updates the state of canvas to avoid losing work
        '''
        if self.hasChanged:
            self.hasChanged = False
        else:
            self.hasChanged = True

    def updateTerm(self):#, by):
        '''
        It is signaled every time there's incoming message from uC
        '''
        if self.port.isOpen():
            wasRead = self.port.readLine()
            self.ui.termEdit.append('<')
            self.ui.termEdit.append((wasRead.data()).decode('utf-8'))

    def setSVGDir(self):
        '''
        Sets the SVG's directory to be used when browsing for the import tool
        '''
        path = QFileDialog.getExistingDirectory(self, "Choose a directory to import SVG's from")
        svg_dir  = path
        self.svg = [os.path.join(svg_dir, f) for f in os.listdir(svg_dir)]
        self.scene.svg = self.svg
        self.nextSVG()

    def nextSVG(self):
        '''
        Browsing of SVG's available for import tool
        '''
        self.svg_index += 1
        self.svg_index = self.svg_index % len(self.svg)
        self.scene.svg_index = self.svg_index
        pix = QPixmap(self.svg[self.svg_index])
        self.ui.nextSVGButton.setIcon(QIcon(pix))

    def updateStepConfig(self, a):
        '''
        Updates the step resolution for scaling of auto mode plotting
        '''
        if a == self.ui.actionFullStep:
            self.terminalThread.scale = FULL_STEP[0]
            self.manualResolution = str(int(FULL_STEP[0]/50))+'$'
        elif a == self.ui.actionHalfStep:
            self.terminalThread.scale = HALF_STEP[0]
            self.manualResolution = str(int(HALF_STEP[0]/50))+'$'
        elif a == self.ui.actionQuarterStep:
            self.terminalThread.scale = QUARTER_STEP[0]
            self.manualResolution = str(int(QUARTER_STEP[0]/50))+'$'
        elif a == self.ui.actionEighthStep:
            self.terminalThread.scale = EIGHTH_STEP[0]
            self.manualResolution = str(int(EIGHTH_STEP[0]/50))+'$'
        else:
            self.terminalThread.scale = SIXTEENTH_STEP[0]
            self.manualResolution = str(int(SIXTEENTH_STEP[0]/50))+'$'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AppWindow()

    sys.exit(app.exec_())

