import Player
from core import env_core
import matplotlib.pyplot as plt
import numpy as np
import re
import sys
for x in sys.argv:
	print("Argument: %s", x)

# re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+',strs)

sim_scenario  = open(sys.argv[1], "r")
pos_scenario  = open(sys.argv[2], "r")
# print(sim_scenario.read())
sim_content = [line.rstrip('\n') for line in sim_scenario]
pos_content = [line.rstrip('\n') for line in pos_scenario]
# print(sim_content)

# print(np.shape(sim_content))

if sim_content[-1] != "endsim":
	sim_scenario.close()
	pos_scenario.close()
	raise ValueError('Simulation scenrio must end with endsim')

lines = []

for i in range(len(sim_content)):
	line = sim_content[i]
	line_seg = line.split(" ")
	# print(line_seg)
	lines.append(line_seg)

poss = []
for i in range(len(pos_content)):
	one_line = pos_content[i]
	line_seg = one_line.split(" ")
	# print(line_seg)
	poss.append(line_seg)

# print(len(poss))

line_counter = 0
pos_counter = 0

try:
	player_num = int(lines[line_counter][0])
	print("Player amount: %d" % player_num)
except ValueError:
	line_counter += 1
	player_num = int(lines[line_counter][0])
	print("Player amount: %d" % player_num)

line_counter += 1

fixed_amt = int(poss[pos_counter][0])
pos_counter+=1
other_amt = int(poss[pos_counter][0])

if player_num > (fixed_amt+other_amt):
	sim_scenario.close()
	pos_scenario.close()
	raise ValueError('Player number in simulation file MUST be LESS OR EQUAL to player number in position file')

pos_counter += 1

players = {}
player_num_to_id = {}

line_start = line_counter

for i in range(line_counter, line_counter+player_num):
	# print(lines[i])
	current_line = lines[i]
	if current_line[1] == "FIX":
		csv = current_line[2].split(",")
		csv = list(map(float, csv))
		new_player = Player.Player(*csv)
		players[current_line[0]] = new_player

		player_num_to_id[line_counter - line_start] = current_line[0]
	elif current_line[1] == "Random":
		orig_csv = current_line[2].split(",")
		csv = list(map(float, orig_csv))
		new_player = Player.Random(*csv)
		players[current_line[0]] = new_player

		player_num_to_id[line_counter - line_start] = current_line[0]
	elif current_line[1] == "CSMA":
		csv = current_line[2].split(",")
		csv = list(map(float, csv))
		new_player = Player.CSMA(*csv)
		players[current_line[0]] = new_player

		player_num_to_id[line_counter - line_start] = current_line[0]
	elif current_line[1] == "UCB" or current_line[1] == "UCB_thresholded" or current_line[1] == "UCB_thresholded2" or current_line[1] == "UCB_d" or current_line[1] == "UCB_sw":
		csv = current_line[2].split(",")
		csv = list(map(float, csv))
		csv[5] = int(csv[5])
		new_player = Player.UCB(*csv)
		players[current_line[0]] = new_player

		player_num_to_id[line_counter - line_start] = current_line[0]
	elif current_line[1] == "Thompsons":
		csv = current_line[2].split(",")
		csv = list(map(float, csv))
		# csv[5] = int(csv[5])
		new_player = Player.Thompsons(*csv)
		players[current_line[0]] = new_player

		player_num_to_id[line_counter - line_start] = current_line[0]
	else:
		sim_scenario.close()
		raise ValueError('Player type not recognized')

	line_counter += 1

players_list = list(players.values())

# print(players_list)
# print(line_counter)

# print(lines[line_counter])

time_ref_csv = lines[line_counter][0].split(",")
time_ref_csv = list(map(int, time_ref_csv))
# print(time_ref_csv)
line_counter += 1

env = env_core(players_list, time_refs = time_ref_csv)

loop_pos_file_flag = False

loopi = line_counter
for i in range(loopi, len(lines)):
	line_counter += 1
	if lines[i][0] == "run":
		pass
		time = int(lines[i][1])
		print(time)
		env.run_simulation(time)
	elif lines[i][0] == "endsim":
		break
	elif lines[i][0] == "pos_deplete":
		loop_pos_file_flag = True
		break
	else:
		if lines[i][0] in players:
			if lines[i][1] == "set_channel":
				parameters = list(map(int, lines[i][2].split(",")))
				players[lines[i][0]].set_channel(*parameters)
			elif lines[i][1] == "update_location":
				parameters = list(map(float, lines[i][2].split(",")))
				players[lines[i][0]].update_location(*parameters)
			else:
				sim_scenario.close()
				raise ValueError("Unrecognized Player simulation command")
		else:
			sim_scenario.close()
			raise ValueError("Unrecognized simulation command")

print(lines[line_counter])

if(loop_pos_file_flag):
	while pos_counter < len(poss):
		if lines[line_counter][0] in players:
			if int(lines[line_counter][1]) == pos_counter-1:
				if lines[line_counter][2] == "set_channel":
					parameters = list(map(int, lines[line_counter][3:]))
					players[lines[line_counter][0]].set_channel(*parameters)
					line_counter += 1
					continue

		pos_line = poss[pos_counter][0]
		pos_line = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+',pos_line)
		# print(pos_line)
		for i in range(len(pos_line)):
			pos_line[i] = pos_line[i].replace('[', '').replace(']', '')
		# print(pos_line)
		for i in range(player_num):
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
			player_id = player_num_to_id[i]
			players[player_id].update_location(*pos_full_list)
		pos_counter += 1
		# print("run 1")
		env.run_simulation(1)

sim_scenario.close()
env.displayResults()
# env.players[0].displayEstimatedProbs()



