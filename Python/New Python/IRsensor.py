import serial
import time
import math

ir1 = 0
ir2 = 0
ir3 = 0
caliV = 3.0449
senVal = 0

arduino = serial.Serial(3, 9600)
f = open('file.txt','w')
time.sleep(2) # waiting the initialization...
print('Initializing...')

print('Begin scan phase')
time.sleep(1)
start = time.time()
tempv = []
tempd = []
while True:
    data = arduino.readline()
    try:
        senVal = int(data)
    except:
        pass
    volt1 = 5.0*senVal/1023.0
    dist1 = -16.124*volt1**3 + 78.966*volt1**2 - 136.84*volt1 + 94.769
    #volt2 = senVal*5.0/1023.0
    #dist2 = 18.4694/(volt2+.168983) - .440678
    tempv.append(volt1)
    tempd.append(dist1)
    if len(tempv)>=20:
        tv = 0
        td = 0
        for i,v in enumerate(tempv):
            tv+=v
            td+=tempd[i]
        print tv/20,td/20
        tempv = []
        tempd = []

f.close()
arduino.close()
print('Scan phase complete')