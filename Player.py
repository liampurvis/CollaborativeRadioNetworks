# -*- coding: utf-8 -*-
"""
Player.py
"""
import numpy as np
import logging
import random
import math
from matplotlib import pyplot as plt

class Player:
    t_x=0
    t_y=0 #position of the transmitter
    r_x=0
    r_y=1 #position of the receiver



    power = 1 #power of transmission
    #central_frequency= 1005
    #channel_width = 5

    min_frequency = 1000 #represents the maximum bandwidth
    max_frequency = 1100

    previous_successes = [] #list of previous successes
    previous_settings = []

    blocker_counter = 0 #when settings have been changed, countdown is >0
    # no communication can be done while countdown > 0

    def __init__(self, id, t_x, t_y, r_x, r_y, starting_frequency = 1005, logfile="logfile.log"):
        self.t_x = float(t_x)
        self.t_y = float(t_y)
        self.r_x = float(r_x)
        self.r_y = float(r_y)
        self.id = id
        self.type = "FIX"
        self.previous_t_positions = []
        self.previous_r_positions = []

        self.power =1
        self.central_frequency=starting_frequency #represents the channel
        self.channel_width = 5 #represents the channel width
        self.blocker_counter = 0

        self.min_frequency = 1000
        self.max_frequency = 1100

        self.previous_successes = list()
        self.previous_settings = list()
        logging.basicConfig(filename=logfile, filemode="w", level=logging.DEBUG)

    # TODO : Why do we have set_channel and change_setting?
    def set_channel(self, central, width = 5, new_power=1): # width default set to
        if central!=self.central_frequency or width!=self.channel_width:
            self.save_setting()
            logging.debug("")
            logging.debug("--------------------------------------------------------------------------------")
            logging.debug("Player " + str(self.id) + " changed settings")
            logging.debug("Previous channel : ["+str(self.central_frequency-self.channel_width)+";"+str(self.central_frequency+self.channel_width)+"]")
            self.central_frequency = central
            self.channel_width = width
            self.power = new_power

            logging.debug("New channel : ["+str(self.central_frequency-self.channel_width)+";"+str(self.central_frequency+self.channel_width)+"]")
            logging.debug("--------------------------------------------------------------------------------")
            logging.debug("")

            self.blocker_counter = 4

    def log_last_step(self, success):
        self.previous_successes.append(success)
        self.save_setting()

        self.previous_t_positions.append([self.t_x, self.t_y])
        self.previous_r_positions.append([self.r_x, self.r_y])

        self.log()

        if self.blocker_counter != 0:
           self.blocker_counter -= 1

    def next_step(self, success, noise_power): #to overwrite depending on the algorithm
        self.log_last_step(success)

    def save_setting(self):
        if self.blocker_counter==0:
            not_blocked = 1
        else:
            not_blocked = 0
        self.previous_settings.append((self.power, self.central_frequency, self.channel_width, not_blocked))

    # change_settings IS DEPRECATED
    # please use set_channel
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
            result = "Pass" if self.previous_successes[-1] == 1 else "Fail"


        info = "Player" + "{:>5}".format(str(self.id)) + "   Type" + "{:>5}".format(self.type) + \
                "   pos_tx" + "{:>10}".format("(" + str(self.t_x) + ", " + str(self.t_y)+ ")") + \
                "   pos_rx" + "{:>10}".format("(" + str(self.r_x) + ", " + str(self.r_y)+ ")") + \
                "   CF" + "{:>7}".format(str(self.central_frequency)) + \
                "   BW" + "{:>4}".format(str(self.channel_width)) + \
                "   result" + "{:>5}".format(result)

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

  def __init__(self, id, t_x, t_y, r_x, r_y, starting_frequency = 1005, prob = .5, random_walk = False, nb_channels=10):
      super().__init__(id, t_x, t_y, r_x, r_y, starting_frequency)
      self.probability_of_changing_channel = prob
      self.type = "Random"
      self.random_walk = random_walk
      self.nb_channels = nb_channels

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
          next_channel = np.random.randint(low = 1, high = 10)*10 + 1005
          self.change_setting(new_central_frequency = next_channel)

class Thompsons(Player):
    def __init__(self, id, t_x, t_y, r_x, r_y, starting_frequency = 1005, a = 2, b = 2):
        super().__init__(id, t_x, t_y, r_x, r_y, starting_frequency)
        self.channels = np.arange(int((self.max_frequency - self.min_frequency)/(2*self.channel_width)))
        self.a = np.ones(len(self.channels))*a
        self.b = np.ones(len(self.channels))*b
        self.type = "Thompsons"


    def next_step(self, last_success, noise = 0):
        if self.blocker_counter == 0:
            self.log_last_step(last_success)
            curr_index = int((self.central_frequency - self.min_frequency)/(2*self.channel_width))
            self.update_posterior(last_prediction = curr_index,
                                 curr_s = last_success,
                                 curr_a = self.a[curr_index],
                                 curr_b = self.b[curr_index])
            next_channel = self.index_of_max_sample() * 10 + 1005
            # self.change_setting(new_central_frequency = next_channel)
            self.set_channel(next_channel, width=self.channel_width)
        else:
            self.log_last_step(last_success)

    def index_of_max_sample(self):
        lst = []
        for i in self.channels:
            lst.append(np.random.beta(a = self.a[i], b = self.b[i], size = 1))
        return int(np.argmax(np.array(lst)))

    def update_posterior(self, last_prediction, curr_a, curr_b, curr_s):
        #updating beta parameter 'a' via bayes rule:
        self.a[last_prediction] = curr_s + curr_a
        #updating beta parameter 'b' via bayes rule:
        self.b[last_prediction] = 1 - curr_s + curr_b
        return

    def get_means():
        return self.a/(self.a + self.b)

class CSMA(Player):

    # probability_of_changing_channel = .5
    csma_threshold = 1   # arbitrary threshold when CSMA consider to be low enough noise while listening. = self power / noise received
    sleeping_period = 3   # amount of time to just sleep, before start listening again
    probability_of_aggresion = 1.0  # probability that when see a window (while listening), this player would start transmitting
                                  # immediately
    sleeping_counter = 0

    current_state = 0
    # State machine, simple design
    # 0 = transmitting
    # 1 = sleeping
    # 2 = listening

    def __init__(self, id, t_x, t_y, r_x, r_y, threshold_input, sleeping_input, aggression_prob, starting_frequency = 1005):
        super().__init__(id, t_x, t_y, r_x, r_y, starting_frequency)
        # self.probability_of_changing_channel = prob
        self.csma_threshold = threshold_input
        self.sleeping_period = sleeping_input
        self.probability_of_aggresion = aggression_prob
        self.type = "CSMA"

        self.current_state = 2
        self.blocker_counter = 1

        self.saved_power = self.power
# For CSMA, since the simple method is only changing power (to denote switching on or off)
# it is not very necessary to impose another blocker counter for changing settings.
    def log(self):
        if not self.previous_successes:
            result = "None"
        else:
            result = "Pass" if self.previous_successes[-1] == 1 else "Fail"

        if self.blocker_counter==0:
            action="SEND"
        elif self.blocker_counter!=0 and self.sleeping_counter != 0:
            action="SLP"
        else:
            action="LIS"


        info = "Player" + "{:>5}".format(str(self.id)) + "   Type" + "{:>5}".format(self.type) + \
            "   pos_tx" + "{:>10}".format("(" + str(self.t_x) + ", " + str(self.t_y)+ ")") + \
                "   pos_rx" + "{:>10}".format("(" + str(self.r_x) + ", " + str(self.r_y)+ ")") + \
                "   CF" + "{:>7}".format(str(self.central_frequency)) + \
                "   BW" + "{:>4}".format(str(self.channel_width)) + \
                "   action" + "{:>5}".format(action) + \
                "   result" + "{:>5}".format(result)

        logging.debug(info)


    def change_pwr_instant(self, new_power = 1):
        #Setting default values
        self.save_setting()
        # self.blocker_counter = 5  # reset internal counter
        self.power = new_power
        self.saved_power = new_power
        # self.central_frequency = new_central_frequency
        # self.channel_width = new_channel_width

    def log_last_step(self, success):
        #This is a hacky fix, until we decide how to implement the movement scenarios
        self.previous_t_positions.append([self.t_x, self.t_y])
        self.previous_r_positions.append([self.r_x, self.r_y])

        self.previous_successes.append(success)
        self.save_setting()

        self.log()

        if self.sleeping_counter != 0:
           self.sleeping_counter -= 1
    def set_channel(self, central, width = 5, new_power=1): # width default set to
        if (central!=self.central_frequency or width !=self.channel_width):
            logging.debug("")
            logging.debug("--------------------------------------------------------------------------------")
            logging.debug("Player " + str(self.id) + " changed settings")
            logging.debug("Previous channel : ["+str(self.central_frequency-self.channel_width)+";"+str(self.central_frequency+self.channel_width)+"]")
            self.central_frequency = central
            self.channel_width = width

            logging.debug("New channel : ["+str(self.central_frequency-self.channel_width)+";"+str(self.central_frequency+self.channel_width)+"]")
            logging.debug("--------------------------------------------------------------------------------")
            logging.debug("")
            self.save_setting()

            self.sleeping_counter = 5
            self.current_state = 1
            self.blocker_counter = 1
            self.power = new_power
    def change_setting(self, new_central_frequency, new_channel_width = 5, new_power = 1):
        #Setting default values
        self.save_setting()
        self.sleeping_counter = 5  # reset internal counter
        self.current_state = 1
        self.blocker_counter = 1
        self.power = new_power
        self.saved_power = new_power
        self.central_frequency = new_central_frequency
        self.channel_width = new_channel_width

    def next_step(self, success, noise_power = 0): #to overwrite depending on the algorithm
        self.log_last_step(success)
        # if previous success is below a certain threshold, we
        # start CSMA and wait a certain period then try again

        dis = math.sqrt((self.t_x - self.r_x)**2 + (self.t_y - self.r_y)**2)
        pwr_thre = float(self.saved_power / dis**2)

        # And we are not in listening mode before, so we don't stuck
        # in a loop
        if self.current_state == 0:
            # print("in state 0")
            if success == 1:
                pass # do nothing
            else:
                self.change_pwr_instant(new_power = 0)
                if self.sleeping_period != 0:  # if in transmitting state
                    self.sleeping_counter = self.sleeping_period
                    self.current_state = 1  # change to sleeping state
                    self.blocker_counter = 1
                else:
                    self.current_state = 2  # change to listening state
                    self.blocker_counter = 1

        elif self.current_state == 1:  # if in sleeping state
            # print("in state 1")
            if self.sleeping_counter > 0:
                pass
            elif self.sleeping_counter == 0:
                self.current_state = 2  # change to listening state
                self.blocker_counter = 1

        elif self.current_state == 2:  # if in listening state
            # print("in state 2")
            if noise_power > self.csma_threshold * pwr_thre:
                # print("noise too large")
                if self.sleeping_period != 0:
                    self.sleeping_counter = self.sleeping_period
                    self.current_state = 1  # change to sleeping state
                    self.blocker_counter = 1
                else:
                    pass
            else:
                # print("noise small enough")
                chance = random.uniform(0, 1)
                if chance >= 1.0 - self.probability_of_aggresion:
                    self.current_state = 0
                    self.change_pwr_instant(new_power = 1)
                    self.blocker_counter = 0
                else:
                    if self.sleeping_period != 0:
                        self.sleeping_counter = self.sleeping_period
                        self.current_state = 1  # change to sleeping state
                        self.blocker_counter = 1
                    else:
                        pass
        else:
            self.current_state = 0
            change_pwr_instant(new_power=1)


class UCB(Player):
    past_predictions = []
    def __init__(self, id, t_x, t_y, r_x, r_y, nb_channels=15, lamda=1, starting_frequency = 1005):
        super().__init__(id, t_x, t_y, r_x, r_y, starting_frequency)

        self.type = "UCB"
        self.nb_channels = nb_channels
        self.lamda = lamda

        self.past_predictions = []
        self.past_predictions.append(0)

        self.previous_channels = []
        self.previous_rewards = []

        channel = np.random.randint(0, self.nb_channels)
        self.central_frequency = self.min_frequency + (self.max_frequency-self.min_frequency)*(channel+0.5)/self.nb_channels
        self.channel_width = (self.max_frequency-self.min_frequency)*0.5/self.nb_channels

        self.previous_estimations = []


    def make_next_prediction(self):
        """
        initialization function
        Inputs:
        - past_predictions: array of the past_predictions made (which channel was predicted)
        - past_rewards: sequential list of rewards form past predictions.
        Returns:
        -channel number to next be explored
        """
        #base case when not all channels have been explored TODO correct bug when counting explored channels
        chosen_channel = -1
        unchosen = []
        for i in range(self.nb_channels):
            # if self.past_predictions.count(i) < 1:
            if self.previous_channels.count(i) < 1:
                unchosen.append(i)
        if len(unchosen)>0:
            chosen_channel = unchosen[np.random.randint(0, len(unchosen))]

        # if self.blocker_counter != 0:
        #     return

        #Getting parameter estimates plus confidence intervals, tuned by lambda
        if chosen_channel==-1:
            UCB_args = []
            for i in range(self.nb_channels):
                # l = [self.previous_successes[j] for j in range(len(self.past_predictions)) if self.past_predictions[j] == i] # and self.previous_settings[j][3]==1
                l = [self.previous_rewards[j] for j in range(len(self.previous_channels)) if self.previous_channels[j] == i] # and self.previous_settings[j][3]==1
                l = l[-200:] #TODO reducing the number of inputs
                p_est = sum(l)/len(l)
                p_est = max(0.05, p_est) # fighting zero values which mess with confidence bounds
                p_est = min(p_est, 0.99) # fighting one values
                UCB_args.append((p_est + self.lamda * self.get_95_Binomial_CI_length(n=len(l), p_est=p_est)))

            #if the estimated reward for the current channel is more than 1, don't switch
            if UCB_args[self.channel()]>0.999:
                chosen_channel = self.channel()
            else:
                # choses a channel (number i) and converts it to a couple (central_frequency, width)
                chosen_channel = int(np.argmax(UCB_args))

            nb_results = UCB_args.count(UCB_args[chosen_channel])
            if nb_results>1: #random choice if same rewards
                randomC = np.random.randint(0, nb_results)
                ct = 0
                for i in range(self.nb_channels):
                    if UCB_args[i] == UCB_args[chosen_channel]:
                        if i == self.past_predictions[-1] and UCB_args[i]!=0: #stay on same channel if it is rewarding
                            break
                        else:
                            ct += 1
                    if ct-1==randomC:
                        break
                chosen_channel = i

            self.previous_estimations.append(UCB_args)
            # print("Player " + str(self.id) + " Channel " + str(chosen_channel) + ", estimated = " + str(UCB_args[chosen_channel]))

        central_frequency = self.min_frequency+(chosen_channel+0.5)*(self.max_frequency-self.min_frequency)*1.0/self.nb_channels
        width = (self.max_frequency-self.min_frequency)*0.5/self.nb_channels

        self.set_channel(central_frequency, width=width)
        self.past_predictions.append(chosen_channel)




    def get_95_Binomial_CI_length(self, n, p_est):
        """
        Input:
        - 'n' is the number of samples
        - 'p_est' is the current estimate of p
        Returns:
        - length of confidence interval with 95% certainty.
        calculation from:
        http://dept.stat.lsa.umich.edu/~kshedden/Courses/Stat485/Notes/binomial_confidence_intervals.pdf
        """
        return 2*2*np.sqrt((p_est*(1 - p_est))/n)

    def next_step(self, success, noise_power): #to overwrite depending on the algorithm

        # TAKE ACTION HERE
        # if success >= 0, it means that the player tried to transmit something
        # if success < 0, it means that the player was listening. Success value
        # corresponds to the current level of noise observed on the channel
        # in the < 0, success is NOT a reward. It can just be used for CSMA
        if self.blocker_counter == 0:
            self.previous_channels.append(int((self.central_frequency-self.min_frequency)//(2*self.channel_width)))
            self.previous_rewards.append(success)
            self.log_last_step(success)
            self.make_next_prediction()
        else:
            self.log_last_step(success)

    def channel(self):
        return int((self.central_frequency-self.min_frequency)/(2*self.channel_width))

    def displayEstimatedProbs(self):
        plt.figure()
        plt.title("Channels estimation over time - player "+str(self.id)+" "+self.type)
        nb_steps = len(self.previous_estimations)
        X = [i for i in range(nb_steps)]
        for i in range(self.nb_channels):
            Y = [self.previous_estimations[j][i] for j in range(len(self.previous_estimations))]
            plt.plot(X, Y, label="Channel " + str(i))
        plt.xlabel("timestep")
        plt.ylabel("Estimated reward")
        plt.legend()











