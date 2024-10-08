# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

'''
Test that all of the metrics work as expected
'''
import os
import numpy as np
from IQM_Vis.metrics import get_all_metrics, get_all_metric_images
from IQM_Vis.utils import load_image
from IQM_Vis.examples.images import IMAGE2


def _get_test_image():
    return load_image(IMAGE2)


def test_all_metrics_initialise():
    # get all metrics 
    all_metrics = get_all_metrics()
    for name, metric in all_metrics.items():
        # assert that the metric is callable
        assert callable(metric)


def test_all_metrics_images_initialise():
    # get all metrics 
    all_metrics = get_all_metric_images()
    for name, metric in all_metrics.items():
        # assert that the metric is callable
        assert callable(metric)


def test_all_metrics_process_image():
    # make a mock image
    image = _get_test_image()
    # test that the default value doesn't change the image
    all_metrics = get_all_metrics()
    for name, metric in all_metrics.items():
        val = metric(image, image)
        if isinstance(val, np.ndarray):
            assert val.size == 1
        else:
            assert isinstance(val, float) or isinstance(val, int)


def test_all_metric_images_process_image():
    # make a mock image
    image = _get_test_image()
    # test that the default value doesn't change the image
    all_metrics = get_all_metric_images()
    for name, metric in all_metrics.items():
        img = metric(image, image)
        assert len(img.shape) == 3 or len(img.shape) == 2


if __name__ == '__main__':
    test_all_metrics_initialise()
    test_all_metrics_images_initialise()
    test_all_metrics_process_image()
