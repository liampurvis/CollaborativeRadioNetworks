import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

f = open('SC2_wildfire.txt','w')
N = 3
step = 360



p1_r = path.point(24, 22, step)
p1_t = path.point(1, 1, 10) + path.point(4, 20, 10) + path.line(4,20,50,20,100) \
        + path.point(1, 1, 120) \
        + path.point(1, 1, 10) + path.point(2, 20, 10) + path.line(2,20,48,20,100)

p2_r = path.point(26, 22, step)
p2_t = path.point(2, 1, 10) + path.point(2, 20, 10) + path.line(2,20,48,20,100) \
        + path.point(2, 1, 10) + path.point(4, 20, 10) + path.line(4,20,50,20,100)\
        + path.point(2, 1, 120)

p3_r = path.point(28, 22, step)
p3_t = path.point(3, 1, 120) \
        + path.point(3, 1, 10) + path.point(2, 20, 10) + path.line(2,20,48,20,100)\
        + path.point(3, 1, 10) + path.point(4, 20, 10) + path.line(4,20,50,20,100)



paths = [p1_r, p1_t, p2_r, p2_t, p3_r, p3_t]
path.myplot(paths, 0, 60, 0, 30)



for ind in range(N*2):
    paths[ind] = [("{0:.2f}".format(i[0]), "{0:.2f}".format(i[1])) for i in paths[ind]]

f.write(str(N) + '\n')
for i in range(step):
    for j in range(N):
        f.write('[')
        f.write('('+paths[2*j][i][0] + ',' + paths[2*j][i][1] + ')')
        f.write('('+paths[2*j+1][i][0] + ',' + paths[2*j+1][i][1] + ')')
        f.write(']')
    f.write('\n')
f.close()







