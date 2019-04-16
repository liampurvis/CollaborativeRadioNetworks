import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees


F = 0
N = 7
step = 5000
mag = 0.5
bound = 20



p1_r = path.randomWalk((5, 5), step, mag, 1, 1, bound, bound)
p1_t = path.randomWalk((6, 6), step, mag, 1, 1, bound, bound)
p2_r = path.randomWalk((7, 5), step, mag, 1, 1, bound, bound)
p2_t = path.randomWalk((8, 6), step, mag, 1, 1, bound, bound)
p3_r = path.randomWalk((1, 5), step, mag, 1, 1, bound, bound)
p3_t = path.randomWalk((2, 6), step, mag, 1, 1, bound, bound)
p4_r = path.randomWalk((3, 5), step, mag, 1, 1, bound, bound)
p4_t = path.randomWalk((4, 6), step, mag, 1, 1, bound, bound)
p5_r = path.randomWalk((3, 1), step, mag, 1, 1, bound, bound)
p5_t = path.randomWalk((4, 2), step, mag, 1, 1, bound, bound)
p6_r = path.randomWalk((3, 7), step, mag, 1, 1, bound, bound)
p6_t = path.randomWalk((4, 8), step, mag, 1, 1, bound, bound)
p7_r = path.randomWalk((3, 2), step, mag, 1, 1, bound, bound)
p7_t = path.randomWalk((4, 1), step, mag, 1, 1, bound, bound)

paths = [p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t, p5_r, p5_t, p6_r, p6_t, p7_r, p7_t]
path.myplot(paths, 0, bound+1, 0, bound+1)


path.myWrite('SC2_randomWalk.txt', F, N, step, paths)






