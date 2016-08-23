"""
BanditVis

Simulate and visualize Bandit algorithms.

:copyright: (c) 2016 by Alex Rutar.
:license: MIT, see LICENSE for more details.
"""

__version__ = '0.2'

from banditvis.manager import run
from banditvis.core import StoBandit, LinBandit, AdvBandit
from banditvis.algorithms import *
from banditvis.arms import BernoulliArm, NormalArm, LinearArm
from banditvis.simulation import Simulation