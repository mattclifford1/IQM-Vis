[![PyPI version](https://badge.fury.io/py/IQM-VIS.svg)](https://badge.fury.io/py/IQM-VIS)

# IQM-VIS
Image Quality Metric Visualision

Extendable user interface for the assessment of transformations on image metrics. Examples of how to use this package are found in [examples](examples).

## UI Examples
Simple UI with single image and image metric
![Alt text](examples/images/ui-simple.png?raw=true "Simple UI")

Extended UI with multiple images and metrics with metric radar comparison plot.
![Alt text](examples/images/ui-multi.png?raw=true "Multi UI")


# Installation
The latest stable version can be downloaded via [PyPi](https://pypi.org/project/IQM-VIS/0.1/).
```
$ pip install IQM-VIS
```

## Dev Setup
First create a new python venv, eg. using conda
```
$ conda create -n iqm_vis python=3.9
```
Activate env:
```
$ conda activate iqm_vis
```
Clone repo
```
$ git clone git@github.com:mattclifford1/IQA_GUI.git
$ cd IQA_GUI
```
Install requirements
```
$ pip install -r requirements-dev.txt
```
Install package in editable mode
```
$ pip install -e .
```
Run MWEs
```
$ python examples/simple.py
$ python examples/multiple.py
```

## To do - datasets
Need to 'scroll' through dataset:
  - directory of images?
  - image paths in list?
  - image paths in csv file?
