from supervisedlearner import SupervisedLearner
import numpy as np


class KNNClassifier(SupervisedLearner):
    def __init__(self, feature_funcs, k):
        super(KNNClassifier, self).__init__(feature_funcs)
        self.k = k
        self.X = None
        self.Y = None

    def train(self, anchor_points, anchor_labels):
        """
        :param anchor_points: a 2D numpy array, in which each row is
                              a datapoint, without its label, to be used
                              for one of the anchor points

        :param anchor_labels: a 1D numpy array in which the i'th element is the correct label
                              of the i'th datapoint in anchor_points

        Does not return anything; simply stores anchor_labels and the
        _features_ of anchor_points.

        Hint: You should use the compute_features method of SupervisedLearner!
        """
        self._trained = True
        self.X = np.array([self.compute_features(x) for x in anchor_points])
        self.Y = anchor_labels

    def euclidean_distance(self, x1, x2):
        return np.linalg.norm(x1 - x2)

    def predict(self, x):
        """
        Given a single data point, x, represented as a 1D numpy array,
        predicts the class of x by taking a plurality vote among its k
        nearest neighbors in feature space. Resolves ties arbitrarily.

        The K nearest neighbors are determined based on Euclidean distance
        in _feature_ space (so be sure to compute the features of x).


        Returns the label of the class to which the data point x is predicted to belong.
        """
        assert self._trained
        x_feat = self.compute_features(x)
        dists = np.array([self.euclidean_distance(xi, x_feat) for xi in self.X])
        k_neighbors = dists.argsort()[:self.k]

        votes = [self.Y[idx] for idx in k_neighbors]
        (val, cnt) = np.unique(votes, return_counts=True)
        return val[np.argmax(cnt)] * 1.0

    def evaluate(self, datapoints, labels):
        """
        :param datapoints: a 2D numpy array, in which each row is a datapoint.
        :param labels: a 1D numpy array, in which the i'th element is the
                       correct label of the i'th datapoint.

        Returns the fraction (between 0 and 1) of the given datapoints to which
        the method predict(.) assigns the correct label
        """
        assert self._trained
        results = np.array([self.predict(x) for x in datapoints])
        diff = np.array([1 if results[i] == labels[i] else 0 for i in range(len(results))])
        return np.sum(diff) / len(diff)
