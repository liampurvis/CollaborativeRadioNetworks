# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 14:08:20 2019

@author: Alexandre
"""

from Player import Player
from core import env_core

p1 = Player(-1,1,1,-1)
p2 = Player(-1,-1,1,1)
p2.set_channel(1050,1060)
p3 = Player(-2,0,2,0)

env = env_core([p1, p2, p3])

env.run_simulation()