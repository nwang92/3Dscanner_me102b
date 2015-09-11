import re, math, time
import matplotlib.pyplot as plt
import numpy as np
f = open('a.txt','rb')
l = re.split('\t|\r|\n',f.readline())
xvals = []
yvals = []
Q = 1e-3
R = 0.1**2


while (float(l[2])==0):
    xvals.append(float(l[0]))
    yvals.append(float(l[1]))
    l = re.split('\t|\r|\n',f.readline())
xy = zip(xvals,yvals)
xy = zip(*sorted(xy,key=lambda xy: xy[0]))
xvals = list(xy[0])
yvals = list(xy[1])
bf = len(xvals)

xhat = np.zeros(bf)
P = np.zeros(bf)
xhatminus=np.zeros(bf)
Pminus = np.zeros(bf)
K = np.zeros(bf)
xhat[0] = xvals[0]
P[0] = 1.0
xtmp = []
for j,x in enumerate(xvals):
    if (x<0) and (yvals[j]<0):
        xhatminus[j]=xhat[j-1]
        Pminus[j]=P[j-1]+Q
        K[j]=Pminus[j]/(Pminus[j]+R)
        xhat[j]=xhatminus[j]+K[j]*(x-xhatminus[j])
        P[j] = (1-K[j])*Pminus[j]
        xtmp.append(x)
yhat = np.zeros(bf)
P = np.zeros(bf)
yhatminus=np.zeros(bf)
Pminus = np.zeros(bf)
K = np.zeros(bf)
yhat[0] = yvals[0]
P[0] = 1.0
ytmp = []
for k,y in enumerate(yvals):
    if (xvals[k]<0) and (y<0):
        yhatminus[j]=xhat[j-1]
        Pminus[j]=P[j-1]+Q
        K[j]=Pminus[j]/(Pminus[j]+R)
        yhat[j]=yhatminus[j]+K[j]*(x-yhatminus[j])
        P[j] = (1-K[j])*Pminus[j] 
        ytmp.append(y)
plt.figure()
plt.scatter(xtmp,ytmp,color = 'r')
plt.scatter(xhat,yhat,color = 'b')
plt.show()

    
