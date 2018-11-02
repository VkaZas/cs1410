import gym
import numpy as np
import random
import tabular_sarsa as Tabular_SARSA
import matplotlib.pyplot as plt


class SARSA(Tabular_SARSA.Tabular_SARSA):
    def __init__(self):
        super(SARSA, self).__init__()

    # TODO
    def learn_policy(
        self, env, gamma, learning_rate, epsilon, lambda_value, num_episodes
    ):
        """
        Implement Sarsa-lambda algorithm to update qtable, etable and learning policy.
        Input:
            all parameters
            
        Output: 
            This function returns the updated qtable, learning policy and the reward after each episode.
    
        """
        self.alpha = learning_rate
        self.epsilon = epsilon
        self.gamma = gamma
        self.lambda_value = lambda_value
        rewards_each_learning_episode = []
        for i in range(num_episodes):
            state = env.reset()
            action = self.LearningPolicy(state)
            episodic_reward = 0
            self.etable = np.zeros((self.num_states, self.num_actions))
            while True:
                next_state, reward, done, info = env.step(action)

                "*** Fill in the rest of the algorithm!! ***"

        np.save("qvalues_taxi_sarsa_lambda", self.qtable)
        np.save("policy_taxi_sarsa_lambda", self.policy)

        return self.policy, self.qtable, rewards_each_learning_episode

    def LearningPolicy(self, state):
        return Tabular_SARSA.Tabular_SARSA.learningPolicy(self, state)


if __name__ == "__main__":
    env = gym.make("Taxi-v2")
    env.reset()
    sarsaLearner = SARSA()
    policySarsa, QValues, episodeRewards = sarsaLearner.learn_policy(
        env, 0.95, 0.2, 0.1, 0.8, 10000
    )
    plt.plot(episodeRewards)
    plt.ylabel("rewards per episode")
    plt.ion()
    plt.savefig("rewards_plot_lambda.png")
    state = env.reset()
    env.render()
    while True:
        # print self.Sample(state, action)
        next_state, reward, done, info = env.step(sarsaLearner.policy[state, 0])
        env.render()
        print(reward)
        state = next_state
        if done:
            break
