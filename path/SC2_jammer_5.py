import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

f = open('SC2_jammer_5.txt','w')
N = 8
step = 500

cx, cy = 20, 20
r1 = 2  # center to jammer
r2 = 4  # center to rx
r3 = 10 # center to tx


# jammers
theta_1, theta_2, theta_3 = 0, 2*pi/3, 4*pi/3
p1_r = path.point(cx + r1 * cos(theta_1), cy + r1 * sin(theta_1), step)
p1_t = [(i[0]+0.1, i[1]+0.1) for i in p1_r]
p2_r = path.point(cx + r1 * cos(theta_2), cy + r1 * sin(theta_2), step)
p2_t = [(i[0]+0.1, i[1]+0.1) for i in p2_r]
p3_r = path.point(cx + r1 * cos(theta_3), cy + r1 * sin(theta_3), step)
p3_t = [(i[0]+0.1, i[1]+0.1) for i in p3_r]

# rx, tx
theta_4, theta_5, theta_6, theta_7, theta_8 = 0, 2*pi/5, 4*pi/5, 6*pi/5, 8*pi/5
p4_r = path.point(cx + r2 * cos(theta_4), cy + r2 * sin(theta_4), step)
p4_t = path.point(cx + r3 * cos(theta_4), cy + r3 * sin(theta_4), step)
p5_r = path.point(cx + r2 * cos(theta_5), cy + r2 * sin(theta_5), step)
p5_t = path.point(cx + r3 * cos(theta_5), cy + r3 * sin(theta_5), step)
p6_r = path.point(cx + r2 * cos(theta_6), cy + r2 * sin(theta_6), step)
p6_t = path.point(cx + r3 * cos(theta_6), cy + r3 * sin(theta_6), step)
p7_r = path.point(cx + r2 * cos(theta_7), cy + r2 * sin(theta_7), step)
p7_t = path.point(cx + r3 * cos(theta_7), cy + r3 * sin(theta_7), step)
p8_r = path.point(cx + r2 * cos(theta_8), cy + r2 * sin(theta_8), step)
p8_t = path.point(cx + r3 * cos(theta_8), cy + r3 * sin(theta_8), step)



paths = [p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, \
         p4_r, p4_t, p5_r, p5_t, p6_r, p6_t, p7_r, p7_t, p8_r, p8_t]

path.myplot(paths)



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
            






