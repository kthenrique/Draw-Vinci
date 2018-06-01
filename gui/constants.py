#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# -- Project    : DRAW-VINCI
# ----------------------------------------------------------------------------
# -- File       : constants.py
# -- Author     : Kelve T. Henrique - Andreas Hofschweiger
# -- Last update: 2018 Jun 01
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
GODOWN = '#G01:Y'
GOUP   = '#G01:Y-'
GOLEFT = '#G01:X-'
GORIGHT= '#G01:X'

# Scale of SVG
SCALE = 250

# Number of points/cubic_bézier
CUBIC_BEZIER = 10

# Number of points/quadratic_bézier
QUAD_BEZIER = 10

# Number of steps for each config of motor
FULL_STEP      = (2010, 1728)
HALF_STEP      = (4017, 3453)
QUARTER_STEP   = (8029, 6902)
EIGHTH_STEP    = (16052, 13800)
SIXTEENTH_STEP = (32101, 27594)
