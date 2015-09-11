import re
import math
import matplotlib.pyplot as plt
import time
f = open('a.txt','rb')
l = re.split('\t|\r|\n',f.readline())
x = []
y = []
i = 0
while (float(l[2])==0):
    x.append(float(l[0]))
    y.append(float(l[1]))
    l = re.split('\t|\r|\n',f.readline())
##    i+=1
##    print i
##xy = zip(x,y)
##xy = zip(*sorted(xy,key=lambda xy: xy[0]))
##x = list(xy[0])
##y = list(xy[1])
x1 = time.clock()
i1 = len(x)/2+len(x)%2
for i in range(i1):
    d = round(2*math.sqrt((x[i]-x[i1])**2 + (y[i] - y[i1])**2))
    dx = (x[i]-x[i1])/d
    dy = (y[i]-y[i1])/d
    for j in range(int((d-1))):
        x.append(x[i]-j*dx)
        y.append(y[i]-j*dy)
    i1+=1
print time.clock()-x1
plt.scatter(x,y)
plt.axis([-10,10,-10,10])
plt.show()

##a = ['A','C','D']
##b = [3,2,1]
##c = zip(a,b)
##print zip(*sorted(c,key=lambda c: c[1]))[0]

##import numpy as np
##inp = '123,,213,323'
##a = inp.rstrip()
##a = a.split(',')
##print a
##if (',,' in a)==-1:
##    a = [float(i) for i in a]
##else:
##    t = 0
##    while (',,' in a)!=-1:
##        try:
##            a.pop(a.index(''))
##            t+=1
##        except:
##            break
##    a = [float(i) for i in a]
##    for i in range(t):
##        a.append(np.median(a))
