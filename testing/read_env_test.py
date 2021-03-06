from Player import Player
from Player import Random
from core import env_core
import matplotlib.pyplot as plt
import numpy as np
import os


import pickle

p1 = Random(id = 666, t_x = 0, t_y = 0, r_x = 1, r_y = 1, prob = .5, random_walk = True)
p2 = Random(id = 420, t_x = -1, t_y = -1, r_x = 1, r_y = 1, prob = .5)
env = env_core([p1], time_refs=[0])
env.run_simulation(1000)
# t_walk = np.array(p1.previous_t_positions)
# r_walk = np.array(p1.previous_r_positions)



# def save_object(obj, filename):
#     with open(filename, 'wb') as output:  # Overwrites any existing file.
#         pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

# os.makedirs("saved/objects/", exist_ok=True) 
# save_object(p1, "saved/objects/location_test.pkl")

env.save_environment()


env.displayGif()
# plt.plot(t_walk[:, 0], t_walk[:, 1], label="transmitter")
# plt.plot(r_walk[:, 0], r_walk[:, 1], label= "reciever")
# plt.legend(loc='upper left')
# plt.title("Random Walk of Transmitter and Reciever")
# plt.ylabel("Longitude")
# plt.xlabel("Latitude")
# plt.show()