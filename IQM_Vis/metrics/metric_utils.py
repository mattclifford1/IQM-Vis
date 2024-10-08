# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
'''
Helper functions for metric computation
'''
import numpy as np
import torch

def _numpy_to_torch_image(image):
    if len(image.shape) == 2:
        image = np.expand_dims(image, axis=2)
    image = image.transpose((2, 0, 1))
    image = np.expand_dims(image, axis=0)   # make into batch one 1
    image = torch.from_numpy(image)
    return image


def _check_shapes(im_ref, im_comp):
    '''
    make sure both images have the same dimensions
    '''
    if im_ref.shape != im_comp.shape:
        raise ValueError(
            f'Refence and transformed images need to have the same shape not: {im_ref.shape} and {im_comp.shape}')
