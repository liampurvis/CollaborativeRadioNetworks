import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

f = open('SC2_jammer.txt','w')
F = 2
N = 6
step = 5000

cx, cy = 20, 20
r1 = 1  # center to jammer
r2 = 2  # center to rx
r3 = 10 # center to tx


# jammers
theta_1, theta_2 = 0, pi
f1_r = path.point(cx + r1 * sin(theta_1), cy + r1 * cos(theta_1), step)
f1_t = [(i[0]+0.1, i[1]+0.1) for i in f1_r]
f2_r = path.point(cx + r1 * sin(theta_2), cy + r1 * cos(theta_2), step)
f2_t = [(i[0]+0.1, i[1]+0.1) for i in f2_r]

# rx, tx
theta_3, theta_4, theta_5, theta_6, theta_7, theta_8 = 0, 2*pi/6, 4*pi/6, 6*pi/6, 8*pi/6, 10*pi/6
p1_r = path.point(cx + r2 * sin(theta_3), cy + r2 * cos(theta_3), step)
p1_t = path.point(cx + r3 * sin(theta_3), cy + r3 * cos(theta_3), step)
p2_r = path.point(cx + r2 * sin(theta_4), cy + r2 * cos(theta_4), step)
p2_t = path.point(cx + r3 * sin(theta_4), cy + r3 * cos(theta_4), step)
p3_r = path.point(cx + r2 * sin(theta_5), cy + r2 * cos(theta_5), step)
p3_t = path.point(cx + r3 * sin(theta_5), cy + r3 * cos(theta_5), step)
p4_r = path.point(cx + r2 * sin(theta_6), cy + r2 * cos(theta_6), step)
p4_t = path.point(cx + r3 * sin(theta_6), cy + r3 * cos(theta_6), step)
p5_r = path.point(cx + r2 * sin(theta_7), cy + r2 * cos(theta_7), step)
p5_t = path.point(cx + r3 * sin(theta_7), cy + r3 * cos(theta_7), step)
p6_r = path.point(cx + r2 * sin(theta_8), cy + r2 * cos(theta_8), step)
p6_t = path.point(cx + r3 * sin(theta_8), cy + r3 * cos(theta_8), step)

paths = [f1_r, f1_t, f2_r, f2_t, \
         p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t, p5_r, p5_t, p6_r, p6_t]
path.myplot(paths, 5, 35, 5, 35)



for ind in range((F+N)*2):
    paths[ind] = [("{0:.2f}".format(i[0]), "{0:.2f}".format(i[1])) for i in paths[ind]]

f.write(str(F) + '\n')
f.write(str(N) + '\n')
for i in range(step):
    for j in range(F+N):
        f.write('[')
        f.write('('+paths[2*j][i][0] + ',' + paths[2*j][i][1] + ')')
        f.write('('+paths[2*j+1][i][0] + ',' + paths[2*j+1][i][1] + ')')
        f.write(']')
    f.write('\n')
f.close()







