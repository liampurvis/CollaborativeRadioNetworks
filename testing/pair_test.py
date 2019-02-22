# testing case for determining the power accumulation when several node-pairs are trying to talk
import sys

# append files in utility folder to use in testing
sys.path.append('../utility/')

import fsl
import numpy as np
from collections import namedtuple

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

node_matrix = np.zeros((5, 5))
node_matrix[0, 0] = 1
node_matrix[4, 3] = 1
node_matrix[4, 4] = 2
print(node_matrix)

comm_pairs = {}
comm_pairs[(0,0)] = (4,4)
comm_pairs[(4,3)] = (4,4)
print(comm_pairs)

comm_info = {}
comm_info[(0,0)] = (10, 1)     # (power, frequency)  Consider adding more info in the future
comm_info[(4,3)] = (100, 1)

threshold = 10   # If background power is this amount of factor than communication, we lose that communication

# The most simple case testing: total collision (frequency doesn't matter)

iter_num = 0
iter_max = 1

while iter_num < iter_max:
	iter_num += 1
	for src, dest in comm_pairs.items():
		print("Iteration # %d, Source: %s, Dest: %s" % (iter_num, (src, ), (dest, ))) # Know that which pair of src and dest
		this_pwr = int(comm_info[src][0])
		print("Relevant power is %d" % this_pwr)
		noise_from_comm = 0.0
		for other_src, pwrs in comm_info.items():   # Determine how much power is generated from other ongoing communcation
			if other_src != src:
				print("Other src %s" % (other_src,))
				noise_pwr = pwrs[0]          # Scale that power from other ongoing comm by the distance
				dist_noise = fsl.distance_2(dest, other_src)
				print("Noise at distance %f" % dist_noise)
				noise_from_comm += noise_pwr / (dist_noise**2)

		print("Power from other comm is %f" % noise_from_comm)
		if noise_from_comm >= threshold * this_pwr:
			print("This comm is overpowered by other comms")
		else:
			print("This comm can be heard normally")

print("---------------------------------------------------")

comm_info[(0,0)] = (100, 1)
comm_info[(4,3)] = (100, 1)

iter_num = 0

while iter_num < iter_max:
	iter_num += 1
	for src, dest in comm_pairs.items():
		print("Iteration # %d, Source: %s, Dest: %s" % (iter_num, (src, ), (dest, ))) # Know that which pair of src and dest
		this_pwr = int(comm_info[src][0])
		print("Relevant power is %d" % this_pwr)
		noise_from_comm = 0.0
		for other_src, pwrs in comm_info.items():   # Determine how much power is generated from other ongoing communcation
			if other_src != src:
				print("Other src %s" % (other_src,))
				noise_pwr = pwrs[0]          # Scale that power from other ongoing comm by the distance
				dist_noise = fsl.distance_2(dest, other_src)
				print("Noise at distance %f" % dist_noise)
				noise_from_comm += noise_pwr / (dist_noise**2)

		print("Power from other comm is %f" % noise_from_comm)
		if noise_from_comm >= threshold * this_pwr:
			print("This comm is overpowered by other comms")
		else:
			print("This comm can be heard normally")


# Then we consider the case where there's partial overlap on channel
# So that preceived power might only be portion of projected power
#
# Let's use a naive model where it's direct percentage of overlap
#
# Also assume that frequency in comm_info is the central frequency, 
# and say that from central frequency each covers +- 5 around them

print("---------------------------------------------------")

comm_info[(0,0)] = (100, 100)
comm_info[(4,3)] = (10, 100)

iter_num = 0

Range = namedtuple('Range', ['start', 'end'])

while iter_num < iter_max:
	iter_num += 1
	for src, dest in comm_pairs.items():
		print("Iteration # %d, Source: %s, Dest: %s" % (iter_num, (src, ), (dest, ))) # Know that which pair of src and dest
		this_pwr = int(comm_info[src][0])
		this_freq_range = comm_info[src][1]
		print("Relevant power is %d" % this_pwr)
		noise_from_comm = 0.0
		r_this = Range(this_freq_range - 5, this_freq_range + 5)
		for other_src, infos in comm_info.items():   # Determine how much power is generated from other ongoing communcation
			if other_src != src:
				print("Other src %s" % (other_src,))
				noise_pwr = infos[0]          # Scale that power from other ongoing comm by the distance
				noise_freq_range = infos[1]
				dist_noise = fsl.distance_2(dest, other_src)

				r_noise = Range(noise_freq_range-5, noise_freq_range+5)

				latest_start = max(r_this.start, r_noise.start)
				earliest_end = min(r_this.end, r_noise.end)
				delta = (earliest_end - latest_start) + 1
				overlap = max(0, delta)
				overlap_percent = overlap / 10     # 5+5=10

				print("Overlap Percent is %f" % overlap_percent)
				print("Noise at distance %f" % dist_noise)
				noise_from_comm += (noise_pwr*overlap_percent) / (dist_noise**2)

		print("Power from other comm is %f" % noise_from_comm)
		scaled_this_pwr = this_pwr/fsl.distance_2(src, dest)**2
		print("This comm pwr is %f" % scaled_this_pwr)
		if noise_from_comm >= threshold * scaled_this_pwr:
			print("This comm is overpowered by other comms")
		else:
			print("This comm can be heard normally")



print("---------------------------------------------------")

comm_info[(0,0)] = (10, 105)
comm_info[(4,3)] = (100, 90)

iter_num = 0

Range = namedtuple('Range', ['start', 'end'])

while iter_num < iter_max:
	iter_num += 1
	for src, dest in comm_pairs.items():
		print("Iteration # %d, Source: %s, Dest: %s" % (iter_num, (src, ), (dest, ))) # Know that which pair of src and dest
		this_pwr = int(comm_info[src][0])
		this_freq_range = comm_info[src][1]
		print("Relevant power is %d" % this_pwr)
		noise_from_comm = 0.0
		r_this = Range(this_freq_range - 5, this_freq_range + 5)
		for other_src, infos in comm_info.items():   # Determine how much power is generated from other ongoing communcation
			if other_src != src:
				print("Other src %s" % (other_src,))
				noise_pwr = infos[0]          # Scale that power from other ongoing comm by the distance
				noise_freq_range = infos[1]
				dist_noise = fsl.distance_2(dest, other_src)

				r_noise = Range(noise_freq_range-5, noise_freq_range+5)

				latest_start = max(r_this.start, r_noise.start)
				earliest_end = min(r_this.end, r_noise.end)
				print("%d , %d " % (latest_start, earliest_end))
				delta = (earliest_end - latest_start)
				print("delta is %d" % delta)
				overlap = max(0.0, float(delta))
				overlap_percent = overlap / 10.0    # 5+5=10

				print("Overlap Percent is %f" % overlap_percent)
				print("Noise at distance %f" % dist_noise)
				noise_from_comm += (noise_pwr*overlap_percent) / (dist_noise**2)

		print("Power from other comm is %f" % noise_from_comm)
		scaled_this_pwr = this_pwr/fsl.distance_2(src, dest)**2
		print("This comm pwr is %f" % scaled_this_pwr)
		if noise_from_comm >= threshold * scaled_this_pwr:
			print("This comm is overpowered by other comms")
		else:
			print("This comm can be heard normally")




