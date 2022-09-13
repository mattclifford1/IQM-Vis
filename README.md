# Image Quality Metric User Interface
Extendable user interface for assessment of image transformations on image metrics

## Minimal Example of API
Define image path and name:
```
image_path = {'X': 'images/image2.jpg'}
```
Define metric function to use:
```
metric = {'MAE': lambda im1, im2: np.abs(im1 - im2).mean()}
```
Define a metric image function:
```
metric_im = {'MAE': lambda im1, im2: np.abs(im1 - im2)}
```
Define a transformation and its parameter value range:
```
trans = {'brightness': {'min':-1, 'max':1, 'init_value':0, 'function':lambda im, val: np.clip(im + val, 0, 1)}}
```
Use the API to create the UI:
```
import api
api.make_UI(image_path, metric, metric_im, trans)
```
![Alt text](images/ui-simple.png?raw=true "Simple UI)




## Installation (todo: `setup.py` and pypi)
Currently under development so install from GitHub. First create a new python venv, eg. using conda
```
$ conda create -n iqa python=3.9
```
Activate env:
```
$ conda activate iqa
```
Clone repo
```
$ git clone git@github.com:mattclifford1/IQA_GUI.git
$ cd IQA_GUI
```
Install requirements
```
$ pip install requirements.txt
```
Run MWE
```
$ python example_simple.py
```

### To do - datasets
Need to 'scroll' through dataset:
  - directory of images?
  - image paths in list?
  - image paths in csv file?
