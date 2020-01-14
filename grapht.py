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