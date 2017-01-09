"""
This module contains the various Bandit classes {StoBandit, LinBandit, AdvBandit} and the Algorithm
class.
"""

import numpy as np
from numpy.linalg import inv
from pprint import pprint

__all__ = ['StoBandit', 'LinBandit', 'AdvBandit', 'Algorithm']


class StoBandit:

    """
    This bandit class simulates a single-dimensional `Sto`chastic bandit.

    Positional Arguments:
        * arm object
    Attributes:
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
    Methods:
        * pullArm(arm): pull a specific arm
        * giveRegret(): calculate the current regret
        * reset(): reset all timestep-based properties
        * fullInfo(): print information about the bandit
    """

    def __init__(self, arm_object_list):
        self.arms = arm_object_list
        self.n_arms = len(arm_object_list)
        self.T = np.zeros(self.n_arms, dtype=np.int)
        self.U = np.zeros(self.n_arms)
        self.U_conf = np.zeros(self.n_arms)
        self.timestep = np.zeros(self.n_arms, dtype=np.int)

        self.mean_list = np.array([self.arms[arm].mean
            for arm in range(self.n_arms)])


    def giveRegret(self):
        return sum(self.T[i] * (np.amax(self.mean_list) - self.arms[i].mean) for i in range(self.n_arms))


    def pullArm(self, arm):
        self.T[arm] += 1
        self.timestep += 1
        self.U[arm] = self.U[arm] + 1/self.T[arm] * (self.arms[arm].pull() - self.U[arm])

        return None


    def reset(self):  # resets everything in the bandit for re-use!
        self.T = np.zeros(self.n_arms, dtype=np.int)
        self.U = np.zeros(self.n_arms)
        self.U_conf = np.zeros(self.n_arms)
        self.timestep = np.zeros(self.n_arms, dtype=np.int)
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
        print("|\n| {0} arms, regret ({1}), timestep ({2} / {3})"
            .format(
                self.n_arms,
                self.giveRegret(),
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

    Positional Arguments:
        * list of arm objects
        * vector mean
    Keyword Arguments:
        * normalized: boolean
    Attributes:
        * normalized: boolean for normalized (all vectors length 1)
        * mean: the vector mean
        * n_arms: the number of arms
        * T: the number of pulls of each arm
        * arms: the arm_object_list input
        * dim: dimension
        * arm_vecs: a list of the arm vectors
        * G: the gram matrix, initialized with the identity to ensure
            invertibility
        * U: the system average vector
        * A: the sum of arm vectors chosen multiplied by the scalar reward
            it recieved
        * U_conf: the confidence value for each arm
        * timestep: the timestep
    Methods:
        * pullArm(arm): pull a specific arm
        * giveRegret(): calculate the current regret
        * reset(): reset all timestep-based properties
        * fullInfo(): print information about the bandit
    """
    def __init__(self, arm_object_list, vector_mean, normalized=False):
        self.mean = vector_mean
        self.arms = arm_object_list
        self.arm_vecs = np.array([arm.arm_vec for arm in self.arms])
        self.normalized = normalized

        if self.normalized:
            self.mean = self.mean/np.linalg.norm(self.mean)
            self.arm_vecs = np.array([arm/np.linalg.norm(arm) for arm in self.arm_vecs])

        self.n_arms =  len(arm_object_list)
        self.T = np.zeros(len(arm_object_list), dtype = int)
        self.dim = arm_object_list[0].dim

        self.G = np.identity(self.dim)  # .dim is the dimension
        self.U = np.zeros(self.dim)  # vector of averages
        self.A = np.zeros(self.dim)  # vectors of actions taken so far weighted by the reward
        self.U_conf = np.zeros(self.n_arms)
        self.timestep = np.zeros(self.n_arms, dtype=np.int)

        # give each arm a vector mean
        for arm in arm_object_list:
            arm.mean_vec = vector_mean

    def pullArm(self, arm):
        self.T[arm] += 1
        self.timestep += 1  # update timesetp

        # self.G is the sum of the products X X^T of the arm pulled in each round X
        # self.arm_vecs[arm] is the arm vector for a given [arm]
        self.G += np.outer(self.arm_vecs[arm], self.arm_vecs[arm])

        # self.A is the sum of the arm vector pulled so far, scaled by the reward each pull resulted in
        self.A += self.arm_vecs[arm] * self.arms[arm].pull()

        # self.U is the "most likely" value of the mean vector; it is calculated based on least squares
        # update the reward approximation based on the inverse of G times the scaled sum of chosen arms
        self.U = np.dot(inv(self.G), self.A)

        return None

    def giveRegret(self):
        return np.amax(np.dot(self.arm_vecs, self.mean)) * self.timestep[0] - np.dot(
            self.T,
            np.dot(self.arm_vecs, self.mean)
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



class AdvBandit:
    def __init__(self, arm_object_list):
        self.arms = arm_object_list
        self.seq = np.array([arm.reward_vec for arm in self.arms])
        self.n_arms, self.horizon = self.seq.shape
        self.horizon = [self.horizon] * self.n_arms

        self.U = np.ones(self.n_arms)
        self.W = np.ones(self.n_arms)  # weights, updated by algorithm
        self.T = np.zeros(self.n_arms)
        self.pulled = np.full(self.seq.shape, False, dtype=bool)
        self.timestep = np.zeros(self.n_arms, dtype=np.int)


    def pullArm(self, arm):
        self.T[arm] += 1
        self.timestep += 1
        self.pulled[arm][self.timestep-1] = True

    def giveRegret(self):
        values = self.pulled * self.seq
        total_reward = np.sum(values)
        # the slice shortens the row by truncating any columns beyond the timestep
        best_arm_reward = np.amin(np.sum(self.seq[:,:self.timestep[0]], axis=1))  # compute the best arm loss
        return total_reward - best_arm_reward


    def reset(self):
        self.W = np.ones(self.n_arms)  # weights, updated by algorithm
        self.T = np.zeros(self.n_arms)
        self.pulled = np.full(self.seq.shape, False, dtype=bool)
        self.timestep = np.zeros(self.n_arms, dtype=np.int)
        self.loss_approx = np.zeros(self.n_arms, dtype=np.int)

    def fullInfo(self):
        print("\n" + "+" + "-"*85 + "+")

        for arm in range(self.n_arms):
            print("| Arm {0}: weight ({1:f}), called ({2}) times".format(
                arm,
                self.W[arm],
                self.T[arm]))
        print("|\n| {0} arms, regret ({1}), timestep ({2} / {3})"
            .format(
                self.n_arms,
                self.giveRegret(),
                self.timestep[0],
                self.horizon[0]))

        print("+" + "-"*85 + "+" + "\n")
        return None


class Bandit:
    def __init__(self, bandit_arm):
        self.seq, self.distr = bandit_arm.give()
        self.info = bandit_arm.info  # the pre-calculated reward sequences
        self.pulled = np.full_like(self.seq, False, dtype=bool)  # tells which arms were pulled in each round (boolean array)
        self.timestep = 0
        self.n_arms, self.horizon = self.seq.shape
        self.T = np.zeros(self.n_arms, dtype=int)
        return None

    def giveRegret(self):
        values = self.pulled * self.distr
        total_reward = np.sum(values)
        # the slice shortens the row by truncating any columns beyond the timestep
        best_arm_reward = np.amin(np.sum(self.distr[:,:self.timestep], axis=1))  # compute the best arm loss
        return total_reward - best_arm_reward

    def pullArm(self, arm):
        self.T[arm] += 1
        self.pulled[arm][self.timestep] = True
        self.timestep += 1
        return None

    def fullInfo(self):
        print("\n" + "+" + "-"*85 + "+")
        for i, sub_dict in enumerate(self.info):
            print('Arm {}, pulled {} times: {}'.format(i, self.T[i], sub_dict))
        print('Regret {}, Timestep {} / {}'.format(self.giveRegret(), self.timestep, self.horizon))
        print(self.seq)
        print(self.pulled)
        print(self.distr)
        print("+" + "-"*85 + "+" + "\n")

class Algorithm:
    """
    The Algorithm class specifies the behaviour of an algorithm.

    Positional Arguments:
        * list of arm objects
        * vector mean
    Keyword Arguments:
        * algtype: the algorithm function you want to use
        * kwargs: other necessary objects depending on the algorithm
    Attributes:
        * var_dict: stores kwargs passed
    Methods:
        * giveArm(arm): provides the 'best' arm based on the algorithm
    Caveats:
        * you must pass it a bandit object
    """
    def __init__(self, **variables):
        self.var_dict = variables

    def giveArm(self):
        return self.var_dict['algtype'](self.bandit, self.var_dict)
