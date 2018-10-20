from scipy.stats import norm
import numpy as np

from hmm import HMM


class suppliedModel:
    """
    A class containing the sensor_model and transition_model
    """

    def __init__(self):
        self.num_states = 4

    def char_to_int(self, letter):
        """
        converts a character to its corresponding place in the alphabet. For example, 'A' Is converted to 0
        """
        if not type(letter) is str:
            print("The input must be a string")
        if not len(letter) == 1:
            print("The letter must be a single letter")
        return ord(letter.lower()) - 97

    def sensor_model(self, observation, state):
        """
        Takes in a letter observation and a state to compute P(observation | state)
        """
        observation_index = self.char_to_int(observation)
        return norm.pdf(observation_index, loc=2 * state, scale=3)

    def transition_model(self, old_state, new_state):
        """
        Takes in two states to calculate P(new_state | old_state)
        """
        M = np.array(
            [[.5, .2, .1, .2], [.2, .5, .2, .1], [.1, .2, .5, .2], [.2, .1, .2, .5]]
        )
        return M[old_state, new_state]


class mismatchedObservations:
    """
    A class containing the sensor_model and transition_model
    Only Accepts observations 'A', 'B', and 'C' for simplicity
    """

    def __init__(self):
        self.num_states = 4

    def char_to_int(self, letter):
        """
        converts a character to its corresponding place in the alphabet. For example, 'A' Is converted to 0
        """
        if not type(letter) is str:
            print("The input must be a string")
        if not len(letter) == 1:
            print("The letter must be a single letter")
        return ord(letter.lower()) - 97

    def sensor_model(self, observation, state):
        """
        Takes in a letter observation and a state to compute P(observation | state)
        Only Accepts observations 'A', 'B', and 'C' for simplicity
        """
        observation_index = self.char_to_int(observation)
        M = np.array([[.5, .2, .3], [.4, .5, .1], [.1, .2, .7], [.1, .9, .0]])
        return M[state, observation_index]

    def transition_model(self, old_state, new_state):
        """
        Takes in two states to calculate P(new_state | old_state)
        """
        M = np.array(
            [[.5, .2, .1, .2], [.2, .5, .2, .1], [.1, .2, .5, .2], [.2, .1, .2, .5]]
        )
        return M[old_state, new_state]


if __name__ == "__main__":
    """
    Runs A REPL function where you can add observations as letters, and it returns the ask() value of the current
    timepoint. You Can also change the model to the mismatchedObservations model to hand simulate more easily!
    """
    model_instance = suppliedModel()
    my_HMM = HMM(
        model_instance.sensor_model,
        model_instance.transition_model,
        model_instance.num_states,
    )
    time = 0
    for i in range(10):
        observation = input("Enter an observation: \n")
        my_HMM.tell(observation)
        time += 1
        print(my_HMM.ask(time))
