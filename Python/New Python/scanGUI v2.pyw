import wx
import serial
import time
import math
import os
import gc
import numpy as np
import pyqtgraph
import glob
import datetime
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
from serial.tools import list_ports

from threading import Thread
from wx.lib.pubsub import pub

'''Code Parameters'''
in2cm = 2.54000508001 #conversion from inches to centimeters
checkDone = 0
command = 0
filename = 0
APP_EXIT = 1
filename = ''
comport = ''
now = datetime.datetime.now()
timestr = str(now.year) + "_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)
defaultFilename = "savedScan" + timestr + ".xyz"

def serial_ports():
    """
    Returns a generator for all available serial ports
    """
    if os.name == 'nt':
        # windows
        for i in range(256):
            try:
                s = serial.Serial(i)
                s.close()
                yield 'COM' + str(i + 1)
            except serial.SerialException:
                pass
    else:
        # unix
        for port in list_ports.comports():
            yield port[0]

def threedeeScan():
    global totalScanTime
    global totalResetTime
    global checkDone
    global filename
    filename = defaultFilename
    
    '''Scanner Parameters'''
    distFromCenter = 7 #in inches
    stageRevolutionSteps = 200*8*32/3.0 #in steps
    height_increment = .282/2
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
    bufferSize = 10
    xvals = []
    yvals = []
    xy_x = []
    xy_y = []
    res = 0
    
    newD = pleaseWait1()
    
    '''Code Parameters'''
    in2cm = 2.54000508001 #conversion from inches to centimeters
    checkDone = 0
    
    '''File Write'''
    filename = str(filename)
    nameOfFile = filename.split('\\')
    nameOfFile = nameOfFile[len(nameOfFile)-1]
    nameOfFile = nameOfFile.split('.')
    nameOfFile = nameOfFile[0]
    #filename = '"' +  filename + '"'
    f = open(filename,'w')
        
    '''Start of Scan'''
    arduino = serial.Serial(comport, 9600)
    time.sleep(2) # waiting the initialization...
    #print('Initializing...')
    #print('Begin scan phase')
    time.sleep(1)

    app = QtGui.QApplication([])
    #win = QtGui.QMainWindow()
    window = pyqtgraph.PlotItem()
    window.autoBtn.show()
    w = gl.GLViewWidget()
    
    w.opts['distance'] = 50
    w.show()
    w.setWindowTitle('Real-Time Point Cloud')
    g = gl.GLGridItem()
    w.addItem(g)
    
    start = time.time()
    arduino.write('1')
    loopcount = 1
    
    while True:
        data = arduino.readline()
        if checkDone == 1:
            data = '999999999'
        if '222222222' in data:
            if int(height) == 0:
                p1 = len(xy_x)/2
                for p2 in range(p1):
                    d1 = round(2*math.sqrt((xy_x[p2]-xy_x[p1])**2+(xy_y[p2]-xy_y[p1])**2))
                    dx = (xy_x[p2]-xy_x[p1])/d1
                    dy = (xy_y[p2]-xy_y[p1])/d1
                    for j in range(int(d1-1)):
                        tmp_x = xy_x[p2]-dx*j
                        tmp_y = xy_y[p2]-dy*j
                        f.write('{0:.6f}'.format(tmp_x) + '\t' + '{0:.6f}'.format(tmp_y) + '\t' + '{0:.6f}'.format(height) + '\n')
                        #array = np.array([[tmp_x, tmp_y, height]])
                        #w.addItem(gl.GLScatterPlotItem(pos=array, size=2, pxMode=True))
                    p1+=1
            xy_x=[]
            xy_y=[]
            height = height + height_increment
            arduino.write('2')
        elif '444444444' in data:
            arduino.write('1')
        elif '999999999' in data:
            if height == 0:
                p1 = len(xy_x)/2
                for p2 in range(p1):
                    d1 = round(2*math.sqrt((xy_x[p2]-xy_x[p1])**2+(xy_y[p2]-xy_y[p1])**2))
                    dx = (xy_x[p2]-xy_x[p1])/d1
                    dy = (xy_y[p2]-xy_y[p1])/d1
                    for j in range(int(d1-1)):
                        tmp_x = xy_x[p2]-dx*j
                        tmp_y = xy_y[p2]-dy*j
                        f.write('{0:.6f}'.format(tmp_x) + '\t' + '{0:.6f}'.format(tmp_y) + '\t' + '{0:.6f}'.format(height) + '\n')
                        #array = np.array([[tmp_x, tmp_y, height]])
                        #w.addItem(gl.GLScatterPlotItem(pos=array, size=2, pxMode=True))
                    p2+=1
            xy_x=[]
            xy_y=[]
            break
        alist = data.rstrip()
        '''
        alist = data.split(',')[0:-1]
        t = 0
        if (',,' in alist)!=-1:
            while (',,' in alist) != -1:
                try:
                    alist.pop(alist.index(''))
                    t+=1
                except:
                    break
        alist = [float(i) for i in alist]
        for i in range(t):
            alist.append(np.median(alist))
        #print alist
        if len(alist) == bufferSize+1:
            stagePos = alist[0]
            IRbuffer = alist[1:]
            ir1 = np.median(IRbuffer)
        '''
        alist = alist.split(',')
        if len(alist) == 2:
            stagePos = float(alist[0])
            ir1 = float(alist[1])
        angle = stagePos/stageRevolutionSteps*360.
        volt1 = 5.0*ir1/1023.0
        dist1 = 20.7965/(volt1+.2128) - 1.6
        #volt2 = 5.0*ir2/1023.0
        #dist2 = 18.4694/(volt+.168983) - .440678
        rawx1 = ((distFromCenter*in2cm)-dist1)*math.cos(math.radians(angle))
        rawy1 = ((distFromCenter*in2cm)-dist1)*math.sin(math.radians(angle))
        array = np.array([[rawx1, rawy1, height]])
        w.addItem(gl.GLScatterPlotItem(pos=array, size=2, pxMode=True))
        loopcount +=1 
        if loopcount == 10:
            QtGui.QApplication.processEvents()
            loopcount = 1
        if dist1 < 20:
            xy_x.append(rawx1)
            xy_y.append(rawy1)
            f.write('{0:.6f}'.format(rawx1) + '\t' + '{0:.6f}'.format(rawy1) + '\t' + '{0:.6f}'.format(height) + '\n')
            '''
            if res<1 and len(alist) == bufferSize+1:
                if len(xvals)<2:
                    xvals.append(rawx1)
                    yvals.append(rawy1)
                    res=0
                else:
                    result = np.polyfit(xvals,yvals,1,full=True)
                    if result[0][0]>=1 or result[0][0]<=-1:
                        #print math.fabs(((rawy1-result[0][0]*rawx1-result[0][1])/(rawy1)))
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
                        xy_x.append(x1)
                        xy_y.append(y1)
                        f.write('{0:.6f}'.format(x1) + '\t' + '{0:.6f}'.format(y1) + '\t' + '{0:.6f}'.format(height) + '\n')
                        f3.write('{0:.6f}'.format(xvals[i]) + '\t' + '{0:.6f}'.format(yvals[i]) + '\t' + '{0:.6f}'.format(height) + '\n')
                    if res>=1:
                        xvals=[rawx1]
                        yvals=[rawy1]
                        res = 0
                    else:
                        xvals = []
                        yvals = []
        '''
    
    scanend = time.time()
    totalScanTime = scanend-start
    #print('Scan/Data Collection time elapsed: ' + '{0:.4f}'.format(scanend-start) + ' seconds')
    
    '''Reset Array'''
    first = 0
    arduino.write('9') 
    
    newD = pleaseWait1()
    
    while True:
        data = arduino.readline()
        if '999999999' in data:
            break
        '''
        val = data.split()
        if first == 0:
            maxVal = float(val[0])
            first = 1
        if '999999999' in data:
            break
        if float(val[0]) < 0:
            val[0] = 0
        pct_cmp = 100.0-(float(val[0])/maxVal*100.0)
        print('Resetting IR array: ' + '{0:.2f}'.format(pct_cmp) + '% complete')
        '''    
    
    newD.Destroy()
    
    end = time.time()
    totalResetTime = end-scanend-1
    #print('Reset Array time elapsed: ' + '{0:.4f}'.format(end-scanend) + ' seconds')
    #print('Total time elapsed: ' + '{0:.4f}'.format(end-start) + ' seconds')
    
    f.close()
    arduino.close()
    
    lastD = pleaseWait2()
    
    dirPath = os.getcwd()
    os.system('cd "C:\Program Files\VCG\MeshLab"')
    os.system('start MeshLabServer -i "' + dirPath + '\\' + nameOfFile + '.xyz" -o "' + dirPath + '\\' + nameOfFile + '.stl" -s "' + dirPath + '\\' + 'STLgen.mlx" -om vc fq wn')
    
    lastD.Destroy()
    
    #print('Scan phase complete')
    
    if __name__ == '__main__':
        import sys
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

class threadScan(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.start()
    
    def run(self):
        threedeeScan()     

class progressBar(wx.Dialog):
 
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Progress", size=(400,200))
        self.count = 0
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#E0E4CC') ##4f5049
        sizer = wx.BoxSizer(wx.VERTICAL)
        textBox = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText(panel, -1, 'Resetting IR sensor array...')
        textBox.Add(self.text)
        sizer.Add(textBox, wx.LEFT, 10)
        self.progress = wx.Gauge(self, range=100)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        self.SetSizer(sizer)
        pub.subscribe(self.updateProgress, 'updateprogress')
 
    def updateProgress(self, msg, arg2=None):
        self.count = int(msg)
        self.progress.SetValue(self.count)
        if self.count >= 100:
            self.Destroy()
           
class doneScan(wx.MessageDialog):
 
    def __init__(self):
        """Constructor"""
        wx.MessageDialog.__init__(self, None, 'Scan completed\nScan Time: ' + totalScanTime + '\nReset Time: ' + totalResetTime + '\n' + '{0:.4f}'.format(float(totalScanTime) + float(totalResetTime)), 'Info', wx.OK)

class pleaseWait1(wx.MessageDialog):
 
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Please wait...", size=(400,200))
        self.count = 0
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#E0E4CC') ##4f5049
        sizer = wx.BoxSizer(wx.VERTICAL)
        textBox = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText(panel, -1, 'Please wait while scan cycle/sensor array resets...')
        textBox.Add(self.text)
        sizer.Add(textBox, wx.LEFT, 10)
        self.progress = wx.Gauge(self, range=100)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        self.SetSizer(sizer)

class pleaseWait2(wx.MessageDialog):
 
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Please wait...", size=(400,200))
        self.count = 0
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#E0E4CC') ##4f5049
        sizer = wx.BoxSizer(wx.VERTICAL)
        textBox = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText(panel, -1, 'Please wait while generating STL file...')
        textBox.Add(self.text)
        sizer.Add(textBox, wx.LEFT, 10)
        self.progress = wx.Gauge(self, range=100)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        self.SetSizer(sizer)

class MainWindow(wx.Frame):
  
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, 
            size=(600, 550))  
        self.InitUI()
        self.Centre()
        self.Show()  
        
    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        '''About'''
        ami = wx.MenuItem(fileMenu, wx.ID_NEW, '&About...')
        fileMenu.AppendItem(ami)
        self.Bind(wx.EVT_MENU, self.aboutWindow, ami)
        fileMenu.AppendSeparator()
        '''Quit'''
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        '''File Menu'''
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        '''Panel''' 
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#E0E4CC') ##4f5049
        box = wx.BoxSizer(wx.VERTICAL)
        '''Title'''
        textbox1 = wx.BoxSizer(wx.HORIZONTAL)
        jpg1 = wx.Image('SCANIR.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        title = wx.StaticBitmap(panel, -1, jpg1, (0,0), (jpg1.GetWidth(), jpg1.GetHeight()))        
        #title = wx.StaticText(panel, -1, '3D SCANNER PROGRAM')
        #title.SetFont(wx.Font(24, wx.SCRIPT, wx.NORMAL, wx.BOLD))
        #title.SetSize(title.GetBestSize())
        textbox1.Add(title, 0, wx.TOP, 10)
        box.Add(textbox1, 0, wx.ALIGN_CENTER | wx.BOTTOM, 3)
        '''Authors'''
        textbox2 = wx.BoxSizer(wx.HORIZONTAL)
        group = wx.StaticText(panel, -1, 'Group 15: Su Teh, Allan Wang, Michael Hwang, Adrian Tabula, and Nelson Wang')
        group.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        group.SetSize(group.GetBestSize())
        textbox2.Add(group, 0, wx.BOTTOM, 5)
        box.Add(textbox2, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)
        '''Explanation Paragraph'''
        textbox3 = wx.BoxSizer(wx.HORIZONTAL)
        expl = wx.StaticText(panel, -1, "       Welcome to the 3D scanner program, created for UC Berkeley's ME102B class. This scanner uses infrared distance measuring sensors and a spinning object to extract a point cloud, which is used to generate an stereolithography (STL) CAD file for solid modeling. Please follow the instructions listed below to begin scanning your object.")
        expl.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL))
        expl.SetSize(expl.GetBestSize())
        expl.Wrap(550)
        textbox3.Add(expl, 0, wx.EXPAND | wx.BOTTOM, 5)
        box.Add(textbox3, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        '''Directions'''
        directionbox = wx.BoxSizer(wx.HORIZONTAL)
        directText = wx.StaticText(panel, -1, "Directions")
        directText.SetFont(wx.Font(11, wx.SWISS,wx.NORMAL, wx.NORMAL, underline=True))
        directText.SetSize(expl.GetBestSize())
        directionbox.Add(directText, 0, wx.EXPAND)
        box.Add(directionbox, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        '''Instructions'''
        textbox4 = wx.BoxSizer(wx.HORIZONTAL)
        expl = wx.StaticText(panel, -1, "1) Place and center your object on the rotating turntable\n2) Select a COM port from the combo box below\n3) Enter a name for the file for the scan to be saved \n4) Press 'Begin Scan!' and wait!")
        expl.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL))
        expl.SetSize(expl.GetBestSize())
        expl.Wrap(550)
        textbox4.Add(expl, 0, wx.EXPAND | wx.BOTTOM, 5)
        box.Add(textbox4, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        '''Combo Box'''
        cbox = wx.BoxSizer(wx.HORIZONTAL)
        ctext = wx.StaticText(panel, -1, "Please select the COM port for the Arduino: ")
        cbox.Add(ctext, 0, wx.TOP, 3)
        com_port_list = list(serial_ports())
        self.combox = wx.ComboBox(panel, -1, size=(75, -1), choices=com_port_list)
        self.combox.SetValue(com_port_list[len(com_port_list)-1])
        cbox.Add(self.combox, 0, wx.LEFT, 10)
        box.Add(cbox, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        '''File Name'''
        textctrlbox = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, -1, 'Please select save file location: ')
        textctrlbox.Add(label, 0, wx.TOP, 3)
        self.selFile = wx.Button(panel, wx.ID_OPEN, "Search...", size=(150, -1))
        self.selFile.Bind(wx.EVT_BUTTON, self.fileDLG)
        textctrlbox.Add(self.selFile, 0, wx.LEFT, 10)
        box.Add(textctrlbox, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        '''Button'''
        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        self.scanstart = wx.Button(panel, wx.ID_CLOSE, "Begin Scan!", size=(200,50))
        self.scanstart.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.scanstart.SetBackgroundColour('#A7DBD8')
        self.scanstart.Bind(wx.EVT_BUTTON, self.startScan)
        buttonbox.Add(self.scanstart, 0, wx.TOP, 15)
        self.stopbutton = wx.Button(panel, wx.ID_CANCEL, "Stop Scan", size=(200,50))
        self.stopbutton.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.stopbutton.SetBackgroundColour('#F38630')
        self.stopbutton.Bind(wx.EVT_BUTTON, self.stopScan)
        self.stopbutton.Disable()
        buttonbox.Add(self.stopbutton, 0, wx.TOP | wx.LEFT, 15)
        box.Add(buttonbox, 0, wx.BOTTOM | wx.ALIGN_CENTER, 20)
        
        panel.SetSizer(box)
        panel.Layout()
    
    def stopScan(self, event):
        global checkDone
        checkDone = 1
        
        btn = event.GetEventObject()
        btn.Disable()
        
        self.scanstart.Enable()
        
    def fileDLG(self, event):
        global filename
        wildcard_types = "Python source (*.xyz)|*.xyz|" \
           "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="Select a File...", defaultDir=os.getcwd(), 
                            defaultFile=filename, wildcard=wildcard_types, style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
        dlg.Destroy()
            
    def startScan(self, event):
        global comport
        comport = self.combox.GetValue()
        
        self.stopbutton.Enable()
        btn = event.GetEventObject()
        btn.Disable()
        
        threadScan()
        
    def OnQuit(self, e):
        self.Close()
        
    def aboutWindow(self, e):
        msg = """ A demo using wxPython with matplotlib:
        
         * Use the matplotlib navigation bar
         * Add values to the text box and press Enter (or click "Draw!")
         * Show or hide the grid
         * Drag the slider to modify the width of the bars
         * Save the plot to a file using the File menu
         * Click on a bar to receive an informative message
        """
        dlg = wx.MessageDialog(self, msg, "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        #AboutWindow(None, title='About the Program')
    
class AboutWindow(wx.Frame):
  
    def __init__(self, parent, title):
        super(AboutWindow, self).__init__(parent, title=title, 
            size=(250, 175))  
        self.InitUI()  
        
    def InitUI(self):
        #menubar = wx.MenuBar()
        #fileMenu = wx.Menu()
        #qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        #fileMenu.AppendItem(qmi)
        #self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        #menubar.Append(fileMenu, '&File')
        #self.SetMenuBar(menubar)
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#E0E4CC') ##4f5049
        box = wx.BoxSizer(wx.VERTICAL)    
        title = wx.StaticText(panel, -1, 'Please wait while ')
        title.SetFont(wx.Font(14, wx.SCRIPT, wx.NORMAL, wx.BOLD))
        title.SetSize(title.GetBestSize())
        textbox1.Add(title, 0, wx.TOP, 10)
        box.Add(textbox1, 0, wx.ALIGN_CENTER | wx.BOTTOM, 3)
        self.Centre()
        self.Show()
        
    def OnQuit(self, e):
        self.Close()

def main():
    ex = wx.App()
    MainWindow(None, title='3D Scanner')
    ex.MainLoop()    

if __name__ == '__main__':
    main()