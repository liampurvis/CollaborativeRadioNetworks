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

NB_CHANNELS = 2
p1 = Player(0,-1,0,1,0)
p2 = UCB(1, -10, 0, 10, 0, nb_channels=NB_CHANNELS)

#p1 is on the same channel as p2
p1.set_channel(p1.min_frequency + (p1.max_frequency-p1.min_frequency)*0.5/NB_CHANNELS, (p1.max_frequency-p1.min_frequency)*0.5/NB_CHANNELS)
p1.blocker_counter = 0
env = env_core([p1, p2], time_refs = [2,4])

env.run_simulation(200)

env.displayResults()
