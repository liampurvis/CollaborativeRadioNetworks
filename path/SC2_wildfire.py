import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

f = open('SC2_wildfire.txt','w')
F = 0
N = 7
step = 120*7



p1_r = path.point(24, 22, step)
p1_t = path.point(1, 1, 10) + path.point(4, 20, 10) + path.line(4,20,50,20,100)     \
        + path.point(1, 1, 120) \
        + path.point(1, 1, 120) \
        + path.point(1, 1, 120) \
        + path.point(1, 1, 120) \
        + path.point(1, 1, 120) \
        + path.point(1, 1, 10) + path.point(2, 20, 10) + path.line(2,20,48,20,100)

p2_r = path.point(26, 22, step)
p2_t = path.point(2, 1, 10) + path.point(2, 20, 10) + path.line(2,20,48,20,100)     \
        + path.point(2, 1, 10) + path.point(4, 20, 10) + path.line(4,20,50,20,100)  \
        + path.point(2, 1, 120) \
        + path.point(2, 1, 120) \
        + path.point(2, 1, 120) \
        + path.point(2, 1, 120) \
        + path.point(2, 1, 120)


p3_r = path.point(28, 22, step)
p3_t = path.point(3, 1, 120) \
        + path.point(3, 1, 10) + path.point(2, 20, 10) + path.line(2,20,48,20,100)  \
        + path.point(3, 1, 10) + path.point(4, 20, 10) + path.line(4,20,50,20,100)  \
        + path.point(3, 1, 120) \
        + path.point(3, 1, 120) \
        + path.point(3, 1, 120) \
        + path.point(3, 1, 120)


p4_r = path.point(30, 22, step)
p4_t = path.point(4, 1, 120) \
        + path.point(4, 1, 10) \
        + path.point(4, 1, 10) + path.point(2, 20, 10) + path.line(2,20,48,20,100)  \
        + path.point(4, 1, 10) + path.point(4, 20, 10) + path.line(4,20,50,20,100)  \
        + path.point(4, 1, 10) \
        + path.point(4, 1, 10) \
        + path.point(4, 1, 10)

p5_r = path.point(32, 22, step)
p5_t = path.point(5, 1, 120) \
        + path.point(5, 1, 10) \
        + path.point(5, 1, 10) \
        + path.point(5, 1, 10) + path.point(2, 20, 10) + path.line(2,20,48,20,100)  \
        + path.point(5, 1, 10) + path.point(4, 20, 10) + path.line(4,20,50,20,100)  \
        + path.point(5, 1, 10) \
        + path.point(5, 1, 10)

p6_r = path.point(34, 22, step)
p6_t = path.point(6, 1, 120) \
        + path.point(6, 1, 10) \
        + path.point(6, 1, 10) \
        + path.point(6, 1, 10) \
        + path.point(6, 1, 10) + path.point(2, 20, 10) + path.line(2,20,48,20,100)  \
        + path.point(6, 1, 10) + path.point(4, 20, 10) + path.line(4,20,50,20,100)  \
        + path.point(6, 1, 10)

p7_r = path.point(36, 22, step)
p7_t = path.point(7, 1, 120) \
        + path.point(7, 1, 10) \
        + path.point(7, 1, 10) \
        + path.point(7, 1, 10) \
        + path.point(7, 1, 10) \
        + path.point(7, 1, 10) + path.point(2, 20, 10) + path.line(2,20,48,20,100)  \
        + path.point(7, 1, 10) + path.point(4, 20, 10) + path.line(4,20,50,20,100)


paths = [p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t, p5_r, p5_t, p6_r, p6_t, p7_r, p7_t]
path.myplot(paths, 0, 60, 0, 30)



for ind in range((F+N)*2):
    paths[ind] = [("{0:.2f}".format(i[0]), "{0:.2f}".format(i[1])) for i in paths[ind]]

f.write(str(F) + '\n')
f.write(str(N) + '\n')
for i in range(step):
    for j in range(N+F):
        f.write('[')
        f.write('('+paths[2*j][i][0] + ',' + paths[2*j][i][1] + ')')
        f.write('('+paths[2*j+1][i][0] + ',' + paths[2*j+1][i][1] + ')')
        f.write(']')
    f.write('\n')
f.close()







