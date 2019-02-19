import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import stats



class UCB_game:

    def __init__(self, minutes = 10, channels = 15, lamda = 1, n = 800):
        """
        initialization function
        Inputs:
        - minutes: the number of minutes we are able to transmit files over the radio.
        - channels: the number of channels we want to have in our simulated environment.

        Returns:
        -channel number to next be explored
        """
        self.channels = channels
        self.minutes = minutes
        self.lamda = lamda
        self.n = n


    def make_next_prediction(self, past_predictions, past_rewards):
        """
        initialization function
        Inputs:
        - past_predictions: array of the past_predictions made (which channel was predicted)
        - past_rewards: sequential list of rewards form past predictions.

        Returns:
        -channel number to next be explored
        """

        #base case when not all channels have been explored
        if sum(past_predictions != -666) < channels:
            for i in np.arange(channels):
                if sum(past_predictions == int(i)) < 1:
                    return int(i)
        #Getting parameter estimates plus confidence intervals, tuned by lamda
        UCB_args = [(past_rewards[past_predictions == int(i)].mean() +
                     self.lamda * self.get_95_Binomial_CI_length(n=sum(past_predictions == i)*self.n,
                                                    p_est=past_rewards[past_predictions == int(i)].mean()))
                    for i in np.arange(self.channels)]

        return int(np.argmax(UCB_args))



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




class thompson_game:

    def __init__(self, minutes = 10, channels = 15, a = 2, b = 2, n = 800):
        #fill me in
        self.minutes = minutes
        self.channels = channels
        #beta distributions of the posterior of each channel parameter
        self.a = np.ones(channels)*a
        self.b = np.ones(channels)*b
        #samples for each iteration:
        self.n = n

    def make_next_prediction(self, past_prediction, past_rewards):
        if (np.sum(past_prediction != -666) > 0):
            last = int(past_prediction[past_prediction != -666][np.sum(past_prediction != -666) - 1])
            #print(self.a[int(last)])
            self.update_posterior(last_prediction = last,
                                 curr_s = past_rewards[past_rewards != -666][np.sum(past_rewards != -666) - 1],
                                 curr_a = self.a[last],
                                 curr_b = self.b[last])
        return self.index_of_max_sample()


    def update_posterior(self, last_prediction, curr_a, curr_b, curr_s):
        #updating beta parameter 'a' via bayes rule:
        self.a[last_prediction] = curr_s + curr_a
        #updating beta parameter 'b' via bayes rule:
        self.b[last_prediction] = self.n - curr_s + curr_b
        return


    def index_of_max_sample(self):
        lst = []
        for i in np.arange(self.channels):
            lst.append(np.random.beta(a = self.a[i], b = self.b[i], size = 1))
        return int(np.argmax(np.array(lst)))


