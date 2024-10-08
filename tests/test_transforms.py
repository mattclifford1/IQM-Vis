# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

'''
Test that all of the transforms work as expected
'''
import numpy as np
from IQM_Vis.transforms import get_all_transforms
from IQM_Vis.utils import load_image
from IQM_Vis.examples.images import IMAGE2


def _get_test_image():
    return load_image(IMAGE2)


def test_all_transforms_init_value_no_change_image():
    # make a mock image
    image = _get_test_image()
    # test that the default value doesn't change the image
    tol = 0.0
    all_transfoms = get_all_transforms()
    for name, transform in all_transfoms.items():
        if 'init_value' in transform:
            value = transform['init_value']
        else:
            value = 0
        assert np.allclose(transform['function'](image, value), image, rtol=tol)


def test_all_transforms_min_max_specified():
    # make a mock image
    image = _get_test_image()
    # test that the default value doesn't change the image
    tol = 0.0
    all_transfoms = get_all_transforms()
    # test that the min and max values work
    for name, transform in all_transfoms.items():
        assert 'min' in transform or 'max' in transform


def test_all_transforms_min_change_image():
    # make a mock image
    image = _get_test_image()
    # test that the default value doesn't change the image
    tol = 0.0
    all_transfoms = get_all_transforms()
    # test that the min and max values work
    for name, transform in all_transfoms.items():
        if 'init_value' in transform:
            if transform['init_value'] == transform['min']:
                continue
        else:
            if transform['min'] == 0:
                continue
        assert not np.allclose(transform['function'](image, transform['min']), image, rtol=tol)


def test_all_transforms_max_change_image():
    # make a mock image
    image = _get_test_image()
    # test that the default value doesn't change the image
    tol = 0.0
    all_transfoms = get_all_transforms()
    # test that the min and max values work
    for name, transform in all_transfoms.items():
        if 'init_value' in transform:
            if transform['init_value'] == transform['max']:
                continue
        else:
            if transform['max'] == 0:
                continue
        assert not np.allclose(transform['function'](image, transform['max']), image, rtol=tol)


if __name__ == '__main__':
    test_all_transforms_max_change_image()
