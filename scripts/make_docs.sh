#!/usr/bin/bash

rm docs/IQM_Vis.*
sphinx-apidoc -o docs IQM_Vis
cd docs
make clean html
make html
