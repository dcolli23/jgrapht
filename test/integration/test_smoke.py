"""Smoke testing for the Grapht repository"""

import os
import sys
import json

ROOT = os.path.realpath(os.path.dirname(__file__))
PACKAGE_ROOT = os.path.join(ROOT, "..", "..", "..")
sys.path.append(PACKAGE_ROOT)
import grapht

DATA_ROOT = os.path.join(ROOT, "..", "data")
print (DATA_ROOT)

def test_default_parameter_placement():
  """Tests the placement of default parameters into a user-defined JSON structure"""

  default_trees = []
  optional_tree_types = []
  required_tree_types = []
  user_specified_trees = []
  result_trees = []

  tree_folders = [dirs for dirs in os.listdir(DATA_ROOT) if
    os.path.isdir(os.path.join(DATA_ROOT, dirs))
    and dirs.startswith("tree_")
  ]

  # Read in all of the necessary trees.
  for tree_folder in tree_folders:
    full_tree_path = os.path.join(DATA_ROOT, tree_folder)

    default_tree_path = os.path.join(full_tree_path, "default_tree.json")
    optional_tree_type_path = os.path.join(full_tree_path, "optional_tree_type.json")
    required_tree_type_path = os.path.join(full_tree_path, "required_tree_type.json")
    user_specified_tree_path = os.path.join(full_tree_path, "user_specified_tree.json")
    result_tree_path = os.path.join(full_tree_path, "result_tree.json")

    with open(default_tree_path, 'r') as f:
      default_trees.append(json.load(f))
    with open(optional_tree_type_path, 'r') as f:
      optional_tree_types.append(json.load(f))
    with open(required_tree_type_path, 'r') as f:
      required_tree_types.append(json.load(f))
    with open(user_specified_tree_path, 'r') as f:
      user_specified_trees.append(json.load(f))
    with open(result_tree_path, 'r') as f:
      result_trees.append(json.load(f))
    
  # Form the trees and check for equivalence with the expected result trees.
  for i in range(len(default_trees)):
    parser = grapht.GraphtParser()
    parser.add_default_input(default_trees[i])
    parser.add_optional_input_types(optional_tree_types[i])
    parser.add_required_input_types(required_tree_types[i])
    parser.add_user_input(user_specified_trees[i])
    assembled_tree = parser.assemble_tree()

    assert (grapht.check_equivalence(assembled_tree, result_trees[i])), ("Smoke test failed!"
      " Assembled graph is different from expected result graph!")
  


