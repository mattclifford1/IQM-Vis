# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

from tests.QtBot_utils import BotTester
import IQM_Vis

import sys
import os
sys.path.append(os.path.abspath('..'))


def get_UI():
    image1 = IQM_Vis.examples.images.IMAGE1
    image2 = IQM_Vis.examples.images.IMAGE2
    images = [image1, image2]
    print(f'Images files: {images}')

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
                               metric_images=metric_images,
                               test=True)
    return test_app


build_IQM_Vis = BotTester(get_UI=get_UI).build_IQM_Vis


def test_build_1(build_IQM_Vis):
    test_window, _ = build_IQM_Vis
    assert test_window.showing == True


