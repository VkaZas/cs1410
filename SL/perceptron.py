import numpy as np


class Perceptron:
    def __init__(self):
        """

        :param lr: the rate at which the weights are modified at each iteration.

        """

        self.weights = None
        self.learning_rate = 1
        self._trained = False

    def step_function(self, inp):
        """

        :param inp: a real number
        :return: the predicted label produced by the given input
        
        Assigns a label of 1.0 to the datapoint if <w,x> is a positive quantity
        otherwise assigns label 0.0
        """
        return 1.0 if inp > 0 else 0.0

    def train(self, X, Y):
        """

        :param X: a 2D numpy array where each row represents a datapoint
        :param Y: a 1D numpy array where i'th element is the label of the corresponding datapoint in X
        :return: 
        
        Does not return anything; only learns and stores as instance variable self.weights a 1D numpy 
        array whose i'th element is the weight on the i'th feature. 
        """
        self.weights = np.zeros(len(X[0]))
        for _ in range(10):
            for i in range(len(X)):
                z = self.step_function(np.dot(self.weights, X[i]))
                if z != Y[i]:
                    self.weights += self.learning_rate * (Y[i] - z) * X[i]

        self._trained = True

    def predict(self, x):
        """
        :param x: a 1D numpy array represeing a single datapoints
        :return:
        
        Given a data point x, produces the learner's estimate
        of f(x). Use self.weights and self.step_function
        """

        assert self._trained
        return self.step_function(np.dot(self.weights, x))

    def evaluate(self, datapoints, labels):
        """

        :param datapoints: a 2D numpy array where each row represents a datapoint
        :param labels: a 1D numpy array where i'th element is the label of the corresponding datapoint in datapoints
        :return:

        Returns the fraction (between 0 and 1) of the given datapoints to which
        the method predict(.) assigns the correct label
        """

        assert self._trained
        results = np.array([self.predict(x) for x in datapoints])
        diff = np.array([1 if results[i] == labels[i] else 0 for i in range(len(results))])
        return np.sum(diff) / len(diff)
