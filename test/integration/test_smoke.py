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

def test_tree_assembly():
  """Tests the assembly of trees given default, optional, required, and user-specified trees"""

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

def test_tree_flattening_0():
  """Tests the flattening of assembled trees"""
  test_dict = {
    "a": {
      "b": {
        "c": 1, 
        "d": {
          "e": 2, 
          "f": 3
        }
      }, 
      "g": [1, 2]
    },
    "h": "flat"
  }
  flattened_truth = [
    (['a', 'b'], ['c', 1]),
    (['a', 'b', 'd'], ['e', 2]),
    (['a', 'b', 'd'], ['f', 3]),
    (['a', 'g'], [0, 1]),
    (['a', 'g'], [1, 2]),
    ([], ['h', 'flat'])
  ]
  flattened_result = grapht.flatten_tree(test_dict)

  print ("flattened result:", flattened_result)

  assert (flattened_result == flattened_truth), "The results of flattening do not validate!"

def test_tree_flattening_1():
  test_dict = {
    "m_kinetics": {
      "m_no_of_cb_states": 2,
      "scheme": [
      {
        "state": 1,
        "type": "d",
        "transition":
        [
        {
          "new_state": 2,
          "rate_type": "gaussian",
          "rate_parameters": [100, 0, 3]
        }
        ]
      },
      {
        "state": 2,
        "type": "a",
        "cb_extension": 4.0,
        "transition":
        [
        {
          "new_state": 1,
          "rate_type": "poly",
          "rate_parameters": [100, 1, 4]
        }
        ]
      }
    ]
    }
  }
  flattened_truth = [
    (["m_kinetics"], ["m_no_of_cb_states", 2]),
    (["m_kinetics", "scheme", 0], ["state", 1]), # Intermediary lists can be as nested as we want with this structure.
    (["m_kinetics", "scheme", 0], ["type", "d"]),
    (["m_kinetics", "scheme", 0, "transition", 0], ["new_state", 2]),
    (["m_kinetics", "scheme", 0, "transition", 0], ["rate_type", "gaussian"]),
    (["m_kinetics", "scheme", 0, "transition", 0, "rate_parameters"], [0, 100]), # None indicates that this is a list element, not a leaf node.
    (["m_kinetics", "scheme", 0, "transition", 0, "rate_parameters"], [1, 0]),
    (["m_kinetics", "scheme", 0, "transition", 0, "rate_parameters"], [2, 3]),
    (["m_kinetics", "scheme", 1], ["state", 2]),
    (["m_kinetics", "scheme", 1], ["type", "a"]),
    (["m_kinetics", "scheme", 1], ["cb_extension", 4.0]),
    (["m_kinetics", "scheme", 1, "transition", 0], ["new_state", 1]),
    (["m_kinetics", "scheme", 1, "transition", 0], ["rate_type", "poly"]),
    (["m_kinetics", "scheme", 1, "transition", 0, "rate_parameters"], [0, 100]),
    (["m_kinetics", "scheme", 1, "transition", 0, "rate_parameters"], [1, 1]),
    (["m_kinetics", "scheme", 1, "transition", 0, "rate_parameters"], [2, 4])
  ]
  flattened_result = grapht.flatten_tree(test_dict)

  print ("flattened result:", flattened_result)

  assert (flattened_result == flattened_truth), "The results of flattening do not validate!"

def test_tree_reformation_0():
  """Tests the reformation of trees after they have been flattened"""
  flattened_tree = [
    (['a', 'b'], ['c', 1]),
    (['a', 'b', 'd'], ['e', 2]),
    (['a', 'b', 'd'], ['f', 3]),
    (['a', 'g'], [0, 1]),
    (['a', 'g'], [1, 2]),
    ([], ['h', 'flat'])
  ]
  nested_tree_truth = {
    "a": {
      "b": {
        "c": 1, 
        "d": {
          "e": 2, 
          "f": 3
        }
      }, 
      "g": [1, 2]
    },
    "h": "flat"
  }

  nested_result = grapht.unflatten_tree(flattened_tree)

  print ("nested result:", nested_result)

  assert (nested_result == nested_tree_truth), "The results of unflattening do not validate!"

def test_tree_reformation_1():
  """Tests the reformation of trees after they have been flattened"""
  flattened_tree = [
    (['a', 'b'], ['long_leaf_name', 1]),
    (['a', 'b', 'd'], ['e', 2]),
    (['a', 'b', 'd'], ['short_name', 3]),
    (['a', 'g'], [0, 1]),
    (['a', 'g'], [1, 2]),
    ([], ['h', 'flat'])
  ]
  nested_tree_truth = {
    "a": {
      "b": {
        "long_leaf_name": 1, 
        "d": {
          "e": 2, 
          "short_name": 3
        }
      }, 
      "g": [1, 2]
    },
    "h": "flat"
  }

  nested_result = grapht.unflatten_tree(flattened_tree)

  print ("nested result:", nested_result)

  assert (grapht.check_equivalence(nested_result, nested_tree_truth)), "The results of unflattening do not validate!"

def test_tree_reformation_2():
  nested_tree_truth = {
      "m_kinetics": {
        "m_no_of_cb_states": 2,
        "scheme": [
        {
          "state": 1,
          "type": "d",
          "transition":
          [
          {
            "new_state": 2,
            "rate_type": "gaussian",
            "rate_parameters": [100, 0, 3]
          }
          ]
        },
        {
          "state": 2,
          "type": "a",
          "cb_extension": 4.0,
          "transition":
          [
          {
            "new_state": 1,
            "rate_type": "poly",
            "rate_parameters": [100, 1, 4]
          }
          ]
        }
      ]
      }
    }
  flattened_tree = [
    (["m_kinetics"], ["m_no_of_cb_states", 2]),
    (["m_kinetics", "scheme", 0], ["state", 1]), # Intermediary lists can be as nested as we want with this structure.
    (["m_kinetics", "scheme", 0], ["type", "d"]),
    (["m_kinetics", "scheme", 0, "transition", 0], ["new_state", 2]),
    (["m_kinetics", "scheme", 0, "transition", 0], ["rate_type", "gaussian"]),
    (["m_kinetics", "scheme", 0, "transition", 0, "rate_parameters"], [0, 100]), # None indicates that this is a list element, not a leaf node.
    (["m_kinetics", "scheme", 0, "transition", 0, "rate_parameters"], [1, 0]),
    (["m_kinetics", "scheme", 0, "transition", 0, "rate_parameters"], [2, 3]),
    (["m_kinetics", "scheme", 1], ["state", 2]),
    (["m_kinetics", "scheme", 1], ["type", "a"]),
    (["m_kinetics", "scheme", 1], ["cb_extension", 4.0]),
    (["m_kinetics", "scheme", 1, "transition", 0], ["new_state", 1]),
    (["m_kinetics", "scheme", 1, "transition", 0], ["rate_type", "poly"]),
    (["m_kinetics", "scheme", 1, "transition", 0, "rate_parameters"], [0, 100]),
    (["m_kinetics", "scheme", 1, "transition", 0, "rate_parameters"], [1, 1]),
    (["m_kinetics", "scheme", 1, "transition", 0, "rate_parameters"], [2, 4])
  ]
  nested_result = grapht.unflatten_tree(flattened_tree)

  print ("nested result:", nested_result)

  assert (grapht.check_equivalence(nested_result, nested_tree_truth)), "The results of unflattening do not validate!"