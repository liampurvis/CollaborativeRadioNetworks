# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 15:06:24 2019

@author: Alexandre
"""

class Player:
    t_x=0
    t_y=0 #position of the transmitter
    r_x=0
    r_y=1 #position of the receiver

    power = 1 #power of transmission
    central_frequency= 1005 #represents the channel
    channel_width = 5
    
    min_frequency = 1000 #represents the maximum bandwidth
    max_frequency = 1100
    
    previous_successes = [] #list of previous successes
    previous_settings = []
    
    blocker_counter = 0 #when settings have been changed, countdown is >0
    # no communication can be done while countdown > 0
    
    def __init__(self, t_x, t_y, r_x, r_y):
        self.t_x = t_x
        self.t_y = t_y
        self.r_x = r_x
        self.r_y = r_y
    
    def set_channel(self, central, width):
        self.central_frequency = central
        self.channel_width = width
        
        self.blocker_counter = 5      
    
    def next_step(self, success): #to overwrite depending on the algorithm
        self.previous_settings.append(success)
        self.save_setting()
        self.blocker_counter -= 1
        
        # TAKE ACTION HERE
        # if success >= 0, it means that the player tried to transmit something
        # if success < 0, it means that the player was listening. Success value 
        # corresponds to the current level of noise observed on the channel
        # in the < 0, success is NOT a reward. It can just be used for CSMA
    
    def save_setting(self):
        self.previous_settings.append((self.power, self.central_frequency, self.channel_width))