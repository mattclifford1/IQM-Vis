# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

import pytest
from PyQt6 import QtTest, QtWidgets, QtCore
from pytestqt.plugin import QtBot, _close_widgets
import IQM_Vis
import threading


def get_UI():
    image1 = IQM_Vis.examples.images.IMAGE1
    image2 = IQM_Vis.examples.images.IMAGE2
    images = [image1, image2]
    print(f'Images files: {images}')

    MAE = IQM_Vis.IQMs.MAE()
    MSE = IQM_Vis.IQMs.MSE()

    metrics = {'MAE': MAE,
               'MSE': MSE,
               }

    MSE_image = IQM_Vis.IQMs.MSE(return_image=True)
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


# building and closing function of UI for testing
@pytest.fixture
def build_IQM_Vis():

    test_window = get_UI()
    qtbotbis = QtBot(test_window.window)

    yield test_window, qtbotbis

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


@pytest.fixture
def build_exp(build_IQM_Vis):
    test_window, qtbotbis = build_IQM_Vis
    assert test_window.showing == True
    # launch experiment
    QtTest.QTest.qWait(1000)
    qtbotbis.mouseClick(
        test_window.window.widget_controls['button']['launch_exp'], QtCore.Qt.MouseButton.LeftButton)
    QtTest.QTest.qWait(500)
    return test_window, qtbotbis


def test_experiment_runs(build_exp):
    test_window, qtbotbis = build_exp
    
    # test launched
    assert test_window.window.experiment.experiments_tab.currentIndex() == 0

    # Start experiment
    qtbotbis.mouseClick(
        test_window.window.experiment.widget_experiments['setup']['start_button'],
        QtCore.Qt.MouseButton.LeftButton)
    assert test_window.window.experiment.experiments_tab.currentIndex() == 1

    # Start
    qtbotbis.mouseClick(
        test_window.window.experiment.widget_experiments['preamble']['start_button'],
        QtCore.Qt.MouseButton.LeftButton)
    assert test_window.window.experiment.experiments_tab.currentIndex() == 2


    # run through experiment
    i = 0
    while test_window.window.experiment.experiments_tab.currentIndex() == 2 and i < 50:
        # just click left image
        qtbotbis.mouseClick(
            test_window.window.experiment.widget_experiments['exp']['A']['data'], QtCore.Qt.MouseButton.LeftButton)
        QtTest.QTest.qWait(50)
        i += 1

    # check finished
    QtTest.QTest.qWait(500)
    assert test_window.window.experiment.experiments_tab.currentIndex() == 3
    QtTest.QTest.qWait(100)


    # leave experiment
    qtbotbis.mouseClick(
        test_window.window.experiment.widget_experiments['final']['quit_button'], QtCore.Qt.MouseButton.LeftButton)
    QtTest.QTest.qWait(100)



