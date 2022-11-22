[![PyPI version](https://badge.fury.io/py/IQM-VIS.svg)](https://badge.fury.io/py/IQM-VIS)

# IQM-VIS
Image Quality Metric Visualision

Extendable user interface for the assessment of transformations on image metrics. Examples of how to use this package are found in [here](https://github.com/mattclifford1/IQM-VIS/tree/main/IQM_VIS/examples) or use our [web version](https://huggingface.co/spaces/mattclifford1/IQM-VIS).

## UI Examples
Simple UI with single image and image metric
```
import IQM_VIS
IQM_VIS.examples.simple.run()
```
![Alt text](https://github.com/mattclifford1/IQM-VIS/blob/main/pics/ui-simple.png?raw=true "Simple UI")

### Extensions
Link to a dataset so you can scroll through and assess many images
```
import IQM_VIS
IQM_VIS.examples.dataset.run()
```
![Alt text](https://github.com/mattclifford1/IQM-VIS/blob/main/pics/ui-dataset.png?raw=true "Dataset UI")

Extend with multiple image rows to compare multiple images at once.
```
import IQM_VIS
IQM_VIS.examples.multiple.run()
```
![Alt text](https://github.com/mattclifford1/IQM-VIS/blob/main/pics/ui-multi.png?raw=true "Multi UI")

# Quick Testing
To use a stripped down version of the application, feel free to first use our [web version](https://huggingface.co/spaces/mattclifford1/IQM-VIS). Here you can upload your own image and choose from a selection of transformations and metrics.

# Installation
The latest stable version can be downloaded via [PyPi](https://pypi.org/project/IQM-VIS).
```
pip install IQM-VIS
```
Example usage of the package can be found in [examples](https://github.com/mattclifford1/IQM-VIS/tree/main/IQM_VIS/examples)

# Dev Setup
First create a new python venv, eg. using conda
```
conda create -n iqm_vis python=3.9
```
Activate env:
```
conda activate iqm_vis
```
Clone repo
```
git clone git@github.com:mattclifford1/IQA_GUI.git
cd IQA_GUI
```
Install requirements
```
pip install -r requirements-dev.txt
```
Install package in editable mode
```
pip install -e .
```
Run MWEs
```
python IQM_VIS/examples/simple.py
python IQM_VIS/examples/multiple.py
```
