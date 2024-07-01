# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

import numpy as np
import pytest
from PyQt6 import QtTest, QtWidgets, QtCore
from pytestqt.plugin import QtBot
import IQM_Vis

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


# building and closing function of UI for testing
@pytest.fixture(scope='function')
def build_IQM_Vis():
    # Setup
    test_window = get_UI()
    qtbotbis = QtBot(test_window.window)

    yield test_window, qtbotbis

    # Clean up
    QtTest.QTest.qWait(1000)

    # need to handle the closing dialog
    def handle_dialog():
        messagebox = QtWidgets.QApplication.activeWindow()
        yes_button = messagebox.button(
            QtWidgets.QMessageBox.StandardButton.Yes)
        qtbotbis.mouseClick(
            yes_button, QtCore.Qt.MouseButton.LeftButton, delay=1)

    QtCore.QTimer.singleShot(100, handle_dialog)

    # test_window.window.quit()
    test_window.window.main.close()
    QtTest.QTest.qWait(1000)


@pytest.fixture(scope='function')
def test_build_3(build_IQM_Vis):
    test_window, _ = build_IQM_Vis
    assert test_window.showing == True


def test_3(test_build_3):
    return