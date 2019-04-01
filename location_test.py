from Player import Player
from Player import Random
from Player import CSMA
from Player import Thompsons, UCB

from core import env_core
import matplotlib.pyplot as plt
import numpy as np

#print(np.ones(5))

import pickle

import time

p1 = Thompsons(id = 1, t_x = -1, t_y = -1, r_x = 1, r_y = 1, starting_frequency = 1085)
p2 = CSMA(id = 2, t_x = -1, t_y = -1, r_x = 1, r_y = 1, threshold_input = 1, sleeping_input = 3, aggression_prob = 1, starting_frequency = 1015)
p3 = Random(id = 3, t_x = -1, t_y = -1, r_x = 1, r_y = 1)
p4 = UCB(id = 4, t_x = -1, t_y = -1, r_x = 1, r_y = 1)

env = env_core([p1, p2, p3, p4])
before = time.time()

env.run_simulation(1000)
after = time.time()
print("total simulation time:"+  str(after - before))

#print(p1.previous_successes)

"""
def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


save_object(p1, "saved/objects/location_test.pkl")
t_walk = np.array(p1.previous_t_positions)
r_walk = np.array(p1.previous_r_positions)

plt.plot(t_walk[:, 0], t_walk[:, 1], label="transmitter")
plt.plot(r_walk[:, 0], r_walk[:, 1], label= "reciever")
plt.legend(loc='upper left')
plt.title("Random Walk of Transmitter and Reciever")
plt.ylabel("Longitude")
plt.xlabel("Latitude")
plt.show()
"""