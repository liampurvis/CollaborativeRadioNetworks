import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

f = open('SC2_alleys.txt','w')
N = 3
step = 2000

r = 3
moving_speed = 0.01
round = 3
rs1 = 1             # rotation speed
rs2 = 2
rs3 = 3

p1_r = path.point(12, 5, step)
p1_r = [(p1_r[i][0], p1_r[i][1]+moving_speed*i) for i in range(step)]

p1_t = path.circle(8, 8, 3, 0, round*2*pi, 1, step);
p1_t = [(p1_t[i][0], p1_t[i][1]+moving_speed*i) for i in range(step)]

p2_r = path.point(10, 5, step)
p2_r = [(p2_r[i][0], p2_r[i][1]+moving_speed*i) for i in range(step)]

p2_t = path.circle(6, 8, 3, 2*pi/3, round*2*pi, 1, step);
p2_t = [(p2_t[i][0], p2_t[i][1]+moving_speed*i) for i in range(step)]

p3_r = path.point(8, 5, step)
p3_r = [(p3_r[i][0], p3_r[i][1]+moving_speed*i) for i in range(step)]

p3_t = path.circle(4, 8, 3, 4*pi/3, round*2*pi, 1, step);
p3_t = [(p3_t[i][0], p3_t[i][1]+moving_speed*i) for i in range(step)]



paths = [p1_r, p1_t, p2_r, p2_t, p3_r, p3_t]
path.myplot(paths, 0, 15, 1, moving_speed*step+30)



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







