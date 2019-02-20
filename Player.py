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
    central_frequency= 1005
    channel_width = 5
    
    min_frequency = 1000 #represents the channel
    max_frequency = 1100 #represents the channel
    
    def __init__(self, t_x, t_y, r_x, r_y):
        self.t_x = t_x
        self.t_y = t_y
        self.r_x = r_x
        self.r_y = r_y
    
    def set_channel(self, central, width):
        self.central_frequency = central
        self.channel_width = width
    
    def next_step(self, success): #to overwrite depending on the algorithm
        pass