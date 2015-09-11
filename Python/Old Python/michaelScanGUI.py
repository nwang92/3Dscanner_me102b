import wx
import serial
import time
import math
import numpy
import wx_mpl_dynamic_graph2 as disp

from threading import Thread
from wx.lib.pubsub import pub

'''Scanner Parameters'''
distFromCenter = 7 #in inches
stageRevolutionSteps = 200*8*32/3.0 #in steps
stagePos = 0
angle = 0
height = 0
sensorPos = 0
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

'''Code Parameters'''
in2cm = 2.54 #conversion from inches to centimeters
checkDone = 0

APP_EXIT = 1

def threedeeScan():
    global checkDone
    #print command
    
    #arduino = serial.Serial(3, 115200)
    f = open('testPointCloud.txt','w')
    f2 = open('rawDataTEST.txt','w')
    time.sleep(2) # waiting the initialization...
    print('Initializing...')
    
    print('Begin scan phase')
    time.sleep(1)
    start = time.time()
    #arduino.write(str(command))
    #data = arduino.readline()
    """
    while True:

        data = arduino.readline()
        list = data.rstrip()
        list = data.split(',')
        if len(list) == 1:
            break
        if len(list) == 2:
            stagePos = float(list[0])
            ir1 = float(list[1])
        angle = stagePos/stageRevolutionSteps*360.0
        while angle > 360:
            angle = angle - 360
        height = 0
        volt1 = 5.0*ir1/1023.0
        dist1 = ((14.4/(volt1-caliV))+2)
        #dist1 = 9.108*math.pow(10,-6)*ir1*ir1 + -1*.03243*ir1 + 33.81
        x1 = ((distFromCenter*in2cm)-dist1)*math.cos(math.radians(angle))
        y1 = ((distFromCenter*in2cm)-dist1)*math.sin(math.radians(angle))
        print data
        if dist1 < 33:
            f.write('{0:.6f}'.format(x1) + '\t' + '{0:.6f}'.format(y1) + '\t' + '{0:.6f}'.format(height) + '\n')
            graphdata = [x1, y1, height]
            zapp.update_data(graphdata)
            f2.write(str(angle) + '\t' + str(dist1) + '\n')
                
    end = time.time()
    print('Time elapsed: ' + '{0:.4f}'.format(end-start) + ' seconds')
    
    f.close()
    f2.close()
    arduino.close()
    checkDone = 1
    """
    print('Scan phase complete')

class threadScan(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.start()
    
    def run(self):
        threedeeScan()

class progressDialog(wx.Dialog):
 
    def __init__(self):
        """Constructor"""
        '''
        wx.Dialog.__init__(self, None, title="Progress")
        self.count = 0
 
        self.progress = wx.Gauge(self, range=100)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        self.SetSizer(sizer)
        '''
        #pub().subscribe(self.updateProgress, "update")
        zapp = wx.App(False)
        zapp.frame = disp.GraphFrame()
        zapp.frame.Show()
        zapp.MainLoop()

        
 
    def updateProgress(self, msg):
        self.count += 1
        if self.count >= 100:
            self.Destroy()
        self.progress.SetValue(self.count)

class MainWindow(wx.Frame):
  
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, 
            size=(625, 400))  
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
        panel.SetBackgroundColour('#4f5049')
        box = wx.BoxSizer(wx.VERTICAL)
        '''Border'''
        '''Title'''
        textbox1 = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(panel, -1, '3D SCANNER PROGRAM')
        title.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD))
        title.SetSize(title.GetBestSize())
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
        box.Add(textbox3, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
        '''Instructions'''
        textbox4 = wx.BoxSizer(wx.HORIZONTAL)
        expl = wx.StaticText(panel, -1, "1) Place and center your object on the disk\n2) Select a scan mode from the options listed below\n3) Press 'Begin Scan!' and wait!")
        expl.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL))
        expl.SetSize(expl.GetBestSize())
        expl.Wrap(550)
        textbox4.Add(expl, 0, wx.EXPAND | wx.BOTTOM, 5)
        box.Add(textbox4, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)
        '''Radiobuttons'''
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
        '''Button'''
        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        scanstart = wx.Button(panel, wx.ID_CLOSE, "Begin Scan!", size=(350,50))
        scanstart.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        scanstart.Bind(wx.EVT_BUTTON, self.startScan)
        buttonbox.Add(scanstart, 0, wx.TOP, 20)
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
        global checkDone
        btn = event.GetEventObject()
        btn.Disable()
        
        threadScan()
        dlg = progressDialog()
        dlg.ShowModal()
 
        btn.Enable()
    
    def ShowDialog(self):
        dial = wx.MessageDialog(None, 'Download completed', 'Info', wx.OK)
        dial.ShowModal()
        
    def OnQuit(self, e):
        self.Close()
        
    def aboutWindow(self, e):
        AboutWindow(None, title='About the Program')

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