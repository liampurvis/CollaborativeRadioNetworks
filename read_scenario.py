import Player
from core import env_core
import matplotlib.pyplot as plt
import numpy as np

import sys
for x in sys.argv:
	print("Argument: %s", x)

file_object  = open(sys.argv[1], "r")
# print(file_object.read())
content = [line.rstrip('\n') for line in file_object]
# print(content)

# print(np.shape(content))

if content[-1] != "endsim":
	file_object.close()
	raise ValueError('Simulation scenrio must end with endsim')

lines = []

for i in range(len(content)):
	line = content[i]
	line_seg = line.split(" ")
	# print(line_seg)
	lines.append(line_seg)

line_counter = 0

player_num = int(lines[line_counter][0])
print(player_num)
line_counter += 1

players = {}

for i in range(line_counter, line_counter+player_num):
	# print(lines[i])
	line_counter += 1
	current_line = lines[i]
	if current_line[1] == "FIX":
		csv = current_line[2].split(",")
		csv = list(map(float, csv))
		new_player = Player.Player(*csv)
		players[current_line[0]] = new_player
	elif current_line[1] == "Random":
		orig_csv = current_line[2].split(",")
		csv = list(map(float, orig_csv[:-2]))
		new_player = Player.Random(*csv, bool(orig_csv[-1]))
		players[current_line[0]] = new_player
	elif current_line[1] == "CSMA":
		csv = current_line[2].split(",")
		csv = list(map(float, csv))
		new_player = Player.CSMA(*csv)
		players[current_line[0]] = new_player
	elif current_line[1] == "UCB":
		csv = current_line[2].split(",")
		csv = list(map(float, csv))
		new_player = Player.UCB(*csv)
		players[current_line[0]] = new_player
	else:
		file_object.close()
		raise ValueError('Player type not recognized')

players_list = list(players.values())

print(players_list)
print(line_counter)

# print(lines[line_counter])

time_ref_csv = lines[line_counter][0].split(",")
time_ref_csv = list(map(int, time_ref_csv))
print(time_ref_csv)
line_counter += 1

env = env_core(players_list, time_refs = time_ref_csv)

for i in range(line_counter, len(lines)):
	if lines[i][0] == "run":
		pass
		time = int(lines[i][1])
		print(time)
		env.run_simulation(time)
	elif lines[i][0] == "endsim":
		break
	else:
		if lines[i][0] in players:
			if lines[i][1] == "set_channel":
				parameters = list(map(int, lines[i][2].split(",")))
				players[lines[i][0]].set_channel(*parameters)
			elif lines[i][1] == "update_location":
				parameters = list(map(float, lines[i][2].split(",")))
				print(parameters)
				players[lines[i][0]].update_location(*parameters)
			else:
				file_object.close()
				raise ValueError("Unrecognized Player simulation command")
		else:
			file_object.close()
			raise ValueError("Unrecognized simulation command")

file_object.close()
env.displayResults()




