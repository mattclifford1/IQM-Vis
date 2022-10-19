#!/usr/bin/bash

git clean -xfd
python setup.py sdist bdist_wheel
twine upload dist/*
