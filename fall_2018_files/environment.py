import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import stats

class radio_env:
    """
    This class allows us to simulate a session on the colosseum where we are
    transmitting a continuous stream of data, but checking 10x a second on our success
    and updating our channels (radio frequency choices). This is a textbook
    multi-armed bandit problem, and this class gies us an inteface to testv our
    algorithms.
    """

    def __init__(self, minutes = 10, channels = 15, num_players = 1, channel_params = [-1]):
        """
        initialization function
        Inputs:
        - minutes: the number of minutes we are able to transmit files over the radio.
        - channels: the number of channels we want to have in our simulated environment.
        """

        #this variable keeps track of how many times we have transmitted a file (pulled an arm)
        self.transmit_counter = 0

        #self.transmissions contains the total number of file transmissions we have to do.
        #Because we examine the success rate at a rate of ten times each second,
        #each minute gets 10*60 transmitions
        self.total_transmitions = minutes*60*10

        #self.channels contains the bernoulli parameter for each channel:
        self.channels = channel_params

        #this keeps track of each reward (continuous from 0-1) we got for our guesses
        #We automatically set values to -666 so we don't mix it up
        self.rewards = np.ones([self.total_transmitions, num_players])*(-666)

        # this variable keeps track of the guesses that were made
        self.guesses = np.ones([self.total_transmitions, num_players])*(-666)
        self.num_players = num_players
        if len(channel_params) == 1 and channel_params[0] == -1:
            self.channels = np.random.beta(a = 2, b = 2, size = channels)



    #tests whether time is left:
    def still_time(self):
        return self.transmit_counter < self.total_transmitions



    #When we want to transmit a file and see how much of it was sucessfully transmitted
    #(reward), then we call this  function:
    def transmit_file_get_reward(self, guesses = 0):
        """
        Inputs:
        - channel: the channel we are selecting

        Returns:
        - the percentage of the file that was successfully transmitted (reward)
        """
        if isinstance(guesses, int):
            guesses = np.array([guesses])
        else:
            guesses = np.array(guesses)
        #testing that everyone has made prediciton for this round:
        if guesses.size != self.num_players:
            raise ValueError("there needs to be a prediciton for each player! Given" +
                             str(guesses.size) + " predictions while there are " +
                             str(self.num_players) + " players")

        #testing that we still have time left in our session
        if self.transmit_counter >= self.total_transmitions:
            raise ValueError("Session ended! " + str(self.transmit_counter)
                       + " transmissions alread logged.")
            return

        #testing that channel parameter is a correct value:

        if ((np.sum(guesses < 0)>0)
            or (np.sum(guesses >= len(self.channels)) >0)):
            raise ValueError('channel parameter must be an int from 0 to ' +
                           str(len(self.channels) - 1) + " inclusive.")
            return

        curr_channel_params = self.update_params_with_conflicts(guesses)
        #print("guesses: " + str(guesses))
        #print("const_params" + str(self.channels))
        #print("curr params: " + str(curr_channel_params))
        for i in np.arange(guesses.size):
            #simulate file transmission
            curr_reward = self.simulate_file_recovery(p=curr_channel_params[guesses[i]])
            #update variables:
            self.rewards[self.transmit_counter, i] = curr_reward
            self.guesses[self.transmit_counter, i] = guesses[i]
        #print("rewards" + str(self.rewards[self.transmit_counter, :]))
        #print("**********************************")
        self.transmit_counter = self.transmit_counter + 1

        return


    def update_params_with_conflicts(self, guesses):
        if guesses.size <= 1:
            return self.channels
        (vals, counts) = np.unique(guesses, return_counts=True)
        channel_copy = np.copy(self.channels)
        #print("Constant params: " + str(channel_copy))
        channel_copy[vals] = channel_copy[vals]*(1/(2**(counts - 1)))
        #print("Updated current params: " + str(channel_copy))
        return channel_copy

    #This function simulates transmitting a file, and returns the rewards
    #(percentage transmitted correctly):
    def simulate_file_recovery(self, p = .5, n = 800,):
        """
        Input:
        - 'p' is the probabiity parameter for the binomial distribution
        - 'n' is the size parameter (number of bits attempted) for the binomial distribution
        (NOTE: n should be 80000, but I am making it a lot smaller as of now.
        See question/concern below.)
        Returns:
        - 'percentage' is the number of successful bits transferred,
        divided by the total number of bits attempted.

        Notes:
        Our target for the colosseum is to send about 1 mb (8,000,000 bits) per second.
        As reccomended by Laura Brink, we are sampling success rates about one hundred times per second.
        This means that for each section of bit-stream we examine will run to be about
        8,000 bits, hence the default of n = 8,000.

        QUESTION/CONCERN: With n being so high, the binomial distribution gives
        low variance values. Is there a better distribution/simulation to use?
        """
        return np.random.binomial(n, p)/n
