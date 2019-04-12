import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

f = open('SC2_randomWalk.txt','w')
N = 4
step = 500
mag = 0.5



p1_r = path.randomWalk((5, 5), step, mag, 1, 1, 10, 10)
p1_t = path.randomWalk((6, 6), step, mag, 1, 1, 10, 10)
p2_r = path.randomWalk((7, 5), step, mag, 1, 1, 10, 10)
p2_t = path.randomWalk((8, 6), step, mag, 1, 1, 10, 10)
p3_r = path.randomWalk((1, 5), step, mag, 1, 1, 10, 10)
p3_t = path.randomWalk((2, 6), step, mag, 1, 1, 10, 10)
p4_r = path.randomWalk((3, 5), step, mag, 1, 1, 10, 10)
p4_t = path.randomWalk((4, 6), step, mag, 1, 1, 10, 10)

paths = [p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t]
path.myplot(paths, 0, 11, 0, 11)



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







