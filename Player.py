# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 15:06:24 2019

@author: Alexandre
"""
import numpy as np

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

    def set_channel(self, central, width = 5): # width default set to
        self.central_frequency = central
        self.channel_width = width

        self.blocker_counter = 5
    def log_last_step(self, success):
        self.previous_successes.append(success)
        self.save_setting()

        if self.blocker_counter != 0:
           self.blocker_counter -= 1

    def next_step(self, success): #to overwrite depending on the algorithm
        pass

    def save_setting(self):
        self.previous_settings.append((self.power, self.central_frequency, self.channel_width))

    def change_setting(self, new_central_frequency, new_channel_width = 5, new_power = 1,):
        #Setting default values
        self.save_setting()
        self.blocker_counter = 5  # reset internal counter
        self.power = new_power
        self.central_frequency = new_central_frequency
        self.channel_width = new_channel_width



class Random(Player):

  probability_of_changing_channel = .5

  def __init__(self, t_x, t_y, r_x, r_y, prob):
    super().__init__(t_x, t_y, r_x, r_y)
    self.probability_of_changing_channel = prob

  def next_step(self, success): #to overwrite depending on the algorithm
    self.log_last_step(success)
    # Randomly choose to seek new channel
    if np.random.binomial(n = 1, p = self.probability_of_changing_channel) == 1:
      # if so randmly generate new channel and switch to it.
      next_channel = np.random.randint(low = 1, high = 20)*5 + 1000
      self.change_setting(new_central_frequency = next_channel)













