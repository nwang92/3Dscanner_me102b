import re, math, time
import matplotlib.pyplot as plt
import numpy as np
f = open('a.txt','rb')
l = re.split('\t|\r|\n',f.readline())
xvals = []
yvals = []

xc = []
yc = []

while (float(l[2])==0):
    xvals.append(float(l[0]))
    yvals.append(float(l[1]))
    l = re.split('\t|\r|\n',f.readline())
for i, x in enumerate(xvals):
    y = yvals[i]
    for (


    
