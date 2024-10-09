# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

import numpy as np
import pytest

import IQM_Vis
import sys
import os
sys.path.append(os.path.abspath('..'))
from tests.QtBot_utils import BotTester

def custom_MAE_function(im_ref, im_comp, **kwargs):
    L1 = np.abs(im_ref - im_comp)
    return L1.mean()


class custom_MAE_class:
    def __init__(self, att=0):
        self.att = att

    def __call__(self, im_ref, im_comp, **kwargs):
        L1 = np.abs(im_ref - im_comp)
        return L1.mean()
    

def dummy_args(im_ref, im_comp, param1=0, **kwargs):
    # now we can use param here
    score = custom_MAE_function(im_ref, im_comp)
    return score + param1


def custom_brightness(image, value=0):
    return np.clip(image + value, 0, 1)


def get_UI():
    metrics = {'MAE function': custom_MAE_function,
               'MAE class': custom_MAE_class(),
               'dummy args': dummy_args}
    params = {'param1': {'min': -1.0, 'max': 1.0, 'init_value': 0}}
    transformations = {'brightness': {'min': -1.0,
                                      'max': 1.0, 'function': custom_brightness}}

    images = ['/home/matt/datasets/kodak/kodim01.png',
              '/home/matt/datasets/kodak/kodim02.png']

    test_app = IQM_Vis.make_UI(transformations=transformations,
                               image_list=images,
                               metrics=metrics,
                               metric_params=params,
                               test=True)
    return test_app


# build_IQM_Vis = BotTester(get_UI=get_UI, wait_time=1000, final_wait=True).build_IQM_Vis
build_IQM_Vis = BotTester(get_UI=get_UI).build_IQM_Vis


# @pytest.fixture(scope='function')
def test_build_3(build_IQM_Vis):
    test_window, _ = build_IQM_Vis
    assert test_window.showing == True
