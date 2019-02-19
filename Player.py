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
    min_frequency = 1000 #represents the channel
    max_frequency = 1010 #represents the channel

    def __init__(self, t_x, t_y, r_x, r_y):
        self.t_x = t_x
        self.t_y = t_y
        self.r_x = r_x
        self.r_y = r_y

    def set_channel(self, min_f, max_f):
        self.min_frequency = min_f
        self.max_frequency = max_f

    def next_step(self, success): #to overwrite depending on the algorithm
        pass

    def update_positions(self, new_t_x, new_t_y, new_r_x, new_r_y):
      t_x = new_t_x
      t_y = new_t_y
      r_x = new_r_x
      r_y = new_r_y