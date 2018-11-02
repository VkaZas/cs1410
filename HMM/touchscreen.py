import numpy as np


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
        self.ntime = 0
        self.nstate = 20 * 20 * 9
        self.dir = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [0, 0]]
        self.opposite = [4, 5, 6, 7, 0, 1, 2, 3, 8]
        self.F = {}
        for i in range(20):
            for j in range(20):
                for d in range(9):
                    self.F[(i, j, d)] = 0.

        self.alpha = 0.5

    def is_adjacent(self, state1, state2):
        return (state1[0] - state2[0]) ** 2 + (state1[1] - state2[1]) ** 2 <= 2

    def try_bounce(self, state):
        if not (0 <= state[0] < 20 and 0 <= state[1] < 20):
            op_dir = self.opposite[state[2]]
            nxt_state = self.forward(state, op_dir)
            return nxt_state
        else:
            return state

    def forward(self, state, d):
        return state[0] + self.dir[d][0], state[1] + self.dir[d][1], d

    def num_adjacent(self, state):
        cnt = 0
        for d in range(9):
            nxt_state = self.forward(state, d)
            nxt_state = self.try_bounce(nxt_state)
            if 0 <= nxt_state[0] < 20 and 0 <= nxt_state[1] < 20:
                cnt += 1
        return cnt

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
        last_state = self.forward(state, self.opposite[state[2]])
        last_state = self.try_bounce(last_state)

        [o_row], [o_col] = np.nonzero(observation)
        prob = np.zeros((20, 20))
        prob += (1 - self.alpha) / 400

        for d in range(9):
            nxt_state = self.forward(last_state, d)
            nxt_state = self.try_bounce(nxt_state)
            prob[nxt_state[0]][nxt_state[1]] += self.alpha / 18

        for d in range(9):
            nxt_state = self.forward(state, d)
            nxt_state = self.try_bounce(nxt_state)
            prob[nxt_state[0]][nxt_state[1]] += self.alpha / 18

        return prob[o_row][o_col]

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
        if not self.is_adjacent(old_state, new_state):
            return 0

        ideal_state = self.forward(old_state, old_state[2])
        ideal_state = self.try_bounce(ideal_state)

        for d in range(9):
            cand_state = self.forward(old_state, d)
            cand_state = self.try_bounce(cand_state)
            if new_state == cand_state:
                if new_state == ideal_state:
                    return self.alpha
                else:
                    return (1 - self.alpha) / 8

        return 0


    def filter_noisy_data(self, frame):
        """
        This is the function we will be calling during grading, passing in a noisy simualation. It should return the
        distribution where you think the actual position of the finger is in the same format that it is passed in as.

        DO NOT CHANGE THE FUNCTION PARAMETERS

        :param frame: A noisy frame to run your HMM on. This is a 2D numpy array filled with 0s, and a single 1 denoting
                    a touch location.
        :return: A 2D numpy array with the probabilities of the actual finger location.
        """
        self.ntime += 1
        print(self.ntime)
        [o_row], [o_col] = np.nonzero(frame)

        if self.ntime == 1:
            for d in range(9):
                self.F[(o_row, o_col, d)] = 1. / 9.
        else:
            tmp_F = {}

            for row in range(20):
                for col in range(20):
                    for d in range(9):
                        s = (row, col, d)
                        for nd in range(9):
                            ns = self.forward(s, nd)
                            ns = self.try_bounce(ns)
                            tmp_F[ns] = tmp_F.get(ns, 0) + self.sensor_model(frame, ns) * self.transition_model(s, ns) * self.F[s]

            self.F = tmp_F

        pred_frame = np.zeros((20, 20))
        for (row, col, d), v in self.F.items():
            pred_frame[row][col] += v
        pred_frame_sum = np.sum(pred_frame)
        for (row, col, d), _ in self.F.items():
            self.F[(row, col, d)] /= pred_frame_sum
        print(pred_frame_sum)
        pred_frame = pred_frame / np.sum(pred_frame)


        return pred_frame

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
