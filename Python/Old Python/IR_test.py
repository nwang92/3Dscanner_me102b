import serial
import csv

baudrate = 9600
COMport = 4
ser = serial.Serial('COM' + str(COMport),baudrate)
contLoop = 1
time = 0
distance = 0
in1 = 0
in2 = 0
templist = []
for x in range(0,10):
    templist.append(0)
volt = 0
logfile = open('IRlog.csv','wb')
caliV = 0.303
logwriter = csv.writer(logfile)
for x in range(0,100):
    in1 = ser.readline()
    in1 = in1.strip()
    in1 = float(in1)
    templist[x%10] = in1
    val = sum(templist)/10.0
    volt = 5.0*val/1023.0
    dist = 15.6/(volt-caliV)
    print dist
    #in2 = float(ser.readline())
    #print in2
    logwriter.writerow([volt,dist])
logfile.close()
ser.close()

