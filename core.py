# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 14:59:06 2019
@author: Alexandre
"""

import numpy as np
import logging

class env_core:
    """
        This class simulates the environment core
    """
    players = [] #list of objects of class Player
    NB_PLAYERS = 0 #number of players = len(players)
    
    time_references = []
    TIME_REFERENCE_UNIT = 1
    current_successes = []
    current_noise_powers = []
    curr_step = 0
    
    SNR_THRESHOLD = 1 #min SNR for success
    

    # initialize the core for a given set of players
    def __init__(self, players, nb_steps=100, time_refs=[]):
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
        self.current_successes = np.zeros(self.NB_PLAYERS)
        self.current_noise_powers = np.zeros(self.NB_PLAYERS)
        
        self.initialization_steps()
        
        logging.basicConfig(filename="logfile.log", level=logging.DEBUG)
        

    def run_simulation(self, nb_steps):
        for i in range(nb_steps*self.TIME_REFERENCE_UNIT):
#            print(self.current_successes)
            self.next_step()

    # computes the success rate for every player and asks for next step
    def next_step(self):
        logging.debug("")
        logging.debug("step " + str(self.curr_step))
        
        (successes, noise_powers) = self.computeSuccess()
        self.current_successes += successes
        
        logging.debug("       |id| type |  pos_tx  |"\
                      + "  pos_rx  | central freq | bandwidth | action | result")
        for i in range(self.NB_PLAYERS):
            if self.time_references[i]==self.curr_step%self.TIME_REFERENCE_UNIT:
                self.players[i].next_step(self.current_successes[i]/self.TIME_REFERENCE_UNIT, noise_powers[i]/self.TIME_REFERENCE_UNIT)
                self.current_successes[i] = 0
                self.current_noise_powers[i] = 0

            self.players[i].log()
        self.curr_step += 1
    
    #initializes success and noise_power values for the initial settings    
    def initialization_steps(self):
        for j in range(self.TIME_REFERENCE_UNIT):
            (successes, noise_powers) = self.computeSuccess()
            self.current_successes += successes
            
            for i in range(self.NB_PLAYERS):
                if self.time_references[i]==j%self.TIME_REFERENCE_UNIT:
                    self.current_successes[i] = 0
                    self.current_noise_powers[i] = 0

    # from a given set of settings, compute the success rate of each player
    def computeSuccess(self):
        success = np.zeros(self.NB_PLAYERS)
        noise_power = np.zeros(self.NB_PLAYERS)
        for i in range(self.NB_PLAYERS):
            signal = float(self.players[i].power) / float(self.distSquare(i, i))
            noise = 0
            for j in range(self.NB_PLAYERS):
                if j!=i:
                    noise += float(self.players[j].power*self.overlap(j, i)) / float(self.distSquare(j, i))
            logging.debug("player " + str(self.players[i].id) + " signal " + str(signal) + \
                          " noise " + str(noise))
            # Success is determine by the comparison of SNR to a threshold
            if self.players[i].blocker_counter <= 0:
                if noise==0:
                    success[i] = 1
                else:
                    SNR = float(signal) / float(noise)
                    if SNR>self.SNR_THRESHOLD:
                        success[i] = 1
                    else:
                        success[i] = 0
                noise_power[i] = 0
            else: #in case of a player not trying to transmit, it receives the current power of noise overlapping on his channel
                success[i] = 0
                noise_power[i] = noise
        return (success, noise_power)

    # square of the distance between transmitter i and receiver j
    def distSquare(self, i, j):
        return (self.players[i].t_x-self.players[j].r_x)**2 + (self.players[i].t_y-self.players[j].r_y)**2

    # how much of his total power transmitter i is overlapping on receiver j
    def overlap(self, i, j):
        m_i = self.players[i].central_frequency-self.players[i].channel_width
        M_i = self.players[i].central_frequency+self.players[i].channel_width
        m_j = self.players[j].central_frequency-self.players[j].channel_width
        M_j = self.players[j].central_frequency+self.players[j].channel_width

        M = min(M_i, M_j)
        m = max(m_i, m_j)

        M = max(M, m_j)
        m = min(m, M_j)

        return float(M-m)/float(self.players[i].max_frequency - self.players[i].min_frequency)
