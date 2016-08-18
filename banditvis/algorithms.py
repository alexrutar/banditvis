import numpy as np
from numpy.linalg import inv


def random(bandit, var_dict):
    """
    Choose arms randomly.

    Arm type support:
        * Bernoulli
        * Normal

    Visualization support:
        *
    """
    return np.random.randint(bandit.n_arms)


def greedy(bandit, var_dict):
    """
    Choose arms greedily.

    Arm type support:
        * Bernoulli
        * Normal

    Visualization support:
        *
    """
    return np.argmax(bandit.U)


def greedy_ep(bandit, var_dict):
    """
    Random with probability epsilon, else greedy.

    Arm type support:
        * Bernoulli
        * Normal

    Visualization support:
        *
    """
    if np.random.random() < var_dict['epsilon']:
        random(bandit, var_dict)
    else:
        greedy(bandit, var_dict)



def UCB(bandit, var_dict):
    """
    Upper Confidence Bound algorithm.

    Arm type support:
        * Bernoulli
        * Normal

    Visualization support:
        * ConfAnimation
    """
    index_type = var_dict['incr']
    alpha = var_dict['alpha']

    # now everything is a vector, and numpy does the operations to all of them at the same time
    bandit.U_conf = bandit.U + np.sqrt(alpha / bandit.T * np.log(index_type(bandit)))
    return(np.argmax(bandit.U_conf))



def UCB_KL(bandit, var_dict):
    """
    KL Upper Confidence Bound algorithm.

    Arm type support:
        * Bernoulli

    Visualization support:
        * ConfAnimation
    """

    # TODO find a way to vectorize this...
    # def v_f(x):  # vector version of f(x)
    #   zero_index = bandit.U == 0
    #   x[zero_index] = np.log(1/(1-x))
    #   x[invert(zero_index)] = bandit.U * np.log(bandit.U/x) + (1-bandit.U) * np.log((1-bandit.U)/(1-x)) - target
    #   return x
    def kl( p,q ):  # the KL entropy form; specified for p = 0 since numpy cannot properly evaluate the limit
        if p == 0:
            return( np.log(1/(1-q)))
        else:
            return( p * np.log(p/q) + (1-p) * np.log((1-p)/(1-q)) )

    def dkl( p,q ):  # the derivative of the KL entropy form with respect to q
        return( (q - p) / (q * (1-q)) )

    index_type = var_dict['incr']
    precision = 1.0/bandit.horizon[0]

    for i, (num, pulls, index) in enumerate(zip(bandit.U, bandit.T, index_type(bandit))):
        target = 1.0/pulls * np.log(index)
        if num == 1:
            bandit.U_conf[i] = 1
        else:
            if bandit.U_conf[i] == 1:
                bandit.U_conf[i] = num
            while True:
                if kl(num, bandit.U_conf[i]) < target:
                    bandit.U_conf[i] = (bandit.U_conf[i] + 1) * 0.5
                else:
                    break
            n = 1
            while n > precision:
                n = (kl(num, bandit.U_conf[i]) - target)/dkl(num, bandit.U_conf[i])
                bandit.U_conf[i] = bandit.U_conf[i] - n
    return np.argmax(bandit.U_conf)


def Bayes_Gauss(bandit, var_dict):
    """
    Bayes Gaussian Algorithm

    Note: for precision reasons, only accurate to a horizon of 5000!

    Arm type support:
        * Bernoulli
        * Normal

    Visualization support:
        * DistAnimation  # TODO - no support yet!
    """
    def npdf(x, mu, sigma):
        return 0.39894228 / sigma * 0.60653066**(((x-mu)/(sigma))**2)
    def ncdf(x, mu, sigma):
        return(1.0 / (1+np.e**(-0.07056*((x-mu)/(sigma))**3 - 1.5976*((x-mu)/(sigma)))))
    index_type = var_dict['incr']

    precision = 1.0 / bandit.horizon[0]
    for i, (num, pulls, index) in enumerate(zip(bandit.U, bandit.T, index_type(bandit))):

        if pulls == 0:
            bandit.U_conf[i] = 100000

        init = num
        mu = num
        sigma = np.sqrt(1.0/pulls)

        n = 1
        while n > precision or n * (-1) > precision:
            n = (ncdf(init, mu, sigma) - (1-1/index))/npdf(init, mu, sigma)
            init = init - n

        bandit.U_conf[i] = init

    return np.argmax(bandit.U_conf)

def TS_Beta(bandit, var_dict):
    """
    Beta Thompson Sampling algorithm

    Arm type support:
        * Bernoulli

    Visualization support:
        * DistAnimation  # TODO - no support yet!
    """
    return np.argmax(np.random.beta(bandit.arm_reward + 1, bandit.T - bandit.arm_reward + 1))

def TS_Gauss(bandit, var_dict):
    """
    Gaussian Thompson Sampling algorithm

    Arm type support:
        * Normal

    Visualization support:
        * DistAnimation  # TODO - no support yet!
    """
    mask = bandit.T == 0
    bandit.U_conf[mask] += 100000
    bandit.U_conf[np.invert(mask)] = np.random.normal(
        bandit.U,
        np.sqrt(1.0/bandit.T))
    return np.argmax(bandit.U_conf)


def UCB_Lin(bandit, var_dict):
    """
    Finite Linear Upper Confidence Bound algorithm

    Arm type support:
        * Linear

    Visualization support:
        * EllipseAnimation
    """
    rho = bandit.dim * np.log(bandit.timestep[0])
    bandit.U_conf = (np.inner(bandit.arm_vecs, bandit.U)
        + np.sqrt(rho * np.einsum('ij,ij->i',
            np.inner(bandit.arm_vecs,
            inv(bandit.G)), bandit.arm_vecs)))

    return np.argmax(bandit.U_conf)

def TS_Lin(bandit, var_dict):
    """
    Does Thompson Sampling from the multivariate distribution with mean
    bandit.U and covariance inv(bandit.G)
    """
    bandit.U_conf = np.einsum('ij,ij->i',
        np.random.multivariate_normal(
            bandit.U,
            inv(bandit.G),
            bandit.n_arms),
        bandit.arm_vecs)

    return np.argmax(bandit.U_conf)

def B1(bandit):
    return bandit.timestep

def B2(bandit):
    return bandit.horizon

def B3(bandit):
    return bandit.horizon / bandit.timestep

def B4(bandit):
    return bandit.timestep / bandit.T

def B5(bandit):
    return bandit.horizon / bandit.T

def B6(bandit):
    """
    * Makes a n * m matrix with every element sqrt(T_n / T_m)
    * Takes the minimum of that matrix and a matric of ones, element by element
    * Takes the sum down columns
    * Multiplies by original T element by element across rows
    * Divides the timestep by each element
    * adds 1
    """
    return 1 + bandit.timestep / (bandit.T * np.sum(
        np.minimum(
            np.ones((bandit.n_arms, bandit.n_arms)),
            (np.tile(np.array([bandit.T]).T, (1, bandit.n_arms))/bandit.T)),
        0))

def B7(bandit):
    """
    * Makes a n * m matrix with every element sqrt(T_n / T_m)
    * Takes the minimum of that matrix and a matric of ones, element by element
    * Takes the sum down columns
    * Multiplies by original T element by element across rows
    * Divides the timestep by each element
    * Takes the maximum of each element with respect to e
    """
    return np.maximum(np.e, bandit.timestep / (bandit.T * np.sum(
        np.minimum(
            np.ones((bandit.n_arms, bandit.n_arms)),
            (np.tile(np.array([bandit.T]).T, (1, bandit.n_arms))/bandit.T)),
        0)))

def B8(bandit):
    return bandit.horizon / (bandit.n_arms * bandit.T)

def B9(bandit):
    return bandit.timestep / (bandit.n_arms * bandit.T) + 1
