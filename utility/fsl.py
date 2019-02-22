import math
import numpy as np

# Assume positions in form (x, y), distance is Euclidean distance
# Gain is in dB, Frequency in Hz

# Valid Unit combinations are: (m & Hz), (m & KHz), (m & MHz), (km & MHz), (km & GHz)

# This will return free space loss in dB
# ? how to use this?
def free_space_loss(src_pos, dst_pos, src_gain, dst_gain, frequency, unit_combination):
	print(distance_2(src_pos, dst_pos))
	print(src_gain)
	print(dst_gain)
	print(frequency)
	print(unit_combination)
	distance_log = 20 * math.log(distance_2(src_pos, dst_pos), 10)
	frequenct_log = 20 * math.log(frequency, 10)
	constant_pi_c = switch_unit2constant(unit_combination)
	print(constant_pi_c)
	fsl = distance_log + frequenct_log + constant_pi_c - src_gain - dst_gain
	return fsl

# Unit of distance uncertain?
def distance_2(pos_1, pos_2):
	print(pos_1, pos_2)
	return math.sqrt( (pos_1[0] - pos_2[0])**2 + (pos_1[1] - pos_2[1])**2)

def switch_unit2constant(argument):
    switcher = {
        ("m", "Hz"): -147.55,
        ("m", "KHz"): -87.55,
        ("m", "MHz"): -27.55,
        ("km", "MHz"): 32.45,
        ("km", "GHz"): 92.45
    }
    if argument in switcher:
    	print(switcher.get(argument))
    	return switcher.get(argument)
    else:
    	raise ValueError('Given wrong unit combination for calculating Free Space Path Loss')

# Src power is measure in 1mW
def log_path_loss_from_src(src_power, path_loss, distance, distance_unit, y = 2.0, X = 0):
	dbm_difference = path_loss + 10*y*math.log(distance/distance_unit) + X
	P_tx_dbm = 10*math.log(src_power / 1)
	P_rx_dbm = P_tx_dbm - dbm_difference
	print("P rx in dbm is %f" % P_rx_dbm)
	P_rx = 10**(P_rx_dbm / 10)
	print(P_rx)
	print("Expect rx to have power of %lf" % P_rx)

# free_space = free_space_loss( (1, 0), (0, 0), 0, 0, 5, ("km", "GHz") )
# print(free_space)

# log_path_loss_from_src(src_power=100, path_loss=free_space, distance=1, distance_unit=1 )




