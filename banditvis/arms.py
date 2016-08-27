"""
Contains all the arm classes.

Methods:
    * pull(): returns info about the arm
    * info(): pulls the arm
"""

import numpy as np

__all__ = ['BernoulliArm', 'NormalArm', 'LinearArm', 'GeneralArm', 'BanditArm']

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

class GeneralArm:
    def __init__(self, reward_vec):
        self.reward_vec = reward_vec
        self.mean = np.average(reward_vec)

    def info(self):
        return["General", self.mean]

    def pull(self, timestep):
        # fixes indexing
        return self.reward_vec[timestep-1]

class BanditArm:
    def __init__(self, horizon, seed=False):
        self.horizon = horizon
        self.seq = np.array([])
        self.info = []
        if seed:
            np.random.seed(seed)
    def give(self):
        return self.seq, self.info


    def add(self, arm_type, **kwargs):
        """
        class to build bandit arms
        Positional
        * arm_type

        Arm Type Dependencies:
            * Custom
                * input_
                * prperties

            * Stochastic
                * dist

            * Linear
                * arm_v
                * mean_v

        Sub Type Dependencies:
            * Bernoulli
                * mean
            * Normal
                * mean, variance
            * Beta
                * alpha
                * beta
        """
        if arm_type == 'Custom':
            self._addCustom(**kwargs)
        elif arm_type == 'Stochastic':
            self._addStochastic(**kwargs)
        elif arm_type == 'Linear':
            self._addLinear(**kwargs)
        else:
            raise AttributeError('BanditArm: {} armtype not recognized'.format(arm_type))

    def _add(self, new_vec):
        if self.seq.size:
            self.seq = np.vstack((self.seq, new_vec))
        else:
            self.seq = new_vec

    def _addStochastic(self, dist=None, mean=0, variance=1, alpha=1, beta=1):
        if dist == 'Bernoulli':
            self._addStochasticBernoulli(mean)
        elif dist == 'Normal':
            self._addStochasticNormal(mean, variance)
        elif dist == 'beta':
            self._addBeta(alpha, beta)
        else:
            raise ValueError("BanditArm: improper distribution")

    def _addCustom(self, input_=None, properties={}):
        # input: array_like or file path
        # define custom properties with additional kwargs, overwrites any existion definitions
        # use this to give your stuff nicer names, etc
        new_vec = np.loadtxt(input_)
        if len(new_vec.shape) == 1:
            x, = new_vec.shape
            if x == self.horizon:
                self._add(new_vec)
                self.info.append({**{'armtype': 'Custom', 'source': input_, 'mean': np.mean(new_vec)}, **properties})
            else:
                raise ValueError("BanditArm: array inconsistent with horizon")
        elif len(new_vec.shape) == 2:
            for row in new_vec:
                x, = row.shape
                if x == self.horizon:
                    self._add(row)
                    self.info.append({**{'armtype': 'Custom', 'source': input_, 'mean': np.mean(row)}, **properties})
                else:
                    raise ValueError("BanditArm: array inconsistent with horizon")
        else:
            raise ValueError("BanditArm: unrecognized input_ shape")
        return None

    def _addLinear(self, arm_v=None, mean_v=None, dist=None, noise=None, mean=0, variance=1):
        # support for vector noise coming later
        if dist == 'Normal':
            self._addLinearNormal(arm_v, mean_v, noise, mean, variance)

        elif dist == 'Bernoulli':
            self._addLinearBernoulli(arm_v, mean_v, noise, mean, variance)
        return None


    def _addStochasticNormal(self, mean, variance):
        self._add(np.random.normal(mean, np.sqrt(variance), size=self.horizon))
        self.info.append({'armtype': 'Stochastic Normal', 'mean': mean, 'variance': variance})
        return None

    def _addStochasticBernoulli(self, mean):
        self._add(np.random.binomial(1, mean, size=self.horizon))
        self.info.append({'armtype': 'Stochastic Bernoulli', 'mean': mean})
        return None

    def _addBeta(self, alpha, beta):
        self._add(np.random.beta(alpha, beta, size=self.horizon))
        self.info.append({'armtype': 'Stochastic Beta', 'alpha': alpha, 'beta': beta})
        return None


    def _addLinearBernoulli(self, arm_v, mean_v, noise, mean, variance):
        if noise == 'scalar':
            # scalar noise just extends each inner product by some noise, preserving direction
            self._add(np.inner(self.arm_vec, self.mean_vec) + np.random.bernoulli(1,mean, size=self.horizon))
        # elif noise == 'vector':
            # vector noise
            # self._add(np.inner(self.arm_vec, self.mean_vec + np.random.normal(mean, variance, size=self.horizon)))
        else:
            raise AttributeError('BanditArm: {} noise not recognized'.format(noise))
        self.info.append({'armtype': 'Linear Bernoulli', 'arm_vector': arm_v, 'mean_vector': mean_v, 'noise': noise, 'mean': mean})

    def _addLinearNormal(self, arm_v, mean_v, noise, mean, variance):
        if noise == 'scalar':
            # scalar noise just extends each inner product by some noise, preserving direction
            self._add(np.inner(self.arm_vec, self.mean_vec) + np.random.normal(mean, variance, size=self.horizon))
        # elif noise == 'vector':
            # vector noise
            # self._add(np.inner(self.arm_vec, self.mean_vec + np.random.normal(mean, variance, size=self.horizon)))
        else:
            raise AttributeError('BanditArm: {} noise not recognized'.format(noise))
        self.info.append({'armtype': 'Linear Normal', 'arm_vector': arm_v, 'mean_vector': mean_v, 'noise': noise, 'mean': mean, 'variance': variance})
        return None
