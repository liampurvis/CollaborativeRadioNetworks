import path
import os
import sys
from math import pi, hypot, sin, cos, atan2, degrees

# one point
f = open('one.txt','w')
N = 2
step = 200

p1_r = path.point(5,5,200)
p1_t = path.point(6,6,200)
p2_r = path.point(5,6,200)
p2_t = path.point(6,7,200)

paths = [p1_r, p1_t, p2_r, p2_t]

"""
# four overlap circles
f = open('circle.txt','w')
N = 4
step = 5000

p1_r = path.point(5,5,5000)
p1_t = path.point(5,1,1) + path.circle(5,1,4,pi,100*pi,1,4999)
p2_r = path.point(11,5,5000)
p2_t = path.point(11,1,1) + path.circle(11,1,4,pi,100*pi,0,4999)
p3_r = path.point(11,11,5000)
p3_t = path.point(11,15,1) + path.circle(11,15,4,0,100*pi,1,4999)
p4_r = path.point(5,11,5000)
p4_t = path.point(5,15,1) + path.circle(5,15,4,0,100*pi,0,4999)

paths = [p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t]

"""
"""
# moving far away and back
f = open('moving.txt','w')
N = 1
step = 100

p1_r = path.point(3,5,100)
p1_t = path.point(5,5,1) + path.line(5,5,500,5,50) + path.line(500,5,5,5,49)

paths = [p1_r, p1_t]
"""


"""
# squeeze and diverge
f = open('squeeze.txt','w')
N = 8
step = 200
mag = 0.1;
p1_r = path.randomPoint(2,2,mag,1) + path.randomLine(2,2,4,4,mag,100) + path.randomLine(4,4,2,2,mag,99)
p1_t = path.randomPoint(2,2,mag,1) + path.randomLine(2,2,4,4,mag,100) + path.randomLine(4,4,2,2,mag,99)
p2_r = path.randomPoint(2,2,mag,1) + path.randomLine(2,2,4,4,mag,100) + path.randomLine(4,4,2,2,mag,99)
p2_t = path.randomPoint(2,2,mag,1) + path.randomLine(2,2,4,4,mag,100) + path.randomLine(4,4,2,2,mag,99)

p3_r = path.randomPoint(2,6,mag,1) + path.randomLine(2,6,4,4,mag,100) + path.randomLine(4,4,2,6,mag,99)
p3_t = path.randomPoint(2,6,mag,1) + path.randomLine(2,6,4,4,mag,100) + path.randomLine(4,4,2,6,mag,99)
p4_r = path.randomPoint(2,6,mag,1) + path.randomLine(2,6,4,4,mag,100) + path.randomLine(4,4,2,6,mag,99)
p4_t = path.randomPoint(2,6,mag,1) + path.randomLine(2,6,4,4,mag,100) + path.randomLine(4,4,2,6,mag,99)

p5_r = path.randomPoint(6,6,mag,1) + path.randomLine(6,6,4,4,mag,100) + path.randomLine(4,4,6,6,mag,99)
p5_t = path.randomPoint(6,6,mag,1) + path.randomLine(6,6,4,4,mag,100) + path.randomLine(4,4,6,6,mag,99)
p6_r = path.randomPoint(6,6,mag,1) + path.randomLine(6,6,4,4,mag,100) + path.randomLine(4,4,6,6,mag,99)
p6_t = path.randomPoint(6,6,mag,1) + path.randomLine(6,6,4,4,mag,100) + path.randomLine(4,4,6,6,mag,99)


p7_r = path.randomPoint(6,2,mag,1) + path.randomLine(6,2,4,4,mag,100) + path.randomLine(4,4,6,2,mag,99)
p7_t = path.randomPoint(6,2,mag,1) + path.randomLine(6,2,4,4,mag,100) + path.randomLine(4,4,6,2,mag,99)
p8_r = path.randomPoint(6,2,mag,1) + path.randomLine(6,2,4,4,mag,100) + path.randomLine(4,4,6,2,mag,99)
p8_t = path.randomPoint(6,2,mag,1) + path.randomLine(6,2,4,4,mag,100) + path.randomLine(4,4,6,2,mag,99)


paths = [p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t, p5_r, p5_t, p6_r, p6_t, p7_r, p7_t, p8_r, p8_t]
"""

"""
# center versus around
f = open("./center.txt","w")
N = 4
step = 1000
mag = 0.2
# center
p1_r = path.point(7.9,7.9,1000)
p1_t = path.point(7.8,7.8,1000)
p2_r = path.point(8,8,1000)
p2_t = path.point(8.1,8.1,1000)
# around
p3_r = path.point(8,10,1) + path.randomCircle(8,10,2,0,8*pi,1,mag,999)
#p3_t = path.point(8.1,10.1,1) + path.randomCircle(8,10,2,0,4*pi,1,mag,99)
p3_t = [(i[0]+0.1, i[1]+0.1) for i in p3_r]
p4_r = path.point(8,6,1) + path.randomCircle(8,6,2,pi,8*pi,1,mag,999)
p4_t = [(i[0]+0.1, i[1]+0.1) for i in p4_r]

paths = [p1_r, p1_t, p2_r, p2_t, p3_r, p3_t, p4_r, p4_t]
"""

path.myplot(paths)

for ind in range(N*2):
    paths[ind] = [("{0:.2f}".format(i[0]), "{0:.2f}".format(i[1])) for i in paths[ind]]



f.write(str(N) + '\n')
for i in range(step):
    #print (i)
    for j in range(N):
        f.write('[')
        f.write('('+paths[2*j][i][0] + ',' + paths[2*j][i][1] + ')')
        f.write('('+paths[2*j+1][i][0] + ',' + paths[2*j+1][i][1] + ')')
        f.write(']')
    f.write('\n')

f.close()
            






