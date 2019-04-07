# -*- coding: utf-8 -*-
"""
This file evaluates the time performance of the core environment with static players
"""

from Player import Player
from Player import Random
from Player import CSMA
from Player import UCB
from Player import Thompsons
from core import env_core
import numpy as np
import random
import time

players = []

MAX_NB_PLAYERS = 10
NB_SIMULATIONS = 50
NB_STEPS = [2000, 5000]

nb_steps_executed = 0


# generates players at random positions & freq
for i in range(MAX_NB_PLAYERS):
    players.append(Player(i, np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand()))
    players.append(Random(i, np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand(), random_walk = False))
    players.append(CSMA(i, np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand(), threshold_input = 0.1, sleeping_input = 0, aggression_prob = 1))
    players.append(UCB(i, np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand(), lamda = 0.7))
    players.append(Thompsons(i, t_x=np.random.rand(), t_y=np.random.rand(), r_x=np.random.rand(), r_y=np.random.rand()))

for i in range(len(players)):
    players[i].set_channel(central = np.random.rand()*100+1000) #random channel between 1000 and 1500
    players[i].blocker_counter = 0

for it in NB_STEPS:
    before = time.process_time()
    nb_steps_executed = 0
    for n in range(NB_SIMULATIONS):
        print("Simulation n°" + str(n))
        env_time_step = np.random.randint(1, 15)
        nb_players = random.randint(6,9)
        time_distribution = [random.randint(0, env_time_step) for i in range(nb_players)]
        env = env_core(random.sample(players, k=nb_players), nb_steps=it, time_refs=time_distribution)
        env.TIME_REFERENCE_UNIT = env_time_step

        env.run_simulation(it)
        nb_steps_executed += env.curr_step

    after = time.process_time()
    total_time = after-before
    print("Total number of steps = " + str(nb_steps_executed))
    print("Total time = " + str(total_time) + "s")
    print("Number of time steps (from player point of view) = " + str(it))
    print("Average time per simulation = " + str(np.trunc(total_time/NB_SIMULATIONS)) + "s")