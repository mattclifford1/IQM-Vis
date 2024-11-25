# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
from tests.QtBot_utils import BotTester
import IQM_Vis.examples.KODAK_dataset
from PyQt6 import QtTest, QtCore

import IQM_Vis
import sys
import os
sys.path.append(os.path.abspath('..'))


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


def test_export_images(build_IQM_Vis):
    test_window, qtbotbis = build_IQM_Vis
    assert test_window.showing == True

    QtTest.QTest.qWait(500)

    # navigate to export images tab
    test_window.window.tabs['slider'].setCurrentIndex(4)

    # click export images button
    qtbotbis.mouseClick(
        test_window.window.widget_controls['button']['export_images'], QtCore.Qt.MouseButton.LeftButton)

    # wait for export to finish
    i = 0
    while test_window.window.export_in_progress == True and test_window.window.last_export == None and i < 10:
        QtTest.QTest.qWait(500)
    
    # check the export has finished
    assert test_window.window.export_in_progress == False
    assert test_window.window.last_export != None
    assert i < 10

    # check not crashed
    assert test_window.showing == True
