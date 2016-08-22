from sys import stdout
import time
from .algorithms import *
from .arms import *
from .core import *

from pprint import pprint


class Simulation:

    """
    The Simulation class combines the Bandit - Algorithm interaction.

    It stores various information about the interaction, and it contains
    various execution methods which are useful depending on the context, and
    various file output methods that are called by other files that need to
    simulate a bandit and access the saved data.

    TODO:
    * what else to track? total reward, calculate regret, ...

    """

    def __init__(self, bandit_inst, algorithm_inst):
        """
        Initializes the Simulation class, and passes certain attributes so that
        Bandit objects and Algorithm objects have acces to certain information.
        """
        self.alg = algorithm_inst
        self.bandit = bandit_inst
        self.alg.bandit = bandit_inst
        self.total_regret = 0
        self.iterations = 0
        self.arm_info = [each_arm.info for each_arm in self.bandit.arms]


    def reset(self):
        """
        Resets the Simulation class the Bandit subclass.
        """
        self.iterations = 0
        self.total_regret = 0
        self.bandit.reset()


    def _print_info(self):
        """
        Prints out information about the Simulation.

        The 'try' statement attempts to print out the .__name__ attribute of
        functions, rather than the object itself; if it fails, it falls back to
        just printing the object itself
        """
        print("\nAverage Regret: {0}".format(
            self.total_regret / self.iterations))

        for i in self.alg.var_dict:
            try:
                print("{0} : {1}".format(i, self.alg.var_dict[i].__name__))
            except AttributeError:
                print("{0} : {1}".format(i, self.alg.var_dict[i]))

        print("{0} Arms: {1}".format(self.bandit.n_arms, self.arm_info))
        print("Horizon: {0}".format(self.horizon))
        print ("Total runtime: {0} seconds".format(self.runtime))
        print ("Average runtime per iteration: {0} seconds".format(
            self.runtime / self.iterations))
        print("\n" + "-"*50 + "\n")
        return None


    def runStep(self, num, horizon):
        """
        Runs the Simulation for one step.

        This method is called during animations.
        """
        self.bandit.horizon = np.full(self.bandit.n_arms, horizon, dtype = int)
        self.horizon = horizon

        for m in range(num):
            self.bandit.pullArm(self.alg.giveArm())
        return None


    def runView(self, horizon):
        """
        Runs a single iteration to a horizon of n and prints out information.

        runView is especially useful for debugging bandit algorithms or seeing
        everything in significant detail as the bandit runs.
        """
        self.bandit.horizon = np.full(self.bandit.n_arms, horizon, dtype = int)
        self.horizon = horizon

        start_time = time.clock()
        for m in range(self.bandit.n_arms):
            self.bandit.pullArm(m)
            self.bandit.fullInfo()
        for m in range(horizon - self.bandit.n_arms):
            self.bandit.pullArm(self.alg.giveArm())
            self.bandit.fullInfo()
        stop_time = time.clock()

        self.total_regret += self.bandit.giveRegret()
        self.iterations += 1
        self.bandit.reset()
        self.runtime = stop_time - start_time
        self._print_info()
        return None


    def runStandard(self, horizon, cycles):
        """
        A standard experiment-running method.

        Runs the bandit for a certain number of cycles each to a certain
        horizon, and prints out the result on screen.

        It uses _print_info to print information about the bandit itself upon
        termination.
        """
        self.bandit.horizon = np.full(self.bandit.n_arms, horizon, dtype = int)
        self.horizon = horizon

        print("-"*50 + "\n")
        start_time = time.clock()

        for i in range(cycles):
            for i in range(self.bandit.n_arms):
                self.bandit.pullArm(i)

            for l in range(horizon - self.bandit.n_arms):
                self.bandit.pullArm(self.alg.giveArm())

            self.total_regret += self.bandit.giveRegret()
            self.iterations += 1
            self.bandit.reset()

            stdout.write(
                "\r----------  "
                "{0:d} out of {1} cycles"
                "----------".format(self.iterations, cycles))
            stdout.flush()

        stop_time = time.clock()
        self.runtime = stop_time - start_time
        self._print_info()
        return None


    def runHist(self, horizon, cycles, out_file):
        """
        Produces Histogram - like data.

        Every cycle, prints the bandit regret it out in the file, followed by a
        newline. These data files are used by many other methods containing
        hist in their name.
        """
        self.bandit.horizon = np.full(self.bandit.n_arms, horizon, dtype = int)
        self.horizon = horizon

        for i in range(cycles):
            for j in range(self.bandit.n_arms):
                self.bandit.pullArm(j)

            for l in range(horizon - self.bandit.n_arms):
                self.bandit.pullArm(self.alg.giveArm())

            self.total_regret += self.bandit.giveRegret()
            self.iterations += 1

            with open(out_file, "a") as outfile:
                outfile.write("{0}\n".format(self.bandit.giveRegret()))
            self.bandit.reset()
        return None


    def runVar(self, horizon, cycles, out_file):
        """
        Produces Variable - like data.

        Runs the simulation for a certain number of cycles, then appends that
        data to the text file
        """
        self.bandit.horizon = np.full(self.bandit.n_arms, horizon, dtype = int)
        self.horizon = horizon

        for i in range(cycles):
            for i in range(self.bandit.n_arms):
                self.bandit.pullArm(i)

            for l in range(horizon - self.bandit.n_arms):
                self.bandit.pullArm(self.alg.giveArm())

            self.total_regret += self.bandit.giveRegret()
            self.iterations += 1

            self.bandit.reset()

        with open(out_file, "a") as outfile:
            outfile.write("{0}\n".format(self.total_regret/self.iterations))
        return None

    def selfCheck(self):
        """
        Checks the simulation for errors
        """
        errors = ""
        return errors

class ObjectDict:
    ArmDict = {
        'Bernoulli' : BernoulliArm,
        'Normal' : NormalArm,
        'Linear' : LinearArm
    }
    AlgDict = {
        'var_dict' : {},
        'random' : random,
        'greedy' : greedy,
        'greedy_ep' : greedy_ep,
        'UCB' : UCB,
        'UCB_KL' : UCB_KL,
        'TS_Beta' : TS_Beta,
        'TS_Gauss' : TS_Gauss,
        'Bayes_Gauss' : Bayes_Gauss,
        'UCB_Lin' : UCB_Lin,
        'TS_Lin' : TS_Lin
    }
    IndexDict = {
        'B1' : B1,
        'B2' : B2,
        'B3' : B3,
        'B4' : B4,
        'B5' : B5,
        'B6' : B6,
        'B7' : B7,
        'B8' : B8,
        'B9' : B9
    }


def ReMapSim(sim_dict):
    """
    Takes a simulation dictionary and turns string names into objects. It uses
    the ObjectDict class in order to create references to the actual objects.
    """
    for alg_key in list(sim_dict['Algorithm'].keys()):
        if alg_key == 'incr':
            sim_dict['Algorithm'][alg_key] = \
                ObjectDict.IndexDict[sim_dict['Algorithm'][alg_key]]
        elif alg_key == 'algtype':
            sim_dict['Algorithm'][alg_key] = \
                ObjectDict.AlgDict[sim_dict['Algorithm'][alg_key]]

    sim_dict['Algorithm'] = Algorithm(**sim_dict['Algorithm'])
    sim_dict['arm_object_list'] = [ObjectDict.ArmDict[arm[0]](arm[1])
        for arm in sim_dict['Bandit']['ArmList']]

    # different parsing for Linear and non-Linear bandits
    if sim_dict['Bandit']['ArmList'][0][0] == 'Linear':
        sim_dict['vector_mean'] = sim_dict['Bandit']['MeanVector']
        sim_dict['Bandit'] = LinBandit(
            sim_dict['arm_object_list'],
            sim_dict['vector_mean'],
            normalized=sim_dict['Normalized'])
        del[sim_dict['vector_mean']]
    else:
        sim_dict['Bandit'] = Bandit(sim_dict['arm_object_list'])

    sim_dict['Simulation'] = Simulation(
        sim_dict['Bandit'],
        sim_dict['Algorithm'])

    # clean up residual keys
    del[sim_dict['Bandit']]
    del[sim_dict['Algorithm']]
    del[sim_dict['arm_object_list']]

    return None
