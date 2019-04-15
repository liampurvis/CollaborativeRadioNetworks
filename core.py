# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 14:59:06 2019
@author: Alexandre
"""

import numpy as np
import logging
import pickle
from pathlib import Path
from matplotlib import pyplot as plt
import os
from gifGen import gif
from Player import *

class env_core:
    """
        This class simulates the environment core
    """
    #players = [] #list of objects of class Player
    NB_PLAYERS = 0 #number of players = len(players)

    time_references = []
    TIME_REFERENCE_UNIT = 10
    current_signal_powers = []
    current_noise_powers = []
    curr_step = 0

    SNR_THRESHOLD = 1 #min SNR for success, modified in __init__

    player_idlist = []
    player_pos_record = {}
    player_frq_record = {}
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'C5', 'C2', 'C7']
    symbols = ['--', '-.', ':', '.', '+', 'x', 'h', '_', '--', '-']

    # initialize the core for a given set of players
    def __init__(self, players, nb_steps=100, time_refs=[], logfile="logfile.log", time_reference_unit=10):
        self.players = players
        self.NB_PLAYERS = len(players)
        self.NB_STEPS = nb_steps

        #setting the time reference for each player
        #allows to have overlapping period of times
        if len(time_refs)!=self.NB_PLAYERS:
            for i in range(self.NB_PLAYERS):
                self.time_references.append(0)
        else:
            # self.time_references = time_refs.copy()
            self.time_references = time_refs[:]
        self.current_signal_powers = np.zeros(self.NB_PLAYERS)
        self.current_noise_powers = np.zeros(self.NB_PLAYERS)

        self.TIME_REFERENCE_UNIT = time_reference_unit

        self.curr_step = 0
        self.SNR_THRESHOLD = 4

        # self.initialization_steps()
        # logging.basicConfig(filename=logfile, filemode="w", level=logging.DEBUG)
        for p in self.players:
            self.player_idlist.append(p.id)
            self.player_pos_record[p.id] = []
            self.player_frq_record[p.id] = []

        self.next_step_vect = np.vectorize(self.next_step_helper, otypes=[None])
        self.signal_power_vect = np.vectorize(self.compute_signal_power_helper)
        self.noise_power_vect = np.vectorize(self.compute_noise_power_helper, otypes = [float])


    def run_simulation(self, nb_steps):
        # print("Running " + str(nb_steps) + "*" + str(self.TIME_REFERENCE_UNIT))
        for _ in range(nb_steps*self.TIME_REFERENCE_UNIT):
            self.next_step()

    # computes the success rate for every player and asks for next step
    def next_step(self):
        # logging.debug("step " + str(self.curr_step*1.0/self.TIME_REFERENCE_UNIT))

        (signal_powers, noise_powers) = self.computePowers()
        # print("Signal =  " + str(signal_powers))
        # print("Noise = " + str(noise_powers))
        self.current_signal_powers += signal_powers
        # print("Current Signal Power = " + str(self.current_signal_powers))
        self.current_noise_powers += noise_powers
        # print("Current Noise Power = " + str(self.current_noise_powers))


        # np.vectorize(self.next_step_helper, otypes=[None])(np.arange(self.NB_PLAYERS))
        self.next_step_vect(np.arange(self.NB_PLAYERS))


        self.curr_step += 1

    #initializes success and noise_power values for the initial settings
    # def initialization_steps(self):
    #     for j in range(self.TIME_REFERENCE_UNIT):
    #         (successes, noise_powers) = self.computePowers()
    #         self.current_successes += successes
    #
    #         for i in range(self.NB_PLAYERS):
    #             if self.time_references[i]==j%self.TIME_REFERENCE_UNIT:
    #                 self.current_successes[i] = 0
    #                 self.current_noise_powers[i] = 0

    def next_step_helper(self, i):
        # print("Helper " + str(i))
        if self.time_references[i]%self.TIME_REFERENCE_UNIT==self.curr_step%self.TIME_REFERENCE_UNIT:
                if (self.players[i].blocker_counter == 0):
                    success = self.computeSuccess(i)
                    noise = 0
                else:
                    success = 0
                    noise = self.computeNoisePower(i)
                self.players[i].next_step(success, noise)


                self.current_signal_powers[i] = 0
                self.current_noise_powers[i] = 0

            # fetch freq and position for gif
        p = self.players[i]
        self.player_pos_record[p.id].append((p.t_x, p.t_y, p.r_x, p.r_y))
        self.player_frq_record[p.id].append((p.central_frequency, p.channel_width))



    def computeSuccess(self, i):
        # print("Compute Success " + str(i))
        # print(self.current_signal_powers[i])
        # print(self.current_signal_powers[i])
        if (self.current_noise_powers[i]==0) or (self.current_signal_powers[i]/self.current_noise_powers[i] > self.SNR_THRESHOLD):
            return 1
        else:
            return 0

    def computeNoisePower(self, i):
        return self.current_noise_powers[i] * 1.0 / self.TIME_REFERENCE_UNIT

    # from a given set of settings, compute the success rate of each player
    def computePowers(self):
        signal_power = self.signal_power_vect(np.arange(self.NB_PLAYERS))

        blocker_counters = np.array([self.players[i].blocker_counter for i in np.arange(self.NB_PLAYERS)])

        # vect = np.vectorize(self.compute_noise_power_helper, otypes = [float])

        noise_power = np.array([np.sum(self.noise_power_vect(np.arange(self.NB_PLAYERS)[(np.arange(len(blocker_counters))!=index) & (blocker_counters == 0)],
                                   index))
                       for index in np.arange(self.NB_PLAYERS)])
        return (signal_power, noise_power)

    def compute_signal_power_helper(self, index):
        return float(self.players[index].power) * 2*(self.players[index].channel_width)/ float(self.distSquare(index, index))

    def compute_noise_power_helper(self, index, fixed):
        return float(self.players[index].power*self.channel_overlap(index, fixed)) / float(self.distSquare(index, fixed))


    # square of the distance between transmitter i and receiver j
    def distSquare(self, i, j):
        return (self.players[i].t_x-self.players[j].r_x)**2 + (self.players[i].t_y-self.players[j].r_y)**2

    # how much of his total power transmitter i is overlapping on receiver j
    def channel_overlap(self, i, j):
        m_i = self.players[i].central_frequency-self.players[i].channel_width
        M_i = self.players[i].central_frequency+self.players[i].channel_width
        m_j = self.players[j].central_frequency-self.players[j].channel_width
        M_j = self.players[j].central_frequency+self.players[j].channel_width

        M = min(M_i, M_j)
        m = max(m_i, m_j)

        M = max(M, m_j)
        m = min(m, M_j)

        return float(M-m)

    def displayCumulativeResults(self, timestamp, plot):
        #plot.figure("Cumulative Results")
        plot.set_title("Cumulative Results")
        X = np.arange(timestamp)
        for i in range(self.NB_PLAYERS):
            plot.plot(X, np.cumsum(self.players[i].previous_successes[:timestamp]), label="Player "+str(self.players[i].id)+" - "+self.players[i].type, color=self.colors[i])
        plot.set_xlabel("timestep")
        plot.set_ylabel("cumulative success")
        plot.legend()

    def displayStepByStepResults(self, timestamp, plot):
        #plot.figure("Step by Step Results")
        plot.set_title("Step by Step Results")
        X = np.arange(timestamp)
        for i in range(self.NB_PLAYERS):
            plot.plot(X, self.players[i].previous_successes[:timestamp], label="Player "+str(self.players[i].id)+" - "+self.players[i].type, color=self.colors[i])
        plot.set_xlabel("timestep")
        plot.set_ylabel("success at each step")
        plot.legend()



    def displayLocationResults(self, timestamp, plot):
            #t_walk = np.array(obj.previous_t_positions)
            #r_walk = np.array(obj.previous_r_positions)
            #plt.xlim(np.min(np.array([np.array(p.previous_t_positions)[:, 0] for p in self.players])),
            #         np.max(np.array([np.array(p.previous_t_positions)[:, 0] for p in self.players]))

            #plt.ylim(min([np.min(t_walk[:, 1]), np.min(r_walk[:, 1])]), max([max(t_walk[:, 1]), max(r_walk[:, 1])]))
        # print(self.players)
        for p in self.players:
            t_walk = np.array(p.previous_t_positions[:])
            r_walk = np.array(p.previous_r_positions[:])
            line1 = plot.plot(t_walk[:, 0], t_walk[:, 1],'.-',label="player " + str(p.id) + " transmitter")[0]
            line2 = plot.plot(r_walk[:, 0], r_walk[:, 1],'.-',label= "player " + str(p.id) + "reciever")[0]
            for i in range(r_walk.shape[0]-1):
                xyp = (r_walk[i+1,0], r_walk[i+1, 1])
                xyb = (r_walk[i,0], r_walk[i, 1])
                plot.annotate(s='', xy = xyp, xytext = xyb, arrowprops=dict(arrowstyle='->', color = line2.get_color()))
            for i in range(t_walk.shape[0]-1):
                xyp = (t_walk[i+1,0], t_walk[i+1, 1])
                xyb = (t_walk[i,0], t_walk[i, 1])
                plot.annotate(s='', xy = xyp, xytext = xyb, arrowprops=dict(arrowstyle='->', color = line1.get_color()))
        plot.legend(loc='upper left')
        plot.set_title("Random Walk of Transmitter and Reciever")
        plot.set_ylabel("Longitude")
        plot.set_xlabel("Latitude")



    def displayChannelsOverTime(self, timestamp, plot):
        #plot.figure("Channels over time")
        plot.set_title("Channels over time")
        nb_steps = timestamp
        print(nb_steps)
        # print(len(self.players[0].previous_settings))
        # print(self.players[0].type)
        X = [i for i in range(nb_steps)]
        # for i in range(self.NB_PLAYERS):
        #     print(str(i))
        #     print(len(self.players[i].previous_settings))
        for i in range(self.NB_PLAYERS):
            print(str(i))
            print(len(self.players[i].previous_settings))
            lower_freq = [self.players[i].previous_settings[j][1]-self.players[i].previous_settings[j][2]*self.players[i].previous_settings[j][3] for j in range(nb_steps)]
            higher_freq = [self.players[i].previous_settings[j][1]+self.players[i].previous_settings[j][2]*self.players[i].previous_settings[j][3] for j in range(nb_steps)]
            plot.plot(X, lower_freq, self.colors[i]+self.symbols[i], label="Player "+str(self.players[i].id)+" - "+self.players[i].type)
            plot.plot(X, higher_freq, self.colors[i]+self.symbols[i])
            plot.fill_between(X, lower_freq, higher_freq, color=self.colors[i], alpha=.3)
            print("done")
        plot.set_xlabel("timestep")
        plot.set_ylabel("Channel (MHz)")
        plot.legend()


# display every visualization tool we have

    def displayResultsJupyter(self, timestamp = -666, figsize = (30,10)):
        if timestamp == -666:
            timestamp = int(self.curr_step / self.TIME_REFERENCE_UNIT)- 1
        f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=figsize)

        self.displayChannelsOverTime(timestamp, ax1)

        self.displayStepByStepResults(timestamp, ax2)

        self.displayLocationResults(timestamp, ax3)

        plt.show()

        #self.displayCumulativeResults(timestamp, ax3)
        #plt.show()

    def displayResults(self, figsize = (10,10)):
        f1, ax1 = plt.subplots(1, 1, figsize=figsize)
        f2, ax2 = plt.subplots(1, 1, figsize=figsize)
        # f3, ax3 = plt.subplots(1, 1, figsize=figsize)
        f4, ax4 = plt.subplots(1, 1, figsize=figsize)
        self.displayChannelsOverTime(int(self.curr_step / self.TIME_REFERENCE_UNIT), ax1)
        self.displayStepByStepResults(int(self.curr_step / self.TIME_REFERENCE_UNIT), ax2) #kind of useless for most cases
        # self.displayLocationResults(int(self.curr_step / self.TIME_REFERENCE_UNIT), ax3)
        self.displayCumulativeResults(int(self.curr_step / self.TIME_REFERENCE_UNIT), ax4)
        plt.show(ax4)

    def generatePlots(self, figsize = (10,10), name="default"):
        print("in gp %d %d"%(self.curr_step, self.TIME_REFERENCE_UNIT))
        f1, ax1 = plt.subplots(1, 1, figsize=figsize)
        # f2, ax2 = plt.subplots(1, 1, figsize=figsize)
        self.displayChannelsOverTime(int(self.curr_step / self.TIME_REFERENCE_UNIT), ax1)
        plt.savefig(name+"_channels.png")
        plt.close()
        # self.displayStepByStepResults(int(self.curr_step / self.TIME_REFERENCE_UNIT), ax2) #kind of useless for most cases
        # f3, ax3 = plt.subplots(1, 1, figsize=figsize)
        # self.displayLocationResults(int(self.curr_step / self.TIME_REFERENCE_UNIT), ax3)
        # plt.savefig(name+"_loc.png")
        # plt.close()
        f4, ax4 = plt.subplots(1, 1, figsize=figsize)
        self.displayCumulativeResults(int(self.curr_step / self.TIME_REFERENCE_UNIT), ax4)

        plt.savefig(name+"_cum.png")
        plt.close()

    def displayGif(self):
        gif(self.player_idlist, self.player_pos_record, self.player_frq_record)

# save the environment
    def save_environment(self, filename="last_environment.pkl"):
        with open("saved_environments/"+filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def save_results(self, filename="last_results.pkl"):
        results = []
        for i in range(len(self.players)):
            results.append([self.players[i].id, self.players[i].type, self.players[i].previous_successes, self.players[i].previous_settings])
        with open("saved_environments/"+filename, 'wb') as output:
            pickle.dump(results, output, pickle.HIGHEST_PROTOCOL)

    def load_results(self, filename="last_results.pkl"):
        filename = "saved_environments/"+filename
        if not Path(filename).is_file():
            print("ERROR: " + filename + " doesn't exist")
            return env_core([])
        with open(filename, 'rb') as input:
            results = pickle.load(input)
            # self.TIME_REFERENCE_UNIT = 1
            self.NB_PLAYERS = len(results)
            self.players = [Player(i, 0, 0, 0, 0) for i in range(self.NB_PLAYERS)]
            self.__init__(self.players)
            for i in range(self.NB_PLAYERS):
                self.players[i].type = results[i][1]
                self.players[i].previous_successes = results[i][2]
                self.players[i].previous_settings = results[i][3]
                # self.players[i].previous_t_positions = results[i][4]
                # self.players[i].previous_r_positions = results[i][5]
            self.curr_step = len(self.players[i].previous_successes)*self.TIME_REFERENCE_UNIT



# load a saved environment
    def load_environment(filename="last_environment.pkl"):
        filename = "saved_environments/"+filename
        if not Path(filename).is_file():
            print("ERROR: " + filename + " doesn't exist")
            return env_core([])
        with open(filename, 'rb') as input:
            return pickle.load(input)
