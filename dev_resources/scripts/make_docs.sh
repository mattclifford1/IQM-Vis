#!/usr/bin/bash
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License


rm dev_resources/docs/IQM_Vis.*
# sphinx-build -o dev_resources/docs IQM_Vis
sphinx-apidoc -o dev_resources/docs IQM_Vis IQM_Vis/metrics/NLPD_torch/*
cd dev_resources/docs
make clean html
make html
