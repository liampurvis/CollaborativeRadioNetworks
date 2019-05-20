# Collaboration and Competiton Between Multi-Armed Bandits 
## Discrete Optimization Across Shared Frequencies
## *Liam Purvis, Alexandre Brenelliere, Sean Ho, Ulysses Tang*

### Hypothesis and Goals
We sought to understand how different  multi-armed bandit algorithms  collaborated and competed in a shared environment with finite resources. Our initial hypothesis (based on preliminary simulations in a simple environment) were that:
UCB has the best performance from an individualistic perspective.
Thompson is better at collaborating and sharing bandwidth by some metrics.
Additionally, we sought to establish which combinations of algorithms  yielded the best results, both individually and collectively, as well as visualize the patterns these bandits fall into. 
We chose to simulate these interactions in an environment simulating radio transmissions, as the finite number of discrete frequencies this problem presents calls for the type of discrete optimization bandits are designed for.

### Methodology
#### Design of Environment:

We created a software environment that simulated radio transmission between players distributed over geospace. We selected a simplified loss model which determines signal strength based on transmitter power output and the squared distance between the listening point and the transmitter’s position and also used a simplified Signal-to-Noise ratio to determine whether certain messages are successfully delivered or not. The signal’s strength is determined by the transmitter’s power level and the distance in between, while the noise strength is determined by other transmitter-receiver pairs’ communication, treated as noises. If the SNR calculated is beyond a specified threshold, then the information is completely lost. 
At each timestep, whether or not a players message is communicated is determined by this model. If two players transmitted on the same channel at the same time, their message would fail to be received unless their physical coordinates were very distant from each other.
In bandit terms, each frequency is a discrete arm, and whether a message got through at time ‘t’ is a binary reward.
Finally, to simulate the cost of changing channels, decided to penalize a player if they changed channel by not letting them communicate for 4 timesteps.

#### Bandit Algorithms:
*UCB:* Balances explore and exploit by choosing channel with maximum reward plus confidence interval.
*Thompson:* Uses bayesian updates to randomly choose channels, according to the probability they are the best.
*Discounted:* Each Bandit had a variant which added decreasing weights to past rewards, to handle non-static environments
*CSMA:* Commonly-used industry standard. Uses randomized timesteps to listen to and send information.
*Random:* Benchmark for performance comparisons.

#### *Visualization of Environment:*
<img src="https://github.com/liampurvis/CollaborativeRadioNetworks/blob/master/readme_images/env.png" width="500" height="500" />

##### *Figure 1*

#### Design of Experiments:
We decided to see how these algorithms fared against each other in majority, equal, minority, and homogenous pairings. For each of these four different matches, we created static and non-static environments.
Required Number of Simulations Per Experiment:
We want to be able to detect average differences between algorithms of at least 3% with 95% confidence. We needed the variance of these players to compute the necessary sample size, so we ran a subset of our experiments, and plugged in the max variance which gave us a conservative estimate of n = 400. We ran 184,000 simulations.

### Results:
#### UCB and UCB-discounted perform best individually:
Here our initial hypothesis about UCB’s performance is confirmed. It performs much better than all other algorithms. Trailing behind it in second is Thompson, followed by CSMA and then our random benchmark. Please note that we bootstrapped 95% confidence intervals for these estimates, giving us bounds of +/- .01. In short, the confidence intervals are so narrow that the dots encompass them.
#### *Individual Success Across All Simulations*
<img src="https://github.com/liampurvis/CollaborativeRadioNetworks/blob/master/readme_images/meta_results.png" width="500" height="400" />

##### *Figure 2 (Note: confidence intervals are +/- .01%)*


#### By Some Collaborative Metrics Thompson’s Performs Much Better:
Here we see the performance of the second-worst player in simulations where the algorithm associated with the histogram is present. As we can see, both UCB and CSMA are very stratifying algorithms: they are likely to have multiple players who don’t transmit any information with some strong winners. Likewise, Thompson and Random both do a much better job of ensuring players can get adequate rewards.

<img src="https://github.com/liampurvis/CollaborativeRadioNetworks/blob/master/readme_images/thompson_collaboration_1.png" width="500" height="400" />

<img src="https://github.com/liampurvis/CollaborativeRadioNetworks/blob/master/readme_images/thompson_collaboration_2.png" width="500" height="400" />

##### *Figure 3*

#### Time to Stabilization:
Observing Figure 1, UCB swiftly settles on a channel, while Thompson takes more time steps to to find a channel to stick with. This happens both at the start of the simulation and after changes to the channel capacity.

#### Thompson Unable to Adjust to Penalties:
Suprisingly, Thompson does worse in an unconstrained environment, while random behaves as expected. Thompson likely amasses penalties as it changes between equally optimal channels. With algorithmic adjustments for penalties Thompson could perform much better.

<img src="https://github.com/liampurvis/CollaborativeRadioNetworks/blob/master/readme_images/Thompson_failures.png" width="500" height="400" />

##### *Figure 4*

#### Heatmap of Minority/Majority Performance: 
In this heatmap, entry (i, j) corresponds to the individual normalized reward of algorithm i when added to an environment that contains a majority of algorithm j, Here we can see that UCB variants perform best against any type of player.

<img src="https://github.com/liampurvis/CollaborativeRadioNetworks/blob/master/readme_images/heatmap.png" width="500" height="400" />

##### *Figure 5*


### Conclusion:
*UCB:* By most metrics, UCB is the optimal choice individually or collectively.
*Thompson:* In a few collaborative metrics Thompsons beats UCB. Additionally, Thompson is uniquely effected by the penalty of switching channels. If we made a few algorithmic changes to account for this, it’s performance would likely significantly increase. Additionally, from figure 1, we can see that Thompson takes longer to stabilize on a channel. 
*Discounted:* One average, discounted variants perform better than  the original. This is to be expected, as sharing resources between randomized players inherently leads to the nonstatic dynamics.

### Acknowledgements:
Thanks to Dr. Sahai and Dr. Warzynek for their guidance.

If you would like to read more of our results, please check out our final paper pdf in this repository.
