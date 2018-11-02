import numpy as np


class HMM:

    # You may add instance variables, but you may not change the
    # initializer; HMMs will be initialized with the given __init__
    # function when grading.

    def __init__(self, sensor_model, transition_model, num_states):
        """
        Inputs:
        - sensor_model: the sensor model of the HMM.
          This is a function that takes in an observation E
          (represented as a string 'A', 'B', ...) and a state S
          (reprensented as a natural number 0, 1, ...) and
          outputs the probability of observing E in state S.

        - transition_model: the transition model of the HMM.
          This is a function that takes in two states, s and s',
          and outputs the probability of transitioning from
          state s to state s'.

        - num_states: this is the number of hidden states in the HMM, an integer
        """
        # Initialize your HMM here!
        self.O = sensor_model
        self.T = transition_model
        self.num_states = num_states
        self.F = np.array([1.0 / num_states for i in range(num_states)])
        self.time_stamp = 0

    def tell(self, observation):
        """
        Takes in an observation and records it.
        You will need to keep track of the current timestep and increment
        it for each observation.

        Input:
        - observation: The observation at the current timestep, a string

        Output:
        - None
        """
        # Write your code here!
        self.time_stamp += 1
        tmp_F = np.zeros(self.num_states)
        for k in range(self.num_states):
            tmp_F[k] = self.O(observation, k) * np.sum([self.T(i, k) for i in range(self.num_states)] * self.F)

        self.F = tmp_F / np.linalg.norm(tmp_F, ord=1)

    def ask(self, time):
        """
        Takes in a timestep that is greater than or equal to
        the current timestep and outputs a probability distribution
        (represented as a list) over states for that timestep.
        The index of the probability is the state it corresponds to.

        Input:
        - time: the timestep to get the observation distribution for, an integer

        Output:
        - a probability distribution over the hidden state for the given timestep, a list of numbers
        """
        # Write your code here!
        pred_F = np.copy(self.F)

        for i in range(time - self.time_stamp):
            tmp_F = np.zeros(self.num_states)
            for cur in range(self.num_states):
                for prev in range(self.num_states):
                    tmp_F[cur] += pred_F[prev] * self.T(prev, cur)
            pred_F = tmp_F

        return list(pred_F)

