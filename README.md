# Introduction
jGrapht is a python package for painless implementation of JSON inputs.

# Index

- [About](#about)
- [Usage](#usage)
  - [Installation](#installation)
    - [Python Package Dependencies](#python-package-dependencies)
- [Development](#development)
  - [Validation Tests](#validation-tests)
- [Community](#community)
  - [Contribution](#contribution)
- [Credit/Acknowledgment](#creditacknowledgment)
- [License](#license)

# About
jGrapht is a python package meant to make the usage of complex JSON trees for file I/O as painless as possible. There is support for data type verification of leaves in the JSON tree, specification of default values if no value is specified, flattening of the structure, and reversing the flattening of the structure.

# Usage
This software is meant to be used as a Python package. You can find further details about the usage of `jGrapht` in the [documentation](docs/usage/usage.md)

### Installation
Installation of jGrapht is simple. To begin working with jGrapht, simply clone the jGrapht repository and import the jGrapht package as normal.

# Development
Thank you for considering contributing to the jGrapht project! Please contact Dylan Colli at dylanfrankcolli@gmail.com.

jGrapht uses the [PyTest](https://docs.pytest.org/en/latest/index.html) framework for validation of functionality. PyTest is not part of Python's standard library and thus needs to be installed before validation of changes can be done. To do so, visit [this page](https://docs.pytest.org/en/latest/getting-started.html) to install PyTest.

### Validation Tests
It is important to validate any code before it is committed (and develop new validation tests as appropriate!). To run a full validation test for the project, execute the following from the project's root directory:
```
$ pytest
```

If you would like to view the output of the tests, simply add `-s` to the previous command.

# Community

Hello! Thanks for taking the time to read through the documentation to learn more about the jGrapht project. We welcome any sort of dialogue about the project and if you have any questions or concerns, feel free to email Dylan Colli at dylanfrankcolli@gmail.com or see below for issue tracking and feature requests.

### Contribution

Your contributions are always welcome and appreciated. Following are the things you can do to contribute to this project:

1. **Report a bug**
If you think you have encountered a bug, feel free to report it using the "Issues" tab in the bitbucket repository and I will take care of it.

2. **Request a feature**
You can also request the addition of a feature using the issue tracker by selecting "proposal" when prompted by the "Kind" dialogue.

# Credit/Acknowledgment
The following is a list of contributors to the jGrapht project

Dylan Colli - dfco222@g.uky.edu<br/>

# License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. The licensce is included in the `COPYING.txt` document.