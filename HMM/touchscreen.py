# Implement part 2 here!


class touchscreenHMM:

    # You may add instance variables, but you may not create a
    # custom initializer; touchscreenHMMs will be initialized
    # with no arguments.

    def __init__(self, width=20, height=20):
        """
        Feel free to initialize things in here!
        """
        self.width = width
        self.height = height
        # Write your code here!
        pass

    def sensor_model(self, observation, state):
        """
        Feel free to change the parameters of this function as you see fit.
        You may even delete this function! It is only here to point you
        in the right direction.

        This is the sensor model to get the probability of getting an observation from a state
        :param observation: A 2D numpy array filled with 0s, and a single 1 denoting
                            a touch location.
        :param state: A 2D numpy array filled with 0s, and a single 1 denoting
                        a touch location.
        :return: The probability of observing that observation from that given state, a number
        """
        # Write your code here!
        return None

    def transition_model(self, old_state, new_state):
        """
        Feel free to change the parameters of this function as you see fit.
        You may even delete this function! It is only here to point you
        in the right direction.

        This will be your transition model to go from the old state to the new state
        :param old_state: A 2D numpy array filled with 0s, and a single 1 denoting
                            a touch location.
        :param new_state: A 2D numpy array filled with 0s, and a single 1 denoting
                            a touch location.
        :return: The probability of transitioning from the old state to the new state, a number
        """
        # Write your code here!
        return None

    def filter_noisy_data(self, frame):
        """
        This is the function we will be calling during grading, passing in a noisy simualation. It should return the
        distribution where you think the actual position of the finger is in the same format that it is passed in as.

        DO NOT CHANGE THE FUNCTION PARAMETERS

        :param frame: A noisy frame to run your HMM on. This is a 2D numpy array filled with 0s, and a single 1 denoting
                    a touch location.
        :return: A 2D numpy array with the probabilities of the actual finger location.
        """
        # Write your code here!
        return frame

    """ 
    THE BELOW FUNCTION IMPLEMENTATIONS ARE OPTIONAL AND WILL BE SCORED AS EXTRA CREDIT
    
    YOU MAY CHOOSE TO IMPLEMENT ONE OF OR BOTH OF THESE FUNCTIONS 
    """

    def touchscreen_smoothing(self, time):
        """
        Takes in a timestep that is LESS THAN the current timestep and outputs a 
        probability distribution (represented as a 2D numpy array) over states for that timestep. 
        While it is not required to store previous states in your touchscreenHMM, using past
        observations wisely may improve the quality of your solution as well as trivialize the
        implementation of this function. Recall the definition of smoothing - your model may want 
        to update the distribution of previous states using new observations for better accuracy! 

        DO NOT CHANGE THE FUNCTION PARAMETERS

        :param time: the past timestep to get the observation distribution for, an integer
        :return: A 2D numpy array with the probabilities of the actual finger location.
        """
        # Write your code here!
        return None

    def touchscreen_prediction(self, time):
        """
        Takes in a timestep that is GREATER THAN the current timestep and outputs a 
        probability distribution (represented as a 2D numpy array) over states for that timestep.
        HINT: this function is similar to the 'ask' function you implemented in part 1. Think about
        how you can use the finger's direction and other information to improve your prediction.  
         
        DO NOT CHANGE THE FUNCTION PARAMETERS

        :param time: the past timestep to get the observation distribution for, an integer
        :return: A 2D numpy Array with the probabilities of the actual finger location.
        """
        # Write your code here!
        return None
