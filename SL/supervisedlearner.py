from abc import ABCMeta, abstractmethod
import numpy as np

"""
DOCUMENTATION NOTE:

One can think of the supervised learning problem as estimating
some function f: X --> Y, which maps each input to a corresponding label. 
Throughout this stencil, we mean "f" to be the underlying function to be estimated.
"""


class SupervisedLearner:
    __metaclass__ = ABCMeta
    """
    INSTANCE VARIABLES: 

    - self.feature_funcs is a list of the feature functions to be used
      for training and predicting. Each takes a datapoint as a 1D array
      as input and outputs a real number.

    - self._trained is a boolean variable indicating whether the
      SupervisedLearner instance has been trained (i.e. the train
      method has been called) yet.
    """

    def __init__(self, feature_funcs):
        """
        :param feature_funcs: a list of feature functions
        """
        self.feature_funcs = feature_funcs
        self._trained = False

    # Implement this!
    def compute_features(self, x):
        """
        :param x: a single datapoint, without its label,
                  represented as a 1D numpy array.

        Returns a 1D numpy array (NOT a list) in which the i'th element is the
        output of the i'th feature function in self.feature_funcs applied to x.
        """
        return np.array([self.feature_funcs[i](x) for i in range(len(self.feature_funcs))])

    @abstractmethod
    def train(self, datapoints, labels):
        """
        :param datapoints: a 2D numpy array, in which each row is a datapoint,
                           without its label.
        :param labels: a 1D numpy array, in which the i'th element is the
                       correct label of the i'th datapoint.

        Learns and stores as instance variable(s) some representation that can
        be used to approximate f.
        """
        pass

    @abstractmethod
    def predict(self, x):
        """
        Given a data point x, produces the learner's estimate
        of f(x).

        In a classification problem, this will produce the label of a class.
        In a regression problem, this will produce a real number.
        """
        pass

    @abstractmethod
    def evaluate(self, datapoints, labels):
        """
        :param datapoints: a 2D numpy array, in which each row is a datapoint,
                           without its label.
        :param labels: a 1D numpy array, in which the i'th element is the
                       correct label of the i'th datapoint.

        Produces some metric that indicates how well the model learned by train()
        does at matching each datapoint in datapoints to its label
        """
        pass
