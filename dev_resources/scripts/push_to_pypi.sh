#!/usr/bin/bash
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License


git clean -xfd
python setup.py sdist bdist_wheel
twine upload dist/*
