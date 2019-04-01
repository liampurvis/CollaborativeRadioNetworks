# location generate
from math import pi, hypot, sin, cos, atan2, degrees
import matplotlib.pyplot as plt




def point(x, y, step):
    return [(x, y) for i in range(step)]


def line(sx, sy, ex, ey, step):
    difx = (ex-sx)/step
    dify = (ey-sy)/step
    return [(sx + i*difx, sy + i*dify) for i in range(1, step+1)]


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




def myplot(paths):
    for p in paths:
        plt.plot([i[0] for i in p], [i[1] for i in p], marker=11)
    plt.show()

