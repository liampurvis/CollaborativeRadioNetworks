# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 14:08:20 2019

Author: Ulysses
"""

"""
Here we create 3 players: 
1. one normal player (which will not self-switch channel or do anything other than
   transmitting unless manully commanded)

2. one CSMA player in 1-persistent mode, never sleep, attempt to seize channal the first
   opportunity it has

3. another CSMA player in p-persistent mode, sleep for certain amount of time, and only try
   try seize channel with a p probability. 

Current limitation: it take a extra one timestamp for CSMA players to swith states, so there's a small
delay before one can truly start trying to seize the channel. Not a big deal, but on list of improvement
in the future. 
"""

from Player import Player
from Player import Random
from Player import CSMA
from core import env_core
import matplotlib.pyplot as plt
import numpy as np

p1 = Player(0,-1,0,1,0)
p2 = CSMA(1,1.01,0,-1.01,0, 0.3, 0, 1.0)
p3 = CSMA(2,0.99,0,-1.01,0, 0.3, 3, 0.5)
# p4 = CSMA(3,1.02,0,-1.01,0, 0.5, 0, 0.5)

# env = env_core([p1, p2], time_refs = [2,4])
env = env_core([p1, p2, p3], time_refs = [2,4,6])

env.run_simulation(5)
# env.players[1].set_channel(1060,5)
# env.run_simulation(10)
env.players[0].set_channel(1060,5)
env.run_simulation(10)
env.players[1].set_channel(1060,5)
env.run_simulation(20)

env.displayResults()
