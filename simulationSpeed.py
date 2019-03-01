# -*- coding: utf-8 -*-
"""
This file evaluates the time performance of the core environment with static players
"""

from Player import Player
from core import env_core
import numpy as np
import random
import time

players = []

MAX_NB_PLAYERS = 10
NB_SIMULATIONS = 50
NB_STEPS = 1000

nb_steps_executed = 0


# generates players at random positions & freq
for i in range(MAX_NB_PLAYERS):
    players.append(Player(i, np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand()))
    players[i].set_channel(np.random.rand()*100+1000) #random channel between 1000 and 1100
    players[i].blocker_counter = 0

before = time.time()
for n in range(NB_SIMULATIONS):
    print("Simulation n°" + str(n))
    env_time_step = np.random.randint(1, 15)
    nb_players = random.randint(2, 10)
    time_distribution = [random.randint(0, env_time_step) for i in range(nb_players)]
    env = env_core(random.sample(players, k=nb_players), nb_steps=NB_STEPS, time_refs=time_distribution)
    env.TIME_REFERENCE_UNIT = env_time_step

    env.run_simulation(NB_STEPS)
    nb_steps_executed += env.curr_step

after = time.time()
total_time = after-before
print("Total number of steps = " + str(nb_steps_executed))
print("Total time = " + str(total_time) + "s")
print("Number of time steps (from player point of view) = " + str(NB_STEPS))
print("Average time per simulation = " + str(np.trunc(total_time/NB_SIMULATIONS*1000)) + "ms")