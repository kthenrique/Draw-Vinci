#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW_VINCI
# ----------------------------------------------------------------------------
# -- File       : parser.py
# -- Author     : Kelve T. Henrique
# -- Last update: 2018 Mai 15
# ----------------------------------------------------------------------------
# -- Description: It parses a svg file:
# --                 - reads svg file
# --                 - transform it in QGraphicsItem's
# ----------------------------------------------------------------------------

from PyQt5.QtCore import QFile, QIODevice
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
            return listOfRect

        gList      = doc.elementsByTagName('g')                  # DomNodeList with g tagged elements
        print(gList.length())
        for index in range(0, gList.length()):
            gNode = gList.item(index)                            # DomNode

            # rectangles
            rect = gNode.firstChildElement('rect')               # DomElement
            if not rect.hasAttributes():
                pass
            else:
                print("rectangle")
                newCanvasRect = QGraphicsRectItem()
                x = float(rect.attribute('x'))
                y = float(rect.attribute('y'))
                width = float(rect.attribute('width'))
                height = float(rect.attribute('height'))

                newCanvasRect.setRect(x, y, width, height)
                listOfItems.append(newCanvasRect)

            # ellipses
            elli = gNode.firstChildElement('ellipse')
            if not elli.hasAttributes():
                pass
            else:
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

            # polyline
            lin = gNode.firstChildElement('polyline')
            if not lin.hasAttributes():
                pass
            else:
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

            # polygons
            poly = gNode.firstChildElement('polygon')
            if not poly.hasAttributes():
                pass
            else:
                print("polygon")
                newPoly       = QPolygonF()
                newCanvasPoly = QGraphicsPolygonItem()

                points = (poly.attribute('points'))
                points = points.split()
                for point in points:
                    coord = point.split(',')
                    newPoly.append(float(coord[0]), float(coord[1]))


                newCanvasPoly.setPolygon(newPoly)
                listOfItems.append(newCanvasPoly)

            # path
            pat = gNode.firstChildElement('path')
            while not pat.isNull():
                print("path")
                newPat       = QPainterPath()
                newCanvasPat = QGraphicsPathItem()

                paths = (pat.attribute('d'))

                # Normalise string
                for letter in ('m', 'M', 'l',  'L', 'h',  'H', 'v',  'V', 'c',  'C', 's',  'S', 'q',  'Q', 't',  'T', 'a',  'A', 'z', 'Z'):
                    paths = paths.replace(letter, ' '+letter)

                print(paths)
                paths = paths.split()
                currentCoord = [50,50]
                lastCtrlPoint= None
                for path in paths:
                    print(path)
                    coord = path[1:]
                    coor = coord.replace('-', ' -')
                    coor = coor.replace(',', ' ')
                    coor = coor.split()
                    coord = coor
                    print(coord)
                    print(currentCoord)
                    if path[0]   == 'M':        # moveTo
                        currentCoord[0] = float(coord[0])
                        currentCoord[1] = float(coord[1])
                        newPat.moveTo(currentCoord[0], currentCoord[1])
                    elif path[0] == 'm':        # moveTo relative
                        currentCoord[0] = currentCoord[0] + float(coord[0])
                        currentCoord[1] = currentCoord[1] + float(coord[1])
                        newPat.moveTo(currentCoord[0], currentCoord[1])
                    elif path[0] == 'L':        # lineTo
                        currentCoord[0] = float(coord[0])
                        currentCoord[1] = float(coord[1])
                        newPat.lineTo(currentCoord[0], currentCoord[1])
                    elif path[0] == 'l':        # lineTo relative
                        currentCoord[0] = currentCoord[0] + float(coord[0])
                        currentCoord[1] = currentCoord[1] + float(coord[1])
                        newPat.lineTo(currentCoord[0], currentCoord[1])
                    elif path[0] == 'H':        # horizontal lineTo
                        currentCoord[0] = float(coord[0])
                        newPat.lineTo(currentCoord[0], currentCoord[1])
                    elif path[0] == 'h':        # horizontal lineTo relative
                        currentCoord[0] = currentCoord[0] + float(coord[0])
                        newPat.lineTo(currentCoord[0], currentCoord[1])
                    elif path[0] == 'V':        # vertical lineTo
                        currentCoord[1] = float(coord[0])
                        newPat.lineTo(currentCoord[0], currentCoord[1])
                    elif path[0] == 'v':        # vertical lineTo relative
                        currentCoord[1] = currentCoord[1] + float(coord[0])
                        newPat.lineTo(currentCoord[0], currentCoord[1])
                    elif path[0] == 'C':        # curveto
                        currentCoord[0] = float(coord[4])
                        currentCoord[1] = float(coord[5])
                        newPat.cubicTo(float(coord[0]), float(coord[1]), float(coord[2]), float(coord[3]), currentCoord[0], currentCoord[1])
                        lastCtrlPoint= [float(coord[2]), float(coord[3])]
                    elif path[0] == 'c':        # curveto relative
                        currentCoord[0] = currentCoord[0] + float(coord[4])
                        currentCoord[1] = currentCoord[1] + float(coord[5])
                        newPat.cubicTo(float(coord[0]), float(coord[1]), float(coord[2]), float(coord[3]), currentCoord[0], currentCoord[1])
                        lastCtrlPoint= [float(coord[2]), float(coord[3])]
                    elif path[0] == 'S':        # smooth curveto
                        if lastCtrlPoint:
                            currentCoord[0] = float(coord[2])
                            currentCoord[1] = float(coord[3])
                            newPat.cubicTo(float(lastCtrlPoint[0]), lastCtrlPoint[1], float(coord[0]), float(coord[1]), currentCoord[0], currentCoord[1])
                        else:
                            newPat.cubicTo(currentCoord[0], currentCoord[1], float(coord[0]), float(coord[1]), float(coord[2]), float(coord[3]))
                            currentCoord[0] = float(coord[2])
                            currentCoord[1] = float(coord[3])
                    elif path[0] == 's':        # smooth curveto relative
                        if lastCtrlPoint:
                            currentCoord[0] = currentCoord[0] + float(coord[2])
                            currentCoord[1] = currentCoord[1] + float(coord[3])
                            newPat.cubicTo(float(lastCtrlPoint[0]), lastCtrlPoint[1], float(coord[0]), float(coord[1]), currentCoord[0], currentCoord[1])
                        else:
                            newPat.cubicTo(currentCoord[0], currentCoord[1], float(coord[0]), float(coord[1]), currentCoord[0] + float(coord[2]), currentCoord[0] + float(coord[2]))
                            currentCoord[0] = currentCoord[0] + float(coord[2])
                            currentCoord[1] = currentCoord[1] + float(coord[3])
                    elif path[0] == 'Q':        # quadratic Bézier curve
                        pass
                    elif path[0] == 'q':        # quadratic Bézier curve relative
                        pass
                    elif path[0] == 'T':        # smooth quadratic Bézier curveto
                        pass
                    elif path[0] == 't':        # smooth quadratic Bézier curveto relative
                        pass
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
            if not tex.hasAttributes():
                pass
            else:
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

        file_.close()
        return listOfItems


