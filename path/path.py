# location generate
from math import pi, hypot, sin, cos, atan2, degrees
import matplotlib.pyplot as plt
import random



def point(x, y, step):
    return [(x, y) for i in range(step)]

def randomPoint(x, y, mag, step):
    return [(x + mag*random.random() * cos(2*pi*random.random()), y + mag*random.random() * sin(2*pi*random.random())) for i in range(step)]


def line(sx, sy, ex, ey, step):
    difx = (ex-sx)/step
    dify = (ey-sy)/step
    return [(sx + i*difx, sy + i*dify) for i in range(1, step+1)]

def randomLine(sx, sy, ex, ey, mag, step):
    x_dir, y_dir = ex-sx, ey-sy
    length = (x_dir**2 + y_dir**2)**0.5
    normalVector_x = -y_dir/length
    normalVector_y = x_dir/length

    difx = (ex-sx)/step
    dify = (ey-sy)/step
    return [(sx + i*difx + normalVector_x*mag*random.random(), sy + i*dify + normalVector_y*mag*random.random()) for i in range(1, step+1)]

def randomStep(init, mag):
    return (init[0] + mag*sin(2*pi*random.random()), init[1] + mag*cos(2*pi*random.random()))

def randomWalk(init, step, mag, xmin, ymin, xmax, ymax):
    re = []
    last = init
    for i in range(step):
        cur = randomStep(last, mag)
        while cur[0] <= xmin or cur[0] >= xmax or cur[1] <= ymin or cur[1] >= ymax:
            cur = randomStep(last, mag)
        re.append(cur)
        last = cur
    return re

def circle(x, y, r, theta, angle, dir, step):
    cx, cy = x - r*sin(theta), y - r*cos(theta)
    omega = angle/step
    re = []
    for i in range(1, step+1):
        if dir == 1: # clockwise
            re.append(( cx + r*sin(theta + omega*(i)), cy + r*cos(theta + omega*(i))) )
        else:
            re.append(( cx + r*sin(theta - omega*(i)), cy + r*cos(theta - omega*(i))) )

    return re

def randomCircle(x, y, r, theta, angle, dir, mag, step):
    cx, cy = x - r*sin(theta), y - r*cos(theta)
    omega = angle/step
    re = []
    for i in range(1, step+1):
        if dir == 1: # clockwise
            re.append(( cx + (r+mag*random.random())*sin(theta + omega*(i)), cy + (r+mag*random.random())*cos(theta + omega*(i))) )
        else:
            re.append(( cx + r*mag*random.random()*sin(theta - omega*(i)), cy + r*mag*random.random()*cos(theta - omega*(i))) )
    return re


def myplot(paths, x1, x2, y1, y2):
    for p in paths:
        plt.plot([i[0] for i in p], [i[1] for i in p], marker=11)
    
    plt.legend([str(i//2)+"_r" if i%2==0 else str(i//2)+"_t" for i in range(len(paths))], loc=1)
    plt.xlim(x1,x2)
    plt.ylim(y1,y2)
    plt.show()

def myWrite(filename, F, N, step, paths):
    for ind in range((F+N)*2):
        paths[ind] = [("{0:.2f}".format(i[0]), "{0:.2f}".format(i[1])) for i in paths[ind]]
    f = open(filename,'w')
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

