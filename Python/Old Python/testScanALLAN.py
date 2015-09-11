import serial
import time
import os
import math
import numpy as np
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
caliV = 0.24
bufferSize = 10
xvals = []
yvals = []
res = 0
xy_x = []
xy_y = []

'''Code Parameters'''
in2cm = 2.54000508001 #conversion from inches to centimeters
checkDone = 0

'''Start of Scan'''
arduino = serial.Serial(3, 115200)
f = open('testPointCloud.xyz','w')
f3 = open('testPointCloud2.xyz','w')
time.sleep(2) # waiting the initialization...
print('Initializing...')

print('Begin scan phase')
time.sleep(1)

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 50
w.show()
w.setWindowTitle('Real-Time Point Cloud')
g = gl.GLGridItem()
w.addItem(g)

start = time.time()
arduino.write('1')

while True:
    data = arduino.readline()
    if len(data)==11:
        if '222222222' in data:
            height = height + height_increment*in2cm
            if len(xy_x)!=0:
                parsed_x = []

                            
            xy_x = []
            xy_y = []
        elif '999999999' in data:
            break
    aalist = data.rstrip()
    alist = data.split(',')[0:-1]
    alist = [float(i) for i in alist]
    print alist
    if len(alist) == bufferSize+1:
        stagePos = alist[0]
        IRbuffer = alist[1:]
        ir1 = np.median(IRbuffer)
    angle = stagePos/stageRevolutionSteps*360.
    while angle > 360:
        angle = angle - 360
    volt1 = 5.0*ir1/1023.0
    dist1 = ((17.2/(volt1-caliV))+1.5)
    rawx1 = ((distFromCenter*in2cm)-dist1)*math.cos(math.radians(angle))
    rawy1 = ((distFromCenter*in2cm)-dist1)*math.sin(math.radians(angle))
    array = [rawx1, rawy1, height]
    array = np.array(array)
    w.addItem(gl.GLScatterPlotItem(pos=array, size=2.5, pxMode=True))
    QtGui.QApplication.processEvents()
    if dist1 < 33:
        if res<1 and len(alist) == bufferSize+1:
            if len(xvals)<2:
                xvals.append(rawx1)
                yvals.append(rawy1)
                res=0
            else:
                result = np.polyfit(xvals,yvals,1,full=True)
                if result[0][0]>=1 or result[0][0]<=-1:
                    if math.fabs(((rawy1-result[0][0]*rawx1-result[0][1])/(rawy1)))<0.15:
                        xvals.append(rawx1)
                        yvals.append(rawy1)
                    else:
                        res=1
                else:
                    result = np.polyfit(yvals,xvals,1,full=True)
                    if math.fabs(((rawx1-result[0][0]*rawy1-result[0][1])/(rawx1)))<0.15:
                        xvals.append(rawx1)
                        yvals.append(rawy1)
                    else:
                        res=1
        else:
            if len(xvals)>0:
                try:
                    result = np.polyfit(xvals,yvals,1,full=True)
                except:
                    continue
                    #print xvals
                corrxvals = []
                corryvals = []
                if result[0][0]>=1 or result[0][0]<=-1:
                    result = np.polyfit(yvals,xvals,1,full=True)
                    for i,tmpy in enumerate(yvals):
                        corryvals.append(tmpy)
                        corrxvals.append(result[0][0]*tmpy+result[0][1])
                else:
                    for i,tmpx in enumerate(xvals):
                        corrxvals.append(tmpx)
                        corryvals.append(result[0][0]*tmpx+result[0][1])
                for i,x1 in enumerate(corrxvals):
                    y1 = corryvals[i]
                    f.write('{0:.6f}'.format(x1) + '\t' + '{0:.6f}'.format(y1) + '\t' + '{0:.6f}'.format(height) + '\n')
                    xy_x.append(x1)
                    xy_y.append(y1)
                    f3.write('{0:.6f}'.format(xvals[i]) + '\t' + '{0:.6f}'.format(yvals[i]) + '\t' + '{0:.6f}'.format(height) + '\n')
                if res>=1:
                    xvals=[rawx1]
                    yvals=[rawy1]
                    res = 0
                else:
                    xvals = []
                    yvals = []
    
scanend = time.time()
print('Scan/Data Collection time elapsed: ' + '{0:.4f}'.format(scanend-start) + ' seconds')

'''Reset Array'''
first = 0
arduino.write('9') 
while True:
    data = arduino.readline()
    val = data.split()
    if int(val[0]) == 999999999:
        break
    if first == 0:
        maxVal = float(val[0])
        first = 1
    if float(val[0]) < 0:
        val[0] = 0
    pct_cmp = 100.0-(float(val[0])/maxVal*100.0)
    print('Resetting IR array: ' + '{0:.2f}'.format(pct_cmp) + '% complete')
        
    
end = time.time()
print('Reset Array time elapsed: ' + '{0:.4f}'.format(end-scanend) + ' seconds')
print('Total time elapsed: ' + '{0:.4f}'.format(end-start) + ' seconds')

f.close()
f3.close()
arduino.close()
print('Scan phase complete')

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
