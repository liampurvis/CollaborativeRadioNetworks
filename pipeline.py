import Player
from core import env_core
import matplotlib.pyplot as plt
import numpy as np
import re
import calendar;
import time;
import sys

# re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+',strs)


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
		if i not in ['R', 'C', 'U', 'Ud', 'T']:
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
		raise ValueError('Not supported yet')
	else:
		print("Provided with %s "%lines[line_counter][0])
		raise ValueError('Must be either static or non-static')

	if int(lines[line_counter][1])!=10:
		raise ValueError('Not 10')

	if int(lines[line_counter][2]) + int(lines[line_counter][3])!=10:
		raise ValueError('Sum not 10')

	pl_ch_sum = int(lines[line_counter][2])
	fix_ch_sum = int(lines[line_counter][3])
	total_steps = int(lines[line_counter][4])

	line_counter += 1
	num_iter = int(lines[line_counter][0])
	line_counter += 1
	time_ref_in = int(lines[line_counter][0])

	players = {}
	player_num_to_id = {}

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
			pass
			# orig_csv = current_line[2].split(",")
			# csv = list(map(float, orig_csv))
			# new_player = Player.Random(*csv)
			# players[i] = new_player

			# player_num_to_id[line_counter - 1] = current_line[0]

		elif player_type_pool[arr_list[i]] == "C":
			pass
			# csv = current_line[2].split(",")
			# csv = list(map(float, csv))
			# new_player = Player.CSMA(*csv)
			# players[i] = new_player

			# player_num_to_id[line_counter - 1] = current_line[0]

		elif player_type_pool[arr_list[i]] == "U":
			# csv = current_line[2].split(",")
			# csv = list(map(float, csv))
			# csv[5] = int(csv[5])
			csv = [i,1,1,0,0,10]
			new_player = Player.UCB(*csv)
			players[i] = new_player

			# player_num_to_id[line_counter - 1] = current_line[0]

		elif player_type_pool[arr_list[i]] == "Ud":
			# csv = current_line[2].split(",")
			# csv = list(map(float, csv))
			# csv[5] = int(csv[5])
			csv = [i,1,1,0,0,10]
			new_player = Player.UCB_d(*csv)
			players[i] = new_player

			# player_num_to_id[line_counter - 1] = current_line[0]
		elif player_type_pool[arr_list[i]] == "Ut":
			csv = [i,1,1,0,0,10]
			new_player = Player.UCB_thresholded(*csv)
			players[i] = new_player

		elif player_type_pool[arr_list[i]] == "Ut2":
			csv = [i,1,1,0,0,10]
			new_player = Player.UCB_thresholded2(*csv)
			players[i] = new_player

		elif player_type_pool[arr_list[i]] == "T":
			# csv = current_line[2].split(",")
			# csv = list(map(float, csv))
			# csv[5] = int(csv[5])
			csv = [i,1,1,0,0,10]
			new_player = Player.Thompsons(*csv)
			players[i] = new_player

		else:
			sim_scenario.close()
			raise ValueError('Player type not recognized')

	impe_center = fix_ch_sum * 5 + 1000
	impe_width = fix_ch_sum * 5
	impe_player = Player.Player(player_num,1,1,0,0,starting_frequency = impe_center)
	impe_player.set_channel(central=impe_center, width = impe_width)
	players[player_num] = impe_player


	players_list = list(players.values())

	# print(players_list)
	# print(line_counter)

	# print(lines[line_counter])
	ts = calendar.timegm(time.gmtime())
	# print(ts)
	for it in range(2):
		log_name = "result_%d.pkl"%ts
		env = env_core(players_list,time_reference_unit = time_ref_in)

		env.run_simulation(total_steps)
		env.save_results(filename=log_name)
		# env.displayResults()

for x in sys.argv:
	print("Argument: %s", x)

all_pipe  = open(sys.argv[1], "r")
# print(sim_scenario.read())
all_pipe_content = [line.rstrip('\n') for line in all_pipe]

for i in all_pipe_content:
	print(i)
	pipeline_routine(i)







