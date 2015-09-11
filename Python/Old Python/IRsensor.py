import serial
import time
import math

ir1 = 0
ir2 = 0
ir3 = 0
caliV = 1.75

arduino = serial.Serial(3, 115200)
f = open('file.txt','w')
time.sleep(2) # waiting the initialization...
print('Initializing...')

print('Begin scan phase')
time.sleep(1)
start = time.time()
arduino.write('1')

while True:
    data = arduino.readline()
    alist = data.split()
    try:
        val = int(alist[0])
    except:
        continue
    volt1 = 5.0*val/1023.0
    dist1 = (((116994.0/1805)/(volt1-(-308.0/475.0)))-180/19)
    dist = 2076.0/(val-11)
    dist_new = 12.21*math.pow(val,-1.15)
    print dist*2.54, dist1, dist_new*1000
    
f.close()
arduino.close()
print('Scan phase complete')
