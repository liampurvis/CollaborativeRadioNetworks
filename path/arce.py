from math import pi, hypot, sin, cos, atan2, degrees

def norm_angle(a):
    # Normalize the angle to be between -pi and pi
    return (a+pi)%(2*pi) - pi

x_0, y_0 = [400,500] # initial position of robot
theta_0 = -pi/2      # initial orientation of robot
step = 10
x_1, y_1 = [200,300] # goal position of robot

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


x = []
y = []
for i in range(step):
    x.append(x_C + r_C*sin(omega*(i) + theta_0))
    y.append(y_C + r_C*sin(omega*(i) + theta_0))

return x, y
