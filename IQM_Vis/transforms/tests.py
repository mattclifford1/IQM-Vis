# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

'''
Test that all of the transforms work as expected
'''
import numpy as np
from IQM_Vis.transforms import get_all_transforms

def test_all_transforms():
    # make a mock image
    image = np.random.rand(256, 256, 3)
    # test that the default value doesn't change the image
    tol = 0.0
    all_transfoms = get_all_transforms()
    for name, transform in all_transfoms.items():
        if 'init_value' in transform:
            assert np.allclose(transform['function'](image, transform['init_value']), image, rtol=tol)
        # also test default in the arg defn
        assert np.allclose(transform['function'](image), image, rtol=tol)

if __name__ == '__main__':
    test_all_transforms()