# -*- coding: utf-8 -*-
"""
Player.py
"""
import numpy as np
import logging

class Player:
    t_x=0
    t_y=0 #position of the transmitter
    r_x=0
    r_y=1 #position of the receiver

    id = 0

    power = 1 #power of transmission
    central_frequency= 1005 #represents the channel
    channel_width = 5

    min_frequency = 1000 #represents the maximum bandwidth
    max_frequency = 1100

    previous_successes = [] #list of previous successes
    previous_settings = []

    previous_t_positions = []
    previous_r_positions = []

    blocker_counter = 0 #when settings have been changed, countdown is >0
    # no communication can be done while countdown > 0

    def __init__(self, id, t_x, t_y, r_x, r_y):
        self.t_x = float(t_x)
        self.t_y = float(t_y)
        self.r_x = float(r_x)
        self.r_y = float(r_y)
        self.id = id
        self.type = "FIX"
        logging.basicConfig(filename="logfile.log", level=logging.DEBUG)

    def set_channel(self, central, width = 5): # width default set to
        logging.debug("")
        logging.debug("--------------------------------------------------------------------------------")
        logging.debug("Player " + str(self.id) + " changed settings")
        logging.debug("Previous channel : ["+str(self.central_frequency-self.channel_width)+";"+str(self.central_frequency+self.channel_width)+"]")
        self.central_frequency = central
        self.channel_width = width

        logging.debug("New channel : ["+str(self.central_frequency-self.channel_width)+";"+str(self.central_frequency+self.channel_width)+"]")
        logging.debug("--------------------------------------------------------------------------------")
        logging.debug("")

        self.blocker_counter = 5

    def log_last_step(self, success):
        self.previous_successes.append(success)
        self.save_setting()

        if self.blocker_counter != 0:
           self.blocker_counter -= 1

    def next_step(self, success, noise_power): #to overwrite depending on the algorithm
        self.log_last_step(success)

        # TAKE ACTION HERE
        # if success >= 0, it means that the player tried to transmit something
        # if success < 0, it means that the player was listening. Success value
        # corresponds to the current level of noise observed on the channel
        # in the < 0, success is NOT a reward. It can just be used for CSMA

    def save_setting(self):
        self.previous_settings.append((self.power, self.central_frequency, self.channel_width))

    def change_setting(self, new_central_frequency, new_channel_width = 5, new_power = 1):
        #Setting default values
        self.save_setting()
        self.blocker_counter = 5  # reset internal counter
        self.power = new_power
        self.central_frequency = new_central_frequency
        self.channel_width = new_channel_width


    def log(self):
        if not self.previous_successes: 
            result = "None"
        else:
            result = "success" if self.previous_successes[-1] == 1 else "fail"
        info = "Player   " + str(self.id) + "  " + self.type + "   " + \
            "(" + str(self.t_x) + "," + str(self.t_y)+ ")" + "   " + \
            "(" + str(self.r_x) + "," + str(self.r_y)+ ")" + "      " + \
            str(self.central_frequency) + "           " + \
            str(self.channel_width) + "         "\
            "SEND" + "   " + \
            result

        logging.debug(info)

    def update_location(self, tx, ty, rx, ry):
        self.previous_t_positions.append([self.t_x, self.t_y])
        self.previous_r_positions.append([self.r_x, self.r_y])

        self.t_x = float(tx)
        self.t_y = float(ty)
        self.r_x = float(rx)
        self.r_y = float(ry)

class Random(Player):

  probability_of_changing_channel = .5

  def __init__(self, id, t_x, t_y, r_x, r_y, prob, random_walk = False):
      super().__init__(id, t_x, t_y, r_x, r_y)
      self.probability_of_changing_channel = prob
      self.type = "Random"
      self.random_walk = random_walk

  def next_step(self, success, noise_power = 0): #to overwrite depending on the algorithm
      self.log_last_step(success)
      if self.random_walk:
          self.update_location(tx = self.t_x + np.random.normal(0,1,1),
                              ty = self.t_y + np.random.normal(0,1,1),
                              rx = self.r_x + np.random.normal(0,1,1),
                              ry = self.r_y + np.random.normal(0,1,1))
      # Randomly choose to seek new channel
      if np.random.binomial(n = 1, p = self.probability_of_changing_channel) == 1:
          # if so randmly generate new channel and switch to it.
          next_channel = np.random.randint(low = 1, high = 20)*5 + 1000
          self.change_setting(new_central_frequency = next_channel)

class CSMA(Player):

  # probability_of_changing_channel = .5
  csma_threshold = 3   # arbitrary threshold where CSMA would consider start listening and switching
  waiting_period = 3

  def __init__(self, id, t_x, t_y, r_x, r_y, threshold_input, waiting_input):
    super().__init__(id, t_x, t_y, r_x, r_y)
    # self.probability_of_changing_channel = prob
    self.csma_threshold = threshold_input
    self.waiting_period = waiting_input

  def next_step(self, success, noise_power = 0): #to overwrite depending on the algorithm
    self.log_last_step(success)
    # if previous success is below a certain threshold, we
    # start CSMA and wait a certain period then try again

    # And we are not in listening mode before, so we don't stuck
    # in a loop
    if success < self.csma_threshold and success >= 0:
        self.blocker_counter = self.waiting_period










