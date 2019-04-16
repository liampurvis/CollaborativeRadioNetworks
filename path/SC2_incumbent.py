import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees


F = 1
N = 7
step = 5000


# increasing incumbent
in_r = path.point(6, 6, step)
in_t = path.point(6.01, 6.01, step)

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
path.myplot(paths, 0, 10, 0, 10)


path.myWrite('SC2_incumbent.txt', F, N, step, paths)







