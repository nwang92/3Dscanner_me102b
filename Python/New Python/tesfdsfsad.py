import serial
import time
import os
import math
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

'''Scanner Parameters'''
distFromCenter = 7 #in inches
stageRevolutionSteps = 200*8*32/3.0 #in steps
height_increment = .05
stagePos = 0
angle = 0
height = 0
ir1 = 0
volt1 = 0
dist1 = 0
ir2 = 0
volt2 = 0
dist2 = 0
ir3 = 0
volt3 = 0
dist3 = 0
caliV = 1.75
bufferSize = 10
xvals = []
yvals = []
res = 0

'''Code Parameters'''
in2cm = 2.54000508001 #conversion from inches to centimeters
checkDone = 0

'''Start of Scan'''

arduino = serial.Serial(3, 9600)

start = time.time()
arduino.write('1')

while True:
    data = arduino.readline()
    print data

arduino.close()