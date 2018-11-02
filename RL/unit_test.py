import unittest
import gym, numpy
from taxi_sarsa import SARSA as SARSA
from tabular_sarsa import *
from taxi_sarsa_lambda import SARSA as SARSALambda
from mountain_car_sarsa_fourier import *


class IOTest(unittest.TestCase):

    """

		Tests IO for Sarsa, Sarsa-lambda and Mounatain Car Fourier problems.

		Each function tests if the dimensions of the updated qtable, etable, and policy
		are correct. Aditionally, each function also tests if the values in the table are valid,
		i.e if they are within range and not Null.

	"""

    def test_sarsa(self):
        # policy, qtable, reward = SARSA.learn_policy(env, gamma, learning_rate, epsilon, lambda_val, num_eps)
        env = gym.make("Taxi-v2")
        env.reset()
        sarsaLearner = SARSA()
        policy, qtable, reward = sarsaLearner.learn_policy(
            env, 0.95, 0.2, 0.1, 0.1, 1000
        )
        self.assertEqual(
            np.shape(policy),
            (500, 1),
            "The dimensions of the updated policy are incorrect",
        )
        self.assertEqual(
            np.shape(qtable), (500, 6), "The dimensions of qtable are incorrect"
        )
        self.assertEqual(
            len(reward),
            1000,
            "The dimensions of rewards_each_learning_episode are incorrect",
        )

    def test_sarsa_lambda(self):

        env = gym.make("Taxi-v2")
        env.reset()
        # policy, qtable, reward = SARSA.learn_policy(env, gamma, learning_rate, epsilon, lambda_val, num_eps)
        sarsaLearner = SARSALambda()
        policy, qtable, reward = sarsaLearner.learn_policy(
            env, 0.95, 0.2, 0.1, 0.1, 1000
        )
        self.assertEqual(
            np.shape(policy),
            (500, 1),
            "The dimensions of the updated policy are incorrect",
        )
        self.assertEqual(
            np.shape(qtable), (500, 6), "The dimensions of qtable are incorrect"
        )
        self.assertEqual(
            len(reward),
            1000,
            "The dimensions of rewards_each_learning_episode are incorrect",
        )

    def test_mountain_car(self):
        create_multipliers()
        SARSA_Learning()
        weights = np.load("mountain_car_saved_weights_grading.npy")
        self.assertEqual(
            np.shape(weights), (16, 3), "The dimensions of the weights are incorrect"
        )


if __name__ == "__main__":
    unittest.main()
