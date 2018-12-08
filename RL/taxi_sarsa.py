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
        Implement Sarsa algorithm to update qtable and learning policy.
        Input:
            all parameters
            
        Output: 
            This function returns the updated qtable, learning policy and the reward after each episode.
    
        """
        self.alpha = learning_rate
        self.epsilon = epsilon
        self.gamma = gamma
        rewards_each_learning_episode = []
        for i in range(num_episodes):
            state = env.reset()
            action = self.LearningPolicy(state)
            episodic_reward = 0
            while True:
                next_state, reward, done, info = env.step(action)  # take a random
                next_action = self.LearningPolicy(next_state)
                td_err = reward + self.gamma * self.qtable[next_state][next_action] - self.qtable[state, action]
                self.qtable[state][action] += self.alpha * td_err
                action = next_action
                state = next_state
                episodic_reward += reward
                if done:
                    break

            rewards_each_learning_episode.append(episodic_reward)



        np.save("qvalues_taxi_sarsa", self.qtable)
        np.save("policy_taxi_sarsa", self.policy)

        return self.policy, self.qtable, rewards_each_learning_episode

    def LearningPolicy(self, state):
        return Tabular_SARSA.Tabular_SARSA.learningPolicy(self, state)


if __name__ == "__main__":
    env = gym.make("Taxi-v2")
    env.reset()
    sarsaLearner = SARSA()
    policySarsa, QValues, episodeRewards = sarsaLearner.learn_policy(
        env, 0.95, 0.2, 0.1, 0.1, 1000
    )
    plt.plot(episodeRewards)
    plt.ylabel("rewards per episode")
    plt.ion()
    plt.savefig("rewards_plot_taxi_sarsa.png")
