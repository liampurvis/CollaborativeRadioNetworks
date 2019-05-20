# -*- coding: utf-8 -*-
"""


"""

from Player import Player
from Player import Random
from Player import CSMA
from core import env_core
import matplotlib.pyplot as plt
import numpy as np

# FIRST PART
# dist(t0, r1) < 1/sqrt(2)=0.7071
# even if there is a switch at half the time, the noise power is more than double the signal power during the
# transition period
# so the average SNR is slightly less than 1
p0 = Player(0, 0.70, 0, 0, 0)
p1 = Player(1, 1, 0, 0, 0)
env = env_core([p0, p1], time_refs = [9, 4])

env.run_simulation(10)
env.players[0].set_channel(1030, 5)
env.players[0].blocker_counter = 0
env.run_simulation(10)
env.displayResults()

# SECOND PART
# dist(t0, r1) > 1/sqrt(2)=0.7071
# since there is a switch at half the time, the noise power is now slightly less than double the signal power during
# the transition period
# so the average SNR is slightly more than 1
p0 = Player(0, 0.71, 0, 0, 0)
p1 = Player(1, 1, 0, 0, 0)
env = env_core([p0, p1], time_refs = [9, 4])

env.run_simulation(10)
env.players[0].set_channel(1030, 5)
env.players[0].blocker_counter = 0
env.run_simulation(10)
env.displayResults()

# SAME EXAMPLE with 1/3 of overlap
# Now the noise power must be three times bigger than signal to get SNR < 1 on the transition period
# So the distance must be less than 1/sqrt(3)=0.5774
# p0 = Player(0, 0.57, 0, 0, 0)
# p1 = Player(1, 1, 0, 0, 0)
# env = env_core([p0, p1], time_refs = [5, 3])
# env.TIME_REFERENCE_UNIT = 6
#
# env.run_simulation(10)
# env.players[0].set_channel(1030, 5)
# env.players[0].blocker_counter = 0
# env.run_simulation(10)
# env.displayResults()
#
# p0 = Player(0, 0.58, 0, 0, 0)
# p1 = Player(1, 1, 0, 0, 0)
# env = env_core([p0, p1], time_refs = [5, 3])
# env.TIME_REFERENCE_UNIT = 6
#
# env.run_simulation(10)
# env.players[0].set_channel(1030, 5)
# env.players[0].blocker_counter = 0
# env.run_simulation(10)
# env.displayResults()