"""
Created on Sun Feb 24 22:19:2018

@author: Sean

Testing simple environment and logfile 

"""

import sys, os
sys.path.append(os.getcwd()+'/..')
sys.path.append(os.getcwd()+'/../visualization')
import datetime as dt
from Player import Player
from core import env_core
import logging
from gifGen import gif


mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)
f = open("logfile.log", "w")
LOG_FILENAME = "logfile.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

#1. close position, then changes freq
logging.debug("start simulation")
p1 = Player(1,0,0,1,1)
p2 = Player(2,1.1,1.1,3,3)


startTime = dt.datetime.now()
env = env_core([p1, p2], time_refs=[0,0])
env.run_simulation(1)


env.players[0].set_channel(2000,5)
env.run_simulation(2)

env.players[1].update_location(3,4,2,1)
env.run_simulation(3)




endTime = dt.datetime.now()
logging.debug("end simulation")
logging.debug("Simulation period : " + str((endTime - startTime).total_seconds()) + " s")

f.close()

env.displayGif()
