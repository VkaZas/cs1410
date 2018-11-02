import copy
import numpy as np


class Tabular_SARSA(object):
    def __init__(
        self,
        num_states=500,
        num_actions=6,
        alpha=0.2,
        gamma=0.9,
        epsilon=0.25,
        lambda_value=0.9,
    ):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.lambda_value = lambda_value
        self.state = 0
        self.action = 0
        self.qtable = np.random.uniform(low=-1, high=1, size=(num_states, num_actions))
        self.etable = np.zeros((num_states, num_actions))
        self.policy = np.random.random_integers(num_actions, size=(num_states, 1))

    def set_lambda(self, lambda_value):
        self.lambda_value = lambda_value

    def set_gamma(self, gamma):
        self.gamma = gamma

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def set_alpha(self, alpha):
        self.alpha = alpha

    def write(self):
        "*** saving the numpy arrays for checking ***"
        np.save("qvalues", self.qtable)
        # for state in self.States:
        #     index = self.hashState(state)
        #     self.PolicyNumpy[index] = self.Policy[state]
        np.save("policy", self.policy)

    def learningPolicy(self, state):
        qmax = float("-inf")
        bestAction = None
        amaxes = []
        for action in range(self.num_actions):
            qval = self.qtable[state, action]

            if qval > qmax:
                amaxes = [action]
                qmax = qval
            elif qval == qmax:
                amaxes.append(action)
        nMaxes = len(amaxes)
        bestAction = amaxes[np.random.randint(nMaxes)]
        self.policy[state] = bestAction
        roll = np.random.random()
        if roll < self.epsilon:
            return np.random.randint(self.num_actions)
        return bestAction
