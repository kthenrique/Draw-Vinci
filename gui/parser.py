#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW_VINCI
# ----------------------------------------------------------------------------
# -- File       : parser.py
# -- Author     : Kelve T. Henrique
# -- Last update: 2018 Mai 13
# ----------------------------------------------------------------------------
# -- Description: It parses a svg file:
# --                 - reads svg file
# --                 - transform it in QGraphicsItem's
# ----------------------------------------------------------------------------

from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsEllipseItem
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
                print("not a rect")
            else:
                newCanvasRect = QGraphicsRectItem()
                x = float(rect.attribute('x'))
                y = float(rect.attribute('y'))
                widht = float(rect.attribute('width'))
                height = float(rect.attribute('height'))

                newCanvasRect.setRect(x, y, width, height)
                listOfItems.append(newCanvasRect)

            # ellipses
            elli = gNode.firstChildElement('ellipse')               # DomElement
            if not elli.hasAttributes():
                print("not a rect")
            else:
                newCanvasElli = QGraphicsEllipseItem()
                cx = float(elli.attribute('cx'))
                cy = float(elli.attribute('cy'))
                width = 2*float(elli.attribute('rx'))
                height = 2*float(elli.attribute('ry'))

                x = cx - float(elli.attribute('rx'))
                y = cy - float(elli.attribute('ry'))

                newCanvasElli.setRect(x, y, width, height)
                listOfItems.append(newCanvasElli)

        file_.close()
        return listOfItems


