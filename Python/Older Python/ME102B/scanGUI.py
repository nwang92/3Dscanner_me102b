import wx
import serial
import time
import math
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

from threading import Thread
from wx.lib.pubsub import pub

'''Code Parameters'''
in2cm = 2.54000508001 #conversion from inches to centimeters
checkDone = 0
command = 0
filename = 0
APP_EXIT = 1
filename = ''

def threedeeScan():
    global totalScanTime
    global totalResetTime
    global arduino
    global checkDone
    global filename
    
    '''Scanner Parameters'''
    distFromCenter = 7 #in inches
    stageRevolutionSteps = 200*8*32/3.0 #in steps
    height_increment = .282/2
    pointCloud = np.array([[0,0,0]])
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
    xy_x = []
    xy_y = []
    res = 0
    
    '''Code Parameters'''
    in2cm = 2.54000508001 #conversion from inches to centimeters
    checkDone = 0
    '''Start of Scan'''
    arduino = serial.Serial(3, 115200)
    f = open(filename + '.xyz','w')
    f3 = open(filename + '2' + '.xyz','w')
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
        print data
        if '222222222' in data:
            if height == 0:
                p1 = len(xy_x)/2
                for p2 in range(p1):
                    print p1,p2,len(xy_x)
                    d1 = round(2*math.sqrt((xy_x[p2]-xy_x[p1])**2+(xy_y[p2]-xy_y[p1])**2))
                    dx = (xy_x[p2]-xy_x[p1])/d1
                    dy = (xy_y[p2]-xy_y[p1])/d1
                    for j in range(int(d1-1)):
                        tmp_x = xy_x[p2]-dx*j
                        tmp_y = xy_y[p2]-dy*j
                        f.write('{0:.6f}'.format(tmp_x) + '\t' + '{0:.6f}'.format(tmp_y) + '\t' + '{0:.6f}'.format(height) + '\n')
                    p1+=1
            xy_x=[]
            xy_y=[]
            height = height + height_increment
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
                    p2+=1
            xy_x=[]
            xy_y=[]
            break
        alist = data.rstrip()
        #print alist
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
        angle = stagePos/stageRevolutionSteps*360.
        while angle > 360:
            angle = angle - 360
        volt1 = 5.0*ir1/1023.0
        dist1 = (1.566/(volt1+.648421))+8.0424
        rawx1 = ((distFromCenter*in2cm)-dist1)*math.cos(math.radians(angle))
        rawy1 = ((distFromCenter*in2cm)-dist1)*math.sin(math.radians(angle))
        array = np.array([[rawx1, rawy1, height]])
        w.addItem(gl.GLScatterPlotItem(pos=array, size=2, pxMode=True))
        QtGui.QApplication.processEvents()
        if dist1 < 30:
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
    '''
    def update():
        ## update volume colors
        global pointCloud
        w.addItem(gl.GLScatterPlotItem(pos=pointCloud, size=2,pxMode=True))
        QtGui.QApplication.processEvents()
        pointCloud = np.array([[0,0,0]])
    
    t = QtCore.QTimer()
    t.timeout.connect(update)
    t.start(50)
    '''
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
        wx.Dialog.__init__(self, None, title="Progress")
        self.count = 0
 
        self.progress = wx.Gauge(self, range=100)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        self.SetSizer(sizer)
        pub.subscribe(self.updateProgress, 'updateprogress')
 
    def updateProgress(self, msg, arg2=None):
        print msg
        self.count = int(msg)
        self.progress.SetValue(self.count)
        if self.count >= 100:
            self.Destroy()
            
class MainWindow(wx.Frame):
  
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, 
            size=(625, 425))  
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
        #jpg1 = wx.Image('SCANIR.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #title = wx.StaticBitmap(self, -1, jpg1, (0,0), (jpg1.GetWidth(), jpg1.GetHeight()))        
        title = wx.StaticText(panel, -1, '3D SCANNER PROGRAM')
        title.SetFont(wx.Font(24, wx.SCRIPT, wx.NORMAL, wx.BOLD))
        title.SetSize(title.GetBestSize())
        textbox1.Add(title, 0, wx.ALL, 10)
        box.Add(textbox1, 0, wx.ALIGN_CENTER | wx.ALL, 3)
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
        box.Add(textbox3, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
        '''Instructions'''
        textbox4 = wx.BoxSizer(wx.HORIZONTAL)
        expl = wx.StaticText(panel, -1, "1) Place and center your object on the rotating turntable\n2) Enter a name for the file for the scan to be saved \n3) Press 'Begin Scan!' and wait!")
        expl.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL))
        expl.SetSize(expl.GetBestSize())
        expl.Wrap(550)
        textbox4.Add(expl, 0, wx.EXPAND | wx.BOTTOM, 5)
        box.Add(textbox4, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)
        '''Radiobuttons
        optionbox = wx.BoxSizer(wx.HORIZONTAL)
        self.rb1 = wx.RadioButton(panel, -1, 'Low Quality', (10, 10), style=wx.RB_GROUP)
        self.Bind(wx.EVT_RADIOBUTTON, self.setState, id=self.rb1.GetId())
        optionbox.Add(self.rb1)
        self.rb2 = wx.RadioButton(panel, -1, 'Medium Quality', (10, 30))
        self.Bind(wx.EVT_RADIOBUTTON, self.setState, id=self.rb2.GetId())
        optionbox.Add(self.rb2, wx.LEFT, border=25)
        self.rb3 = wx.RadioButton(panel, -1, 'High Quality', (10, 50))
        self.Bind(wx.EVT_RADIOBUTTON, self.setState, id=self.rb3.GetId())
        optionbox.Add(self.rb3, 0, wx.LEFT, border=10)
        box.Add(optionbox, 0, wx.ALIGN_CENTER | wx.ALL, border=10)
        '''
        '''File Name'''
        textctrlbox = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, -1, 'Please enter a file name:')
        textctrlbox.Add(label, 0, wx.TOP, 5)
        self.inputbox = wx.TextCtrl(panel, size=(250, -1))
        self.inputbox.SetValue('testPointCloud')
        textctrlbox.Add(self.inputbox, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        box.Add(textctrlbox, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        '''Button'''
        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        scanstart = wx.Button(panel, wx.ID_CLOSE, "Begin Scan!", size=(275,50))
        scanstart.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        scanstart.SetBackgroundColour('#A7DBD8')
        scanstart.Bind(wx.EVT_BUTTON, self.startScan)
        buttonbox.Add(scanstart, 0, wx.TOP, 20)
        quitbutton = wx.Button(panel, wx.ID_CANCEL, "Quit Application", size=(275,50))
        quitbutton.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        quitbutton.SetBackgroundColour('#F38630')
        quitbutton.Bind(wx.EVT_BUTTON, self.OnQuit)
        buttonbox.Add(quitbutton, 0, wx.TOP | wx.LEFT, 20)
        box.Add(buttonbox, 0, wx.BOTTOM | wx.ALIGN_CENTER, 20)
        
        panel.SetSizer(box)
        panel.Layout()
    
    def setState(self, event):
        global command
        state1 = self.rb1.GetValue()
        state2 = self.rb2.GetValue()
        state3 = self.rb3.GetValue()
        if state1:
            command = 1
        elif state2:
            command = 2
        elif state3:
            command = 3
            
    def startScan(self, event):
        global filename
        filename = self.inputbox.GetValue()
        
        btn = event.GetEventObject()
        btn.Disable()
        
        threadScan()
        
        self.ShowWithEffect(wx.SHOW_EFFECT_BLEND)
        btn.Enable()
    
    def ShowDialog(self):
        dial = wx.MessageDialog(None, 'Scan completed\nScan Time: ' + totalScanTime + '\nReset Time: ' + totalResetTime + '\n' + '{0:.4f}'.format(float(totalScanTime) + float(totalResetTime)), 'Info', wx.OK)
        dial.ShowModal()
        
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
            size=(400, 300))  
        self.InitUI()  
        
    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
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