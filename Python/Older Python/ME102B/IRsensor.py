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

while True:
    data = arduino.readline()
    try:
        senVal = int(data)
    except:
        pass
    volt1 = 5.0*senVal/1023.0
    dist1 = 20.7965/(volt1+.2128) - 1.6
    #volt2 = senVal*5.0/1023.0
    #dist2 = 18.4694/(volt2+.168983) - .440678
    print dist1
    
f.close()
arduino.close()
print('Scan phase complete')