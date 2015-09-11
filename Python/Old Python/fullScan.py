import serial
import time

distFromCenter = 7 #in inches
stageRevolutionSteps = 200*8*32/3.0 #in steps
revNum = 1
in2cm = 2.54 #conversion from inches to centimeters
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
caliV = 0.303

arduino = serial.Serial(3, 115200)
f = open('file.txt','w')
time.sleep(2) # waiting the initialization...
print('Initializing...')

#arduino.write('1')
#data = 'START'
print('Begin scan phase')
time.sleep(1)
start = time.time()
arduino.write('1')
#data = arduino.readline()

while True:
    data = arduino.readline()
    list = data.split(',')
    if len(list) == 5:
        try:
            stagePos = float(list[0])
        except ValueError:
            stagePos = stagePos
        try:
            sensorPos = float(list[1])
        except ValueError:
            sensorPos = sensorPos
        try:
            ir1 = float(list[2])
        except ValueError:
            ir1 = ir1
        try:
            ir2 = float(list[3])
        except ValueError:
            ir2 = ir2
        try:
            ir3 = float(list[4])
        except ValueError:
            ir3 = ir3
    if int(stagePos) == 20037:
            break
    angle = stagePos/stageRevolutionSteps*360.0
    while angle > 360:
        angle - 360
    height = sensorPos/(400*16)*.1*in2cm
    volt1 = 5.0*ir1/1023.0
    dist1 = 15.6/(volt1-caliV)
    volt2 = 5.0*ir2/1023.0
    dist2 = 15.6/(volt2-caliV)
    volt3 = 5.0*ir3/1023.0
    dist3 = 15.6/(volt3-caliV)
    f.write('{0:.6f}'.format(angle) + '\t' '{0:.6f}'.format(height) + '\n')
    percentage_completed = stagePos/(revNum*stageRevolutionSteps)*100.0
    #print('Scanning: ' + '{0:.2f}'.format(percentage_completed) + '% complete')
    print data
    
first = 0
while True:
    data = arduino.readline()
    #print data
    val = data.split()
    if first == 0:
        maxVal = float(val[0])
        first = 1
    if int(val[0]) == 999999999:
        break
    if float(val[0]) < 0:
        val[0] = 0
    pct_cmp = 100.0-(float(val[0])/maxVal*100.0)
    print('Resetting IR array: ' + '{0:.2f}'.format(pct_cmp) + '% complete')
            
end = time.time()
print('Time elapsed: ' + '{0:.4f}'.format(end-start) + ' seconds')

f.close()
arduino.close()
print('Scan phase complete')