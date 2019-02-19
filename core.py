# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 14:59:06 2019

@author: Alexandre
"""

class env_core:
    """
        This class simulates the environment core
    """
    players = [] #list of objects of class Player
    NB_PLAYERS = 0 #number of players = len(players)
    NB_STEPS = 100 #number of steps to play
    
    SNR_THRESHOLD = 1 #min SNR for success
    
    # initialize the core for a given set of players
    def __init__(self, players, nb_steps=100):
        self.players = players
        self.NB_PLAYERS = len(players)
        self.NB_STEPS = nb_steps
    
    def run_simulation(self):
        for i in range(self.NB_STEPS):
            self.next_step()
            
    # computes the success rate for every player and asks for next step    
    def next_step(self):
        success = self.computeSuccess()
        print(success) #logging the results
        for i in range(self.NB_PLAYERS):
            self.players[i].next_step(success[i])
    
    # from a given set of settings, compute the success rate of each player        
    def computeSuccess(self):
        success = []
        for i in range(self.NB_PLAYERS):
            signal = self.players[i].power / self.distSquare(i, i)
            noise = 0
            for j in range(self.NB_PLAYERS):
                if j!=i:
                    noise += self.players[j].power*self.overlap(j, i) / self.distSquare(j, i)
            
            # Success is determine by the comparison of SNR to a threshold
            if noise==0:
                success.append(1)
            else:
                SNR = signal / noise
                if SNR>self.SNR_THRESHOLD:
                    success.append(1)
                else:
                    success.append(0)
        return success
    
    # square of the distance between transmitter i and receiver j
    def distSquare(self, i, j):
        return (self.players[i].t_x-self.players[j].r_x)**2 + (self.players[i].t_y-self.players[j].r_y)**2
    
    # how much of his total power transmitter i is overlapping on receiver j
    def overlap(self, i, j):
        M = min(self.players[i].max_frequency, self.players[j].max_frequency)
        m = max(self.players[i].min_frequency, self.players[j].min_frequency)
        
        M = max(M, self.players[j].min_frequency)
        m = min(m, self.players[j].max_frequency)
        
        return (M-m)/(self.players[i].max_frequency - self.players[i].min_frequency)