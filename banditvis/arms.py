"""
Contains all the arm classes.

Methods:
    * pull(): returns info about the arm
    * info(): pulls the arm
"""

import numpy as np

__all__ = ['BernoulliArm', 'NormalArm', 'LinearArm']

class BernoulliArm:
    """
    Arm with reward probabilty from a Bernoulli distribution.

    Positional Arguments:
        * attribute list [mean]
    Attributes:
        * mean: the mean of the random distribution
    Methods:
        * info(): returns info about the arm
        * pull(): pulls the arm

    Examples:

    >>> arm = banditvis.BernoulliArm([0.7])
    >>> arm.info()
    ['Bernoulli', 0.7]
    >>> arm.mean
    0.7
    """
    def __init__(self, attr_list):
        self.mean = attr_list[0]

    def info(self):
        return ["Bernoulli", self.mean]

    def pull(self):
        if np.random.random() > self.mean:
            return 0
        return 1


class NormalArm:
    """
    A NormalArm selects rewards from a normal distribution.

    Positional Arguments:
        * attribute list [mean, variance]
    Attributes:
        * mean: the mean of the random distribution
        * variance: the variance of the random distribution
    Methods:
        * info(): returns info about the arm
        * pull(): pulls the arm

    Examples:

    >>> arm = banditvis.NormalArm([0.7,1])
    >>> arm.info()
    ['Normal', 0.7, 1]
    >>> arm.mean
    0.7
    >>> arm.variance
    1
    """
    def __init__(self, attr_list):
        self.mean = attr_list[0]
        self.variance = attr_list[1]

    def info(self):
        return ["Normal", self.mean, self.variance]

    def pull(self):
        return np.random.normal(self.mean, np.sqrt(self.variance))


class LinearArm:
    """
    A LinearArm selects rewards as a linear function of the arm and the mean.

    Positional Arguments:
        * arm_vector
    Attributes:
        * arm_vec: the arm vector
        * dim: dimension
    Methods:
        * info(): returns info about the arm
        * pull(): pulls the arm
    Caveats:
        * you must manually add an arm_vec method; this is also added when added as an argument to
            a LinBandit object

    Examples:

    >>> arm = banditvis.LinearArm([1,2,3])

    We haven't contributed the mean_vec attribute, so we get an AttributeError:
    >>> arm.info()
    Traceback (most recent call last):
        ...
    AttributeError: 'LinearArm' object has no attribute 'mean_vec'

    Now everything is fine.
    >>> arm.mean_vec = [-1,0,1]
    >>> arm.info()
    ['Linear', [1, 2, 3], [-1, 0, 1]]
    >>> arm.dim
    3
    """
    def __init__(self, arm_vector):
        self.arm_vec = arm_vector
        self.dim = len(arm_vector)

    def info(self):
        return ["Linear", self.arm_vec, self.mean_vec]

    def pull(self):
        return np.inner(self.arm_vec, self.mean_vec) + np.random.normal(0,1)