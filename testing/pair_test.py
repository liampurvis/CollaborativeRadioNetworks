# testing case for determining the power accumulation when several node-pairs are trying to talk
import sys

# append files in utility folder to use in testing
sys.path.append('../utility/')

import fsl

# free_space = fsl.free_space_loss( (1, 0), (0, 0), 0, 0, 5, ("km", "GHz") )
# print(free_space)

# Testing methodology:
#
# I want to first create a location matrix detailing where each node are. 
# For a simple case, the row & column value is there location; 0 = no node, 1 = transmit node, 2 = receive node
#
# Then we also have a dict to store all the communication i.e. ((1,2), (3,4)) means node at (1,2) will
# try to send to node at (3,4) all the time
#
# Then another dict to store all the information related to communication, e.g. power, frequency, etc.
#
# For a simple case testing, I will assume one transmission, and see how the power-overlap functions.
# I'll also assume some naive models to determine the cut-off power ratio of which transmission is lost. 