import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

f = open('SC2_wildfire.txt','w')
F = 2
N = 6
step = 120*8

f1_r = path.point(30, 15, step)
f2_r = path.point(31, 15, step)

f1_t = path.point(18, 20, 10) + path.line(18,20,35,20,110)      \
        + path.point(18, 20, 10) + path.line(18,20,35,20,110)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,110)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,110)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,110)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,110)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,110)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,110)

f2_t = path.point(16, 20, 10) + path.line(16,20,33,20,110)      \
        + path.point(16, 20, 10) + path.line(16,20,33,20,110)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,110)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,110)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,110)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,110)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,110)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,110)

p1_r = path.point(24, 22, step)
p1_t = path.point(24, 18, step)

p2_r = path.point(25, 22, step)
p2_t = path.point(25, 18, step)

p3_r = path.point(26, 22, step)
p3_t = path.point(26, 18, step)

p4_r = path.point(27, 22, step)
p4_t = path.point(27, 18, step)

p5_r = path.point(28, 22, step)
p5_t = path.point(28, 18, step)

p6_r = path.point(29, 22, step)
p6_t = path.point(29, 18, step)



paths = [f1_r, f1_t, f2_r, f2_t, \
         p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t, p5_r, p5_t, p6_r, p6_t]
path.myplot(paths, 10, 40, 10, 30)


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







