[![PyPI version](https://badge.fury.io/py/IQM-Vis.svg)](https://badge.fury.io/py/IQM-Vis)

# IQM-Vis
Image Quality Metric Visualision. An extendable user interface for the assessment of transformations on image metrics.

Head over to the [DOCUMENTATION](https://mattclifford1.github.io/IQM-Vis/) for tutorials and package reference.

# Installation
First create a new python venv, eg. using conda
```
conda create -n IQM_Vis python=3.9
```
Activate env:
```
conda activate IQM_Vis
```
The latest stable version can be downloaded via [PyPi](https://pypi.org/project/IQM-Vis).
```
pip install IQM-Vis
```
Example usage of the package can be found in [examples](https://github.com/mattclifford1/IQM-Vis/tree/main/IQM_Vis/examples)

# Usage
To create the UI you need to define 3 things minimum:
  - metrics
  - images
  - transformations

### Metrics
A dictionary containing the metric names and callable function/class:
```
metrics = {'my_metric': my_metric_function}
```
`my_metric_function` expects to take arguments `image_reference`, `image_comparison`, `**kwargs`

### Images
A list of image files to use:
```
images = ['/file/path/to/my_image.jpg']
```

### Transformations
A dictionary containing the transformation names, with corresponding function and parameter values:
```
transformations = {'my_trans': {'function': my_trans_function, 'min':-1.0, 'max':'1.0'}}
```
`my_trans_function` expects to take arguments `image`, `parameter`
## Making the UI
First you need to make a dataset and metric object:
```
import IQM_Vis
data = IQM_Vis.dataset_holder(image_list=images,
                              metrics=metrics)
```
Then we need to create the UI
```

IQM_Vis.make_UI(data,
              transformations,
              metrics_avg_graph=True)
```

# UI Example
![Alt text](https://github.com/mattclifford1/IQM-Vis/blob/main/pics/UI-all.png?raw=true "Dataset UI")
<!--
## UI Examples (section needs pictures updating)
Simple UI with single image and image metric
```
import IQM_Vis
IQM_Vis.examples.simple.run()
```
![Alt text](https://github.com/mattclifford1/IQM-Vis/blob/main/pics/ui-simple.png?raw=true "Simple UI")

### Extensions
Link to a dataset so you can scroll through and assess many images
```
import IQM_Vis
IQM_Vis.examples.dataset.run()
```
![Alt text](https://github.com/mattclifford1/IQM-Vis/blob/main/pics/ui-dataset.png?raw=true "Dataset UI")

Extend with multiple image rows to compare multiple images at once.
```
import IQM_Vis
IQM_Vis.examples.multiple.run()
```
![Alt text](https://github.com/mattclifford1/IQM-Vis/blob/main/pics/ui-multi.png?raw=true "Multi UI")
-->

# Quick testing with our web version
To use a stripped down version of the application, feel free to first use our [web version](https://huggingface.co/spaces/mattclifford1/IQM-Vis). Here you can upload your own image and choose from a selection of transformations and metrics.

# Dev Setup (only use if editting the package)
See the [installation](https://github.com/mattclifford1/IQM-Vis#installation) section if you are just using IQM-Vis.

### Python Environment
First create a new python venv, eg. using conda
```
conda create -n IQM_Vis python=3.9
```
Activate env:
```
conda activate IQM_Vis
```

### Clone repo
```
git clone git@github.com:mattclifford1/IQM-Vis.git
cd IQM-Vis
```
### Install requirements
```
pip install -r requirements-dev.txt
```
### Install IQM-Vis in editable mode
```
pip install -e .
```
### Run MWEs
```
python IQM_Vis/examples/dataset.py
```

### Extras
To be able to generate documentation you will also need pandoc bins via:
```
conda install pandoc
```
