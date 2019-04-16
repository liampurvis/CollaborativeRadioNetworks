import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

F = 2
N = 7
step = 625*8


f1_r = path.point(30, 15, step)
f2_r = path.point(31, 15, step)

f1_t = path.point(18, 20, 10) + path.line(18,20,35,20,615)      \
        + path.point(18, 20, 10) + path.line(18,20,35,20,615)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,615)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,615)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,615)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,615)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,615)   \
        + path.point(18, 20, 10) + path.line(18,20,35,20,615)

f2_t = path.point(16, 20, 10) + path.line(16,20,33,20,615)      \
        + path.point(16, 20, 10) + path.line(16,20,33,20,615)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,615)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,615)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,615)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,615)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,615)   \
        + path.point(16, 20, 10) + path.line(16,20,33,20,615)

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

p7_r = path.point(30, 22, step)
p7_t = path.point(30, 18, step)


paths = [f1_r, f1_t, f2_r, f2_t, \
         p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t, p5_r, p5_t, p6_r, p6_t, p7_r, p7_t]
path.myplot(paths, 10, 40, 10, 30)


path.myWrite('SC2_wildfire.txt', F, N, step, paths)






