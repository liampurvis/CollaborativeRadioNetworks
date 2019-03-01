# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 14:08:20 2019

@author: Alexandre
"""

from Player import Player
from Player import Random
from Player import CSMA
from core import env_core
import matplotlib.pyplot as plt
import numpy as np

p1 = Player(0,-1,0,1,0)
p2 = Player(1,1.01,0,-1.01,0)
p3 = Player(2, -0.5, -0.5, 0.5, 0.5)

env = env_core([p1, p2, p3], time_refs = [2,6,0])

env.players[2].set_channel(1030, 5)
env.players[2].blocker_counter = 0

env.run_simulation(5)
env.players[1].set_channel(1060,5)
env.run_simulation(10)
env.players[0].set_channel(1060,5)
env.run_simulation(10)

env.displayResults()
