from regression import RegressionLearner
from supervisedlearner import SupervisedLearner
from bicycleregression import all_monomials_with_maximum_degrees
from perceptron import Perceptron
from knn import KNNClassifier
import numpy as np

import unittest


class IOTest(unittest.TestCase):

    def test_knn(self):
        knn_model = KNNClassifier(all_monomials_with_maximum_degrees([1, 1, 1]), 1)


        knn_model.train(np.array([[1], [10], [2], [30]]), np.array([1, 0, 1, 0]))
        self.assertEqual(
            knn_model._trained,
            True,
            "Initially False. Change this property to True after self.train() is called",
        )

        self.assertIn(
            type(knn_model.predict(np.array([1]))),
            (np.float64, float),
            "Return type of predict() is np.float64 or float",
        )


        self.assertIn(
            type(
                knn_model.evaluate(
                    np.array([[1], [10], [2], [20]]), np.array([1, 0, 1, 0])
                )
            ),
            (float, np.float64, int, np.int64),
            "Return type of evaluate() is np.float64 or float",
        )
        self.assertIn(
            knn_model.evaluate(
                np.array([[1], [10], [2], [30]]), np.array([1, 0, 1, 0])
            ),
            (1.0,1),
            "evaluate() for same data returns 1.0",
        )

    def test_regression(self):
        reg = RegressionLearner(all_monomials_with_maximum_degrees([1, 1, 1]))


        reg.train(
            np.array([[1, 2, 1], [6, 2, 5], [10, 11, 10], [20, 24, 21]]),
            np.array([1, 2, 5, 8]),
        )
        self.assertEqual(
            reg._trained,
            True,
            "Initially False. Change this property to True after train() is called",
        )

        self.assertIn(
            type(reg.predict(np.array([1, 2, 1]))),
            (np.float64, float),
            "Return type of predict() is np.float64 or float"
        )

        self.assertIn(
            type(
                reg.evaluate(
                    np.array([[1, 2, 1], [6, 2, 5], [10, 11, 10], [20, 24, 21]]),
                    np.array([1, 2, 3, 4]),
                )
            ),
            (np.float64, float),
            "Return type of evaluate() is np.float64 or float"
        )

    def test_perceptron(self):

        model = Perceptron()
        self.assertEqual(
            model._trained,
            False,
            "Initially False. Change this property to True after train() is called",
        )
        model.train(np.array([[1, 1], [10, 1]]), np.array([1, 0]))
        self.assertEqual(
            model._trained,
            True,
            "Initially False. Change this property to True after train() is called",
        )



        self.assertIn(
            type(model.predict(np.array([1,1]))),
            (np.float64, float ),
            "Return type of predict() is np.float64 or float"
        )

        self.assertIn(
            type(model.evaluate(np.array([[1,1], [10,1]]), np.array([1, 0]))),
            (float, np.float64,),
            "Return type of evaluate() is np.float64 or float"
        )


if __name__ == "__main__":
    unittest.main()
