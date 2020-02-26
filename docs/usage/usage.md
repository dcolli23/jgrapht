# jGrapht Usage

This document provides a few specific use cases for the jGrapht package.

# Flattening a Tree to a List of Leaves

If you have a tree that you would like to iterate through all of the leaves to perform some action, like forming entries for all of the leaves in a GUI, then it is beneficial to have all of the leaves represented in a list than having to write a recursive function to handle the finding of leaves and also implement the functionality of the GUI. To flatten a tree into a list of leaves using the jGrapht repo, follow the example here.

Our sample tree is:

```json
{
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
```

The code to flattent this tree using jGrapht would be:

```python
flattened_result = jgrapht.flatten_tree(our_tree)
```

Which would produce:

```python
[
  (['a', 'b'], ['c', 1]),
  (['a', 'b', 'd'], ['e', 2]),
  (['a', 'b', 'd'], ['f', 3]),
  (['a', 'g'], [0, 1]),
  (['a', 'g'], [1, 2]),
  ([], ['h', 'flat'])
]
```

Which is a list of tuples where the first index is a list indicating the path to the leaf node and the second index is a list where the first index is the leaf name (or index in the case of an array) and the second index is the leaf value.

# Form a Tree from List of Leaves

Continuing the example above, if we have formed a list of entries for a GUI from our list of leaves, then we'll need to collate the leaf values back into a tree structure to reform the original tree and use it in the future. To do this, follow the example:

Flattened list of leaves:

```python
our_flattened_list = [
  (['a', 'b'], ['c', 1]),
  (['a', 'b', 'd'], ['e', 2]),
  (['a', 'b', 'd'], ['f', 3]),
  (['a', 'g'], [0, 1]),
  (['a', 'g'], [1, 2]),
  ([], ['h', 'flat'])
]
```

To reform the tree:

```python
reformed_tree = jgrapht.unflatten_tree(our_flatted_list)
```

Which will give us what we started with in the first example.

```json
{
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
```