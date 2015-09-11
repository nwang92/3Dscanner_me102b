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
filename = 0
renderOn = 0
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
    global renderOn
    global app
    filename = defaultFilename
    
    '''Scanner Parameters'''
    distFromCenter = 7 #in inches
    stageRevolutionSteps = 200*8*32/3.0 #in steps
    height_increment = .282*.75
    stagePos = 0
    angle = 0
    height = 0
    ir1 = 0
    volt1 = 0
    dist1 = 0
    bufferSize = 10
    xvals = []
    yvals = []
    xy_x = []
    xy_y = []
    res = 0

    '''Code Parameters'''
    in2cm = 2.54000508001 #conversion from inches to centimeters
    checkDone = 0
    
    '''File Write'''
    filename = str(filename)
    nameOfFile = filename.split('\\')
    nameOfFile = nameOfFile[len(nameOfFile)-1]
    nameOfFile = nameOfFile.split('.')
    nameOfFile = nameOfFile[0]
    f = open(filename,'w')
    
    '''Start of Scan'''
    arduino = serial.Serial(comport, 9600)
    time.sleep(3)

    renderOn = 1
    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    #w.resize(800, 600)
    w.opts['distance'] = 50
    w.showFullScreen()
    w.setWindowTitle('Real-Time Point Cloud')
    g = gl.GLGridItem()
    w.addItem(g)
    
    start = time.time()
    arduino.write('1')
    loopcount = 1
    
    while True:
        data = arduino.readline()
        if checkDone == 1:
            break
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
            break
        alist = data.rstrip()
        alist = alist.split(',')
        if len(alist) == 2:
            stagePos = float(alist[0])
            ir1 = float(alist[1])
        angle = stagePos/stageRevolutionSteps*360.
        volt1 = 5.0*ir1/1023.0
        dist1 = -16.124*volt1**3 + 78.966*volt1**2 - 136.84*volt1 + 94.769        
        #dist1 = 20.7965/(volt1+.2128) - 1.6
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

    try:
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
    except:
        pass

    scanend = time.time()
    totalScanTime = scanend-start
    
    '''Reset Array'''
    first = 0
    arduino.write('9') 
    
    newD = pleaseWait1()
    newD.ShowWithEffect(wx.SHOW_EFFECT_BLEND)
    
    while True:
        data = arduino.readline()
        if '999999999' in data:
            break
            
    newD.Destroy()
    
    end = time.time()
    totalResetTime = end-scanend
    
    f.close()
    arduino.close()
    
    lastD = pleaseWait2()
    lastD.ShowWithEffect(wx.SHOW_EFFECT_BLEND)

    dirPath = os.getcwd()
    os.system('cd "C:\Program Files\VCG\MeshLab"')
    os.system('start MeshLabServer -i "' + dirPath + '\\' + nameOfFile + '.xyz" -o "' + dirPath + '\\' + nameOfFile + '.stl" -s "' + dirPath + '\\' + 'STLgen.mlx" -om vc fq wn')

    lastD.Destroy()
    app.quit()
    
    doneD = doneScan()
    doneD.ShowModal()
    
    pub.sendMessage("donewithscan", message='1')
    
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

class doneScan(wx.Dialog):
 
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Scan Complete", size=(225,200))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#E0E4CC') ##4f5049
        sizer = wx.BoxSizer(wx.VERTICAL)
        textBox = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText(panel, -1, 'Scan completed!\n\nScan Time: ' + '{0:.4f}'.format(totalScanTime) + '\nReset Time: ' + '{0:.4f}'.format(totalResetTime) + '\nTotal Time: ' + '{0:.4f}'.format(float(totalScanTime)+float(totalResetTime)), style=wx.ALIGN_CENTRE_HORIZONTAL)
        textBox.Add(self.text)
        sizer.Add(textBox, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 15)
        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        self.close = wx.Button(panel, wx.ID_CLOSE, "Close", size=(100,35))
        self.close.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.close.SetBackgroundColour('#F38630')
        self.close.Bind(wx.EVT_BUTTON, self.OnQuit)
        buttonbox.Add(self.close, 0, wx.TOP, 5)
        sizer.Add(buttonbox, wx.ALIGN_CENTER | wx.ALL, 5)
        panel.SetSizer(sizer)
        panel.Layout()
        self.Centre()
        
    def OnQuit(self, e):
        self.Close()

class pleaseWait1(wx.Dialog):
 
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Please wait...", size=(375,75))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#E0E4CC') ##4f5049
        sizer = wx.BoxSizer(wx.VERTICAL)
        textBox = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText(panel, -1, 'Please wait while scan cycle/sensor array resets...')
        self.text.Wrap(300)
        textBox.Add(self.text, 0, wx.ALIGN_CENTER)
        sizer.Add(self.text, 0, wx.ALIGN_CENTER | wx.TOP, 12)
        panel.SetSizer(sizer)
        panel.Layout()
        self.Centre()

class pleaseWait2(wx.Dialog):
 
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Please wait...", size=(375,75))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#E0E4CC') ##4f5049
        sizer = wx.BoxSizer(wx.VERTICAL)
        textBox = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText(panel, -1, 'Please wait while generating STL file...')
        self.text.Wrap(300)
        textBox.Add(self.text, 0, wx.ALIGN_CENTER)
        sizer.Add(textBox, 0, wx.ALIGN_CENTER | wx.TOP, 12)
        panel.SetSizer(sizer)
        panel.Layout()
        self.Centre()

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
        global renderOn
        comport = self.combox.GetValue()
        
        if renderOn == 1:
            renderOn = 0
            app.quit()
        
        self.stopbutton.Enable()
        btn = event.GetEventObject()
        btn.Disable()
        threadScan()
        pub.subscribe(self.resetButton, 'donewithscan')
        
    def resetButton(self, message):
        if message == '1':
            self.stopbutton.Disable()
            self.scanstart.Enable()
        
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
    
def main():
    ex = wx.App()
    MainWindow(None, title='3D Scanner')
    ex.MainLoop()    

if __name__ == '__main__':
    main()