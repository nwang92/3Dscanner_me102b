import serial
import time
import math

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

arduino = serial.Serial(3, 115200)
f = open('testPointCloudNELSON.xyz','w')
f2 = open('rawDataTEST.txt','w')
time.sleep(2) # waiting the initialization...
print('Initializing...')

print('Begin scan phase')
time.sleep(1)
start = time.time()
arduino.write('1')
#data = arduino.readline()

while True:
    data = arduino.readline()
    alist = data.rstrip()
    alist = data.split(',')
    if len(alist) == 1:
        if int(alist[0]) == 222222222:
            print 'fuck you'
            height = height + .2*in2cm
        else:
            break
    if len(alist) == 2:
        stagePos = float(alist[0])
        ir1 = float(alist[1])
    angle = stagePos/stageRevolutionSteps*360.0
    while angle > 360:
        angle = angle - 360
    volt1 = 5.0*ir1/1023.0
    print angle
    dist1 = ((17.2/(volt1-caliV))+1.5)
    #dist1 = 9.108*math.pow(10,-6)*ir1*ir1 + -1*.03243*ir1 + 33.81
    x1 = ((distFromCenter*in2cm)-dist1)*math.cos(math.radians(angle))
    y1 = ((distFromCenter*in2cm)-dist1)*math.sin(math.radians(angle))
    if dist1 < 33:
        f.write('{0:.6f}'.format(x1) + '\t' + '{0:.6f}'.format(y1) + '\t' + '{0:.6f}'.format(height) + '\n')
        #f2.write(str(angle) + '\t' + str(dist1) + '\n')
            
scanend = time.time()
print('Scan/Data Collection time elapsed: ' + '{0:.4f}'.format(scanend-start) + ' seconds')

'''Reset Array'''
arduino.write('9')    
while True:
    data = arduino.readline()
    if len(data)==11:
        break
    
end = time.time()
print('Reset Array time elapsed: ' + '{0:.4f}'.format(end-scanend) + ' seconds')
print('Total time elapsed: ' + '{0:.4f}'.format(end-start) + ' seconds')

f.close()
f2.close()
arduino.close()
print('Scan phase complete')