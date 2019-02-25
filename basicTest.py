"""
Created on Sun Feb 24 22:19:2018

@author: Sean

Testing simple environment and logfile 

"""
from Player import Player
from core import env_core
import os
import logging 

f = open("logfile.log", "w")
LOG_FILENAME = "logfile.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

#1. close position, then changes freq
logging.debug("start simulation")
p1 = Player(1,0,0,1,1)
p2 = Player(2,1.1,1.1,3,3)

env = env_core([p1, p2], time_refs=[0,0])
env.run_simulation(5)


env.players[0].set_channel(2000,5)
env.run_simulation(20)





logging.debug("end simulation")
