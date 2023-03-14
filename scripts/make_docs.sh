#!/usr/bin/bash

sphinx-apidoc -o docs IQM_Vis
cd docs
make clean html
make html
