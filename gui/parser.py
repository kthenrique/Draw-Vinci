#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW_VINCI
# ----------------------------------------------------------------------------
# -- File       : parser.py
# -- Author     : Kelve T. Henrique
# -- Last update: 2018 Jun 13
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

from math import sqrt

from constants import *


def getElements(filename, writeCode = False, toScale = False, RESOLUTION = QUARTER_STEP[0]):
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

    print("****************************** PARSING SVG FILE ******************************")
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

        REPOSITION = (int(-viewBox[0]+abs(viewBox[0]))/CANVAS_WIDTH, int(-viewBox[1]+abs(viewBox[1]))/CANVAS_WIDTH) # Just for plotter
        RESOLUTION = RESOLUTION / CANVAS_WIDTH  # Just for plotter
        RESOLUTION = int(RESOLUTION)
        if viewBox[2] > CANVAS_WIDTH or viewBox[3] > CANVAS_HEIGHT: # rescale when image is bigger than canvas
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
                print('NOT TRANSLATING RECT')
                trafo = None

            newCanvasRect = QGraphicsRectItem()
            x      = float(rect.attribute('x'))
            y      = float(rect.attribute('y'))
            width  = float(rect.attribute('width'))
            height = float(rect.attribute('height'))

            # Translate
            if trafo:
                x += trafo[4]
                y += trafo[5]

            if toScale:
                x      = RESCALE * x
                y      = RESCALE * y
                width  = RESCALE * width
                height = RESCALE * height

            newCanvasRect.setRect(x, y, width, height)
            listOfItems.append(newCanvasRect)

            # G-CODE
            if writeCode:
                x      = RESOLUTION * (x + REPOSITION[0])
                y      = RESOLUTION * (y + REPOSITION[1])
                width  = RESOLUTION * (width)
                height = RESOLUTION * (height)
                if not penUp:
                    text += '#G01:Z0$\n'
                    penUp = True
                if isRelative:
                    text += '#G90$\n'
                    isRelative = False
                text += '#G01:X{0}:Y{1}$\n'.format(int(x),int(y))
                if penUp:
                    text += '#G01:Z1$\n'
                    penUp = False

                text += '#G01:X{0}:Y{1}$\n'.format(int(x+width),int(y))+\
                        '#G01:X{0}:Y{1}$\n'.format(int(x+width),int(y+height))+\
                        '#G01:X{0}:Y{1}$\n'.format(int(x),int(y+height))+\
                        '#G01:X{0}:Y{1}$\n'.format(int(x),int(y))

            rect = rect.nextSiblingElement('rect')

        # ellipses
        elli = gNode.firstChildElement('ellipse')
        while not elli.isNull():
            print("ellipse")
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
                print('NOT TRANSLATING ELLIPSE')
                trafo = None

            newCanvasElli = QGraphicsEllipseItem()
            cx = float(elli.attribute('cx'))
            cy = float(elli.attribute('cy'))
            width = 2*float(elli.attribute('rx'))
            height = 2*float(elli.attribute('ry'))

            # Translate
            if trafo:
                cx += trafo[4]
                cy += trafo[5]

            x = cx - float(elli.attribute('rx'))
            y = cy - float(elli.attribute('ry'))

            if toScale:
                x      = RESCALE * x
                y      = RESCALE * y
                width  = RESCALE * width
                height = RESCALE * height

            newCanvasElli.setRect(x, y, width, height)
            listOfItems.append(newCanvasElli)

            # G-CODE
            if writeCode:
                x      = RESOLUTION * (cx + REPOSITION[0])
                y      = RESOLUTION * (cy + REPOSITION[1])
                rx     = RESOLUTION * (float(elli.attribute('rx')))
                ry     = RESOLUTION * (float(elli.attribute('ry')))

                if isRelative:
                    text += '#G90$\n'
                    isRelative = False
                if not penUp:
                    text += '#G01:Z0$\n'
                    penUp = True
                text += '#G01:X{0}:Y{1}$\n'.format(int(x+rx),int(y))
                if penUp:
                    text += '#G01:Z1$\n'
                    penUp = False

                underSide  = []
                underSide.append(((x+rx),y))
                for step in range(ELLIPSES+1):
                    nextX = x+rx - step*2*rx/ELLIPSES
                    nextY = y + sqrt(ry**2 - (ry*(nextX-x)/rx)**2)
                    underSide.append((nextX, 2*y-nextY))
                    text += '#G01:X{0}:Y{1}$\n'.format(int(nextX),int(nextY))

                for step in range(ELLIPSES+1):
                    nextX,nextY = underSide.pop()
                    text += '#G01:X{0}:Y{1}$\n'.format(int(nextX),int(nextY))

                text += '#G01:X{0}:Y{1}$\n'.format(int(nextX),int(nextY))
            elli = elli.nextSiblingElement('ellipse')

        # circles
        cir = gNode.firstChildElement('circle')
        while not cir.isNull():
            print("circle")
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
                print('NOT TRANSLATING CIRCLE')
                trafo = None

            newCanvasCir = QGraphicsEllipseItem()
            cx = float(cir.attribute('cx'))
            cy = float(cir.attribute('cy'))
            width = 2*float(cir.attribute('r'))
            height = width

            # Translate
            if trafo:
                cx += trafo[4]
                cy += trafo[5]

            x = cx - float(cir.attribute('r'))
            y = cy - float(cir.attribute('r'))

            if toScale:
                x      = RESCALE * x
                y      = RESCALE * y
                width  = RESCALE * width
                height = RESCALE * height
                cx     = RESCALE * cx
                cy     = RESCALE * cy

            newCanvasCir.setRect(x, y, width, height)
            listOfItems.append(newCanvasCir)

            # G-CODE
            if writeCode:
                x      = RESOLUTION * (cx + REPOSITION[0])
                y      = RESOLUTION * (cy + REPOSITION[1])
                r      = RESOLUTION * (width/2)
                if isRelative:
                    text += '#G90$\n'
                    isRelative = False
                if not penUp:
                    text += '#G01:Z0$\n'
                    penUp = True
                text += '#G01:X{0}:Y{1}$\n'.format(int(x+r),int(y))
                if penUp:
                    text += '#G01:Z1$\n'
                    penUp = False
                text += '#G02:X{0}:Y{1}:I{2}:J{3}$\n'.format(int(x-2*r),int(y),int(-r),0)

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
            x1 = float(coord1[0])
            y1 = float(coord1[1])
            x2 = float(coord2[0])
            y2 = float(coord2[1])

            if toScale:
                x1     = RESCALE * x1
                y1     = RESCALE * y1
                x2     = RESCALE * x2
                y2     = RESCALE * y2

            newCanvasLin.setLine(x1, y1, x2, y2)
            listOfItems.append(newCanvasLin)

            # G-CODE
            if writeCode:
                x1      = RESOLUTION * (x1 + REPOSITION[0])
                y1      = RESOLUTION * (y1 + REPOSITION[1])
                x2      = RESOLUTION * (x2 + REPOSITION[0])
                y2      = RESOLUTION * (y2 + REPOSITION[1])
                if not penUp:
                    text += '#G01:Z0$\n'
                    penUp = True
                if isRelative:
                    text += '#G90$\n'
                    isRelative = False
                text  += '#G01:X{0}:Y{1}$\n'.format(int(x1),int(y1))
                if penUp:
                    text += '#G01:Z1$\n'
                    penUp = False

                text += '#G01:X{0}:Y{1}$\n'.format(int(x2),int(y2))

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
                    x  = RESOLUTION * (int(coord[0]))
                    y  = RESOLUTION * (int(coord[1]))
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
                    print(' -M-',end='',flush=True)
                    newPat.moveTo(coord[0], coord[1])
                    # G-CODE
                    if writeCode:
                        x  = RESOLUTION * (coord[0] + REPOSITION[0])
                        y  = RESOLUTION * (coord[1] + REPOSITION[1])
                        if not penUp:
                            text += '#G01:Z0$\n'
                            penUp = True
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        text  += '#G01:X{0}:Y{1}$\n'.format(int(x),int(y))
                elif path[0] == 'm':        # moveTo relative
                    print(' -m-',end='',flush=True)
                    newPat.moveTo(newPat.currentPosition() + QPointF(coord[0], coord[1]))
                    # G-CODE
                    if writeCode:
                        x  = RESOLUTION * (coord[0] + REPOSITION[0])
                        y  = RESOLUTION * (coord[1] + REPOSITION[1])
                        if not penUp:
                            text += '#G01:Z0$\n'
                            penUp = True
                        if not isRelative:
                            text += '#G91$\n'
                        text  += '#G01:X{0}:Y{1}$\n'.format(int(x),int(y))
                elif path[0] == 'L':        # lineTo
                    print(' -L-',end='',flush=True)
                    newPat.lineTo(coord[0], coord[1])
                    # G-CODE
                    if writeCode:
                        x  = RESOLUTION * (coord[0] + REPOSITION[0])
                        y  = RESOLUTION * (coord[1] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        text  += '#G01:X{0}:Y{1}$\n'.format(int(x),int(y))
                elif path[0] == 'l':        # lineTo relative
                    print(' -l-',end='',flush=True)
                    newPat.lineTo(newPat.currentPosition() + QPointF(coord[0], coord[1]))
                    # G-CODE
                    if writeCode:
                        x  = RESOLUTION * (coord[0] + REPOSITION[0])
                        y  = RESOLUTION * (coord[1] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if not isRelative:
                            text += '#G91$\n'
                            isRelative = True
                        text  += '#G01:X{0}:Y{1}$\n'.format(int(x),int(y))
                elif path[0] == 'H':        # horizontal lineTo
                    print(' -H-',end='',flush=True)
                    newPat.lineTo(coord[0], newPat.currentPosition().y())
                    # G-CODE
                    if writeCode:
                        x  = RESOLUTION * (coord[0] + REPOSITION[0])
                        #y  = int(newPat.currentPosition().y()) + REPOSITION[1]
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        text  += '#G01:X{0}$\n'.format(int(x))
                elif path[0] == 'h':        # horizontal lineTo relative
                    print(' -h-',end='',flush=True)
                    newPat.lineTo(newPat.currentPosition().x()+coord[0], newPat.currentPosition().y())
                    # G-CODE
                    if writeCode:
                        x  = RESOLUTION * (coord[0] + REPOSITION[0])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if not isRelative:
                            text += '#G91$\n'
                            isRelative = True
                        text  += '#G01:X{0}$\n'.format(int(x))
                elif path[0] == 'V':        # vertical lineTo
                    print(' -V-',end='',flush=True)
                    newPat.lineTo(newPat.currentPosition().x(), coord[0])
                    # G-CODE
                    if writeCode:
                        #x  = int(newPat.currentPosition().x()) + REPOSITION[0]
                        y  = RESOLUTION * (coord[0] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        text  += '#G01:Y{0}$\n'.format(int(y))
                elif path[0] == 'v':        # vertical lineTo relative
                    print(' -v-',end='',flush=True)
                    newPat.lineTo(newPat.currentPosition().x(), newPat.currentPosition().y()+coord[0])
                    # G-CODE
                    if writeCode:
                        y  = RESOLUTION * (coord[0] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if not isRelative:
                            text += '#G91$\n'
                            isRelative = True
                        text  += '#G01:Y{0}$\n'.format(int(y))
                elif path[0] == 'C':        # curveto
                    print(' -C-',end='',flush=True)
                    # G-CODE
                    if writeCode:
                        P0x = RESOLUTION * ((newPat.currentPosition()).x() + REPOSITION[0])
                        P0y = RESOLUTION * ((newPat.currentPosition()).y() + REPOSITION[1])
                        P1x = RESOLUTION * (coord[0] + REPOSITION[0])
                        P1y = RESOLUTION * (coord[1] + REPOSITION[1])
                        P2x = RESOLUTION * (coord[2] + REPOSITION[0])
                        P2y = RESOLUTION * (coord[3] + REPOSITION[1])
                        P3x = RESOLUTION * (coord[4] + REPOSITION[0])
                        P3y = RESOLUTION * (coord[5] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        for i in range(CUBIC_BEZIER+1):      # Transform cubic bézier in lines
                            t = i/CUBIC_BEZIER
                            B = ['','']
                            B[0] = P0x*(1-t)**3 + P1x*3*t*(1-t)**2 + P2x*3*(t**2)*(1-t) + P3x*t**3
                            B[1] = P0y*(1-t)**3 + P1y*3*t*(1-t)**2 + P2y*3*(t**2)*(1-t) + P3y*t**3
                            text += '#G01:X{0}:Y{1}$\n'.format(int(B[0]),int(B[1]))
                    lastCubicCtrl = QPointF(coord[2], coord[3])
                    newPat.cubicTo(coord[0], coord[1], coord[2], coord[3], coord[4], coord[5])
                    Ctrl = newPat.currentPosition() - (lastCubicCtrl-newPat.currentPosition())
                elif path[0] == 'c':        # curveto relative
                    print(' -c-',end='',flush=True)
                    # G-CODE
                    if writeCode:
                        P0x = RESOLUTION * ((newPat.currentPosition()).x() + REPOSITION[0])
                        P0y = RESOLUTION * ((newPat.currentPosition()).y() + REPOSITION[1])
                        P1x = RESOLUTION * (newPat.currentPosition().x() + coord[0] + REPOSITION[0])
                        P1y = RESOLUTION * (newPat.currentPosition().y() + coord[1] + REPOSITION[1])
                        P2x = RESOLUTION * (newPat.currentPosition().x() + coord[2] + REPOSITION[0])
                        P2y = RESOLUTION * (newPat.currentPosition().y() + coord[3] + REPOSITION[1])
                        P3x = RESOLUTION * (newPat.currentPosition().x() + coord[4] + REPOSITION[0])
                        P3y = RESOLUTION * (newPat.currentPosition().y() + coord[5] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        for i in range(CUBIC_BEZIER+1):      # Transform cubic bézier in lines
                            t = i/CUBIC_BEZIER
                            B = ['','']
                            B[0] = P0x*(1-t)**3 + P1x*3*t*(1-t)**2 + P2x*3*(t**2)*(1-t) + P3x*t**3
                            B[1] = P0y*(1-t)**3 + P1y*3*t*(1-t)**2 + P2y*3*(t**2)*(1-t) + P3y*t**3
                            text += '#G01:X{0}:Y{1}$\n'.format(int(B[0]),int(B[1]))
                    lastCubicCtrl = newPat.currentPosition()+QPointF(coord[2], coord[3])
                    newPat.cubicTo(newPat.currentPosition()+QPointF(coord[0],coord[1]),\
                                    newPat.currentPosition()+QPointF(coord[2],coord[3]),\
                                    newPat.currentPosition()+QPointF(coord[4],coord[5]))
                    Ctrl = newPat.currentPosition() - (lastCubicCtrl-newPat.currentPosition())
                elif path[0] == 'S':        # smooth curveto
                    print(' -S-',end='',flush=True)
                    if lastCubicCtrl:
                        Ctrl = newPat.currentPosition() - (lastCubicCtrl-newPat.currentPosition())
                    else:
                        Ctrl = newPat.currentPosition()
                    # G-CODE
                    if writeCode:
                        P0x = RESOLUTION * ((newPat.currentPosition()).x() + REPOSITION[0])
                        P0y = RESOLUTION * ((newPat.currentPosition()).y() + REPOSITION[1])
                        P1x = RESOLUTION * (Ctrl.x() + REPOSITION[0])
                        P1y = RESOLUTION * (Ctrl.y() + REPOSITION[1])
                        P2x = RESOLUTION * (coord[0] + REPOSITION[0])
                        P2y = RESOLUTION * (coord[1] + REPOSITION[1])
                        P3x = RESOLUTION * (coord[2] + REPOSITION[0])
                        P3y = RESOLUTION * (coord[3] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        for i in range(CUBIC_BEZIER+1):      # Transform cubic bézier in lines
                            t = i/CUBIC_BEZIER
                            B = ['','']
                            B[0] = P0x*(1-t)**3 + P1x*3*t*(1-t)**2 + P2x*3*(t**2)*(1-t) + P3x*t**3
                            B[1] = P0y*(1-t)**3 + P1y*3*t*(1-t)**2 + P2y*3*(t**2)*(1-t) + P3y*t**3
                            text += '#G01:X{0}:Y{1}$\n'.format(int(B[0]),int(B[1]))

                    lastCubicCtrl = QPointF(coord[0], coord[1])
                    newPat.cubicTo(Ctrl,\
                                    QPointF(coord[0], coord[1]),\
                                    QPointF(coord[2], coord[3]))
                elif path[0] == 's':        # smooth curveto relative
                    print(' -s-',end='',flush=True)
                    if lastCubicCtrl:
                        Ctrl = newPat.currentPosition() - (lastCubicCtrl-newPat.currentPosition())
                    else:
                        print("smooth without last ctrl")
                        Ctrl = newPat.currentPosition()
                    # G-CODE
                    if writeCode:
                        P0x = RESOLUTION * ((newPat.currentPosition()).x() + REPOSITION[0])
                        P0y = RESOLUTION * ((newPat.currentPosition()).y() + REPOSITION[1])
                        P1x = RESOLUTION * (Ctrl.x() + REPOSITION[0])
                        P1y = RESOLUTION * (Ctrl.y() + REPOSITION[1])
                        P2x = RESOLUTION * (newPat.currentPosition().x() + coord[0] + REPOSITION[0])
                        P2y = RESOLUTION * (newPat.currentPosition().y() + coord[1] + REPOSITION[1])
                        P3x = RESOLUTION * (newPat.currentPosition().x() + coord[2] + REPOSITION[0])
                        P3y = RESOLUTION * (newPat.currentPosition().y() + coord[3] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        for i in range(CUBIC_BEZIER+1):      # Transform cubic bézier in lines
                            t = i/CUBIC_BEZIER
                            B = ['','']
                            B[0] = P0x*(1-t)**3 + P1x*3*t*(1-t)**2 + P2x*3*(t**2)*(1-t) + P3x*t**3
                            B[1] = P0y*(1-t)**3 + P1y*3*t*(1-t)**2 + P2y*3*(t**2)*(1-t) + P3y*t**3
                            text += '#G01:X{0}:Y{1}$\n'.format(int(B[0]),int(B[1]))
                    lastCubicCtrl = QPointF(newPat.currentPosition().x()+coord[0],\
                                            newPat.currentPosition().y()+coord[1])
                    newPat.cubicTo(Ctrl.x(),\
                                    Ctrl.y(),\
                                    newPat.currentPosition().x()+coord[0],\
                                    newPat.currentPosition().y()+coord[1],\
                                    newPat.currentPosition().x()+coord[2],\
                                    newPat.currentPosition().y()+coord[3])
                elif path[0] == 'Q':        # quadratic Bézier curve
                    print(' -Q-',end='',flush=True)
                    # G-CODE
                    if writeCode:
                        P0x = RESOLUTION * ((newPat.currentPosition()).x() + REPOSITION[0])
                        P0y = RESOLUTION * ((newPat.currentPosition()).y() + REPOSITION[1])
                        P1x = RESOLUTION * (coord[0] + REPOSITION[0])
                        P1y = RESOLUTION * (coord[1] + REPOSITION[1])
                        P2x = RESOLUTION * (coord[2] + REPOSITION[0])
                        P2y = RESOLUTION * (coord[3] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        for i in range(QUAD_BEZIER+1):      # Transform cubic bézier in lines
                            t = i/QUAD_BEZIER
                            B = ['','']
                            B[0] = P0x*(1-t)**2 + P1x*2*t*(1-t) + P2x*t**2
                            B[1] = P0y*(1-t)**2 + P1y*2*t*(1-t) + P2y*t**2
                            text += '#G01:X{0}:Y{1}$\n'.format(int(B[0]),int(B[1]))
                    lastQuadCtrl = QPointF(coord[0], coord[1])
                    newPat.quadTo(coord[0], coord[1], coord[2], coord[3])
                elif path[0] == 'q':        # quadratic Bézier curve relative
                    print(' -q-',end='',flush=True)
                    # G-CODE
                    if writeCode:
                        P0x = RESOLUTION * ((newPat.currentPosition()).x() + REPOSITION[0])
                        P0y = RESOLUTION * ((newPat.currentPosition()).y() + REPOSITION[1])
                        P1x = RESOLUTION * (newPat.currentPosition().x() + coord[0] + REPOSITION[0])
                        P1y = RESOLUTION * (newPat.currentPosition().y() + coord[1] + REPOSITION[1])
                        P2x = RESOLUTION * (newPat.currentPosition().x() + coord[2] + REPOSITION[0])
                        P2y = RESOLUTION * (newPat.currentPosition().y() + coord[3] + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z1$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        for i in range(QUAD_BEZIER+1):      # Transform cubic bézier in lines
                            t = i/QUAD_BEZIER
                            B = ['','']
                            B[0] = P0x*(1-t)**2 + P1x*2*t*(1-t) + P2x*t**2
                            B[1] = P0y*(1-t)**2 + P1y*2*t*(1-t) + P2y*t**2
                            text += '#G01:X{0}:Y{1}$\n'.format(int(B[0]),int(B[1]))
                    lastQuadCtrl = newPat.currentPosition()+QPointF(coord[0], coord[1])
                    newPat.quadTo(newPat.currentPosition()+QPointf(coord[0], coord[1]),\
                                    newPat.currentPosition()+QPointf(coord[2], coord[3]))
                elif path[0] == 'T':        # smooth quadratic Bézier curveto
                    print(' -T-',end='',flush=True)
                    if lastQuadCtrl:
                        Ctrl = newPat.currentPosition() - (lastQuadCtrl-newPat.currentPosition())
                        newPat.quadTo(Ctrl, QPointF(coord[0], coord[1]))
                        lastQuadCtrl = Ctrl
                    else:
                        newPat.quadTo(newPat.currentPosition(),\
                                        QPointF(coord[0], coord[1]))
                        lastQuadCtrl = newPat.currentPosition()
                elif path[0] == 't':        # smooth quadratic Bézier curveto relative
                    print(' -t-',end='',flush=True)
                    if lastQuadCtrl:
                        Ctrl = newPat.currentPosition() - (lastQuadCtrl-newPat.currentPosition())
                        newPat.quadTo(Ctrl, newPat.currentPosition()+QPointF(coord[0], coord[1]))
                        lastQuadCtrl = Ctrl
                    else:
                        newPat.quadTo(newPat.currentPosition(),\
                                        newPat.currentPosition()+QPointF(coord[0], coord[1]))
                        lastQuadCtrl = newPat.currentPosition()
                elif path[0] == 'A':        # elliptical arc
                    print(' -A-',end='',flush=True)
                    pass
                elif path[0] == 'a':        # elliptical arc relative
                    print(' -a-',end='',flush=True)
                    pass
                elif path[0] == 'Z' or path[0] == 'z':        # closePath
                    print(' -Z-',end='',flush=True)
                    newPat.closeSubpath()
                    # G-CODE
                    if writeCode:
                        x  = RESOLUTION * (newPat.currentPosition().x() + REPOSITION[0])
                        y  = RESOLUTION * (newPat.currentPosition().y() + REPOSITION[1])
                        if penUp:
                            text += '#G01:Z0$\n'
                            penUp = False
                        if isRelative:
                            text += '#G90$\n'
                            isRelative = False
                        text  += '#G01:X{0}:Y{1}$\n'.format(int(x),int(y))
                else:
                    print('Strange Command at path tag in SVG file')
                    print(path)

            print('')
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

    print("******************************************************************************")
    if writeCode:
        text += '#G28$'
        g_code.write(text)
    file_.close()
    if writeCode:
        g_code.close()
        return True
    else:
        return listOfItems
