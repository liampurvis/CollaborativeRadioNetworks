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
        self.available_strategy = {}
    
    def set_channel(self, central, width):
        self.central_frequency = central
        self.channel_width = width
        
        self.blocker_counter = 5    
    
    def next_step(self, success): #to overwrite depending on the algorithm
        self.previous_successes.append(success)
        self.save_setting()
        self.blocker_counter -= 1
        
        # TAKE ACTION HERE
        # if success >= 0, it means that the player tried to transmit something
        # if success < 0, it means that the player was listening. Success value 
        # corresponds to the current level of noise observed on the channel
        # in the < 0, success is NOT a reward. It can just be used for CSMA
        if self.blocker_counter <= 0:
            if success >= 0:
                # determine if want to change setting or not
                #change_setting( etc )
                pass
            else:
                # determine if want to change setting or not
                pass
            return 1  # dummy return value to tell outside environment if we are acting this step or not
        else:
            return 0
    
    def save_setting(self):
        self.previous_settings.append((self.power, self.central_frequency, self.channel_width))

    def change_setting(self, new_power, new_central_frequency, new_channel_width):
        #
        save_setting()
        self.blocker_counter = 5  # reset internal counter
        self.power = new_power
        self.central_frequency = new_central_frequency
        self.channel_width = new_channel_width

    def CSMA_init(self, CSMA_mode, waiting_time_center, max_random_variance):
        CSMA_config(CSMA_mode, waiting_time_center, max_random_variance)
        self.available_strategy.append("CSMA")
        pass

    def CSMA_config(self,  CSMA_mode, waiting_time_center, max_random_variance):
        self.
        pass

    def UCB_init():
        UCB_config()
        self.available_strategy.append("UCB")
        pass

    def UCB_config():
        pass

    def Tompson_init():
        Tompson_config()
        self.available_strategy.append("Tompson")
        pass

    def Tompson_config():
        pass











