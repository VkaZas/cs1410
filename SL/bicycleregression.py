from regression import RegressionLearner
import numpy as np
from functools import reduce

# The data are pre-loaded here!
all_data = np.load("student_data.npy")
datapoints = all_data[:, :-1]
labels = all_data[:, -1]


def create_monomial_feature_func(exponents):
    """
    :param exponents: a list of 3 exponents

    If this function takes in [a, b, c] as input, it will
    return a function that takes in a numpy array [x1, x2, x3]
    and outputs x1^a * x2^b * x3^c

    For example:
    create_monomial_feature_func([1, 2, 3]) produces the function
    f(x, y, z) = x * y^2 * z^3 or, written in Python's lambda notation:
    lambda(x, y, z): x * (y ** 2) * (z ** 3)
    """

    def monomial_feature_func(x):
        raised_list = [
            component ** exponent for (component, exponent) in zip(x, exponents)
        ]
        return (2 ** sum(exponents)) * reduce((lambda a, b: a * b), raised_list)

    return monomial_feature_func


def all_monomials_with_maximum_degrees(max_exponents):
    """
    :param max_exponents: a list of natural numbers

    Returns a list containing all monomial functions in which the exponent
    of the i'th factor is no more than the i'th element of max_exponents

    For example:
    all_monomials_with_maximum_degrees([1, 2]) would return:
    [lambda(x, y): 1, lambda(x, y): x, lambda(x, y): y, lambda(x, y): x * y,
     lambda(x, y): y ** 2, lambda(x, y): x * y ** 2]
    """
    num_factors = len(max_exponents)
    monomial_degrees = {tuple([0] * num_factors)}

    def add_monomials(cur_exponents):
        for i in range(num_factors):
            if cur_exponents[i] < max_exponents[i]:
                new_exponents = cur_exponents[:]
                new_exponents[i] += 1
                new_exponents = tuple(new_exponents)
                if not (new_exponents in monomial_degrees):
                    monomial_degrees.add(new_exponents)
                    add_monomials(list(new_exponents))

    add_monomials([0] * num_factors)
    return [create_monomial_feature_func(exponents) for exponents in monomial_degrees]


# Finish implementing this!
def produce_regression_model():
    """
    Returns a pre-trained RegressionLearner that uses your
    regression model on calls to predict(.)
    """
    # Change the features!------------------------------------------------
    features = all_monomials_with_maximum_degrees([9, 1, 3])
    # ---------------------------------------------------------------------
    model = RegressionLearner(features)
    # Train your model here!----------------------------------------------
    # "model.train(...)"
    # ---------------------------------------------------------------------
    model.train(datapoints, labels)
    return model
