# -*- coding: utf-8 -*-
"""
"""

"""
DESCRIPTION
"""

from Player import Player
from Player import Random
from Player import CSMA
from Player import UCB
from core import env_core
import matplotlib.pyplot as plt
import numpy as np


## THIS IS A DEMO WITH FIXED PLAYER
# NB_CHANNELS = 10
# p1 = Player(0,-1,0,1,0)
# p2 = UCB(1, -10, 0, 10, 0, nb_channels=NB_CHANNELS, lamda=0.7)
#
# #p1 is on the same channel as p2
# p1.set_channel(p1.min_frequency + (p1.max_frequency-p1.min_frequency)*0.5/NB_CHANNELS, (p1.max_frequency-p1.min_frequency)*0.5/NB_CHANNELS)
# p1.blocker_counter = 0
# env = env_core([p1, p2], time_refs = [2,4])
#
# env.run_simulation(50)
# env.players[0].set_channel(1015,5)
# env.run_simulation(30)
# env.players[0].set_channel(1025,5)
# env.run_simulation(30)
#
#
# env.displayResults()
# env.players[1].displayEstimatedProbs()



##THIS IS A DEMO WITH A RANDOM PLAYER
# NB_CHANNELS = 10
p1 = Random(0,-1,0,1,0, prob=0.03)
p2 = UCB(1, -10, 0, 10, 0, nb_channels=NB_CHANNELS, lamda=0.7)

#p1 is on the same channel as p2
p1.set_channel(p1.min_frequency + (p1.max_frequency-p1.min_frequency)*0.5/NB_CHANNELS, (p1.max_frequency-p1.min_frequency)*0.5/NB_CHANNELS)
p1.blocker_counter = 0
env = env_core([p1, p2], time_refs = [2,4])

env.run_simulation(1000)

env.displayResults()
env.players[1].displayEstimatedProbs()
