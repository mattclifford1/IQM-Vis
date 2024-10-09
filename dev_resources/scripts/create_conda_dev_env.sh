#!/usr/bin/bash
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License


VENV=IQM_Vis
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

conda create -n IQM_Vis python=3.9 -y
conda activate $VENV

pip install -r requirements-dev.txt
pip install -e .
