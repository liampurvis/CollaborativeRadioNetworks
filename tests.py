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




p1 = Player(-1,1,1,-1)
p2 = Random(-1,-1,1,1, .5)

env = env_core([p1, p2], time_refs = [2,6])

print("First steps")
env.run_simulation(5)
env.players[1].set_channel(1060,5)
print("After changing settings")
env.run_simulation(20)
