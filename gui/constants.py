#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : constants.py
# -- Author     : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Mai 31
# ----------------------------------------------------------------------------
# -- Description: All relevant constants for the GUI
# ----------------------------------------------------------------------------

import os

# Used for the messages in statusbar
TIMEOUT_STATUS = 1000

# Canvas properties
CANVAS_WIDTH  = 640
CANVAS_HEIGHT = 460
VIEW_X        = 0
VIEW_Y        = 0

# Text properties
FONT_SIZES    = [4, 6, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20,
                22, 24, 28, 32, 36, 40, 48, 56, 64, 72, 144]

# SVG's path
SVG_DIR = './svg'
SVG     = [os.path.join(SVG_DIR, f) for f in os.listdir(SVG_DIR)]

# Step length for manual mode
GODOWN = '#G01:Y100$'
GOUP   = '#G01:Y-100$'
GOLEFT = '#G01:X-100$'
GORIGHT= '#G01:X100$'

# Scale of SVG
SCALE = 250

# Number of points/cubic_bézier
CUBIC_BEZIER = 10

# Number of points/quadratic_bézier
QUAD_BEZIER = 10
