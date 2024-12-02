# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
from PyQt6 import QtTest, QtCore

import IQM_Vis
import sys
import os
sys.path.append(os.path.abspath('..'))
import IQM_Vis.examples.KODAK_dataset
from tests.QtBot_utils import BotTester


def get_UI():
    images = IQM_Vis.examples.KODAK_dataset.KODAK_IMAGES

    MAE = IQM_Vis.metrics.MAE()
    MSE = IQM_Vis.metrics.MSE()
    SSIM = IQM_Vis.metrics.SSIM()

    metrics = {'MAE': MAE,
               'MSE': MSE,
               '1-SSIM': SSIM}

    rotation = IQM_Vis.transforms.rotation
    blur = IQM_Vis.transforms.blur
    brightness = IQM_Vis.transforms.brightness
    jpeg_compression = IQM_Vis.transforms.jpeg_compression

    transformations = {
        # normal input
        'rotation':  {'min': -180, 'max': 180, 'function': rotation},
        # only odd ints since it's a kernel
        'blur':      {'min': 1,    'max': 41,  'function': blur, 'normalise': 'odd'},
        # float values
        'brightness': {'min': -1.0, 'max': 1.0, 'function': brightness},
        # non zero inital value
        'jpg comp.': {'min': 1,    'max': 100, 'function': jpeg_compression, 'init_value': 100},
    }

    test_app = IQM_Vis.make_UI(transformations=transformations,
                               image_list=images,
                               metrics=metrics,
                            #    metric_images=metric_images,
                               test=True)
    return test_app


build_IQM_Vis = BotTester(get_UI=get_UI, wait_time=1000,
                          final_wait=True).build_IQM_Vis

def test_change_graphs(build_IQM_Vis):
    test_window, qtbotbis = build_IQM_Vis
    assert test_window.showing == True


    # move slider
    for i in range(21):
        test_window.window.widget_controls['slider']['brightness']['data'].setValue(i)
        QtTest.QTest.qWait(50)

    # move another
    for i in range(21):
        test_window.window.widget_controls['slider']['rotation']['data'].setValue(
            i)
        QtTest.QTest.qWait(50)

    # check not crashed
    assert test_window.showing == True

