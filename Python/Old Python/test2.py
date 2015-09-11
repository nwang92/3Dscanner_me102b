'''Visual Real-Time Point Cloud'''
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import time

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 50
w.show()
w.setWindowTitle('Real-Time Point Cloud')
g = gl.GLGridItem()
w.addItem(g)

f = open('testPointCloudNELSON.xyz','r')
array = []
for line in f:
    try:
        data = line.strip()
        data = line.split('\t')
        array.append((float(data[0]), float(data[1]), float(data[2])))
    except:
        pass
    
f.close()

x = np.array(array)
w.addItem(gl.GLScatterPlotItem(pos=x[0], size = 5, pxMode=True))

i = 1
def update():
    ## update volume colors
    global x, i
    w.addItem(gl.GLScatterPlotItem(pos=x[i], size =5,pxMode=True))
    i = i+1
    #sp1.setData(color=color)
    #phase -= 0.1

t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
