import json
import copy

DATA_TYPE_MAP = {"str": str, "int": int, "float": float, "list": list, "tuple": tuple, "dict": dict,
  "bool": bool, "None": type(None)}

class GraphtParser:
  """Parser for JSON I/O"""
  def __init__(self):
    return

  def add_required_input_types(self, required_tree_types):
    """Add the JSON tree describing the required input valid data types"""
    self.required_tree_types = required_tree_types

  def add_optional_input_types(self, optional_tree_types):
    """Add the JSON tree describing the optional input valid data types"""
    self.optional_tree_types = optional_tree_types

  def add_default_input(self, default_tree):
    """Add the JSON tree describing default values for parameters
    
    Note: This need not describe all parameters. Just the ones you would like to give default values
    to.
    """
    self.default_tree = default_tree

  def add_user_input(self, user_tree):
    """Add the JSON tree describing the user input values for parameters"""
    self.user_tree = user_tree

  def assemble_tree(self):
    """Assembles the tree given the input trees"""
    # Do some error checking to make sure the user specified values are of correct data type.
    self.__dfs_param_check(self.user_tree, self.required_tree_types, required_check=True)
    self.__dfs_param_check(self.user_tree, self.optional_tree_types)

    # Make a copy of the user input tree
    assembled_tree = copy.deepcopy(self.user_tree)
    self.__dfs_param_set(assembled_tree, self.default_tree)

    return assembled_tree

  def __dfs_param_check(self, d, type_dict, required_check=False, key=None):
    """Traverses dictionary d and checks that all values of correct data type
    
    inputs:
      d - dict. The dictionary to check.
      type_dict - dict. Same structure as d. Contains the valid data types of all tree leaves either
                  as a single type (e.g. float) or as a tuple of valid type (e.g. (float, int)).
      required_check - bool. Specifies whether the parameters specified in type_dict will raise an 
                       error if they are not specified.
      key - The current key of the traversal. Necessary for recursion.
    """
    if key is None:
      assert(isinstance(d, dict)), "Argument 'd' must be a dictionary!"
      assert(isinstance(type_dict, dict)), "Argument 'type_dict' must be a dictionary!"
      # Traverse the tree.
      for sub_key in type_dict.keys():
        self.__dfs_param_check(d, type_dict, required_check, sub_key)
    else:
      if isinstance(type_dict[key], dict):
        # This is another node and we must traverse deeper into the tree.
        key_present = key in d.keys()
        if not key_present:
          if required_check:
            raise RuntimeError("The parameter \""+key+"\" is not specified and it is required!")
        else:
          d = d[key]
          type_dict = type_dict[key]

          for sub_key in type_dict.keys():
            self.__dfs_param_check(d, type_dict, required_check, sub_key)
      else:
        # This is a parameter.
        # Double-check that the type specified is acceptable.
        data_type = type_dict[key]
        if isinstance(data_type, (tuple, list)):
          for dat in data_type:
            assert (dat in DATA_TYPE_MAP.keys()), ("Data type, \""+dat+"\" for parameter \""+key
              +"\" is not supported!")
        else:
          assert (data_type in DATA_TYPE_MAP.keys()), ("Data type, \""+data_type+"\" for parameter "
            '\"'+key+"\" is not supported!")

        # Double-check parameter is the right data type and if it is required.
        key_present = key in d.keys()
        if not key_present:
          if required_check:
           raise RuntimeError("The parameter \""+key+"\" is not specified and it is required!")
        else:
          # Get the data type(s) from the mapping.
          if isinstance(data_type, (list, tuple)):
            dtype = tuple([DATA_TYPE_MAP[dat] for dat in data_type])
          else:
            dtype = DATA_TYPE_MAP[data_type]

          assert isinstance(d[key], dtype), ("The parameter \""+key+"\" is not of the "
            "correct data type. Valid options are:", dtype)

  def __dfs_param_set(self, dict_1, dict_default, key=None):
    """Depth-first default parameter setting"""
    if key is None:
      assert (isinstance(dict_1, dict)), "Argument 'dict_1' must be a dictionary!"
      assert (isinstance(dict_default, dict)), "Argument 'dict_default' must be a dictionary!"
      # Traverse the tree.
      for sub_key in dict_default.keys():
        self.__dfs_param_set(dict_1, dict_default, key=sub_key)
    else:
      if key not in dict_1.keys():
        # key isn't present in the dictionary user supplied so we specify the value as default.
        dict_1[key] = dict_default[key]
      else:
        if isinstance(dict_default[key], dict):
          dict_default = dict_default[key]
          dict_1 = dict_1[key]
          # Traverse the tree.
          for sub_key in dict_default.keys():
            self.__dfs_param_set(dict_1, dict_default, key=sub_key)

def check_equivalence(tree_1, tree_2, key=None, verbose=False):
  """Checks that the two given trees are equivalent"""
  is_equivalent = True

  if key is None:
    assert(isinstance(tree_1, dict)), "Argument 'tree_1' must be a dictionary!"
    assert(isinstance(tree_2, dict)), "Argument 'tree_2' must be a dictionary!"
    
    # Traverse the tree.
    for sub_key in tree_1.keys():
      is_equivalent = (check_equivalence(tree_1, tree_2, key=sub_key) and is_equivalent)
  
  else:
    if isinstance(tree_1[key], dict):
      # First check to make sure that tree_2 is also a dict.
      is_equivalent = (isinstance(tree_2[key], dict))
      if not is_equivalent:
        print ("Tree 2 has a leaf node where tree 1 has a node of degree "
        "> 1 at key: \"{}\"".format(key))
        return is_equivalent
      
      # Traverse the tree.
      tree_1 = tree_1[key]
      tree_2 = tree_2[key]
      for sub_key in tree_1.keys():
        is_equivalent = (is_equivalent and check_equivalence(tree_1, tree_2, key=sub_key))
      
    else:
      # First check to make sure that tree_2 is also not a dict.
      is_equivalent = (not isinstance(tree_2[key], dict))
      if not is_equivalent:
        print ("Tree 2 has a node of degree > 1 where tree 1 has a"
        " leaf node at key: \"{}\"".format(key))
        return is_equivalent
      
      is_equivalent = (is_equivalent and (tree_1[key] == tree_2[key]))
  
  return is_equivalent

def __recurs_flatten_tree(tree, full_path_to_leaves, key=None, this_path_to_leaf=[]):
  """Modifies full_path_to_leaves in place to give list of paths, names, and values of all leaves
  
  Inputs:
    tree - dict. The tree to be flattened.
    full_path_to_leaves - list. List that contains all of the paths, names, and values to all leaves
                          in the tree. Modified in place so should be given as an empty list when
                          function is first called.
    key - dictionary key. The key of the node we're currently visiting.
    this_path_to_leaf - list. The path to the node we're currently visiting.
  
  Returns:
    No return
  """
  if key is None:
    for sub_key in tree.keys():
      __recurs_flatten_tree(tree, full_path_to_leaves, key=sub_key, 
        this_path_to_leaf=this_path_to_leaf)
  elif isinstance(tree[key], dict):
    tree = tree[key]
    this_path_to_leaf = this_path_to_leaf + [key]
    for sub_key in tree.keys():
      __recurs_flatten_tree(tree, full_path_to_leaves, key=sub_key, 
        this_path_to_leaf=this_path_to_leaf)
  else:
    # This is a leaf. We need to append a tuple describing the path to the leaf and leaf value.
    full_path_to_leaves.append(
      (this_path_to_leaf, [key, tree[key]])
    )


def flatten_tree(tree):
  """Returns a list containing paths, names, and values of all leaves in the tree
  
  Inputs:
    tree - dict. The tree to be flattened.
  
  Returns:
    full_path_to_leaves - list. List of leaves in the tree where zeroth index of list a list 
                          containing the path to the leaf, first index of the list is a tuple that
                          containes (name_of_leaf_key, leaf_value).
  """
  # Form the list that we're going to modify in place using the recursive flatten tree function.
  full_path_to_leaves = []
  __recurs_flatten_tree(tree, full_path_to_leaves)
  return full_path_to_leaves

def unflatten_tree(flattened_tree):
  """Returns the nested tree form described by the given flattened tree
  
  Inputs:
    flattened_tree - list of tuples. This is the list of tuples returned by the function 
                     flatten_tree()
  
  Returns:
    nested_tree - nested dict. The tree structure in the nested dictionary form.
  """
  # Create our nested tree.
  nested_tree = {}

  for leaf_tuple in flattened_tree:
    # Set the current node as the root of the tree.
    current_node = nested_tree

    # Create all of the non-leaf nodes.
    for path_list in leaf_tuple[0]:
      for path_node in path_list:
        if path_node not in current_node.keys():
          current_node[path_node] = {}
        current_node = current_node[path_node]

    # Create the leaf node.
    current_node[leaf_tuple[1][0]] = leaf_tuple[1][1]
  
  return nested_tree

    