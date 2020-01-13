import json

class GraphtParser:
  """Parser for JSON I/O"""
  def __init__(self):
    return

  def add_required_input_types(self, required_tree):
    """Add the JSON tree describing the required input valid data types"""
    self.required_tree_types = required_tree_types

  def add_optional_input_types(self, optional_tree):
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
    self.assembled_tree = self.user_tree.deepcopy()
    self.__dfs_param_set(self.assembled_tree, self.default_tree)

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
        d = d[key]
        type_dict = type_dict[key]

        for sub_key in type_dict.keys():
          self.__dfs_param_check(d, type_dict, required_check, sub_key)
      else:
        # This is a parameter and we need to double-check it's the right data type and if it is
        # required.
        if required_check:
          assert (key in d.keys()), "The parameter \""+key+"\" is not specified and it is required!"
        assert isinstance(d[key], type_dict[key]), ("The parameter \""+key+"\" is not of the "
       "correct data type. Valid options are:", type_dict[key])

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
        dict_1[key] = dict_default
      else:
        if isinstance(dict_default, dict):
          dict_default = dict_default[key]
          dict_1 = dict_1[key]
          # Traverse the tree.
          for sub_key in dict_default.keys():
            self.__dfs_param_set(dict_1, dict_default, key=sub_key)


