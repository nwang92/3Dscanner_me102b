##a = ['A','C','D']
##b = [3,2,1]
##c = zip(a,b)
##print zip(*sorted(c,key=lambda c: c[1]))[0]
import numpy as np
inp = '123,,213,323'
a = inp.rstrip()
a = a.split(',')
print a
if (',,' in a)==-1:
    a = [float(i) for i in a]
else:
    t = 0
    while (',,' in a)!=-1:
        try:
            a.pop(a.index(''))
            t+=1
        except:
            break
    a = [float(i) for i in a]
    for i in range(t):
        a.append(np.median(a))
