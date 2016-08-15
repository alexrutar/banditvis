import numpy as np
from numpy.linalg import inv


class Bandit:

    """
    The basic Bandit class.

    The Bandit class defines the bandit itself. As an argument, it takes a list
    of arm objects, defining the behaviour of the environment. When the
    Bandit.pullArm(n) method is called, the n^th arm (indexed from 0) is
    pulled, updating various information stored within the bandit. This
    information is stored as follows:

        * Bandit.arms : list of arms objects within the bandit, which contains:
            * Bandit.arms[n].mean : the mean of the n^th arm
            * Bandit.arms[n].info : info about the n_th arm
        * Bandit.n_arms : number of arms that the Bandit has
        * Bandit.T : a vector storing the number of pulls of each arm
        * Bandit.U : a vector storing the cumulative average of each arm
        * Bandit.U_conf : the adjusted version of U [n] taking into account
            some confidence interval (not always used)
        * Bandit.timestep[0] : the number of timesteps that have passed so far
            (incremented with every arm pull)
            * Note : Bandit.timestep is a vector for use in algorithms
        * Bandit.total_reward : the total reward that the Bandit has
            accumulated so far
        * Bandit.arm_reward : the reward that each arm has so far
        * Bandit.reward : the reward that the Bandit recieved after the
            previous timestep

    The Bandit class also contains an interactive method called by
    Bandit.pullArm(n). The algorithm does the following:

        * pulls the n^th arm
        * increments T[n]
        * increments timestep
        * updates U[n] in a linear fashion (so that U[n] is simply an
            unweighted average of all previous rewards)
        * increments total_reward and arm_reward[n] to store the information

    The method Bandit.reset() reverts the Bandit to the original state in which
    it started, while still storing the arms; it resets tracking information.
    There is also a method called by Bandit.fullInfo(), which returns a large
    amount of information about the bandit. This is mostly good for trouble-
    shooting and examining the behaviour of the bandit in detail. Specifically,
    it gives the following information:

        * for each arm :
            * the mean of the distribution
            * the current system average
            * the number of pulls
            * confidence
        * the number of arms
        * the timestep
        * the horizon
        * the total reward
    """

    def __init__(self, arm_type_object):
        self.arms = arm_type_object
        self.n_arms = len(arm_type_object)
        self.T = np.zeros(self.n_arms, dtype=np.int)
        self.U = np.zeros(self.n_arms)
        self.U_conf = np.zeros(self.n_arms)
        self.timestep = np.zeros(self.n_arms, dtype=np.int)
        self.total_reward = 0
        self.arm_reward = np.zeros(self.n_arms, dtype=np.int)

        self.mean_list = np.array([self.arms[arm].mean
            for arm in range(self.n_arms)])



    def giveRegret(self):
        self.regret = 0
        for arm in range(self.n_arms):
            self.regret += self.T[arm] * (np.amax(self.mean_list) - self.arms[arm].mean)

        return(self.regret)


    def pullArm(self, arm):
        self.T[arm] += 1
        self.timestep += 1

        self.reward = self.arms[arm].pull()

        self.U[arm] = self.U[arm] + 1/self.T[arm] * (self.reward - self.U[arm])

        self.total_reward += self.reward
        self.arm_reward[arm] += self.reward

        return None


    def reset(self):  # resets everything in the bandit for re-use!
        self.T = np.zeros(self.n_arms, dtype=np.int)
        self.U = np.zeros(self.n_arms)
        self.U_conf = np.zeros(self.n_arms)
        self.timestep = np.zeros(self.n_arms, dtype=np.int)
        self.total_reward = 0
        self.arm_reward = np.zeros(self.n_arms, dtype=np.int)
        self.regret = 0

        return None


    def fullInfo(self):
        print("\n" + "+" + "-"*85 + "+")

        for arm in range(self.n_arms):
            print("| Arm {0}: mean ({1}) average reward ({2:f}), confidence "
                "({3:f}), called ({4}) times"
                .format(
                    arm,
                    self.arms[arm].mean,
                    self.U[arm],
                    self.U_conf[arm],
                    self.T[arm]))
        print("|\n| {0} arms, total reward ({1}), timestep ({2} / {3})"
            .format(
                self.n_arms,
                self.total_reward,
                self.timestep[0],
                self.horizon[0]))

        print("+" + "-"*85 + "+" + "\n")
        return None




class LinBandit:
    """
    The Linear Bandit class is very similar to the original Bandit class, in
    that it contains similar methods which do the same thing as the original
    Bandit. However, it differs in the way in which is stores averages, and
    takes different arm arguments.

    It takes a list of Linear arms and a vector mean to initialize.

    If the normalized option is True, it preserves vector direction but makes
    each vector unit length. It stores the following information internally:
        * self.normalized: boolean for normalized
        * self.mean: the vector mean
        * self.n_arms: the number of arms
        * self.T: the number of pulls of each arm
        * self.arms: the arm_object_list input
        * self.dim: dimension
        * self.arm_vecs: a list of the arm vectors
        * self.G: the gram matrix, initialized with the identity to ensure
            invertibility
        * self.U: the system average vector
        * self.A: the sum of arm vectors chosen multiplied by the scalar reward
            it recieved
        * self.U_conf: the confidence value for each arm
        * self.timestep: the timestep
    """
    def __init__(self, arm_object_list, vector_mean, normalized=False):
        self.normalized = normalized
        self.mean = vector_mean
        self.n_arms =  len(arm_object_list)
        self.T = np.zeros(len(arm_object_list), dtype = int)
        self.arms = arm_object_list
        self.dim = arm_object_list[0].dim
        self.arm_vecs = np.array([arm.arm_vec for arm in self.arms])
        self.G = np.identity(self.dim)  # .dim is the dimension
        self.U = np.zeros(self.dim)  # vector of averages
        self.A = np.zeros(self.dim)  # vectors of actions taken so far weighted by the reward
        self.U_conf = np.zeros(self.n_arms)
        self.timestep = np.zeros(self.n_arms, dtype=np.int)
        for arm in arm_object_list:
            arm.mean_vec = vector_mean
        if self.normalized:
            self.mean = self.mean/np.linalg.norm(self.mean)
            self.arm_vecs = np.array([arm/np.linalg.norm(arm) for arm in self.arm_vecs])
    def pullArm(self, arm):
        self.T[arm] += 1
        self.timestep += 1  # update timesetp

        # self.G is the sum of the products X X^T of the arm pulled in each round X
        self.G += np.outer(self.arm_vecs[arm], self.arm_vecs[arm])  # self.arm_vecs[arm] is the arm vector for a given [arm]

        # self.A is the sum of the arm vector pulled so far, scaled by the reward each pull resulted in
        self.A += self.arm_vecs[arm] * self.arms[arm].pull()

        # self.U is the "most likely" value of the mean vector; it is calculated based on least squares
        # update the reward approximation based on the inverse of G times the scaled sum of chosen arms
        self.U = np.dot(inv(self.G), self.A)

        return None

    def giveRegret(self):
        return (np.amax(np.dot(self.arm_vecs, self.mean)) * self.timestep[0] - np.dot(
            self.T,
            np.dot(self.arm_vecs, self.mean))
        )

    def reset(self):
        self.T = np.zeros(self.n_arms)
        self.G = np.identity(self.dim)  # .dim is the dimension
        self.U = np.zeros(self.dim)  # vector
        self.A = np.zeros(self.dim)  # vectors of actions taken so far weighted by the reward
        self.U_conf = np.zeros(self.n_arms)
        self.timestep = np.zeros(self.n_arms, dtype=np.int)
        return None

    def fullInfo(self):
        print("\n" + "+" + "-"*105 + "+")
        print("| Mean Vector: {}\n|".format(self.mean))
        print("| Gram Matrix: \n{}\n| ".format(self.G))
        for arm in range(self.n_arms):
            print("| Arm {0}: {1}, confidence ({2:f}), called ({3}) times\n| ".format(
                arm,
                self.arms[arm].arm_vec,
                self.U_conf[arm],
                self.T[arm])
            )
        print("Mean Reward Vector: {}".format(self.U))
        print("|\n| {0} arms,  timestep ({1} / {2})".format(
            self.n_arms,
            self.timestep[0],
            self.horizon[0])
        )
        print("+" + "-"*105 + "+" + "\n")
        return None

class Algorithm:
    """
    The Algorithm class specifies the behaviour of an algorithm.

    As an argument, it is passed a dictionary containing an 'algtype' key along
    with other keys.

    The Algorithm.giveArm() chooses an arm based on the internal state of the
    bandit or other factors. For a list of the supported algorithms and more
    detailed information, see the algorithm_types module.
    """
    def __init__(self, **variables):
        self.var_dict = variables

    def giveArm(self):
        return(self.var_dict['algtype'](self.bandit, self.var_dict))
