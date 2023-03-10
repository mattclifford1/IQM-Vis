'''
test invalid input to api throws an error
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import pytest
import numpy as np

from IQM_Vis import api

def test_not_dict():
    with pytest.raises(TypeError) as val_error:
        api.make_UI([],
                {'a':1},
                {'a':1},
                {'a':1},
                metrics_info_format='text')

def test_not_str():
    with pytest.raises(TypeError) as val_error:
        api.make_UI({'a':1},
                {'a':1},
                {'a':1},
                {'a':1},
                metrics_info_format=[])

def test_warn_empty():
    image_path = {'X': 'examples/images/image2.jpg'}
    metric = {'MAE': lambda im1, im2: np.abs(im1 - im2).mean()}
    metric_im = {'MAE': lambda im1, im2: np.abs(im1 - im2)}
    trans = {'brightness': {'min':-1, 'max':1, 'init_value':0, 'function':lambda im, val: np.clip(im + val, 0, 1)}}

    with pytest.warns():
        ui = api.UI_wrapper({},
                metric,
                metric_im,
                trans,
                metrics_info_format='text')
        ui._check_inputs()

if __name__ == '__main__':
    test_inputs()
