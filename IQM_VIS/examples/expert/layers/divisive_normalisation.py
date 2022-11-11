"""
The :mod:`expert.layers.divisive_normalisation` module holds classes of
layers for a network that use divisive normalisation. This includes
generalised divisive normalisation.
"""
# Author: Alex Hepburn <alex.hepburn@bristol.ac.uk>
# License: new BSD

import torch
import torch.nn as nn
import torch.nn.functional as F

__all__ = ['GDN']


class GDN(nn.Module):
    """
    Generalised Divisve Normalisation proposed in [BALLE2015GDN]_.

    The activation function this layer implements when kernel size is 1 is
    given by:
    .. math::
        y[i] = x[i] / sqrt(beta[i] + sum_j(gamma[j, i] * x[j]^2))
    where `i` and `j` run over channels.

    If the kernel_size is kept to the default value of 1, this represents the
    true generalised divisve normalisation proposed in [BALLE2015GDN]_. If the
    kernel size is larger than 1, the convolution acts not only channel wise
    but also acts spatially. This is called spatial generalised divisive
    normalisation.

    .. [BALLE2015GDN] Ballé, Johannes, et al. Density Modeling of Images Using
       a Generalized Normalization Transformation. Nov. 2015. arxiv.org,
       https://arxiv.org/abs/1511.06281v4.

    Parameters
    ----------
    n_channels : int
        Number of channels that the input to this layer will have.
    kernel_size : int, optional (default=1)
        Size of the kernel. A square kernel is always used and will have shape
        [kernel_size, kernel_size]
    stride : int, optional (default=1)
        The stride of the convolution in the forward pass.
    padding : int, optional (default=0)
        The padding to be used in the convolution in the forward pass. In order
        to get the output of the convolution to be the same size as the input,
        to avoid having to interpolate, then the ``padding`` parameter should
        be chosen carefully.
    gamma_init : float, optional (default=0.1)
        The value that the gamma matrix will be initialised with, it will be
        the identity multiplied by this value.
    reparam_offset : float, optional (default=2*1e-18)
    beta_min : float, optional (default=1e-6)
        The minimum value that the beta value can reach.
    apply_independently : boolean, optional (default=False)
        A boolean that determines whether this operation is applied channel
        wise or not. If not, then the divisive normalisation just divides each
        channel by a learnable parameter, and they are treated independently.

    Raises
    ------
    TypeError
        ``n_channels`` parameter is not an integer larger than 0. ``stride``
        parameter is not an integer larger than 0. ``padding`` parameter is not
        an integer larger or equal to 0. ``gamma_init`` parameter is not a
        positive float. ``reparam_offset`` parameter is not a positive float.
        ``beta_min`` parameter is not a positive float. ``apply_independently``
        is not a boolean.

    Attributes
    ----------
    reparam_offset : float
        Reparameterisation offset as to avoid gamma or beta going close to zero
        and the gradients when backpropogating to approaching zero.
    beta_reparam : float
        Reparameterisation offset for the beta parameter specifically.
    groups : int
        Number of groups to use in the convolution operation. If
        ``apply_independently`` is ``True`` then this should be 1, otherwise
        equal to ``n_channels``.
    gamma : torch.Tensor
        The torch tensor for the weights to be used in the convolution
        operation.
    beta : torch.Tensor
        The torch tensor for the bias to be used in the convoltuion operation.
    """

    def __init__(self,
                 n_channels: int,
                 kernel_size: int = 1,
                 stride: int = 1,
                 padding: int = 0,
                 gamma_init: float = .1,
                 reparam_offset: float = 2**-18,
                 beta_min: float = 1e-6,
                 apply_independently: bool = False) -> None:
        """
        Constructs a ``GDN`` generalised divisive normalisation class.
        """
        super(GDN, self).__init__()
        assert self._validate_input(n_channels, kernel_size, stride, padding,
                                    gamma_init, reparam_offset, beta_min,
                                    apply_independently)
        self.stride = stride
        self.padding = padding
        self.reparam_offset = reparam_offset
        self.beta_reparam = (beta_min + self.reparam_offset**2)**0.5

        if apply_independently:
            self.groups = n_channels
        else:
            self.groups = 1

        # Initialise the gamma and beta parameters
        gamma_bound = self.reparam_offset
        gamma = torch.eye(n_channels, dtype=torch.float)
        gamma = gamma.view(n_channels, n_channels, 1, 1)
        gamma = gamma.repeat(1, 1, kernel_size, kernel_size)
        gamma = torch.sqrt(gamma_init*gamma + self.reparam_offset**2)
        gamma = torch.mul(gamma, gamma)
        if apply_independently:
            gammas = [g[i, :, :] for i, g in enumerate(gamma)]
            gamma = torch.stack(gammas).unsqueeze(1)
        self.gamma = nn.Parameter(gamma)
        beta = torch.ones((n_channels,))
        beta = torch.sqrt(beta + self.reparam_offset**2)
        self.beta = nn.Parameter(beta)

    def _validate_input(self,
                        n_channels: int,
                        kernel_size: int,
                        stride: int,
                        padding: int,
                        gamma_init: float,
                        reparam_offset: float,
                        beta_min: float,
                        apply_independently: bool) -> bool:
        """
        Validates input of the generalised divisive normalisation class.

        For the description of the input parameters and exceptions raised by
        this function, please see the documentation of the
        :class:`expert.layers.divisive_normalisation.GDN` class.

        Returns
        -------
        is_valid
            ``True`` if input is valid, ``False`` otherwise.
        """
        is_valid = False

        if not isinstance(n_channels, int) or n_channels <= 0:
            raise TypeError('n_channels parameter must be an integer greater '
                            'than 0.')

        if not isinstance(kernel_size, int) or kernel_size <= 0:
            raise TypeError('kernel_size parameter must be an integer greater '
                            'than 0.')

        if not isinstance(stride, int) or stride <= 0:
            raise TypeError('stride parameter must be an integer greater than '
                            '0.')

        if not isinstance(padding, int) or padding < 0:
            raise TypeError('padding parameter must be a positive integer.')

        if not isinstance(gamma_init, float) or gamma_init < 0:
            raise TypeError('gamma_init parameter must be a positive float.')

        if not isinstance(reparam_offset, float) or reparam_offset < 0:
            raise TypeError('reparam_offset parameter must be a positive '
                            'float.')

        if not isinstance(beta_min, float) or beta_min < 0:
            raise TypeError('beta_min parameter must be a positive float.')

        if not isinstance(apply_independently, bool):
            raise TypeError('apply_independently parameter must be a boolean.')

        is_valid = True
        return is_valid

    def clamp_parameters(self) -> None:
        """
        Clamps the gamma and beta parameters that are used in the convolution.

        The gamma and beta parameters are clamped, ignoring the gradient of
        the clamping, to the ``reparam_offset`` and ``beta_reparam``
        parameters.
        """
        with torch.no_grad():
            self.gamma = nn.Parameter(torch.clamp(self.gamma.data,
                                                  min=self.reparam_offset))
            self.beta = nn.Parameter(torch.clamp(self.beta.data,
                                                 min=self.beta_reparam))

    def forward(self,
                x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the layer

        Parameters
        ----------
        x : torch.Tensor
            The input to the layer. Must be of shape [batch_size, channels,
            height, width].

        Raises
        ------
        TypeError:
            Input parameter ``x`` is not of dtype torch.float.

        Returns
        -------
        output : torch.Tensor
            Output of the generalised divisive normalisation layer.
        """
        if x.dtype != torch.float32:
            raise TypeError('Input x must be of type torch.float32.')

        self.clamp_parameters()
        norm_pool = F.conv2d(torch.mul(x, x), self.gamma, bias=self.beta,
                             groups=self.groups, stride=self.stride,
                             padding=self.padding)
        norm_pool = torch.sqrt(norm_pool)
        _, _, height, width = x.size()
        image_size = [int(height), int(width)]
        norm_pool = F.interpolate(norm_pool, size=image_size)
        output = x / norm_pool
        return output
