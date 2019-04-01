import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

f = open('circle.txt','w')
N = 4
step = 100

p1_r = path.point(5,5,100)
p1_t = path.point(5,1,1) + path.circle(5,1,4,pi,4*pi,1,99)
p2_r = path.point(11,5,100)
p2_t = path.point(11,1,1) + path.circle(11,1,4,pi,4*pi,0,99)
p3_r = path.point(11,11,100)
p3_t = path.point(11,15,1) + path.circle(11,15,4,0,4*pi,1,99)
p4_r = path.point(5,11,100)
p4_t = path.point(5,15,1) + path.circle(5,15,4,0,4*pi,0,99)

paths = [p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t]

path.myplot(paths)

for ind in range(N*2):
    paths[ind] = [("{0:.2f}".format(i[0]), "{0:.2f}".format(i[1])) for i in paths[ind]]

print (paths)

f.write(str(N) + '\n')
for i in range(step):
    #print (i)
    for j in range(N):
        f.write('[')
        f.write('('+paths[2*j][i][0] + ',' + paths[2*j][i][1] + ')')
        f.write(',')
        f.write('('+paths[2*j+1][i][0] + ',' + paths[2*j+1][i][1] + ')')
        f.write(']')
    f.write('\n')

f.close()
            






