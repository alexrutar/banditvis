"""
BanditVis

Simulate and visualize Bandit algorithms.

:copyright: (c) 2016 by Alex Rutar.
:license: MIT, see LICENSE for more details.
"""

__version__ = '0.2'

from banditvis.core import StoBandit, LinBandit, Algorithm
from banditvis.algorithms import *
from banditvis.arms import BernoulliArm, NormalArm, LinearArm
from banditvis.simulation import Simulation