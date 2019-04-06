# -*- coding: utf-8 -*-
"""
"""

"""
DESCRIPTION
"""

from Player import *
# from Player import Random
# from Player import CSMA
# from Player import UCB
from core import env_core
import matplotlib.pyplot as plt
import numpy as np

NB_CHANNELS = 10


def fix_player_enough_channels():
    p0 = UCB(0, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p1 = UCB(1, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p2 = UCB(2, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p3 = UCB(3, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p4 = Player(4, -1, 0, 1, 0)

    p4.set_channel(1050, 30)
    p4.power = 6
    p4.blocker_counter = 0

    np.random.seed()
    env = env_core([p0, p1, p2, p3, p4])

    env.run_simulation(1000)

    env.players[0].displayEstimatedProbs()
    env.players[1].displayEstimatedProbs()
    env.players[2].displayEstimatedProbs()
    # for i in range(len(env.players[0].previous_successes)):
    #     print(str(i) + " - " + str(env.players[0].previous_successes[i]))
    print(env.players[0].previous_channels)
    env.displayResults()

def fix_player_not_enough_channels():
    p0 = UCB(0, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p1 = UCB(1, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p2 = UCB(2, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p3 = UCB(3, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p4 = UCB(4, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p5 = Player(5, -1, 0, 1, 0)

    p5.set_channel(1050, 30)
    p5.power = 6
    p5.blocker_counter = 0

    np.random.seed()

    # p1 is on the same channel as p2
    p1.set_channel(p1.min_frequency + (p1.max_frequency - p1.min_frequency) * 0.5 / NB_CHANNELS,
                   (p1.max_frequency - p1.min_frequency) * 0.5 / NB_CHANNELS)
    p1.blocker_counter = 0
    env = env_core([p0, p1, p2, p3, p4, p5])

    env.run_simulation(1000)

    env.players[0].displayEstimatedProbs()
    env.players[1].displayEstimatedProbs()
    env.players[2].displayEstimatedProbs()
    env.displayResults()

def random_players():
    p0 = UCB(0, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p1 = UCB(1, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p2 = UCB(2, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p3 = Random(3,-1,0,1,0, prob=0.05)
    p4 = Random(4,-1,0,1,0, prob=0.05)
    p5 = Random(5,-1,0,1,0, prob=0.05)

    np.random.seed()

    # p1 is on the same channel as p2
    p1.set_channel(p1.min_frequency + (p1.max_frequency - p1.min_frequency) * 0.5 / NB_CHANNELS,
                   (p1.max_frequency - p1.min_frequency) * 0.5 / NB_CHANNELS)
    p1.blocker_counter = 0
    env = env_core([p0, p1, p2, p3, p4, p5])

    env.run_simulation(2000)

    env.players[0].displayEstimatedProbs()
    env.players[1].displayEstimatedProbs()
    env.players[2].displayEstimatedProbs()
    env.displayResults()

def csma_players():
    p0 = UCB(0, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p1 = UCB(1, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p2 = UCB(2, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p3 = CSMA(3,-1,0,1,0, 0.3, 3, 0.5)
    np.random.seed()

    # p1 is on the same channel as p2
    p1.set_channel(p1.min_frequency + (p1.max_frequency - p1.min_frequency) * 0.5 / NB_CHANNELS,
                   (p1.max_frequency - p1.min_frequency) * 0.5 / NB_CHANNELS)
    p1.blocker_counter = 0
    env = env_core([p0, p1, p2, p3])

    env.run_simulation(1000)

    env.players[0].displayEstimatedProbs()
    env.players[1].displayEstimatedProbs()
    env.players[2].displayEstimatedProbs()
    env.displayResults()

def different_ucbs():
    p0 = UCB(0, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p1 = UCB_window(1, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p2 = UCB_thresholded(2, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p3 = Player(3, -1, 0, 1, 0)
    np.random.seed()

    p3.set_channel(1005)

    env = env_core([p0, p1, p2, p3])
    env.run_simulation(3000)

    env.players[0].displayEstimatedProbs()
    env.players[1].displayEstimatedProbs()
    env.players[2].displayEstimatedProbs()
    env.displayResults()

def fix_player_enough_channels_unaligned():
    p0 = UCB(0, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p1 = UCB(1, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p2 = UCB(2, -1, 0, 1, 0, nb_channels=NB_CHANNELS, lamda=0.7)
    p3 = UCB(3, -1, 0, 1, 0, nb_channels=NB_CHANNELS*2, lamda=0.7)

    p3.min_frequency = 1002.5
    p3.max_frequency  = 1102.5
    p4 = Player(4, -1, 0, 1, 0)

    p4.set_channel(1050, 30)
    p4.blocker_counter = 0

    np.random.seed()
    env = env_core([p0, p1, p2, p3, p4])

    env.run_simulation(1000)
    print(env.computePowers())

    env.players[0].displayEstimatedProbs()
    env.players[1].displayEstimatedProbs()
    env.players[2].displayEstimatedProbs()
    # for i in range(len(env.players[0].previous_successes)):
    #     print(str(i) + " - " + str(env.players[0].previous_successes[i]))
    # print(env.players[0].previous_channels)
    env.displayResults()

def enough_players_fully_unaligned():
    p0 = UCB(0, -1, 0, 1, 0, nb_channels=3, lamda=0.7)
    p1 = UCB(1, -1, 0, 1, 0, nb_channels=5, lamda=0.7)
    p2 = UCB(2, -1, 0, 1, 0, nb_channels=10, lamda=0.7)
    p3 = UCB(3, -1, 0, 1, 0, nb_channels=13, lamda=0.7)
    p4 = UCB(4, -1, 0, 1, 0, nb_channels=13, lamda=0.7)
    p5 = UCB(5, -1, 0, 1, 0, nb_channels=25, lamda=0.7)
    p6 = UCB(6, -1, 0, 1, 0, nb_channels=13, lamda=0.7)

    p3.min_frequency = 1002.5
    p3.max_frequency  = 1102.5
    p5.min_frequency = 1001
    p5.max_frequency = 1101

    np.random.seed()
    env = env_core([p0, p1, p2, p3, p4, p5, p6])

    env.run_simulation(1000)
    print(env.computePowers())

    env.players[0].displayEstimatedProbs()
    env.players[1].displayEstimatedProbs()
    env.players[2].displayEstimatedProbs()
    # for i in range(len(env.players[0].previous_successes)):
    #     print(str(i) + " - " + str(env.players[0].previous_successes[i]))
    # print(env.players[0].previous_channels)
    env.displayResults()


def debug():

    p0 = Player(0, -1, 0, 1, 0)
    p0.set_channel(1025, 25)

    p1 = Player(1, -1, 0, 1, 0)
    p1.set_channel(1050, 25)

    env = env_core([p0, p1])

    env.run_simulation(10)

    print(env.computePowers())
    print(env.NB_PLAYERS)
    print(np.arange(env.NB_PLAYERS))

    env.displayResults()


# fix_player_enough_channels()
# fix_player_not_enough_channels()
# random_players()
# csma_players()
# fix_player_enough_channels_unaligned()
# enough_players_fully_unaligned()
different_ucbs()
# debug()