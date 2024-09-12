# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

import pytest
from PyQt6 import QtTest, QtWidgets, QtCore
from pytestqt.plugin import QtBot
import IQM_Vis


def get_UI():
    image1 = IQM_Vis.examples.images.IMAGE1
    image2 = IQM_Vis.examples.images.IMAGE2
    images = [image1, image2]
    print(f'Images files: {images}')

    MAE = IQM_Vis.IQMs.MAE()
    MSE = IQM_Vis.IQMs.MSE()
    SSIM = IQM_Vis.IQMs.SSIM()

    metrics = {'MAE': MAE,
               'MSE': MSE,
               '1-SSIM': SSIM}

    MSE_image = IQM_Vis.IQMs.MSE(return_image=True)
    SSIM_image = IQM_Vis.IQMs.SSIM(return_image=True)
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
                               metric_images=metric_images,
                               test=True)
    return test_app


# building and closing function of UI for testing
@pytest.fixture(scope='function')
def build_IQM_Vis():
    # QtTest.QTest.qWait(5000)
    # Setup 
    test_window = get_UI()
    qtbotbis = QtBot(test_window.window)

    yield test_window, qtbotbis

    # Clean up
    QtTest.QTest.qWait(100)

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
    # QtTest.QTest.qWait(5000)


def test_build_2(build_IQM_Vis):
    test_window, _ = build_IQM_Vis
    assert test_window.showing == True


