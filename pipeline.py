import Player
from core import env_core
import matplotlib.pyplot as plt
import numpy as np
import re
import calendar;
import time;
import sys
import os
import copy
import random
import gc
import argparse
from threading import Thread
from multiprocessing import Process, Pool, Queue, cpu_count

_ALL_LOC_DICT_ = {}

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

# def read_sce_helper():
# 	pass
def check_pos(pl_amt):
	global _ALL_LOC_DICT_

	viable = []
	for key,val in _ALL_LOC_DICT_.items():
		sum = val[2]
		if pl_amt <= sum:
			viable.append(key)

	return viable



def pipeline_routine(pipefile, it_begin, nb_it):
	global _ALL_LOC_DICT_

	# if (it_begin != 0):
	# 	time.sleep(2) #leaving time for main process to create the dir

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

	mobile_flag = False
	if lines[line_counter][0] == "mobile":
		mobile_flag = True
	if lines[line_counter][0] != "fixed" and lines[line_counter][0] != "mobile":
		raise ValueError('Current pipeline only support fixed/mobile positions for players')

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
	num_iter = nb_it#int(lines[line_counter][0])
	line_counter += 1
	time_ref_in = 10#int(lines[line_counter][0])

	pls = ''.join(player_type_pool)
	dis = ''.join(str(e) for e in arr_list)

	directory = "%s_%s_%s/" % (pls, dis, env_type)
	dd = "saved_environments/" + directory

	if it_begin==0 and not os.path.exists(dd):
		os.makedirs(dd)
	else:
		time.sleep(0.1)

	pick_list = list(range(total_channels))
	for it in range(num_iter):
		# players = {}
		players = []

		if env_type == "s" or env_type == "ns":
			for i in range(0, player_num):
				if player_type_pool[arr_list[i]] == "FIX":
					pass

				elif player_type_pool[arr_list[i]] == "R":
					csv = [i,1,1,0,0,1005,0.01,False,total_channels]
					new_player = Player.Random(*csv)
					# players[i] = new_player
					players.append(new_player)

				elif player_type_pool[arr_list[i]] == "C":
					# csv = current_line[2].split(",")
					# csv = list(map(float, csv))

					chosed = random.choice(pick_list)
					csma_freq = (1100 - 5) - chosed * 10

					csv = [i,1,1,0,0,0.1,3,0.9,csma_freq]
					new_player = Player.CSMA(*csv)
					# players[i] = new_player
					players.append(new_player)

				elif player_type_pool[arr_list[i]] == "U":
					# csv = current_line[2].split(",")
					# csv = list(map(float, csv))
					# csv[5] = int(csv[5])
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.UCB(*csv)
					# players[i] = new_player
					players.append(new_player)

					# player_num_to_id[line_counter - 1] = current_line[0]

				elif player_type_pool[arr_list[i]] == "Ud":
					# csv = current_line[2].split(",")
					# csv = list(map(float, csv))
					# csv[5] = int(csv[5])
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.UCB_d(*csv)
					# players[i] = new_player
					players.append(new_player)

					# player_num_to_id[line_counter - 1] = current_line[0]
				elif player_type_pool[arr_list[i]] == "Ut":
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.UCB_thresholded(*csv)
					# players[i] = new_player
					players.append(new_player)

				elif player_type_pool[arr_list[i]] == "Ut2":
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.UCB_thresholded2(*csv)
					# players[i] = new_player
					players.append(new_player)

				elif player_type_pool[arr_list[i]] == "T":
					# csv = current_line[2].split(",")
					# csv = list(map(float, csv))
					# csv[5] = int(csv[5])
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.Thompsons(*csv)
					# players[i] = new_player
					players.append(new_player)

				elif player_type_pool[arr_list[i]] == "Td":
					# csv = current_line[2].split(",")
					# csv = list(map(float, csv))
					# csv[5] = int(csv[5])
					csv = [i,1,1,0,0,total_channels]
					new_player = Player.Thompsons_d(*csv)
					# players[i] = new_player
					players.append(new_player)

				else:
					sim_scenario.close()
					raise ValueError('Player type not recognized')


		if not mobile_flag:
			if env_type == "s":
				impe_center = fix_ch_sum * 5 + 1000
				impe_width = fix_ch_sum * 5
				impe_player = Player.Player(player_num,1,1,0,0,starting_frequency = impe_center)
				impe_player.set_channel(central=impe_center, width = impe_width)
				# players[player_num] = impe_player
				players.append(new_player)

			if pl_ch_sum >= player_num and env_type == "s":
				random_w = Player.Random_Weights(player_num+1,1,1,0,0,probs=False,nb_channels=total_channels)
				# players[player_num+1] = random_w
				players.append(new_player)
				# print("yes")
			elif env_type == "ns":
				random_ns = Player.Random_ns(player_num+1,1,1,0,0)
				# players[player_num+1] = random_ns
				players.append(new_player)
		else:
			viable_pos = check_pos(player_num)
			if viable_pos:
				one_pick = random.choice(viable_pos)
				if not one_pick:
					raise ValueError('No path file can support %d players'%player_num)
				aux_info = _ALL_LOC_DICT_[one_pick]
			for i in range(int(aux_info[1])):
				new_player = Player.Player(player_num+1+i,1,1,0,0)
				players.insert(0,new_player)


		# players_list = list(players.values())
		print("total pls %d"%len(players))
		players_list = players

		player_num_to_id = {}
	# print(players_list)
	# print(line_counter)

	# print(lines[line_counter])
	# print(ts)
		ts = calendar.timegm(time.gmtime())
		pls = ''.join(player_type_pool)
		dis = ''.join(str(e) for e in arr_list)
		if mobile_flag:
			pls = "m_"+pls
		directory = "%s_%s_%s/"%(pls,dis,env_type)
		dd = "saved_environments/"+directory

		if not os.path.exists(dd):
		    os.makedirs(dd)

		log_name = "result_%s_%s_%d_%s.pkl"%(pls,dis,it+it_begin, env_type)
		# WITHOUT TIME OFFSETS
		# env = env_core(players_list,time_reference_unit = time_ref_in)
		# env.TIME_REFERENCE_UNIT = 1

		time_distribution = [random.randint(0, time_ref_in-1) for i in range(len(players_list))]
		print(time_distribution)
		env = env_core(players_list,time_reference_unit = time_ref_in, time_refs=time_distribution)

		# WITH TIME OFFSETS
		if not mobile_flag:
			env.TIME_REFERENCE_UNIT = time_ref_in

			env.run_simulation(total_steps)
			env.save_results(filename=directory+log_name)
		else:
			sce_file = open(one_pick, 'r')
			path_file = open(_ALL_LOC_DICT_[one_pick][0],'r')
			sce_counter = 1
			path_counter = 0
			sce_content = [line.rstrip('\n') for line in sce_file]
			path_content = [line.rstrip('\n') for line in path_file]
			sce_file.close()
			path_file.close()
			sce_pl_amt = int(sce_content[sce_counter][0])
			sce_counter += 1
			for i in range(sce_pl_amt):
				ssv = sce_content[sce_counter].split(" ")
				player_num_to_id[ssv[0]] = i
				sce_counter += 1
			sce_counter += 2
			path_counter = 2
#######################
			
			print(path_content[path_counter])

			while path_counter < len(path_content):
				sc = sce_content[sce_counter].split(" ")
				if sc[0] in player_num_to_id:
					if int(sc[1]) == path_counter-1:
						if sc[2] == "set_channel":
							parameters = list(map(int, sc[3:]))
							nid = player_num_to_id[sc[0]]
							players[nid].set_channel(*parameters)
							sce_counter += 1
							continue

				pos_line = path_content[path_counter]
				pos_line = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+',pos_line)
				for i in range(len(pos_line)):
					pos_line[i] = pos_line[i].replace('[', '').replace(']', '')
				for i in range(len(players)):
					pos_all = pos_line[i]
					pos_in_pairs = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+',pos_all)

					pos_full_list = []

					for j in range(len(pos_in_pairs)):
						pos_in_pairs[j] = pos_in_pairs[j].replace('(', '').replace(')', '')
						csv = pos_in_pairs[j].split(",")
						csv = list(map(float, csv))
						pos_in_pairs[j] = csv
						pos_full_list += pos_in_pairs[j]
					# print("test:")
					# print(pos_full_list)
					# player_id = player_num_to_id[i]
					players[i].update_location(*pos_full_list)
				print(path_counter)
				path_counter += 1
				# print("run 1")
				env.run_simulation(1)

			env.save_results(filename=directory+log_name)
#######################
		# env.displayResults()


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_pipe", required=True,
	help="Text file that contain paths to all the single pipe files")
parser.add_argument("-l", "--locations", required=False,
	help="Text file that contain paths to all the location movement files")

p_args_f = vars(parser.parse_args())

print(p_args_f)
pipe_file = p_args_f["input_pipe"]
if "locations" in p_args_f:
	loc_file = p_args_f["locations"]

for x in sys.argv:
	print("Argument: %s", x)

# all_pipe  = open(sys.argv[1], "r")
# print(sim_scenario.read())
# pipe_file = sys.argv[1]

try:
    all_pipe = open(pipe_file, 'r')
    # Store configuration file values
except FileNotFoundError:
    print('Input file %s does not exist'%pipe_file)
    sys.exit()

loc_flag = False
if loc_file is not None:
	try:
	    all_loc = open(loc_file, 'r')
	    # Store configuration file values
	    loc_flag = True
	except FileNotFoundError:
	    print('Location file %s does not exist'%loc_file)
	    all_loc.close()
	    sys.exit()

all_pipe_content = [line.rstrip('\n') for line in all_pipe]

if loc_flag:
	all_loc_content = [line.rstrip('\n') for line in all_loc]
	for onef in all_loc_content:
		one_loc = open(onef, 'r')
		corre_path = one_loc.readline().rstrip('\n')
		corre_path_f = open(corre_path, 'r')
		fix_amt = int(corre_path_f.readline().rstrip('\n'))
		flex_amt = int(corre_path_f.readline().rstrip('\n'))
		_ALL_LOC_DICT_[onef] = (corre_path,fix_amt,flex_amt)
		one_loc.close()
		corre_path_f.close()

all_loc.close()

print(_ALL_LOC_DICT_)

counter = 1

NB_ITER=1
NB_PROCESSES = 1#cpu_count()
NB_IT_BY_PROCESS = int(NB_ITER / NB_PROCESSES +1)
for f in all_pipe_content:
	print("Step " + str(counter) + "/" + str(len(all_pipe_content)))
	counter += 1
	p = list()
	for i in range(NB_PROCESSES):
		process = Process(target = pipeline_routine, args=(f,i*NB_IT_BY_PROCESS, NB_IT_BY_PROCESS))
		p.append(process)
		p[i].start()
	for i in range(NB_PROCESSES):
		p[i].join()

	# thread = Thread(target = pipeline_routine, args=(i, ))
	# thread.start()
	# thread.join()
	# del thread
	# dump_garbage()
	# input()







