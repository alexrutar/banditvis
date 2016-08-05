import numpy as np


class BernoulliArm:
    """
    Arm with reward probabilty from a Bernoulli distribution.

    A BernoulliArm is called with a single argument: the mean (p). It returns a
    reward of 1 with probability p, and a reward of 0 with probability (1 - p).
    """
    def __init__(self, attr_list):
        self.mean = attr_list[0]
        self.info = ["Bernoulli", self.mean]

    def pull(self):
        if np.random.random() > self.mean:
            return 0
        return 1


class NormalArm:
    """
    A NormalArm selects rewards from a normal distribution.

    The mean and variance are provided during initialization.
    """
    def __init__(self, attr_list):
        self.mean = attr_list[0]
        self.variance = attr_list[1]
        self.info = ["Normal", self.mean, self.variance]

    def pull(self):
        return np.random.normal(self.mean, np.sqrt(self.variance))


class LinearArm:
    """
    A LinearArm selects rewards as a linear function of the arm and the mean.

    The arm vector and mean vector are provided as arguments; the reward from
    pulling a certain arm is given by the inner product of that vector and the
    mean vector plus some scalar sub-gaussian noise.

    Note that in the LinBandit declaration, the mean vector is passed to the
    LinearArm for use as the mean_vec.
    """
    def __init__(self, arm_vector):
        self.arm_vec = arm_vector
        self.dim = len(arm_vector)
        self.info = ["Linear", self.arm_vec]

    def pull(self):
        return np.inner(self.arm_vec, self.mean_vec) + np.random.normal(0,1)