"""
The :mod:`expert.utils.conv` module holds util functions for convolutions, like
padding to maintain the size of the image.
"""
# Author: Alex Hepburn <alex.hepburn@bristol.ac.uk>
# License: new BSD

from typing import List

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

__all__ = ['pad']


def pad(im_size, filt_size, stride):
    """
    Returns the amount of padding needed on [height, width] to maintain image
    size.

    This function calculates the amount of padding needed to keep the output
    image shape the same as the input image shape.

    Parameters
    ----------
    im_size : List[int]
        List of [height, width] of the image to pad.
    filt_size : int
        The width of the filter being used in the convolution, assumed to be
        square.
    stride : int
        Amount of stride in the convolution.

    Returns
    -------
    padding : List[int]
        Amount of padding needed for []
    """
    out_height = math.ceil(float(im_size[0]) / float(stride))
    out_width  = math.ceil(float(im_size[1]) / float(stride))

    pad_h = max((out_height - 1) * stride + filt_size - im_size[0], 0)
    pad_w = max((out_width - 1) * stride + filt_size - im_size[1], 0)

    pad_top = pad_h // 2
    pad_bottom = pad_h - pad_top
    pad_left = pad_w // 2
    pad_right = pad_w- pad_left

    # Append lists to each other for use in func:`torch.nn.functional.pad`.
    return [pad_left, pad_right, pad_top, pad_bottom]
