# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 14:08:20 2019

@author: Alexandre
"""

from Player import Player
from Player import Random
from core import env_core
import matplotlib.pyplot as plt
import numpy as np

test_random_walk = True
# if we are testing random walk
if test_random_walk:
    p1 = Random(id = -666, t_x = 0, t_y = 0, r_x = 1, r_y = 1, prob = .5, random_walk = True)
    p2 = Random(id = 420, t_x = -1, t_y = -1, r_x = 1, r_y = 1, prob = .5)
    env = env_core([p1, p2])
    env.run_simulation(1000)
    t_walk = np.array(p1.previous_t_positions)
    r_walk = np.array(p1.previous_r_positions)
    plt.plot(t_walk[:, 0], t_walk[:, 1], label="transmitter")
    plt.plot(r_walk[:, 0], r_walk[:, 1], label= "reciever")
    plt.legend(loc='upper left')
    plt.title("Random Walk of Transmitter and Reciever")
    plt.ylabel("Longitude")
    plt.xlabel("Latitude")
    plt.show()

else:
    p1 = Player(-1,1,1,-1)
    p2 = Random(-1,-1,1,1, .5)

    env = env_core([p1, p2])

    print("First steps")
    env.run_simulation(5)
    env.players[1].set_channel(1060,1070)
    print("After changing settings")
    env.run_simulation(20)