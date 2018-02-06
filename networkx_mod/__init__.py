"""
NetworkX
========

    NetworkX (NX) is a Python package for the creation, manipulation, and
    study of the structure, dynamics, and functions of complex networks.

    https://networkx_mod.lanl.gov/

Using
-----

    Just write in Python

    >>> import networkx_mod as nx
    >>> G=nx.Graph()
    >>> G.add_edge(1,2)
    >>> G.add_node(42)
    >>> print(sorted(G.nodes()))
    [1, 2, 42]
    >>> print(sorted(G.edges()))
    [(1, 2)]
"""
#    Copyright (C) 2004-2010 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
#
# Add platform dependent shared library path to sys.path
#

from __future__ import absolute_import
#import networkx_mod_mod as networkx_mod
import sys
if sys.version_info[:2] < (2, 7):
    m = "Python 2.7 or later is required for NetworkX (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

# Release data
from networkx_mod import release

__author__   = '%s <%s>\n%s <%s>\n%s <%s>' % \
              ( release.authors['Hagberg'] + release.authors['Schult'] + \
                release.authors['Swart'] )
__license__  = release.license

__date__ = release.date
__version__ = release.version

__bibtex__ = """@inproceedings{hagberg-2008-exploring,
author = {Aric A. Hagberg and Daniel A. Schult and Pieter J. Swart},
title = {Exploring network structure, dynamics, and function using {NetworkX}},
year = {2008},
month = Aug,
urlpdf = {http://math.lanl.gov/~hagberg/Papers/hagberg-2008-exploring.pdf},
booktitle = {Proceedings of the 7th Python in Science Conference (SciPy2008)},
editors = {G\"{a}el Varoquaux, Travis Vaught, and Jarrod Millman},
address = {Pasadena, CA USA},
pages = {11--15}
}"""

#These are import orderwise
from networkx_mod.exception import  *
import networkx_mod.external
import networkx_mod.utils

import networkx_mod.classes
from networkx_mod.classes import *


import networkx_mod.convert
from networkx_mod.convert import *

import networkx_mod.convert_matrix
from networkx_mod.convert_matrix import *


import networkx_mod.relabel
from networkx_mod.relabel import *

import networkx_mod.generators
from networkx_mod.generators import *

import networkx_mod.readwrite
from networkx_mod.readwrite import *

#Need to test with SciPy, when available
import networkx_mod.algorithms
from networkx_mod.algorithms import *
import networkx_mod.linalg

from networkx_mod.linalg import *
from networkx_mod.tests.test import run as test

import networkx_mod.drawing
from networkx_mod.drawing import *

