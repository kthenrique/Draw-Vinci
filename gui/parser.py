#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW_VINCI
# ----------------------------------------------------------------------------
# -- File       : parser.py
# -- Author     : Kelve T. Henrique
# -- Last update: 2018 Mai 18
# ----------------------------------------------------------------------------
# -- Description: It parses a svg file:
# --                 - reads svg file
# --                 - transform it in QGraphicsItem's
# ----------------------------------------------------------------------------

from PyQt5.QtCore import QFile, QIODevice, QPointF
from PyQt5.QtWidgets import (QGraphicsRectItem, QGraphicsEllipseItem,
        QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsPathItem,
        QGraphicsTextItem)
from PyQt5.QtGui import QPolygonF, QPainterPath, QFont
from PyQt5.QtXml import QDomDocument, QDomNodeList, QDomNode, QDomElement


class parser():
    '''
    SVG Parser
    '''
    def __init__(self):
        pass

    def getElements(self, filename):
        listOfItems = []                      # list of rectangles items
        doc         = QDomDocument()          # file to parse
        file_       = QFile(filename)         # open svg file

        if not file_.open(QIODevice.ReadOnly) or not doc.setContent(file_):    # if couldn't open or failed to make i QDomDocument
            print("Couldn't open or failed to make th DomDoc")
            return False

        gList      = doc.elementsByTagName('g')                  # DomNodeList with g tagged elements
        print(gList.length())
        for index in range(0, gList.length()):
            gNode = gList.item(index)                            # DomNode

            # rectangles
            rect = gNode.firstChildElement('rect')               # DomElement
            while not rect.isNull():
                print("rectangle")
                newCanvasRect = QGraphicsRectItem()
                x = float(rect.attribute('x'))
                y = float(rect.attribute('y'))
                width = float(rect.attribute('width'))
                height = float(rect.attribute('height'))

                newCanvasRect.setRect(x, y, width, height)
                listOfItems.append(newCanvasRect)
                rect = rect.nextSiblingElement('rect')

            # ellipses
            elli = gNode.firstChildElement('ellipse')
            while not elli.isNull():
                print("ellipse")
                newCanvasElli = QGraphicsEllipseItem()
                cx = float(elli.attribute('cx'))
                cy = float(elli.attribute('cy'))
                width = 2*float(elli.attribute('rx'))
                height = 2*float(elli.attribute('ry'))

                x = cx - float(elli.attribute('rx'))
                y = cy - float(elli.attribute('ry'))

                newCanvasElli.setRect(x, y, width, height)
                listOfItems.append(newCanvasElli)
                elli = elli.nextSiblingElement('ellipse')

            # polyline
            lin = gNode.firstChildElement('polyline')
            while not lin.isNull():
                print("line")
                newCanvasLin = QGraphicsLineItem()
                points = (lin.attribute('points'))
                points = points.split()
                coord1 = points[0].split(',')
                coord2 = points[1].split(',')
                x1 = float(coord1[0])
                y1 = float(coord1[1])
                x2 = float(coord2[0])
                y2 = float(coord2[1])

                newCanvasLin.setLine(x1, y1, x2, y2)
                listOfItems.append(newCanvasLin)
                lin = lin.nextSiblingElement('polyline')

            # polygons
            poly = gNode.firstChildElement('polygon')
            while not poly.isNull():
                print("polygon")
                newPoly       = QPolygonF()
                newCanvasPoly = QGraphicsPolygonItem()

                points = (poly.attribute('points'))
                points = points.split()
                for point in points:
                    coord = point.split(',')
                    newPoly.append(QPointF(float(coord[0]), float(coord[1])))


                newCanvasPoly.setPolygon(newPoly)
                listOfItems.append(newCanvasPoly)
                poly = poly.nextSiblingElement('polygon')

            # path
            pat = gNode.firstChildElement('path')
            newPat       = QPainterPath()
            newCanvasPat = QGraphicsPathItem()
            while not pat.isNull():
                print("path")

                paths = (pat.attribute('d'))

                # Normalise string
                paths = paths.replace(' ', ',')
                for letter in ('m', 'M', 'l',  'L', 'h',  'H', 'v',  'V', 'c',  'C', 's',  'S', 'q',  'Q', 't',  'T', 'a',  'A', 'z', 'Z'):
                    paths = paths.replace(letter, ' '+letter)

                paths = paths.split()
                lastCubicCtrl = None
                lastQuadCtrl = None
                for path in paths:
                    coord = path[1:]
                    coord = coord.replace('-', ' -')
                    coord = coord.replace(',', ' ')
                    coord = coord.split()
                    for index in range(len(coord)):  # Convert str to float
                        coord[index] = float(coord[index])
                    if path[0]   == 'M':        # moveTo
                        newPat.moveTo(coord[0], coord[1])
                    elif path[0] == 'm':        # moveTo relative
                        newPat.moveTo(newPat.currentPosition() + QPointF(coord[0], coord[1]))
                    elif path[0] == 'L':        # lineTo
                        newPat.lineTo(coord[0], coord[1])
                    elif path[0] == 'l':        # lineTo relative
                        newPat.lineTo(newPat.currentPosition() + QPointF(coord[0], coord[1]))
                    elif path[0] == 'H':        # horizontal lineTo
                        newPat.lineTo(coord[0], newPat.currentPosition().y())
                    elif path[0] == 'h':        # horizontal lineTo relative
                        newPat.lineTo(newPat.currentPosition().x()+coord[0], newPat.currentPosition().y())
                    elif path[0] == 'V':        # vertical lineTo
                        newPat.lineTo(newPat.currentPosition().x(), coord[0])
                    elif path[0] == 'v':        # vertical lineTo relative
                        newPat.lineTo(newPat.currentPosition().x(), newPat.currentPosition().y()+coord[0])
                    elif path[0] == 'C':        # curveto
                        lastCubicCtrl = QPointF(coord[2], coord[3])
                        newPat.cubicTo(coord[0], coord[1], coord[2], coord[3], coord[4], coord[5])
                        Ctrl = newPat.currentPosition() - (lastCubicCtrl-newPat.currentPosition())
                    elif path[0] == 'c':        # curveto relative
                        lastCubicCtrl = newPat.currentPosition()+QPointF(coord[2], coord[3])
                        newPat.cubicTo(newPat.currentPosition()+QPointF(coord[0],coord[1]),\
                                       newPat.currentPosition()+QPointF(coord[2],coord[3]),\
                                       newPat.currentPosition()+QPointF(coord[4],coord[5]))
                        Ctrl = newPat.currentPosition() - (lastCubicCtrl-newPat.currentPosition())
                    elif path[0] == 'S':        # smooth curveto
                        if lastCubicCtrl:
                            Ctrl = newPat.currentPosition() - (lastCubicCtrl-newPat.currentPosition())
                            lastCubicCtrl = QPointF(coord[0], coord[1])
                            newPat.cubicTo(Ctrl,\
                                           QPointF(coord[0], coord[1]),\
                                           QPointF(coord[2], coord[3]))
                        else:
                            newPat.cubicTo(newPat.currentPosition().x(),\
                                           newPat.currentPosition().y(),\
                                           coord[0], coord[1],\
                                           coord[2], coord[3])
                    elif path[0] == 's':        # smooth curveto relative
                        if lastCubicCtrl:
                            Ctrl = newPat.currentPosition() - (lastCubicCtrl-newPat.currentPosition())
                            lastCubicCtrl = QPointF(newPat.currentPosition().x()+coord[0],\
                                                    newPat.currentPosition().y()+coord[1])
                            newPat.cubicTo(Ctrl.x(),\
                                           Ctrl.y(),\
                                           newPat.currentPosition().x()+coord[0],\
                                           newPat.currentPosition().y()+coord[1],\
                                           newPat.currentPosition().x()+coord[2],\
                                           newPat.currentPosition().y()+coord[3])
                        else:
                            newPat.cubicTo(newPat.currentPosition().x(),\
                                           newPat.currentPosition().y(),\
                                           newPat.currentPosition().x()+coord[0],\
                                           newPat.currentPosition().y()+coord[1],\
                                           newPat.currentPosition().x()+coord[2],\
                                           newPat.currentPosition().y()+coord[3])
                    elif path[0] == 'Q':        # quadratic Bézier curve
                        newPat.quadTo(coord[0], coord[1], coord[2], coord[3])
                        lastQuadCtrl = QPointF(coord[0], coord[1])
                    elif path[0] == 'q':        # quadratic Bézier curve relative
                        newPat.quadTo(newPat.currentPosition()+QPointf(coord[0], coord[1]),\
                                      newPat.currentPosition()+QPointf(coord[2], coord[3]))
                        lastQuadCtrl = QPointF(coord[0], coord[1])
                    elif path[0] == 'T':        # smooth quadratic Bézier curveto
                        if lastQuadCtrl:
                            Ctrl = newPat.currentPosition() - (lastQuadCtrl-newPat.currentPosition())
                            newPat.quadTo(Ctrl, QPointF(coord[0], coord[1]))
                            lastQuadCtrl = Ctrl
                        else:
                            newPat.quadTo(newPat.currentPosition(),\
                                          QPointF(coord[0], coord[1]))
                            lastQuadCtrl = newPat.currentPosition()
                    elif path[0] == 't':        # smooth quadratic Bézier curveto relative
                        if lastQuadCtrl:
                            Ctrl = newPat.currentPosition() - (lastQuadCtrl-newPat.currentPosition())
                            newPat.quadTo(Ctrl, newPat.currentPosition()+QPointF(coord[0], coord[1]))
                            lastQuadCtrl = Ctrl
                        else:
                            newPat.quadTo(newPat.currentPosition(),\
                                          newPat.currentPosition()+QPointF(coord[0], coord[1]))
                            lastQuadCtrl = newPat.currentPosition()
                    elif path[0] == 'A':        # elliptical arc
                        pass
                    elif path[0] == 'a':        # elliptical arc relative
                        pass
                    elif path[0] == 'Z' or path[0] == 'z':        # closePath
                        newPat.closeSubpath()
                    else:
                        print('Strange Command at path tag in SVG file')

                newCanvasPat.setPath(newPat)
                listOfItems.append(newCanvasPat)
                pat = pat.nextSiblingElement('path')

            # text
            tex = gNode.firstChildElement('text')
            while not tex.isNull():
                print("text")

                x     = float(tex.attribute('x'))
                y     = float(tex.attribute('y'))
                font  = tex.attribute('font-family')
                size  = float(tex.attribute('font-size'))
                weight= float(tex.attribute('font-weight'))
                style = tex.attribute('font-style')
                isItalic = False
                if style == 'italic':
                    isItalic = True

                newCanvasTex = QGraphicsTextItem(tex.text())
                newCanvasTex.setFont(QFont(font, size, weight, isItalic))
                newCanvasTex.setPos(x,y)

                listOfItems.append(newCanvasTex)
                tex = tex.nextSiblingElement('text')

        file_.close()
        return listOfItems
