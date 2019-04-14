import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

f = open('SC2_incumbent.txt','w')
F = 1
N = 7
step = 1000


# increasing incumbent
in_r = path.point(4, 4, step)
in_t = path.point(4.01, 4.01, step)

# players
p1_r = path.point(3, 2, step)
p1_t = path.point(3.5, 3, step)

p2_r = path.point(5, 2, step)
p2_t = path.point(4.5, 3, step)

p3_r = path.point(6, 3, step)
p3_t = path.point(5, 3.5, step)

p4_r = path.point(6, 5, step)
p4_t = path.point(5, 4.5, step)

p5_r = path.point(4, 6, step)
p5_t = path.point(4, 5, step)

p6_r = path.point(2, 5, step)
p6_t = path.point(3, 4.5, step)

p7_r = path.point(2, 3, step)
p7_t = path.point(3, 3.5, step)

paths = [in_r, in_t, \
         p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t, p5_r, p5_t, p6_r, p6_t, p7_r, p7_t]
path.myplot(paths, 0, 8, 0, 8)



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







