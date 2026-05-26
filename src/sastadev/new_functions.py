"""
scratch file to add new functions while the system is running so we do not want to change files that are in use
"""
from sastadev import correctionlabels
from sastadev.macros import expandmacros
from sastadev.metadata import Meta
from sastadev.missing_det import get_missing_det
from sastadev.sastatypes import SynTree
from sastadev.sastatoken import Token

from sastadev.treebankfunctions import getattval, getnodeyield
from typing import List

gav = getattval



