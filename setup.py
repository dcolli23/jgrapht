import setuptools

with open("README.md", 'r') as f:
  long_description = f.read()

setuptools.setup(
  name="jgrapht",
  version="0.0.2",
  author="Dylan Colli",
  author_email="dylanfrankcolli@gmail.com",
  description="Painless usage of JSON trees for parameter I/O",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/dcolli23/jgrapht",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent"
  ]
)