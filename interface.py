from Build.Core.core import *
from Build.Core.algorithm_types import *
from Build.Core.arm_classes import *
from Build.Core.simulation_class import *
from pprint import pprint

# sim1 = Simulation( \
# 	Bandit([BernoulliArm([0.2]), BernoulliArm([0.3])]), \
# 	Algorithm(algtype = UCB, incr = B7, alpha = 0.5) \
# 	)
# sim1.runStandard(500, 1000)




sim2 = Simulation( \
	LinBandit([LinearArm([1,-1]), LinearArm([0,1]), LinearArm([2,2])], [0.5,0.6]), \
	Algorithm(algtype = Lin_TS) \
	)
sim2.runStandard(500, 1000)

# sim2 = Simulation( \
# 	# Bandit([NormalArm([0.2,1]), NormalArm([0.3,1]), NormalArm([0.4,1]), NormalArm([0.5,1]), NormalArm([0.4,1]), NormalArm([0.4,1]),
# 	Bandit([BernoulliArm([0.2]), BernoulliArm([0.3])]), \
# 	Algorithm(algtype = TS_Beta, incr = B1) \
# 	)
# sim2.runStandard(500, 2000)
# sim2.runView(500)

