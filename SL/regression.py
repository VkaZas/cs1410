from supervisedlearner import SupervisedLearner
import numpy as np


class RegressionLearner(SupervisedLearner):

    """
    INSTANCE VARIABLES:

    All of those from SupervisedLearner, and self.weights, which is a 1D
    numpy array whose i'th element is the weight on the i'th feature function,
    learned when train(.) is called.
    """

    # Inherits initializer from SupervisedLearner

    def train(self, datapoints, labels):
        """
        :param datapoints: a 2D numpy array, in which each row is a datapoint,
                           without its label.
        :param labels: a 1D numpy array, in which the i'th element is the
                       correct label of the i'th datapoint.

        Does not return anything; only learns and stores as an instance variable,
        a list of weights for the regression model.
        The i'th weight should be the coefficient of the i'th feature.

        Note: The matrix A and the vector b are defined in the lecture slides.
        """
        X = np.array([self.compute_features(x) for x in datapoints])
        Xt = np.transpose(X)
        A = np.dot(Xt, X)
        b = np.dot(Xt, labels)
        self.weights = np.linalg.solve(A, b)

        self._trained = True

    def predict(self, x):
        """
        :param x: a
        Given a data point x, it produces the learner's estimate
        of f(x). Use self.weights and self.feature_funcs.
        """
        assert self._trained
        return np.dot(self.weights, self.compute_features(x))

    def evaluate(self, datapoints, labels):
        """
        :param datapoints: a 2D numpy array, in which each row is a datapoint,
                           without its label.
        :param labels: a 1D numpy array, in which the i'th element is the
                       correct label of the i'th datapoint.

        Returns the _average_ (not sum of) squared error (quadratic loss) of
        the model that is learned by train(), evaluated on the given datapoints.
        The regression learner aims to minimize this quantity.
        """
        assert self._trained
        return np.average([(self.predict(datapoints[i]) - labels[i]) ** 2 for i in range(len(datapoints))])
