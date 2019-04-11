import Player
from core import env_core
import matplotlib.pyplot as plt
import numpy as np
import re
import calendar;
import time;
import sys
import os
import gc
from threading import Thread
from multiprocessing import Process, Queue

def dump_garbage():
	"""
    show us what's the garbage about
    """

	# force collection
	print("GARBAGE:")
	gc.collect()

	print("GARBAGE OBJECTS:")
	print(gc.garbage)
	for x in gc.garbage:
		print("1")
		s = str(x)
		if len(s) > 80:
			s = s[:80]
		print(s)

# re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+',strs)

gc.enable()

# print(sim_content)

# print(np.shape(sim_content))

# if sim_content[-1] != "endsim":
# 	sim_scenario.close()
# 	raise ValueError('Simulation scenrio must end with endsim')

def pipeline_routine(pipefile):

	pipeline_config  = open(pipefile, "r")
	# print(sim_scenario.read())
	pipeline_content = [line.rstrip('\n') for line in pipeline_config]

	lines = []

	for i in range(len(pipeline_content)):
		line = pipeline_content[i]
		line_seg = line.split(",")
		# print(line_seg)
		lines.append(line_seg)

	# print(len(poss))

	pipeline_config.close() # at this point we have transferred all data into a list. Close file. 

	line_counter = 0

	mode = int(lines[line_counter][0])   # mode 1 = single type players, mode 2 = double type players
	player_num = int(lines[line_counter][1])
	print("mode: %d"%mode)
	print("Player amount: %d" % player_num)
	line_counter += 1

	if lines[line_counter][0] != "fixed":
		raise ValueError('Current pipeline only support fixed positions for players')

	line_counter += 1

	player_type_pool = []

	print(lines[line_counter])
	if mode == 1 and len(lines[line_counter]) == 1:
		player_type_pool = lines[line_counter]
	elif mode == 2 and len(lines[line_counter]) == 2:
		player_type_pool = lines[line_counter]
	else:
		raise ValueError('Pipeline mode does not support provided player type configuration')

	for i in player_type_pool:
		# support R, C, U, Ud, T
		if i not in ['R', 'C', 'U', 'Ud','Ut','Ut2', 'T','Td']:
			raise ValueError('Player type %s not supported' % i)

	line_counter += 1

	if player_num != len(lines[line_counter]):
		print("Initial provided player number is %d, but %d of players is demanded in the arrangement"% (player_num, len(lines[line_counter])))
		raise ValueError('Player number must be the same, both in the starting line & in the arrangement line')

	# arr_list = lines[line_counter]
	arr_list = [ int(x) for x in lines[line_counter] ]
	print(arr_list)
	line_counter += 1

	if lines[line_counter][0]=='s':
		pass
	elif lines[line_counter][0]=='ns':
		pass
		# raise ValueError('Not supported yet')
	else:
		print("Provided with %s "%lines[line_counter][0])
		raise ValueError('Must be either static or non-static')

	total_channels = int(lines[line_counter][1])
	print("total channels %d"%total_channels)

	# if int(lines[line_counter][1])!=10:
	# 	raise ValueError('Not 10')

	if int(lines[line_counter][2]) + int(lines[line_counter][3])!=total_channels:
		raise ValueError('Sum not the same')

	env_type = lines[line_counter][0]
	pl_ch_sum = int(lines[line_counter][2])
	fix_ch_sum = int(lines[line_counter][3])
	total_steps = int(lines[line_counter][4])

	line_counter += 1
	num_iter = int(lines[line_counter][0])
	line_counter += 1
	time_ref_in = int(lines[line_counter][0])


	for it in range(num_iter):
		players = {}
		player_num_to_id = {}

		if env_type == "s" or env_type == "ns":
			top = 0
			for i in range(0, player_num):
				if player_type_pool[arr_list[i]] == "FIX":
					pass
					# csv = current_line[2].split(",")
					# csv = list(map(float, csv))
					# # new_player = Player.Player(*csv)
					# csv = [1,1,0,0]
					# new_player = Player.Player(*csv)
					# players[i] = new_player

					# player_num_to_id[line_counter - 1] = current_line[0]

				elif player_type_pool[arr_list[i]] == "R":
					csv = [i,1,1,0,0,1005,0.01,False,total_channels]
					new_player = Player.Random(*csv)
					players[i] = new_player

				elif player_type_pool[arr_list[i]] == "C":
					# csv = current_line[2].split(",")
					# csv = list(map(float, csv))
					csma_freq = (1100 - 5) - top * 10
					top+=1
					csv = [i,1,1,0,0,0.1,3,0.9,csma_freq]
					new_player = Player.CSMA(*csv)
					players[i] = new_player

				elif player_type_pool[arr_list[i]] == "U":
					# csv = current_line[2].split(",")
					# csv = list(map(float, csv))
					# csv[5] = int(csv[5])
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.UCB(*csv)
					players[i] = new_player

					# player_num_to_id[line_counter - 1] = current_line[0]

				elif player_type_pool[arr_list[i]] == "Ud":
					# csv = current_line[2].split(",")
					# csv = list(map(float, csv))
					# csv[5] = int(csv[5])
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.UCB_d(*csv)
					players[i] = new_player

					# player_num_to_id[line_counter - 1] = current_line[0]
				elif player_type_pool[arr_list[i]] == "Ut":
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.UCB_thresholded(*csv)
					players[i] = new_player

				elif player_type_pool[arr_list[i]] == "Ut2":
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.UCB_thresholded2(*csv)
					players[i] = new_player

				elif player_type_pool[arr_list[i]] == "T":
					# csv = current_line[2].split(",")
					# csv = list(map(float, csv))
					# csv[5] = int(csv[5])
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.Thompsons(*csv)
					players[i] = new_player

				elif player_type_pool[arr_list[i]] == "Td":
					# csv = current_line[2].split(",")
					# csv = list(map(float, csv))
					# csv[5] = int(csv[5])
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.Thompsons_d(*csv)
					players[i] = new_player

				else:
					sim_scenario.close()
					raise ValueError('Player type not recognized')

		

		# print(pl_ch_sum)
		# print(player_num)
		# print(env_type)
		if env_type == "s":
			impe_center = fix_ch_sum * 5 + 1000
			impe_width = fix_ch_sum * 5
			impe_player = Player.Player(player_num,1,1,0,0,starting_frequency = impe_center)
			impe_player.set_channel(central=impe_center, width = impe_width)
			players[player_num] = impe_player

		if pl_ch_sum >= player_num and env_type == "s":
			random_w = Player.Random_Weights(player_num+1,1,1,0,0,probs=False,nb_channels=total_channels)
			players[player_num+1] = random_w
			# print("yes")
		elif env_type == "ns":
			random_ns = Player.Random_ns(player_num+1,1,1,0,0)
			players[player_num+1] = random_ns


		players_list = list(players.values())

	# print(players_list)
	# print(line_counter)

	# print(lines[line_counter])
	# print(ts)
		ts = calendar.timegm(time.gmtime())
		pls = ''.join(player_type_pool)
		dis = ''.join(str(e) for e in arr_list)

		directory = "%s_%s/"%(pls,dis)
		dd = "saved_environments/"+directory

		if not os.path.exists(dd):
		    os.makedirs(dd)

		log_name = "result_%s_%s_%d.pkl"%(pls,dis,it)
		env = env_core(players_list,time_reference_unit = time_ref_in)

		env.run_simulation(total_steps)
		env.save_results(filename=directory+log_name)
		# env.displayResults()


for x in sys.argv:
	print("Argument: %s", x)

all_pipe  = open(sys.argv[1], "r")
# print(sim_scenario.read())
all_pipe_content = [line.rstrip('\n') for line in all_pipe]

counter = 1
for i in all_pipe_content:
	print("Step " + str(counter) + "/" + str(len(all_pipe_content)))
	counter += 1

	p = Process(target = pipeline_routine, args=(i,))
	p.start()
	p.join()

	# thread = Thread(target = pipeline_routine, args=(i, ))
	# thread.start()
	# thread.join()
	# del thread
	# dump_garbage()
	# input()







