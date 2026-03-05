# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
'''
Helper functions for metric computation
'''
import numpy as np
import torch


def _numpy_to_torch_image(image: np.ndarray) -> torch.Tensor:
    '''Convert a numpy image (H×W or H×W×C) to a float32 PyTorch batch tensor (1×C×H×W).

    Args:
        image: Input image array. Either greyscale (H, W) or colour (H, W, C).

    Returns:
        A 4-D tensor with shape (1, C, H, W).
    '''
    if len(image.shape) == 2:
        image = np.expand_dims(image, axis=2)
    image = image.transpose((2, 0, 1))
    image = np.expand_dims(image, axis=0)   # make into batch one 1
    image = torch.from_numpy(image)
    return image


def _check_shapes(im_ref: np.ndarray, im_comp: np.ndarray) -> None:
    '''Raise :exc:`ValueError` if the two images do not have the same shape.

    Args:
        im_ref: Reference image array.
        im_comp: Comparison image array.

    Raises:
        ValueError: If ``im_ref.shape != im_comp.shape``.
    '''
    if im_ref.shape != im_comp.shape:
        raise ValueError(
            f'Refence and transformed images need to have the same shape not: {im_ref.shape} and {im_comp.shape}')
