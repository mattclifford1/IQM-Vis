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


from IQM_Vis.transforms.additive_noise import Gaussian_noise


def test_gaussian_noise_reject_low_noise_returns_array():
    """reject_low_noise=True must not crash and must return a valid array."""
    img = _get_test_image()
    noiser = Gaussian_noise(reject_low_noise=True)
    result = noiser(img, 0.1)
    assert isinstance(result, np.ndarray)
    assert result.shape == img.shape


def test_additive_noise_best_fallback_no_unbound_error():
    """Bug 4 regression: when every iteration returns img unchanged, the
    best-is-None fallback must prevent UnboundLocalError."""

    class _AlwaysAbsorbedNoise(Gaussian_noise):
        def _make_noisey_image(self, img: np.ndarray):
            # non-zero expected_noise but no actual change after clipping
            return img.copy(), np.ones_like(img)

    img = _get_test_image()
    noiser = _AlwaysAbsorbedNoise(reject_low_noise=True, max_iter=3, acceptable_percent=0.9)
    result = noiser(img, 0.1)
    assert isinstance(result, np.ndarray)
    assert np.allclose(result, img)


if __name__ == '__main__':
    test_all_transforms_max_change_image()
