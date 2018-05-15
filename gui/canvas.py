#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : canvas.py
# -- Author     : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Mai 15
# ----------------------------------------------------------------------------
# -- Description: Dealing with the drawing functionality
# ----------------------------------------------------------------------------

from PyQt5.Qt import Qt                              # Some relevant constants
from PyQt5.QtCore import QLineF, QRectF, QPointF
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import (QPainter, QPixmap, QColor, QPolygonF, QPainterPath,
        QCursor, QTextCursor, QTransform, QPen, QFont)

from constants import *

class MainScene(QGraphicsScene):
    ''' THE CANVAS
    Implementation of tools for drawing, updating the statusbar and keeping
    of the current image being edited
    '''
    def __init__(self, toolsButtonGroup, toolLabel):
        super().__init__()
        self.setSceneRect(VIEW_X, VIEW_Y, CANVAS_WIDTH, CANVAS_HEIGHT)
        self.toolsButtonGroup = toolsButtonGroup
        self.toolLabel = toolLabel
        self.statusbar = self.toolLabel.parentWidget()
        self.textTools = None
        self.view      = None

        self.toolsButtonGroup.buttonClicked.connect(self.setIconTool)

        # The drawable elements
        self.tools     = [1,
                          QPainterPath(),
                          QLineF(),
                          '',          # str instead of QString
                          QRectF(),
                          QRectF(),
                          QPolygonF(),
                          None,
                          QRectF()]

        # Icons for cursor and toolLabel
        self.pixTools  = (QPixmap("./img/eraser.png"),
                          QPixmap("./img/freehand.png"),
                          QPixmap("./img/line.png"),
                          QPixmap("./img/text.png"),
                          QPixmap("./img/rectangle.png"),
                          QPixmap("./img/ellipse.png"),
                          QPixmap("./img/polygon.png"),
                          QPixmap("./img/select.png"),
                          QPixmap("./img/magnifier.png"))

        self.index      = 0        # According to the tools buttons
        self.isDrawing  = False    # While drawing
        self.clickedPos = None     # position where drawing began
        self.isTyping   = False    # Flags when to add a text until next click
        self.item       = None     # Item being drawn - last item drawn
        self.itemsDrawn = None     # List of items on canvas

    # Reimplementing mouse events
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.tools[7]: # Resetting selection
                self.setFocus(0)
                self.item.setFlag(4, False) # set it focusable
                self.removeItem(self.tools[7])
                self.tools[7] = None
            self.isDrawing = True
            pos = e.scenePos()
            self.clickedPos = QPointF(pos.x(), pos.y())
            self.index = self.toolsButtonGroup.checkedId()
            if self.index == 0: # eraser
                self.item = self.itemAt(self.clickedPos, QTransform())
                self.tools[self.index] = self.tools[self.index] - 0.1
                if self.item:
                    self.item.setOpacity(self.tools[self.index])
            elif self.index == 1: # freehand
                self.tools[self.index].moveTo(pos)
                self.item = self.addPath(self.tools[self.index])
            elif self.index == 2: # line
                self.tools[self.index].setP1(self.clickedPos)
                self.tools[self.index].setP2(self.clickedPos)
                self.item = self.addLine(self.tools[self.index])
            elif self.index == 3: # text
                self.item = None
                self.isTyping  = not self.isTyping
                if self.isTyping:
                    self.tools[self.index] = ''
                    self.item = self.addText(self.tools[self.index])
                    self.item.setTextInteractionFlags(Qt.TextEditable)
                    self.item.setPos(self.clickedPos)
                    font = QFont(self.textTools[0].currentFont())
                    font.setPointSize(int(self.textTools[1].currentText()))
                    font.setItalic(self.textTools[2].isChecked())
                    font.setUnderline(self.textTools[3].isChecked())
                    self.item.setFont(font)
            elif self.index == 4: # rectangle
                self.tools[self.index].setTopLeft(self.clickedPos)
                self.tools[self.index].setBottomRight(self.clickedPos)
                self.item = self.addRect(self.tools[self.index])
            elif self.index == 5: # ellipse
                self.tools[self.index].setTopLeft(self.clickedPos)
                self.tools[self.index].setBottomRight(self.clickedPos)
                self.item = self.addEllipse(self.tools[self.index])
            elif self.index == 6: # polygon
                if not self.tools[self.index].isEmpty():
                    self.tools[self.index].append(self.clickedPos)
                    self.item.setPolygon(self.tools[self.index])
                else:
                    self.tools[self.index].append(self.clickedPos)
                    self.item = self.addPolygon(self.tools[self.index])
            elif self.index == 7: # select
                self.item = self.itemAt(self.clickedPos, QTransform())
                if self.item:
                    self.item.setFlag(4) # set it focusable
                    self.setFocusItem(self.item)
                    rectangle = self.item.sceneBoundingRect()
                    pen       = QPen(Qt.DotLine)
                    self.tools[self.index] = self.addRect(rectangle, pen)
            elif self.index == 8: # magnifier
                self.tools[self.index].setTopLeft(self.clickedPos)
                self.tools[self.index].setBottomRight(self.clickedPos)
                pen       = QPen(Qt.DotLine)
                self.item = self.addRect(self.tools[self.index], pen)
        else:
            if self.index == 8:               # magnifier
                self.view.resetTransform()

    def mouseDoubleClickEvent(self, e):
        if self.index == 6:               # polygon
            self.isDrawing = False
            self.tools[self.index].clear()

    def mouseMoveEvent(self, e):
        if self.isDrawing:
            pos = e.scenePos()
            mousePos = QPointF(pos.x(), pos.y())
            if self.index == 0: # eraser
                pass
            elif self.index == 1: # freehand
                self.tools[self.index].lineTo(pos)
                self.item.setPath(self.tools[self.index])
            elif self.index == 2: # line
                self.tools[self.index].setP2(mousePos)
                self.item.setLine(self.tools[self.index])
            elif self.index == 3: # text
                pass
            elif self.index == 4: # rectangle
                if self.clickedPos.x() > mousePos.x() and self.clickedPos.y() > mousePos.y():
                    self.tools[self.index].setBottomRight(self.clickedPos)
                    self.tools[self.index].setTopLeft(mousePos)
                elif self.clickedPos.y() > mousePos.y():
                    self.tools[self.index].setBottomLeft(self.clickedPos)
                    self.tools[self.index].setTopRight(mousePos)
                elif self.clickedPos.x() > mousePos.x():
                    self.tools[self.index].setTopRight(self.clickedPos)
                    self.tools[self.index].setBottomLeft(mousePos)
                else:
                    self.tools[self.index].setBottomRight(mousePos)

                self.item.setRect(self.tools[self.index])
            elif self.index == 5: # ellipse
                if self.clickedPos.x() > mousePos.x() and self.clickedPos.y() > mousePos.y():
                    self.tools[self.index].setBottomRight(self.clickedPos)
                    self.tools[self.index].setTopLeft(mousePos)
                elif self.clickedPos.y() > mousePos.y():
                    self.tools[self.index].setBottomLeft(self.clickedPos)
                    self.tools[self.index].setTopRight(mousePos)
                elif self.clickedPos.x() > mousePos.x():
                    self.tools[self.index].setTopRight(self.clickedPos)
                    self.tools[self.index].setBottomLeft(mousePos)
                else:
                    self.tools[self.index].setBottomRight(mousePos)

                self.item.setRect(self.tools[self.index])
            elif self.index == 6: # polygon
                self.tools[self.index].append(mousePos)
                self.item.setPolygon(self.tools[self.index])
                toRemove = self.tools[self.index].lastIndexOf(self.tools[self.index].last())
                self.tools[self.index].remove(toRemove)
            elif self.index == 7: # select
                m = mousePos - self.clickedPos
                self.clickedPos = mousePos
                if self.item:
                    self.item.moveBy(m.x(), m.y())
                    mousePos = self.item.mapFromScene(mousePos)
                    self.tools[self.index].moveBy(m.x(), m.y())
            elif self.index == 8: # magnifier
                if self.clickedPos.x() > mousePos.x() and self.clickedPos.y() > mousePos.y():
                    self.tools[self.index].setBottomRight(self.clickedPos)
                    self.tools[self.index].setTopLeft(mousePos)
                elif self.clickedPos.y() > mousePos.y():
                    self.tools[self.index].setBottomLeft(self.clickedPos)
                    self.tools[self.index].setTopRight(mousePos)
                elif self.clickedPos.x() > mousePos.x():
                    self.tools[self.index].setTopRight(self.clickedPos)
                    self.tools[self.index].setBottomLeft(mousePos)
                else:
                    self.tools[self.index].setBottomRight(mousePos)

                self.item.setRect(self.tools[self.index])

    def mouseReleaseEvent(self, e):
        if self.index in (0,1,2,4,5,7): # except polygon, text, magnifier
            self.isDrawing = False
        if self.index == 8 and self.isDrawing:
            self.isDrawing = False
            self.view.fitInView(self.item)
            self.removeItem(self.item)

    def wheelEvent(self, e):
        pass

    # Reimplementing keypress events
    def keyPressEvent(self, e):
        # Ctrl-Z Functionality
        if e.modifiers() and Qt.ControlModifier and e.key() == Qt.Key_Z:
            try:
                self.itemsDrawn = self.items(Qt.AscendingOrder)
                self.removeItem(self.itemsDrawn[-1])
                # Cleaning in case smth was being drawn
                self.isDrawing = False
                self.isTyping  = False
                self.tools[1]  = QPainterPath()
                self.tools[6].clear()
            except:
                self.statusbar.showMessage("There is no item in Canvas", TIMEOUT_STATUS)
        # Delete Functionality
        if e.key() == Qt.Key_Delete:
            if self.item == self.focusItem():
                self.removeItem(self.tools[7])
                self.tools[7] = None
                self.removeItem(self.item)
        # Text Functionality
        if self.isTyping:
            if e.key() == Qt.Key_Backspace:
                self.tools[self.index] = self.tools[self.index][:-1]
            else:
                self.tools[self.index] = self.tools[self.index] + e.text()
            self.item.setPlainText(self.tools[self.index])

    def setIconTool(self, button):
        ''' Sets the icon for the statusbar and the image for cursor on the canvas '''
        if button.isChecked():
            index = self.toolsButtonGroup.id(button)
            pixel = self.pixTools[index]
            cursor = QCursor(pixel, 0, pixel.height())
            self.view.setCursor(cursor)
            self.toolLabel.setPixmap(self.pixTools[index])
