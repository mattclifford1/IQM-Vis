#!/usr/bin/bash

VENV=iqm_vis
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

conda create -n iqm_vis python=3.9 -y
conda activate $VENV

pip install -r requirements-dev.txt
pip install -e .
