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
from PyQt5.QtGui import QPainter, QPixmap, QColor, QPolygonF, QPicture, QPainterPath
from PyQt5.QtCore import QLineF, QRectF, QPointF

CANVAS_WIDTH = 390
CANVAS_HEIGHT = 310

class MainScene(QGraphicsScene):
    def __init__(self, toolsButtonGroup, artworkLabel):
        super().__init__()
        self.setSceneRect(0,0,CANVAS_WIDTH,CANVAS_HEIGHT)
        self.toolsButtonGroup = toolsButtonGroup
        self.artworkLabel = artworkLabel

        # The drawable elements
        self.eraser    = None
        self.freehand  = QPainterPath()
        self.line      = QLineF()
        self.text      = None
        self.rectangle = QRectF()
        self.ellipse   = QRectF()
        self.polygon   = QPolygonF()

        self.isDrawing  = False
        self.clickedPos = None
        self.item       = None

    # Reimplementing mouse events
    def mousePressEvent(self, e):
        pos = e.scenePos()
        self.clickedPos = QPointF(pos.x(), pos.y())
        if self.toolsButtonGroup.checkedId() == 1: # eraser
            pic = QPixmap("./img/eraser.png")
            self.artworkLabel.setPixmap(pic)
        if self.toolsButtonGroup.checkedId() == 2: # freehand
            pic = QPixmap("./img/freehand.png")
            self.artworkLabel.setPixmap(pic)
            self.isDrawing = True
            self.freehand.moveTo(pos)
            self.item = self.addPath(self.freehand)
        if self.toolsButtonGroup.checkedId() == 3: # line
            pic = QPixmap("./img/line.png")
            self.artworkLabel.setPixmap(pic)
            self.isDrawing = True
            self.line.setP1(self.clickedPos)
            self.line.setP2(self.clickedPos)
            self.item = self.addLine(self.line)
        if self.toolsButtonGroup.checkedId() == 4: # text
            pic = QPixmap("./img/text.png")
            self.artworkLabel.setPixmap(pic)
        if self.toolsButtonGroup.checkedId() == 5: # rectangle
            pic = QPixmap("./img/rectangle.png")
            self.artworkLabel.setPixmap(pic)
            self.isDrawing = True
            self.rectangle.setTopLeft(self.clickedPos)
            self.rectangle.setBottomRight(self.clickedPos)
            self.item = self.addRect(self.rectangle)
        if self.toolsButtonGroup.checkedId() == 6: # ellipse
            pic = QPixmap("./img/ellipse.png")
            self.artworkLabel.setPixmap(pic)
            self.isDrawing = True
            self.ellipse.setTopLeft(self.clickedPos)
            self.ellipse.setBottomRight(self.clickedPos)
            self.item = self.addEllipse(self.ellipse)
        if self.toolsButtonGroup.checkedId() == 7: # polygon
            pic = QPixmap("./img/polygon.png")
            self.artworkLabel.setPixmap(pic)
            self.isDrawing = True
            self.polygon.united(QPolygonF(self.clickedPos))
            self.item = self.addPolygon(self.polygon)

    def dragLeaveEvent(self, e):
        pass

    def mouseMoveEvent(self, e):
        if self.isDrawing:
            pos = e.scenePos()
            mousePos = QPointF(pos.x(), pos.y())
            if self.toolsButtonGroup.checkedId() == 1: # eraser
                pass
            if self.toolsButtonGroup.checkedId() == 2: # freehand
                self.freehand.lineTo(pos)
                self.item.setPath(self.freehand)
            if self.toolsButtonGroup.checkedId() == 3: # line
                self.line.setP2(mousePos)
                self.item.setLine(self.line)
            if self.toolsButtonGroup.checkedId() == 4: # text
                pass
            if self.toolsButtonGroup.checkedId() == 5: # rectangle
                if self.clickedPos.x() > mousePos.x() and self.clickedPos.y() > mousePos.y():
                    self.rectangle.setBottomRight(self.clickedPos)
                    self.rectangle.setTopLeft(mousePos)
                elif self.clickedPos.y() > mousePos.y():
                    self.rectangle.setBottomLeft(self.clickedPos)
                    self.rectangle.setTopRight(mousePos)
                elif self.clickedPos.x() > mousePos.x():
                    self.rectangle.setTopRight(self.clickedPos)
                    self.rectangle.setBottomLeft(mousePos)
                else:
                    self.rectangle.setBottomRight(mousePos)
                    self.rectangle = self.rectangle.normalized()

                self.item.setRect(self.rectangle)
            if self.toolsButtonGroup.checkedId() == 6: # ellipse
                if self.clickedPos.x() > mousePos.x() and self.clickedPos.y() > mousePos.y():
                    self.ellipse.setBottomRight(self.clickedPos)
                    self.ellipse.setTopLeft(mousePos)
                elif self.clickedPos.y() > mousePos.y():
                    self.ellipse.setBottomLeft(self.clickedPos)
                    self.ellipse.setTopRight(mousePos)
                elif self.clickedPos.x() > mousePos.x():
                    self.ellipse.setTopRight(self.clickedPos)
                    self.ellipse.setBottomLeft(mousePos)
                else:
                    self.ellipse.setBottomRight(mousePos)
                    self.ellipse = self.ellipse.normalized()

                self.item.setRect(self.ellipse)
            if self.toolsButtonGroup.checkedId() == 7: # polygon
                self.polygon.united(QPolygonF(mousePos))
                self.item.setPolygon(self.polygon)

    def mouseReleaseEvent(self, e):
        self.isDrawing = False
        if self.toolsButtonGroup.checkedId() == 1: # eraser
            pass
        if self.toolsButtonGroup.checkedId() == 2: # freehand
            pass
        if self.toolsButtonGroup.checkedId() == 3: # line
            pass
        if self.toolsButtonGroup.checkedId() == 4: # text
            pass
        if self.toolsButtonGroup.checkedId() == 5: # rectangle
            pass
        if self.toolsButtonGroup.checkedId() == 6: # ellipse
            pass
        if self.toolsButtonGroup.checkedId() == 7: # polygon
            pass

