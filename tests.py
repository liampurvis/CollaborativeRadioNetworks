# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 14:08:20 2019

@author: Alexandre
"""

from Player import Player
from core import env_core

p1 = Player(-1,1,1,-1)
p2 = Player(-1,-1,1,1)

env = env_core([p1, p2])

print("First steps")
env.run_simulation(5)
env.players[1].set_channel(1060,1070)
print("After changing settings")
env.run_simulation(20)