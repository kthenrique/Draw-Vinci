#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : canvas.py
# -- Author     : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Mai 02
# ----------------------------------------------------------------------------
# -- Description: Dealing with the drawing functionality
# ----------------------------------------------------------------------------

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import (QPainter, QPixmap, QColor, QPolygonF, QPainterPath,
        QCursor)
from PyQt5.QtCore import QLineF, QRectF, QPointF

CANVAS_WIDTH = 390
CANVAS_HEIGHT = 310

class MainScene(QGraphicsScene):
    ''' THE CANVAS
    Implementation of tools for drawing, updating the statusbar and keeping
    of the current image being edited
    '''
    def __init__(self, toolsButtonGroup, toolLabel):
        super().__init__()
        self.setSceneRect(0,0,CANVAS_WIDTH,CANVAS_HEIGHT)
        self.toolsButtonGroup = toolsButtonGroup
        self.toolLabel = toolLabel
        self.view = None

        self.toolsButtonGroup.buttonPressed.connect(self.setIconTool)

        # The drawable elements
        self.tools     = (None,
                          QPainterPath(),
                          QLineF(),
                          None,
                          QRectF(),
                          QRectF(),
                          QPolygonF())

        # Icons for cursor and toolLabel
        self.pixTools  = (QPixmap("./img/eraser.png"),
                          QPixmap("./img/freehand.png"),
                          QPixmap("./img/line.png"),
                          QPixmap("./img/text.png"),
                          QPixmap("./img/rectangle.png"),
                          QPixmap("./img/ellipse.png"),
                          QPixmap("./img/polygon.png"),
                          QPixmap("./img/select.png"))

        self.index      = 0        # According to the tools buttons
        self.isDrawing  = False    # While drawing
        self.clickedPos = None     # position where drawing began
        self.item       = None     # Item being drawn

    # Reimplementing mouse events
    def mousePressEvent(self, e):
        self.isDrawing = True
        pos = e.scenePos()
        self.clickedPos = QPointF(pos.x(), pos.y())

        self.index = self.toolsButtonGroup.checkedId()

        if self.index == 0: # eraser
            pass
        if self.index == 1: # freehand
            self.tools[self.index].moveTo(pos)
            self.item = self.addPath(self.tools[self.index])
        if self.index == 2: # line
            self.tools[self.index].setP1(self.clickedPos)
            self.tools[self.index].setP2(self.clickedPos)
            self.item = self.addLine(self.tools[self.index])
        if self.index == 3: # text
            pass
        if self.index == 4: # rectangle
            self.tools[self.index].setTopLeft(self.clickedPos)
            self.tools[self.index].setBottomRight(self.clickedPos)
            self.item = self.addRect(self.tools[self.index])
        if self.index == 5: # ellipse
            self.tools[self.index].setTopLeft(self.clickedPos)
            self.tools[self.index].setBottomRight(self.clickedPos)
            self.item = self.addEllipse(self.tools[self.index])
        if self.index == 6: # polygon
            if self.item:
                self.tools[self.index].append(self.clickedPos)
                self.item.setPolygon(self.tools[self.index])
            else:
                self.tools[self.index].clear()
                self.tools[self.index].append(self.clickedPos)
                self.item = self.addPolygon(self.tools[self.index])

    def mouseDoubleClickEvent(self, e):
        self.isDrawing = False
        self.item      = None

    def mouseMoveEvent(self, e):
        if self.isDrawing:
            pos = e.scenePos()
            mousePos = QPointF(pos.x(), pos.y())
            if self.index == 0: # eraser
                pass
            if self.index == 1: # freehand
                self.tools[self.index].lineTo(pos)
                self.item.setPath(self.tools[self.index])
            if self.index == 2: # line
                self.tools[self.index].setP2(mousePos)
                self.item.setLine(self.tools[self.index])
            if self.index == 3: # text
                pass
            if self.index == 4: # rectangle
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
            if self.index == 5: # ellipse
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
            if self.index == 6: # polygon
                self.tools[self.index].append(mousePos)
                self.item.setPolygon(self.tools[self.index])
                toRemove = self.tools[self.index].lastIndexOf(self.tools[self.index].last())
                self.tools[self.index].remove(toRemove)

    def mouseReleaseEvent(self, e):
        if self.index != 6:
            self.isDrawing = False
            self.item  = None

    def setIconTool(self, button):
        ''' Sets the icon for the statusbar and the image for cursor on the canvas '''
        index = self.toolsButtonGroup.id(button)
        cursor = QCursor(self.pixTools[index])
        self.view.setCursor(cursor)
        self.toolLabel.setPixmap(self.pixTools[index])