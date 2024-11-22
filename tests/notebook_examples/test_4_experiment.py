'''
this test only crashes as part of pytest but will run fine on its own e.g.

$ pytest tests/run_this_individually_4_experiment_.py 

TODO: find out why that is the case...
    will likely be to do with the cleanup of closing the app not working fully
    - not just for this file but the 4th pyqt window opened crashes...
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

import pytest
from PyQt6 import QtTest, QtCore

import IQM_Vis
import sys
import os
sys.path.append(os.path.abspath('..'))
from tests.QtBot_utils import BotTester


def get_UI():
    image1 = IQM_Vis.examples.images.IMAGE1
    image2 = IQM_Vis.examples.images.IMAGE2
    images = [image1, image2]

    MAE = IQM_Vis.metrics.MAE()
    MSE = IQM_Vis.metrics.MSE()

    metrics = {'MAE': MAE,
               'MSE': MSE,
               }

    MSE_image = IQM_Vis.metrics.MSE(return_image=True)
    metric_images = {'MSE': MSE_image,
                     }

    brightness = IQM_Vis.transforms.brightness

    transformations = {
        # normal input
        'brightness': {'min': -1.0, 'max': 1.0, 'function': brightness},
    }

    test_app = IQM_Vis.make_UI(transformations=transformations,
                               image_list=images,
                               metrics=metrics,
                               metric_images=metric_images,
                               test=True)
    return test_app


build_IQM_Vis = BotTester(get_UI=get_UI).build_IQM_Vis


@pytest.fixture(scope='function')
def build_exp(build_IQM_Vis):
    test_window, qtbotbis = build_IQM_Vis
    assert test_window.showing == True
    # launch experiment
    QtTest.QTest.qWait(500)

    # qtbotbis.mouseClick(
    #     test_window.window.tabs['slider'], QtCore.Qt.MouseButton.LeftButton)
    test_window.window.tabs['slider'].setCurrentIndex(3)


    QtTest.QTest.qWait(500)

    qtbotbis.mouseClick(
        test_window.window.widget_controls['button']['launch_exp_2AF'], QtCore.Qt.MouseButton.LeftButton)
    QtTest.QTest.qWait(500)
    yield test_window, qtbotbis
    QtTest.QTest.qWait(500)


def test_experiment_runs(build_exp):
    test_window, qtbotbis = build_exp
    
    # test launched
    assert test_window.window.experiment_2AF.experiments_tab.currentIndex() == 0

    # Start experiment
    qtbotbis.mouseClick(
        test_window.window.experiment_2AF.widget_experiments['setup']['start_button'],
        QtCore.Qt.MouseButton.LeftButton)
    assert test_window.window.experiment_2AF.experiments_tab.currentIndex() == 1

    # Start
    qtbotbis.mouseClick(
        test_window.window.experiment_2AF.widget_experiments['preamble']['start_button'],
        QtCore.Qt.MouseButton.LeftButton)
    assert test_window.window.experiment_2AF.experiments_tab.currentIndex() == 2


    # run through experiment
    i = 0
    while test_window.window.experiment_2AF.experiments_tab.currentIndex() == 2 and i < 50:
        # just click left image
        qtbotbis.mouseClick(
            test_window.window.experiment_2AF.widget_experiments['exp']['A']['data'], QtCore.Qt.MouseButton.LeftButton)
        QtTest.QTest.qWait(50)
        i += 1

    # check finished
    QtTest.QTest.qWait(500)
    assert test_window.window.experiment_2AF.experiments_tab.currentIndex() == 3
    QtTest.QTest.qWait(100)


    # leave experiment
    QtTest.QTest.qWait(1000)
    qtbotbis.mouseClick(
        test_window.window.experiment_2AF.widget_experiments['final']['quit_button'], QtCore.Qt.MouseButton.LeftButton)



