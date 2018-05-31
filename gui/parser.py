#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW_VINCI
# ----------------------------------------------------------------------------
# -- File       : parser.py
# -- Author     : Kelve T. Henrique
# -- Last update: 2018 Mai 31
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

from constants import CANVAS_HEIGHT, CANVAS_WIDTH, SCALE


def getElements(filename, writeCode = False, toScale = False):
    '''
    SVG Parser
    '''
    if writeCode:
        g_code_path = filename.replace('.svg', '.gcode')
        g_code = open(g_code_path, mode ='w', encoding='utf-8')
        print('Initializing G-CODE')
        text  = '#G28$\n'+\
                '#G90$\n'
        isRelative = False
        penUp = True

    listOfItems = []                      # list of items
    doc         = QDomDocument()          # file to parse
    file_       = QFile(filename)         # open svg file

    if not file_.open(QIODevice.ReadOnly) or not doc.setContent(file_):    # if couldn't open or failed to make i QDomDocument
        print("Couldn't open or failed to make DomDoc")
        if writeCode:
            g_code.close()
        return False

    # Acquiring dimensions & viewBox parameters
    rootElement = doc.documentElement()
    svg_width  = rootElement.attribute('width')
    svg_height = rootElement.attribute('height')
    print('width:{0} height:{1}'.format(svg_width, svg_height))
    viewBox = rootElement.attribute('viewBox')
    viewBox = viewBox.split()
    for index in range(len(viewBox)):
        viewBox[index] = float(viewBox[index])
    if viewBox:
        dx_scale = viewBox[2]-viewBox[0]
        dy_scale = viewBox[3]-viewBox[1]
        print('viewbox delta: ({0}, {1})'.format(dx_scale, dy_scale))

        REPOSITION = (-viewBox[0], -viewBox[1]) # Just for plotter
        if viewBox[2] > CANVAS_WIDTH or viewBox[3] > CANVAS_HEIGHT:
            RESCALE  = SCALE/viewBox[3]
        else:
            RESCALE  = 1
    else:
        REPOSITION = (0,0)
        RESCALE    = 1

    gList = doc.elementsByTagName('g')
    for index in range(0, gList.length()):
        gNode = gList.item(index)

        # rectangles
        rect = gNode.firstChildElement('rect')
        while not rect.isNull():
            print("rectangle")
            newCanvasRect = QGraphicsRectItem()
            x      = float(rect.attribute('x'))
            y      = float(rect.attribute('y'))
            width  = float(rect.attribute('width'))
            height = float(rect.attribute('height'))

            if toScale:
                x      = RESCALE * x
                y      = RESCALE * y
                width  = RESCALE * width
                height = RESCALE * height

            newCanvasRect.setRect(x, y, width, height)
            listOfItems.append(newCanvasRect)

            # G-CODE
            if writeCode:
                x      = int(x) + REPOSITION[0]
                y      = int(y) + REPOSITION[1]
                width  = int(width)
                height = int(height)
                if not penUp:
                    text += '#G01:Z0$\n'
                    penUp = True
                if isRelative:
                    text += '#G90$\n'
                    isRelative = False
                text += '#G01:X{0}:Y{1}$\n'.format(x,y)
                if penUp:
                    text += '#G01:Z1$\n'
                    penUp = False

                text += '#G01:X{0}:Y{1}$\n'.format(x+width,y)+\
                        '#G01:X{0}:Y{1}$\n'.format(x+width,y+height)+\
                        '#G01:X{0}:Y{1}$\n'.format(x,y+height)+\
                        '#G01:X{0}:Y{1}$\n'.format(x,y)

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

            if toScale:
                x      = RESCALE * x
                y      = RESCALE * y
                width  = RESCALE * width
                height = RESCALE * height

            newCanvasElli.setRect(x, y, width, height)
            listOfItems.append(newCanvasElli)
            elli = elli.nextSiblingElement('ellipse')

        # circles
        cir = gNode.firstChildElement('circle')
        while not cir.isNull():
            print("circle")
            newCanvasCir = QGraphicsEllipseItem()
            cx = float(cir.attribute('cx'))
            cy = float(cir.attribute('cy'))
            width = 2*float(cir.attribute('r'))
            height = width

            x = cx - float(cir.attribute('r'))
            y = cy - float(cir.attribute('r'))

            if toScale:
                x      = RESCALE * x
                y      = RESCALE * y
                width  = RESCALE * width
                height = RESCALE * height

            newCanvasCir.setRect(x, y, width, height)
            listOfItems.append(newCanvasCir)

            if writeCode:
                x      = int(x) + REPOSITION[0]
                y      = int(y) + REPOSITION[1]
                r      = int(width/2)
                if isRelative:
                    text += '#G90$\n'
                    isRelative = False
                text += '#G01:X{0}:Y{1}$\n'.format(x-r,y)
                text += '#G02:X{0}:Y{1}:I{2}:J{3}$\n'.format(x+r,y,-r,0)

            cir = cir.nextSiblingElement('circle')

        # polyline
        lin = gNode.firstChildElement('polyline')
        while not lin.isNull():
            print("line")
            newCanvasLin = QGraphicsLineItem()
            points = (lin.attribute('points'))
            points = points.split()
            coord1 = points[0].split(',')
            coord2 = points[1].split(',')
            x1 = float(coord1[0]) + REPOSITION[0]
            y1 = float(coord1[1]) + REPOSITION[1]
            x2 = float(coord2[0]) + REPOSITION[0]
            y2 = float(coord2[1]) + REPOSITION[1]

            if toScale:
                x1     = RESCALE * x1
                y1     = RESCALE * y1
                x2     = RESCALE * x2
                y2     = RESCALE * y2

            newCanvasLin.setLine(x1, y1, x2, y2)
            listOfItems.append(newCanvasLin)

            # G-CODE
            if writeCode:
                x1      = int(x1)
                y1      = int(y1)
                x2      = int(x2)
                y2      = int(y2)
                if not penUp:
                    text += '#G01:Z0$\n'
                    penUp = True
                if isRelative:
                    text += '#G90$\n'
                    isRelative = False
                text  += '#G01:X{0}:Y{1}$\n'.format(x1,y1)
                if penUp:
                    text += '#G01:Z1$\n'
                    penUp = False

                text += '#G01:X{0}:Y{1}$\n'.format(x2,y2)

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
                coord[0] = float(coord[0]) + REPOSITION[0]
                coord[1] = float(coord[1]) + REPOSITION[1]

                if toScale:
                    coord[0] = RESCALE * coord[0]
                    coord[1] = RESCALE * coord[1]

                newPoly.append(QPointF(coord[0], coord[1]))

                # G-CODE
                if writeCode:
                    x  = int(coord[0])
                    y  = int(coord[1])
                    if points.index(point) == 0:
                        if not penUp:
                            text += '#G01:Z0$\n'
                            penUp = True
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        text  += '#G01:X{0}:Y{1}$\n'.format(x,y)
                    else:
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        text  = '#G01:X{0}:Y{1}$\n'.format(x,y)

            newCanvasPoly.setPolygon(newPoly)
            listOfItems.append(newCanvasPoly)


            poly = poly.nextSiblingElement('polygon')

        # path
        pat = gNode.firstChildElement('path')
        newPat       = QPainterPath()
        newCanvasPat = QGraphicsPathItem()
        while not pat.isNull():
            print("path")

            # Taking the transform matrix
            trafo = gNode.toElement()
            trafo = trafo.attribute('transform')
            trafo = trafo.replace('matrix(', '')
            trafo = trafo.replace(')', '')
            trafo = trafo.replace(',', ' ')
            trafo = trafo.split()
            for index in range(len(trafo)):
                trafo[index] = float(trafo[index])
            if trafo and (trafo[0],trafo[1],trafo[2],trafo[3]) != (1,0,0,1): # i.e. it's not a translation transform
                print('NOT TRANSLATING PATH')
                trafo = None
            print(trafo)

            paths = (pat.attribute('d'))
            # Normalise string
            paths = paths.replace(' ', ',')
            for letter in ('m', 'M', 'l',  'L', 'h',  'H', 'v',  'V', 'c',  'C', 's',  'S', 'q',  'Q', 't',  'T', 'a',  'A', 'z', 'Z'):
                paths = paths.replace(letter, ' '+letter)

            paths = paths.split()
            while paths.count(','):
                paths.remove(',')
            lastCubicCtrl = None
            lastQuadCtrl = None
            for path in paths:
                coord = path[1:]
                coord = coord.replace('-', ' -')
                coord = coord.replace('e -', 'e-')
                coord = coord.replace(',', ' ')
                coord = coord.split()
                for index in range(len(coord)):  # Convert str to float
                    coord[index] = float(coord[index])
                    if index in (0,2,4) and trafo:
                        coord[index] += trafo[4]
                    elif trafo:
                        coord[index] += trafo[5]
                    if toScale:
                        coord[index] = RESCALE * coord[index]
                if path[0]   == 'M':        # moveTo
                    newPat.moveTo(coord[0], coord[1])
                    # G-CODE
                    if writeCode:
                        x  = int(coord[0]) + REPOSITION[0]
                        y  = int(coord[1]) + REPOSITION[1]
                        if not penUp:
                            text += '#G01:Z0$\n'
                            penUp = True
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        text  += '#G01:X{0}:Y{1}$\n'.format(x,y)
                elif path[0] == 'm':        # moveTo relative
                    newPat.moveTo(newPat.currentPosition() + QPointF(coord[0], coord[1]))
                    # G-CODE
                    if writeCode:
                        x  = int(coord[0]) + REPOSITION[0]
                        y  = int(coord[1]) + REPOSITION[1]
                        if not penUp:
                            text += '#G01:Z0$\n'
                            penUp = True
                        if not isRelative:
                            text += '#G91$\n'
                        text  += '#G01:X{0}:Y{1}$\n'.format(x,y)
                elif path[0] == 'L':        # lineTo
                    newPat.lineTo(coord[0], coord[1])
                    # G-CODE
                    if writeCode:
                        x  = int(coord[0]) + REPOSITION[0]
                        y  = int(coord[1]) + REPOSITION[1]
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        text  += '#G01:X{0}:Y{1}$\n'.format(x,y)
                elif path[0] == 'l':        # lineTo relative
                    newPat.lineTo(newPat.currentPosition() + QPointF(coord[0], coord[1]))
                    # G-CODE
                    if writeCode:
                        x  = int(coord[0]) + REPOSITION[0]
                        y  = int(coord[1]) + REPOSITION[1]
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if not isRelative:
                            text += '#G91$\n'
                            isRelative = True
                        text  += '#G01:X{0}:Y{1}$\n'.format(x,y)
                elif path[0] == 'H':        # horizontal lineTo
                    newPat.lineTo(coord[0], newPat.currentPosition().y())
                    # G-CODE
                    if writeCode:
                        x  = int(coord[0]) + REPOSITION[0]
                        #y  = int(newPat.currentPosition().y()) + REPOSITION[1]
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        text  += '#G01:X{0}$\n'.format(x)
                elif path[0] == 'h':        # horizontal lineTo relative
                    newPat.lineTo(newPat.currentPosition().x()+coord[0], newPat.currentPosition().y())
                    # G-CODE
                    if writeCode:
                        x  = int(coord[0]) + REPOSITION[0]
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if not isRelative:
                            text += '#G91$\n'
                            isRelative = True
                        text  += '#G01:X{0}$\n'.format(x)
                elif path[0] == 'V':        # vertical lineTo
                    newPat.lineTo(newPat.currentPosition().x(), coord[0])
                    # G-CODE
                    if writeCode:
                        #x  = int(newPat.currentPosition().x()) + REPOSITION[0]
                        y  = int(coord[0]) + REPOSITION[1]
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        text  += '#G01:Y{1}$\n'.format(y)
                elif path[0] == 'v':        # vertical lineTo relative
                    newPat.lineTo(newPat.currentPosition().x(), newPat.currentPosition().y()+coord[0])
                    # G-CODE
                    if writeCode:
                        y  = int(coord[0]) + REPOSITION[1]
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if not isRelative:
                            text += '#G91$\n'
                            isRelative = True
                        text  += '#G01:Y{0}$\n'.format(y)
                elif path[0] == 'C':        # curveto
                    lastCubicCtrl = QPointF(coord[2], coord[3])
                    newPat.cubicTo(coord[0], coord[1], coord[2], coord[3], coord[4], coord[5])
                    Ctrl = newPat.currentPosition() - (lastCubicCtrl-newPat.currentPosition())
                    # G-CODE
                    if writeCode:
                        ctrl1  = (coord[0] + REPOSITION[0], coord[1] + REPOSITION[1])
                        ctrl2  = (coord[2] + REPOSITION[0], coord[3] + REPOSITION[1])
                        endP   = (coord[4] + REPOSITION[0], coord[5] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        #text  += '#G01:Y{1}$\n'.format(y)
                elif path[0] == 'c':        # curveto relative
                    lastCubicCtrl = newPat.currentPosition()+QPointF(coord[2], coord[3])
                    newPat.cubicTo(newPat.currentPosition()+QPointF(coord[0],coord[1]),\
                                    newPat.currentPosition()+QPointF(coord[2],coord[3]),\
                                    newPat.currentPosition()+QPointF(coord[4],coord[5]))
                    Ctrl = newPat.currentPosition() - (lastCubicCtrl-newPat.currentPosition())
                    # G-CODE
                    if writeCode:
                        ctrl1  = newPat.currentPosition()+QPointF(coord[0] + REPOSITION[0],coord[1] + REPOSITION[1])
                        ctrl2  = newPat.currentPosition()+QPointF(coord[2] + REPOSITION[0],coord[3] + REPOSITION[1])
                        endP   = newPat.currentPosition()+QPointF(coord[4] + REPOSITION[0],coord[5] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        #text  += '#G01:Y{1}$\n'.format(y)
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
                    lastQuadCtrl = QPointF(coord[0], coord[1])
                    newPat.quadTo(coord[0], coord[1], coord[2], coord[3])
                elif path[0] == 'q':        # quadratic Bézier curve relative
                    lastQuadCtrl = newPat.currentPosition()+QPointF(coord[0], coord[1])
                    newPat.quadTo(newPat.currentPosition()+QPointf(coord[0], coord[1]),\
                                    newPat.currentPosition()+QPointf(coord[2], coord[3]))
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
                    print(path)

            newCanvasPat.setPath(newPat)
            listOfItems.append(newCanvasPat)
            pat = pat.nextSiblingElement('path')

        # text
        tex = gNode.firstChildElement('text')
        while not tex.isNull():
            print("text")

            # Taking the transform matrix
            trafo = gNode.toElement()
            trafo = trafo.attribute('transform')
            trafo = trafo.replace('matrix(', '')
            trafo = trafo.replace(')', '')
            trafo = trafo.replace(',', ' ')
            trafo = trafo.split()
            print(trafo)

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
            newCanvasTex.setX(float(trafo[4]))
            newCanvasTex.setY(float(trafo[5]))

            listOfItems.append(newCanvasTex)
            tex = tex.nextSiblingElement('text')

    if writeCode:
        g_code.write(text)
    file_.close()
    if writeCode:
        g_code.close()
        return True
    else:
        return listOfItems
