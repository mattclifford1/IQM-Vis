#!/usr/bin/bash
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License


git clean -xfd
python setup.py sdist bdist_wheel
# make sure to add the IQM_Vis repository to your .pypirc file and create tokens on PyPI
# e.g.
# [distutils]
#   index-servers =
#     pypi
#     IQM_Vis

# [pypi]
#   username = __token__
#   password = pypi-token-goes-here
# [IQM_Vis]
#   repository = https://pypi.org/project/IQM-Vis/
#   username = __token__
#   password = pypi-token-goes-here
twine upload dist/* --repository IQM_Vis
