from Player import Player
from Player import Random
from Player import Random_Weights

from Player import CSMA
from Player import Thompsons, UCB, Thompsons_d

from core import env_core
import matplotlib.pyplot as plt
import numpy as np

#print(np.ones(5))

import pickle

import time

p1 = Random_Weights(id = 1, t_x = 1, t_y = 1, r_x = 1.1, r_y = 1.1, probs = [1,2,3,4,5,6,7], nb_channels=7)
p2 = Thompsons(id = 2, t_x = 1, t_y = 1, r_x = 1.1, r_y = 1.1, nb_channels = 7)
p3 = Thompsons_d(id = 3, t_x = 1, t_y = 1, r_x = 1.1, r_y = 1.1, nb_channels = 7)
p4 = Thompsons(id = 4, t_x = 1, t_y = 1, r_x = 1.1, r_y = 1.1, nb_channels = 7)
p5 = Thompsons_d(id = 5, t_x = 1, t_y = 1, r_x = 1.1, r_y = 1.1, nb_channels = 7)
p6 = Thompsons(id = 6, t_x = 1, t_y = 1, r_x = 1.1, r_y = 1.1, nb_channels = 7)
p7 = Thompsons_d(id = 7, t_x = 1, t_y = 1, r_x = 1.1, r_y = 1.1, nb_channels = 7)

env = env_core([p1, p2, p3, p4, p5, p6, p7])
before = time.time()

env.run_simulation(2000)
after = time.time()
print("total simulation time:"+  str(after - before))
env.save_results(filename = "/experiment_test_2/two_simulation.pkl")

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