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

class env_core:
    """
        This class simulates the environment core
    """
    players = [] #list of objects of class Player
    NB_PLAYERS = 0 #number of players = len(players)

    time_references = []
    TIME_REFERENCE_UNIT = 10
    current_signal_powers = []
    current_noise_powers = []
    curr_step = 0

    SNR_THRESHOLD = 1 #min SNR for success
    
    player_idlist = [] 
    player_pos_record = {}
    player_frq_record = {}

    # initialize the core for a given set of players
    def __init__(self, players, nb_steps=100, time_refs=[], logfile="logfile.log"):
        self.players = players
        self.NB_PLAYERS = len(players)
        self.NB_STEPS = nb_steps

        #setting the time reference for each player
        #allows to have overlapping period of times
        if len(time_refs)!=self.NB_PLAYERS:
            for i in range(self.NB_PLAYERS):
                self.time_references.append(0)
        else:
            #self.time_references = time_refs.copy()
            self.time_references = time_refs[:]
        self.current_signal_powers = np.zeros(self.NB_PLAYERS)
        self.current_noise_powers = np.zeros(self.NB_PLAYERS)
        
        # self.initialization_steps()
        logging.basicConfig(filename=logfile, filemode="w", level=logging.DEBUG)
        for p in self.players:
            self.player_idlist.append(p.id)
            self.player_pos_record[p.id] = []
            self.player_frq_record[p.id] = []


    def run_simulation(self, nb_steps):
        for i in range(nb_steps*self.TIME_REFERENCE_UNIT):
#            print(self.current_successes)
            self.next_step()

    # computes the success rate for every player and asks for next step
    def next_step(self):
        logging.debug("step " + str(self.curr_step*1.0/self.TIME_REFERENCE_UNIT))

        (signal_powers, noise_powers) = self.computePowers()
        self.current_signal_powers += signal_powers
        self.current_noise_powers += noise_powers


        for i in range(self.NB_PLAYERS):
            if self.time_references[i]==self.curr_step%self.TIME_REFERENCE_UNIT:
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

    def computeSuccess(self, i):
        if (self.current_noise_powers[i]==0) or (self.current_signal_powers[i]/self.current_noise_powers[i] >= self.SNR_THRESHOLD):
            return 1
        else:
            return 0

    def computeNoisePower(self, i):
        return self.current_noise_powers[i] * 1.0 / self.TIME_REFERENCE_UNIT

    # from a given set of settings, compute the success rate of each player
    def computePowers(self):
        signal_power = np.zeros(self.NB_PLAYERS)
        noise_power = np.zeros(self.NB_PLAYERS)

        for i in range(self.NB_PLAYERS):
            signal = float(self.players[i].power) / float(self.distSquare(i, i))
            noise = 0
            for j in range(self.NB_PLAYERS):
                if j!=i and self.players[j].blocker_counter==0:
                    noise += float(self.players[j].power*self.channel_overlap(j, i)) / float(self.distSquare(j, i))
            # logging.debug("player " + str(self.players[i].id) + " signal " + str(signal) + \
            #               " noise " + str(noise))
            print(i)
            print(signal)
            print(noise)
            signal_power[i] = signal
            noise_power[i] = noise

        return (signal_power, noise_power)

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

        return float(M-m)/(2*self.players[i].channel_width)

    def displayCumulativeResults(self):
        plt.figure("Cumulative Results")
        plt.title("Cumulative Results")
        X = [i for i in range(len(self.players[0].previous_successes))]
        for i in range(self.NB_PLAYERS):
            plt.plot(X, np.cumsum(self.players[i].previous_successes), label="Player "+str(self.players[i].id))
        plt.xlabel("timestep")
        plt.ylabel("cumulative success")
        plt.legend()

    def displayStepByStepResults(self):
        plt.figure("Step by Step Results")
        plt.title("Step by Step Results")
        X = [i for i in range(len(self.players[0].previous_successes))]
        for i in range(self.NB_PLAYERS):
            plt.plot(X, self.players[i].previous_successes, label="Player "+str(self.players[i].id))
        plt.xlabel("timestep")
        plt.ylabel("success at each step")
        plt.legend()

# display every visualization tool we have
    def displayResults(self):
        self.displayCumulativeResults()
        self.displayStepByStepResults()
        plt.show()

    def displayGif(self):
        gif(self.player_idlist, self.player_pos_record, self.player_frq_record)
# save the environment
    def save_environment(self, filename="last_environment.pkl"):
        with open("saved_environments/"+filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

# load a saved environment
    def load_environment(filename="last_environment.pkl"):
        filename = "saved_environments/"+filename
        if not Path(filename).is_file():
            print("ERROR: " + filename + " doesn't exist")
            return env_core([])
        with open(filename, 'rb') as input:
            return pickle.load(input)

