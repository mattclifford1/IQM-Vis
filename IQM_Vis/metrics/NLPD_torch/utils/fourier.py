"""
The :mod:`expert.utils.fourier` module holds functions for use in Fourier
domain and wavelet transforms
"""
# Author: Alex Hepburn <alex.hepburn@bristol.ac.uk>
# License: new BSD

import math

import torch

from .interp1d import Interp1d

__all__ = ['harmonic_column', 'raised_cosine', 'steer_to_harmonics',
           'point_operation_filter']


def harmonic_column(harmonic: torch.Tensor,
                    angles: torch.Tensor,
                    phase: str) -> torch.Tensor:
    """
    For a singular harmonic, generates the neccesary values to compute
    steering matrix.

    FFor the description of the input parameters and exceptions raised by
    this function, please see the documentation of the
    :func:`expert.models.pyramids.SteerableWavelet.steer_to_harmonics`
    function.

    Returns
    -------
    column : torch.Tensor
        Column to create a steer matrix for harmonic.
    """
    if harmonic == 0:
            column = torch.ones(angles.size(0), 1)
    else:
        args = harmonic * angles
        sin_args = torch.sin(args).unsqueeze(1)
        cos_args = torch.cos(args).unsqueeze(1)
        if phase == 'sin':
            column = torch.cat([sin_args, -cos_args], axis=1)
        else:
            column = torch.cat([cos_args, sin_args], axis=1)

    return column

def raised_cosine(width: int = 1,
                  position: float = -0.5,
                  func_min: float = 0.0,
                  func_max: float = 1.0,
                  size: int = 256) -> torch.Tensor:
    """
    Raised cosine function.

    Returns the X and Y values of a raised cosine soft threshold function.

    Parameters
    ----------
    width : int, optional (default=1)
        Width of region for transition.
    position : float, optional (default=-0.5)
        The location of the center of threshold.
    func_min : float, optional (default=0.0)
        Value to the left of the transition.
    func_max : float, optional (default=1.0)
        Value to the right of the transition.
    size : int, optional (default=256)
            Number of points to sample is `size+2`.
    Returns
    -------
    X : torch.Tensor
        X values for rasied cosine function.
    Y : torch.Tensor
        Y values for raised cosine function.
    """
    X = math.pi *  torch.arange(-size-1, 2)/ (2 * size)
    Y = func_min + (func_max-func_min) * torch.cos(X)**2
    Y[0] = Y[1]
    Y[-1] = Y[-2]
    X = position + (2*width/math.pi) * (X + math.pi/4)
    return (X, Y)

def steer_to_harmonics(harmonics: torch.Tensor,
                       angles: torch.Tensor,
                       phase: str = 'sin') -> torch.Tensor:
    """
    Maps a directional basis set onto the angular Fourier harmonics.

    Parameters
    ----------
    harmonics : torch.Tensor
    angles : torch.Tensor
    phase : str, optional (default='sin')

    Raises
    ------
    TODO: error checking input dimensions

    Returns
    -------
    harmonics_matrix : torch.Tensor
    """
    num = 2*harmonics.size(0) - (harmonics == 0).sum()
    zero_indices = harmonics == 0
    zero_imtx = torch.ones(angles.size(0), zero_indices.sum())
    non_zero_imtx = angles.repeat(num-zero_indices.sum(), 1)

    columns = [harmonic_column(h, angles, phase) for h in harmonics]
    matrix = torch.cat(columns, axis=1)

    harmonic_matrix = torch.pinverse(matrix)
    return harmonic_matrix

def point_operation_filter(image : torch.Tensor,
                           samples : torch.Tensor,
                           origin : float,
                           increment : float) -> torch.Tensor:
    """
    Performs 1-D Interpolation.

    Parameters
    ----------
    image : torch.Tensor
    samples : torch.Tensor
    origin : float
    increment : float

    Returns
    -------
    mask : torch.Tensor
        Values that are interpolated and reshaped to shape of image.
    """
    interp_X = origin + increment*torch.arange(0, samples.size(0))

    interpolated_values = Interp1d()(interp_X, samples, torch.flatten(image))
    mask = interpolated_values.reshape(image.size())
    return mask

def roll(x, shift, dim):
    """
    Similar to np.roll but applies to PyTorch Tensors
    https://github.com/khammernik/sigmanet
    """
    if isinstance(shift, (tuple, list)):
        assert len(shift) == len(dim)
        for s, d in zip(shift, dim):
            x = roll(x, s, d)
        return x
    shift = shift % x.size(dim)
    if shift == 0:
        return x
    left = x.narrow(dim, 0, x.size(dim) - shift)
    right = x.narrow(dim, x.size(dim) - shift, shift)
    return torch.cat((right, left), dim=dim)


def fftshift(x, dim=None):
    """
    Similar to np.fft.fftshift but applies to PyTorch Tensors
    """
    if dim is None:
        dim = tuple(range(x.dim()))
        shift = [dim // 2 for dim in x.shape]
    elif isinstance(dim, int):
        shift = x.shape[dim] // 2
    else:
        shift = [x.shape[i] // 2 for i in dim]
    return roll(x, shift, dim)


def ifftshift(x, dim=None):
    """
    Similar to np.fft.ifftshift but applies to PyTorch Tensors
    """
    if dim is None:
        dim = tuple(range(x.dim()))
        shift = [(dim + 1) // 2 for dim in x.shape]
    elif isinstance(dim, int):
        shift = (x.shape[dim] + 1) // 2
    else:
        shift = [(x.shape[i] + 1) // 2 for i in dim]
    return roll(x, shift, dim)
