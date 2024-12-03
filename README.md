| | |
|-|-|
| Software | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white) ![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white) |
| Download | [![PyPI version](https://badge.fury.io/py/IQM-Vis.svg)](https://badge.fury.io/py/IQM-Vis) [![PyPI download month](https://img.shields.io/pypi/dm/IQM-Vis.svg)](https://pypi.python.org/pypi/IQM-Vis/) |
| Documentation | [![Generic badge](https://img.shields.io/badge/DOCS-Read-blue.svg)](https://mattclifford1.github.io/IQM-Vis/) |     
| Installation | [![Generic badge](https://img.shields.io/badge/INSTALL-View-green.svg)](https://mattclifford1.github.io/IQM-Vis/getting_started.html) | 
| Tutorials | [![Generic badge](https://img.shields.io/badge/TUTORIALS-View-blue.svg)](https://mattclifford1.github.io/IQM-Vis/Tutorials.html) | 
| Demos | [![Generic badge](https://img.shields.io/badge/HuggingFaceSpace-Launch-red.svg)](https://huggingface.co/spaces/mattclifford1/IQM-VIS) |
| Tests | [![Generic badge](https://github.com/mattclifford1/IQM-Vis/blob/main/tests/reports/tests_badge.svg)](https://github.com/mattclifford1/IQM-Vis/blob/main/tests) [![Generic badge](https://github.com/mattclifford1/IQM-Vis/blob/main/tests/reports/coverage_badge.svg)](https://github.com/mattclifford1/IQM-Vis/blob/main/tests) |


# IQM-Vis
Image Quality Metric Visualision. An extendable user interface for the assessment of transformations on image metrics.

Head over to the [DOCUMENTATION](https://mattclifford1.github.io/IQM-Vis/) for tutorials and package reference. Read our [PAPER](https://github.com/mattclifford1/IQM-Vis/blob/main/dev_resources/docs/resources/Software_paper.pdf) for in depth details of the software.

### IQM's average sensitivity to tranforms
![Alt text](https://github.com/mattclifford1/IQM-Vis/blob/main/dev_resources/pics/data_graphs.gif?raw=true "Dataset UI") 

### IQM's sensitivity to tranforms specific parameters
![Alt text](https://github.com/mattclifford1/IQM-Vis/blob/main/dev_resources/pics/params.gif?raw=true "Dataset UI") 

### IQM's correlation to human scores
![Alt text](https://github.com/mattclifford1/IQM-Vis/blob/main/dev_resources/pics/correlation.gif?raw=true "Dataset UI") 


# Documentation
Please refer to our [website](https://mattclifford1.github.io/IQM-Vis/) for a full guide on installing and using IQM-Vis. However, we provide some brief instruction below.

### Installation
It is important to run IQM-Vis in a fresh python virtual environment. This is so that there will be no dependancy clashes with the required libraries. Python version 3.9 is recommended, but newer versions should work as well.

You can make a new environment by using anaconda (conda):
```
    conda create -n IQM_Vis python=3.9 -y
    conda activate IQM_Vis
```

If you have a GPU and would like to use CUDA then at this point head over to the pytorch website and download the relevent packages e.g.

If you don't have a GPU then you can skip this step.

```
    conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia
```

Now we can install IQM-Vis from the PyPi index:

```
    pip install IQM-Vis
```

#### Testing the installation

Run a demonstration example by running the python code:

```
    import IQM_Vis
    IQM_Vis.make_UI()
```

### Tutorials
Head over to our [tutorials page](https://mattclifford1.github.io/IQM-Vis/Tutorials.html) for details on how get started with using and customising IQM-Vis.