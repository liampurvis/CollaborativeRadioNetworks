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


"""
def norm_angle(a):
    # Normalize the angle to be between -pi and pi
    return (a+pi)%(2*pi) - pi

def arce(sx, sy, ex, ey, step, orient):
    x_0, y_0 = [sx, sy] # initial position of robot
    theta_0 = orient      # initial orientation of robot
    x_1, y_1 = [ex, ey] # goal position of robot

    # To be computed:
    r_G = hypot(x_1 - x_0, y_1 - y_0)        # relative polar coordinates of the goal
    phi_G = atan2(y_1 - y_0, x_1 - x_0)
    phi = 2*norm_angle(phi_G - theta_0)      # angle and
    r_C = r_G/(2*sin(phi_G - theta_0))       # radius (sometimes negative) of the arc
    L = r_C*phi                              # length of the arc
    if phi > pi:
        phi -= 2*pi
        L = -r_C*phi
    elif phi < -pi:
        phi += 2*pi
        L = -r_C*phi
    omega = phi/step                         # angular velocity
    x_C = x_0 - r_C*sin(theta_0)             # center of rotation
    y_C = y_0 + r_C*cos(theta_0)


    re = []
    for i in range(1,step+1):
        re.append( ( x_C + r_C*sin(omega*(i) + theta_0), y_C - r_C*cos(omega*(i) + theta_0)) )
    return re

"""


def myplot(paths, x1, x2, y1, y2):
    for p in paths:
        plt.plot([i[0] for i in p], [i[1] for i in p], marker=11)
    
    plt.legend([str(i//2)+"_r" if i%2==0 else str(i//2)+"_t" for i in range(len(paths))], loc=1)
    plt.xlim(x1,x2)
    plt.ylim(y1,y2)
    plt.show()

