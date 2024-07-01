#!/usr/bin/bash
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License


rm docs/IQM_Vis.*
# sphinx-build -o docs IQM_Vis
sphinx-apidoc -o docs IQM_Vis IQM_Vis/metrics/NLPD_torch/*
cd docs
make clean html
make html
