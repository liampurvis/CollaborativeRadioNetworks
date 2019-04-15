import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

f = open('SC2_alleys.txt','w')
F = 0
N = 6
step = 5000

r = 3
moving_speed = 0.01
round = 6
rs1 = 1             # rotation speed
rs2 = 2
rs3 = 3

p1_r = path.point(12, 5, step)
p1_r = [(p1_r[i][0], p1_r[i][1]+moving_speed*i) for i in range(step)]

p1_t = path.circle(8, 8, rs3, 0, round*2*pi, 1, step);
p1_t = [(p1_t[i][0], p1_t[i][1]+moving_speed*i) for i in range(step)]

p2_r = path.point(10, 5, step)
p2_r = [(p2_r[i][0], p2_r[i][1]+moving_speed*i) for i in range(step)]

p2_t = path.circle(6, 8, rs3, 2*pi/3, round*2*pi, 1, step);
p2_t = [(p2_t[i][0], p2_t[i][1]+moving_speed*i) for i in range(step)]

p3_r = path.point(8, 5, step)
p3_r = [(p3_r[i][0], p3_r[i][1]+moving_speed*i) for i in range(step)]

p3_t = path.circle(4, 8, rs3, 4*pi/3, round*2*pi, 1, step);
p3_t = [(p3_t[i][0], p3_t[i][1]+moving_speed*i) for i in range(step)]

p4_r = path.point(11, 8, step)
p4_r = [(p4_r[i][0], p4_r[i][1]+moving_speed*i) for i in range(step)]

p4_t = path.circle(7, 11, rs3, 0, round*2*pi, 1, step);
p4_t = [(p4_t[i][0], p4_t[i][1]+moving_speed*i) for i in range(step)]

p5_r = path.point(13, 8, step)
p5_r = [(p5_r[i][0], p5_r[i][1]+moving_speed*i) for i in range(step)]

p5_t = path.circle(9, 11, rs3, 0, round*2*pi, 1, step);
p5_t = [(p5_t[i][0], p5_t[i][1]+moving_speed*i) for i in range(step)]

p6_r = path.point(15, 8, step)
p6_r = [(p6_r[i][0], p6_r[i][1]+moving_speed*i) for i in range(step)]

p6_t = path.circle(11, 11, rs3, 0, round*2*pi, 1, step);
p6_t = [(p6_t[i][0], p6_t[i][1]+moving_speed*i) for i in range(step)]

paths = [p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t, p5_r, p5_t, p6_r, p6_t]
path.myplot(paths, 0, 15, 1, moving_speed*step+30)



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







