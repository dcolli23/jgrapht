"""Smoke testing for the Grapht repository"""

import os
import sys

ROOT = os.path.realpath(os.path.dirname(__file__))
PACKAGE_ROOT = os.path.join(ROOT, "..", "..", "..")
sys.path.append(PACKAGE_ROOT)
import grapht

DATA_ROOT = os.path.join(ROOT, "..", "data")
print (DATA_ROOT)

def test_default_parameter_placement():
  """Tests the placement of default parameters into a user-defined JSON structure"""

  default_trees = []
  default_tree_types = []
  user_specified_trees = []

  tree_folders = [dirs for dirs in os.listdir(DATA_ROOT) if
    os.path.isdir(os.path.join(DATA_ROOT, dirs))
    and dirs.startswith("tree_")
  ]
  


