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

    MSE_image = IQM_Vis.metrics.MSE(return_image=True)
    SSIM_image = IQM_Vis.metrics.SSIM(return_image=True)
    metric_images = {'MSE': MSE_image,
                     '1-SSIM': SSIM_image}

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

def test_dataset_scrolling(build_IQM_Vis):
    test_window, qtbotbis = build_IQM_Vis
    assert test_window.showing == True

    QtTest.QTest.qWait(500)

    # cycle the dataset backwards
    for _ in range(2):
        button = test_window.window.widget_controls['button']['prev_data']
        qtbotbis.mouseClick(button, QtCore.Qt.MouseButton.LeftButton)
        QtTest.QTest.qWait(500)
    # check not crashed
    assert test_window.showing == True

    # click on an image to change the image
    for i in range(1,5):
        image = test_window.window.widget_controls['images'][i]
        qtbotbis.mouseClick(image, QtCore.Qt.MouseButton.LeftButton)
        QtTest.QTest.qWait(500)

    # cycle the dataset forwards
    for _ in range(3):
        button = test_window.window.widget_controls['button']['prev_data']
        qtbotbis.mouseClick(button, QtCore.Qt.MouseButton.LeftButton)
        QtTest.QTest.qWait(500)
    # check not crashed
    assert test_window.showing == True

    # click on an image to change the image
    for i in range(1,5):
        image = test_window.window.widget_controls['images'][i]
        qtbotbis.mouseClick(image, QtCore.Qt.MouseButton.LeftButton)
        QtTest.QTest.qWait(500)
    # check not crashed
    assert test_window.showing == True



