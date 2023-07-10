"""
The :mod:`expert.layers.wavelet_transformation` module holds classes of
layers for wavelet transformations.
"""
# Author: Alex Hepburn <alex.hepburn@bristol.ac.uk>
# License: new BSD

# import expert.utils.fourier as fourier ## needed for SteerableWavelet - includes extra dependancies so wont use for now
from .utils import conv as conv_utils
from .utils import pyramid_filters as pyr_filts
from .utils import fourier
from .layers import divisive_normalisation as expert_divisive_normalisation
import torch.nn.functional as F
import torch.nn as nn
import torch
from typing import List, Union

import math

import numpy as np
np.set_printoptions(precision=2)  # TODO: remove


__all__ = ['SteerableWavelet', 'SteerablePyramid', 'LaplacianPyramid',
           'LaplacianPyramidGDN']

LAPLACIAN_FILTER = np.array([[0.0025, 0.0125, 0.0200, 0.0125, 0.0025],
                             [0.0125, 0.0625, 0.1000, 0.0625, 0.0125],
                             [0.0200, 0.1000, 0.1600, 0.1000, 0.0200],
                             [0.0125, 0.0625, 0.1000, 0.0625, 0.0125],
                             [0.0025, 0.0125, 0.0200, 0.0125, 0.0025]],
                            dtype=np.float32)


class LaplacianPyramid(nn.Module):
    def __init__(self, k, dims=3, filt=None, trainable=False):
        super(LaplacianPyramid, self).__init__()
        if filt is None:
            filt = np.reshape(np.tile(LAPLACIAN_FILTER, (dims, 1, 1)),
                              (dims, 1, 5, 5))
        self.k = k
        self.trainable = trainable
        self.dims = dims
        self.filt = nn.Parameter(torch.Tensor(filt), requires_grad=False)
        self.dn_filts, self.sigmas = self.DN_filters()

    def DN_filters(self):
        sigmas = [0.0248, 0.0185, 0.0179, 0.0191, 0.0220, 0.2782]
        dn_filts = []
        dn_filts.append(torch.Tensor(np.reshape([[0, 0.1011, 0],
                                                 [0.1493, 0, 0.1460],
                                                 [0, 0.1015, 0.]]*self.dims,
                                                (self.dims,  1, 3, 3)).astype(np.float32)))

        dn_filts.append(torch.Tensor(np.reshape([[0, 0.0757, 0],
                                                 [0.1986, 0, 0.1846],
                                                 [0, 0.0837, 0]]*self.dims,
                                                (self.dims, 1, 3, 3)).astype(np.float32)))

        dn_filts.append(torch.Tensor(np.reshape([[0, 0.0477, 0],
                                                 [0.2138, 0, 0.2243],
                                                 [0, 0.0467, 0]]*self.dims,
                                                (self.dims, 1, 3, 3)).astype(np.float32)))

        dn_filts.append(torch.Tensor(np.reshape([[0, 0, 0],
                                                 [0.2503, 0, 0.2616],
                                                 [0, 0, 0]]*self.dims,
                                                (self.dims, 1, 3, 3)).astype(np.float32)))

        dn_filts.append(torch.Tensor(np.reshape([[0, 0, 0],
                                                 [0.2598, 0, 0.2552],
                                                 [0, 0, 0]]*self.dims,
                                                (self.dims, 1, 3, 3)).astype(np.float32)))

        dn_filts.append(torch.Tensor(np.reshape([[0, 0, 0],
                                                 [0.2215, 0, 0.0717],
                                                 [0, 0, 0]]*self.dims,
                                                (self.dims, 1, 3, 3)).astype(np.float32)))
        dn_filts = nn.ParameterList([nn.Parameter(x, requires_grad=self.trainable)
                                     for x in dn_filts])
        sigmas = nn.ParameterList([nn.Parameter(torch.Tensor(np.array(x)),
                                                requires_grad=self.trainable) for x in sigmas])
        return dn_filts, sigmas

    def pyramid(self, im):
        out = []
        J = im
        pyr = []
        for i in range(0, self.k):
            J_padding_amount = conv_utils.pad([J.size(2), J.size(3)],
                                              self.filt.size(3), stride=2)
            I = F.conv2d(F.pad(J, J_padding_amount, mode='reflect'), self.filt,
                         stride=2, padding=0, groups=self.dims)
            I_up = F.interpolate(I, size=[J.size(2), J.size(3)],
                                 align_corners=True, mode='bilinear')
            I_padding_amount = conv_utils.pad([I_up.size(2), I_up.size(3)],
                                              self.filt.size(3), stride=1)
            I_up_conv = F.conv2d(F.pad(I_up, I_padding_amount, mode='reflect'),
                                 self.filt, stride=1, padding=0,
                                 groups=self.dims)
            out = J - I_up_conv
            out_padding_amount = conv_utils.pad(
                [out.size(2), out.size(3)], self.dn_filts[i].size(2), stride=1)
            out_conv = F.conv2d(
                F.pad(torch.abs(out), out_padding_amount, mode='reflect'),
                self.dn_filts[i],
                stride=1,
                groups=self.dims)
            out_norm = out / (self.sigmas[i]+out_conv)
            pyr.append(out_norm)
            J = I
        return pyr

    def forward(self, x1, x2):
        # make inputs 3 channel if greyscale
        if x1.shape[1] == 1:
            x1 = torch.cat([x1, x1, x1], dim=1)
        if x2.shape[1] == 1:
            x2 = torch.cat([x2, x2, x2], dim=1)
        y1 = self.pyramid(x1)
        y2 = self.pyramid(x2)
        total = []
        # Calculate difference in perceptual space (Tensors are stored
        # strangley to avoid needing to pad tensors)
        for z1, z2 in zip(y1, y2):
            diff = (z1 - z2) ** 2
            sqrt = torch.sqrt(torch.mean(diff, (1, 2, 3)))
            total.append(sqrt)
        return torch.norm(torch.stack(total), 0.6)


class LaplacianPyramidGDN(nn.Module):
    def __init__(self, k, dims=3, filt=None):
        super(LaplacianPyramidGDN, self).__init__()
        if filt is None:
            filt = np.tile(LAPLACIAN_FILTER, (dims, 1, 1))
            filt = np.reshape(np.tile(LAPLACIAN_FILTER, (dims, 1, 1)),
                              (dims, 1, 5, 5))
        self.k = k
        self.dims = dims
        self.filt = nn.Parameter(torch.Tensor(filt))
        self.filt.requires_grad = False
        self.gdns = nn.ModuleList([expert_divisive_normalisation.GDN(
            dims, apply_independently=True) for i in range(self.k)])
        self.pad_one = nn.ReflectionPad2d(1)
        self.pad_two = nn.ReflectionPad2d(2)
        self.mse = nn.MSELoss(reduction='none')
        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear',
                                    align_corners=True)

    def pyramid(self, im):
        J = im
        pyr = []
        for i in range(0, self.k):
            I = F.conv2d(self.pad_two(J), self.filt, stride=2, padding=0,
                         groups=self.dims)
            I_up = self.upsample(I)
            I_up_conv = F.conv2d(self.pad_two(I_up), self.filt, stride=1,
                                 padding=0, groups=self.dims)
            if J.size() != I_up_conv.size():
                I_up_conv = torch.nn.functional.interpolate(
                    I_up_conv, [J.size(2), J.size(3)])
            pyr.append(self.gdns[i](J - I_up_conv))
            J = I
        return pyr

    def compare(self, x1, x2):
        y1 = self.pyramid(x1)
        y2 = self.pyramid(x2)
        total = []
        # Calculate difference in perceptual space (Tensors are stored
        # strangley to avoid needing to pad tensors)
        for z1, z2 in zip(y1, y2):
            diff = (z1 - z2) ** 2
            sqrt = torch.sqrt(torch.mean(diff, (1, 2, 3)))
            total.append(sqrt)
        return torch.norm(torch.stack(total), 0.6)


class SteerableWavelet(nn.Module):
    """
    Steerable wavelet pyramid.

    Performs a high-pass and low-pass filtering. The low-pass filtered image
    is then passed through ``wavelets`` wavelet transformations, each
    with a different orientation. This is done at ``scales`` dfferent scales
    where each scale is downsampled by ``downsampled``.

    TODO : pass dimension parameter into __init__ and precompute log_rad
           and angle.

    Parameters
    ----------
    stages : int, optional (default=4)
        Number of stages to be used in the pyramid.
    order: int, optional (default=3)
        Defined angular functions. Angular functions are
        `cos(theta-order\pi/(order+1))^order` (order is one less than the
        number of orientation bands).
    twidth : int, optional(default=1)
        width of the transition region of the radial lowpass function in
        octaves.

    Raises
    ------

    Attributes
    ----------
    num_orientations : integer
    harmincs : torch.Tensor
    angles : torch.Tensor
    steer_matrix : torch.Tensor
    Xrcos : torch.Tensor
    Yrcos : torch.Tensor
    YIrcos : torch.Tensor
    Xcosn : torch.Tensor
    const : float
    Ycosn : torch.Tensor
    """

    def __init__(self,
                 stages: int = 4,
                 order: int = 3,
                 twidth: int = 1):
        """
        Constructs a ``SteerableWavelet`` class.
        """
        super(SteerableWavelet, self).__init__()
        assert self._validate_input(stages, order, twidth)
        self.stages = stages
        self.num_orientations = order + 1
        self.twidth = twidth

        if self.num_orientations % 2 == 0:
            self.harmonics = torch.arange(0, self.num_orientations/2)*2+1
        else:
            self.harmonics = torch.arange(0, order)*2

        self.angles = torch.arange(0, order+1) * \
            math.pi / self.num_orientations
        self.steer_matrix = fourier.steer_to_harmonics(
            self.harmonics, self.angles, 'sin')

        # CONSTANTS
        self.Xrcos, self.Yrcos = fourier.raised_cosine(
            twidth, -twidth/2, func_min=0.0, func_max=1.0, size=10)
        self.Yrcos = torch.sqrt(self.Yrcos)
        self.YIrcos = torch.sqrt(1.0 - self.Yrcos**2)
        self.Xcosn = math.pi * torch.arange(-2047, 1024+2) / 1024  # (-2*pi:pi]
        self.const = 2**(2*order) * math.factorial(order)**2 \
            / (self.num_orientations * math.factorial(order*2))
        self.Ycosn = math.sqrt(self.const) * torch.cos(self.Xcosn)**order

        # Orientation angles
        self.band_angles = torch.Tensor(
            [self.Xcosn[0] + math.pi*i/self.num_orientations
             for i in range(self.num_orientations)])

    def _validate_input(self,
                        stages: int,
                        order: int,
                        twidth: int) -> bool:
        """
        Validates input of the steerable wavelet class.

        For the description of the input parameters and exceptions raised by
        this function, please see the documentation of the
        :class:`expert.models.pyramids.SteerableWavelet` class.

        Returns
        -------
        is_valid
            ``True`` if input is valid, ``False`` otherwise.
        """
        is_valid = False

        if not isinstance(stages, int) or stages <= 0:
            raise TypeError('stages parameter must be an integer greater than '
                            '0.')

        if not isinstance(order, int) or order <= 0:
            raise TypeError('order parameter must be an integer '
                            'greater than 0.')

        if not isinstance(twidth, int) or twidth <= 0:
            raise TypeError('twidth parameter must be an integer greater than '
                            '0.')

        is_valid = True
        return is_valid

    def meshgrid_angle(self,
                       dims: List[int]) -> torch.Tensor:
        """
        Computes meshgrid of input dimensions and angles

        Takes the dimensions of an image, and computes a meshgrid over these
        values. Then computes the angles and log radians of this meshgrid.

        Parameters
        ----------
        dims : List[Integer]
            List of length two sepcificy [h, w] of image.

        Returns
        -------
        angle : torch.Tensor
            Angle of meshgrid.
        log_rad : torch.Tensor
            Angle in log radians.
        """
        ctr = [math.ceil((d+0.5)/2) for d in dims]
        vectors = [
            (torch.arange(1, dims[i]+1)-ctr[i]) / (dims[i]/2) for i in range(2)]
        yramp, xramp = torch.meshgrid(vectors[1], vectors[0])
        angle = torch.atan2(yramp, xramp)
        log_rad = torch.sqrt(xramp**2 + yramp**2)

        # Replace middle element in matrix
        log_rad[ctr[0]-1, ctr[1]-1] = log_rad[ctr[0]-1, ctr[1]-2]
        log_rad = torch.log2(log_rad)

        return angle, log_rad

    def _check_height(self,
                      size_x: torch.Size) -> bool:
        """
        Checks if dimensions of image is compatible with height of pyramid.

        Calculates the max height a pyramid with the given `size_x` and
        compares this with the height intialised with this pyramid.

        Parameters
        ----------
        size_x : torch.Size
            Size of input x. First dimension is batch dimension.

        Raises
        ------
        ValueError:
            If the maximum height of pyramid for `size_x` is larger than the
            height of `self.stages`

        Returns
        -------
        is_valid : boolean
            ``True`` the `size_x` dimensions are compatible with `self.stages`,
            else ``False``.
        """
        is_valid = False
        dims = list(size_x)[1:]
        max_height = math.floor(math.log2(min(dims))) - 2
        if self.stages > max_height:
            raise ValueError('Input maximum number of stages is %d but number '
                             'of pyramid stages is %d. Please use larger input '
                             'images or initialise pyramid with different '
                             'number of stages.' % (max_height, self.stages))

        is_valid = True
        return is_valid

    def _complex_number_product(self,
                                x: torch.Tensor) -> torch.Tensor:
        """
        Multiple tensor with imaginary number.

        If `o` is the order within the pyramid, then output `y` is given by
        .. math::
            \mathbf{y} = ((-\sqrt{-1})^o) * \mathbf{x}.

        The value of (-sqrt(-1))^order cycles through values. List below are
        the possible cases.
        If order % 4 == 0, (-sqrt(-1))^order = 1
        If order % 4 == 1, (-sqrt(-1))^order = -j
        If order % 4 == 2, (-sqrt(-1))^order = -1
        If order % 4 == 3, (-sqrt(-1))^order = j

        Parameters
        ----------
        x : torch.Tensor
            Input tensor.

        Returns
        -------
        y: torch.Tensor
            Output tensor.
        """
        value = ((self.num_orientations-1) % 4)
        if value == 0:  # x * 1
            return x
        else:
            real, imag = torch.unbind(x, -1)
            if value == 1:  # x * -j
                real_new = imag
                imag_new = -real
            elif value == 2:  # x * -1
                real_new = -real
                imag_new = -imag
            elif value == 3:  # x * j
                real_new = -imag
                imag_new = real
            return torch.stack((real_new, imag_new), -1)

    def forward(
        self,
        x: torch.tensor,
        upsample_output: bool = False
    ) -> Union[List[torch.Tensor], torch.Tensor]:
        """
        Forward pass of the pyramid.

        This function returns a lit of Tensors for the subbands in each stage
        of the pyramid or, if ``upsample_output`` is ``True``, a Tensor
        containing every subband at every level that has been upsampled to be
        the same size as the input Tensor.

        Parameters
        ----------
        x : torch.Tensor
            Input to the pyramid.
        upsample_output : boolean
            If ``True`` then the every subband will be upsampled to be the same
            size as the input and then stacked to be a singular tensor.

        Raises
        ------
        TypeError:
            Input parameter ``x`` is not of dtype torch.float.

        Returns
        -------
        pyramid : Union[List[torch.Tensor], Tensor]
            List of tensors, where the first tensor is the high pass residual,
            and from thereon each entry contains the subbands at each stage of
            the pyramid. The low pass residual is the last element in the
            pyramid. If ``upsample_output`` is ``True`` then this will be one
            Tensor where each subband has been upsample to be the same
            dimensions as the input.
        """
        assert self._check_height(x.size())

        dims = [x.size(1), x.size(2)]
        self.angle, self.log_rad = self.meshgrid_angle(dims=dims)

        low_mask = fourier.point_operation_filter(
            self.log_rad, self.YIrcos, origin=self.Xrcos[0],
            increment=self.Xrcos[1]-self.Xrcos[0]).to(x.device)
        self.low_mask = low_mask.view(1, low_mask.size(0), low_mask.size(1), 1)

        high_mask = fourier.point_operation_filter(
            self.log_rad, self.Yrcos, origin=self.Xrcos[0],
            increment=self.Xrcos[1]-self.Xrcos[0]).to(x.device)
        self.high_mask = high_mask.view(
            1, high_mask.size(0), high_mask.size(1), 1)

        # Shape [batch, height, width, 2] where last dimension is real and
        # imaginary part of Fourier transform.
        discrete_fourier_image = fourier.fftshift(
            torch.rfft(x, signal_ndim=2, onesided=False), dim=(-3, -2))

        # Calculate highpass and lowpass of the image.
        low_pass = discrete_fourier_image * self.low_mask
        high_pass = discrete_fourier_image * self.high_mask

        # First element in the pyramid will be the high pass residual
        high_pass_residual = torch.irfft(fourier.ifftshift(
            high_pass, dim=(-3, -2)), signal_ndim=2, onesided=False)
        pyramid = [high_pass_residual]

        # Intiailised parameters that are going to change each stage
        Xrcos = self.Xrcos
        log_rad = self.log_rad
        angle = self.angle

        # Stages in pyramid
        for h in range(0, self.stages):
            Xrcos = Xrcos - math.log2(2)
            himask = fourier.point_operation_filter(
                log_rad, self.Yrcos, origin=Xrcos[0],
                increment=Xrcos[1]-Xrcos[0])
            himask = himask.view(1, himask.size(0), himask.size(1), 1)

            # Orientation band masks
            angle_masks = torch.stack(
                [fourier.point_operation_filter(angle, self.Ycosn,
                                                origin=a, increment=self.Xcosn[1]-self.Xcosn[0])
                 for a in self.band_angles])
            fourier_band = (low_pass.permute(3, 0, 1, 2) *
                            angle_masks).unsqueeze(0).permute(0, 2, 3, 4, 1)
            # TODO: computation only works for batch_size=1
            fourier_band = fourier_band * himask
            fourier_band = self._complex_number_product(fourier_band)
            # Collapse from [batch, bands, height, width, 2] to
            # [batch*bands, height, width, 2] for ifft.
            bands = torch.irfft(fourier.ifftshift(
                fourier_band.view(-1, fourier_band.size(2),
                                  fourier_band.size(3), 2), dim=(-3, -2)), signal_ndim=2,
                                onesided=False)
            # Expand back out to [batch, bands, height, width] after doing
            # inverse fast fourier transform.
            bands = bands.view(x.size(0), self.num_orientations, bands.size(1),
                               bands.size(2))
            pyramid.append(bands)

            # Subsampling operations
            dims = [low_pass.size(1), low_pass.size(2)]
            ctr = [math.ceil((d+0.5)/2) for d in dims]
            lodims = [math.ceil((d-0.5)/2) for d in dims]
            loctr = [math.ceil((d+0.5)/2) for d in lodims]

            lostart = [c-l for c, l in zip(ctr, loctr)]
            loend = [ls+lo for ls, lo in zip(lostart, lodims)]

            log_rad = log_rad[lostart[0]:loend[0], lostart[1]:loend[1]]
            angle = angle[lostart[0]:loend[0], lostart[1]:loend[1]]
            low_pass = low_pass[:, lostart[0]:loend[0], lostart[1]:loend[1]]

            # Low pass to use in the next stage
            low_mask = fourier.point_operation_filter(
                log_rad, self.YIrcos, origin=Xrcos[0],
                increment=Xrcos[1]-Xrcos[0]).to(x.device)
            low_mask = low_mask.view(1, low_mask.size(0), low_mask.size(1), 1)
            low_pass = low_pass * low_mask

        low_pass_residual = torch.irfft(fourier.ifftshift(
            low_pass, dim=(-3, -2)), signal_ndim=2, onesided=False)
        pyramid.append(low_pass_residual)

        if upsample_output:
            original_size = [high_pass.size(2), high_pass.size(3)]
            pyr_upsample = [
                F.interpolate(stage, size=original_size) for stage in pyramid
            ]
            pyramid = torch.cat(pyr_upsample, dim=1)

        return pyramid


class SteerablePyramid(nn.Module):
    """
    Steerable pyramid model implemented in spatial domain, introduced in
    [SIMON1995PYR]_.

    Parameters
    ----------
    stages : int, optional (default=4)
        Number of stages to be used in the pyramid.
    num_orientations: int, optional (default=2)
        Number of orientations to be used at each stage of the pyramid (number
        of subbands). If ``pretrained`` is ``True`` then this must be 2 as the
        pretarined weights from the original implementation use 2 subbands.
    pretrained : bool, optional (default=False)
        Whether to load the pretrained filters, specified in the original paper
        [SIMON1995PYR]_.

    Raises
    ------


    Attributes
    ----------

    .. [SIMON1995PYR] E P Simoncelli and W T Freeman, "The Steerable Pyramid:
       A Flexible Architecture for Multi-Scale Derivative Computation," Second
       Int'l Conf on Image Processing, Washington, DC, Oct 1995.

    TODO: implement an initialisation that sets ``num_orientations`` filters
          that are rotated a different amounts, and optimise only over the
          amount of rotation for each filter.
    """

    def __init__(self,
                 stages: int = 4,
                 num_orientations: int = 2,
                 pretrained: bool = False) -> None:
        """
        Constructs a ``SteerablePyramid`` class.
        """
        super(SteerablePyramid, self).__init__()
        assert self._validate_input(stages, num_orientations, pretrained)
        self.stages = stages
        self.num_orientations = num_orientations

        self.lo0filt = nn.Parameter(torch.ones(1, 1, 9, 9))
        self.hi0filt = nn.Parameter(torch.ones(1, 1, 9, 9))
        self.lofilt = nn.Parameter(torch.ones(1, 1, 17, 17))
        self.bfilts = nn.Parameter(torch.ones(self.num_orientations, 1, 9, 9))

        for param in self.parameters():
            torch.nn.init.normal_(param)

        if pretrained:
            filters = pyr_filts.STEERABLE_SPATIAL_FILTERS_1
            with torch.no_grad():
                self.lo0filt.data = filters['lo0filt']
                self.hi0filt.data = filters['hi0filt']
                self.lofilt.data = filters['lofilt']
                self.bfilts.data = filters['bfilts']

    def _validate_input(self,
                        stages: int,
                        num_orientations: int,
                        pretrained: bool) -> bool:
        """
        Validates input of the steerable pyramid class.

        For the description of the input parameters and exceptions raised by
        this function, please see the documentation of the
        :class:`expert.models.pyramids.SteerablePyramid` class.

        Returns
        -------
        is_valid
            ``True`` if input is valid, ``False`` otherwise.
        """
        is_valid = False

        if not isinstance(stages, int) or stages <= 0:
            raise TypeError('stages parameter must be an integer greater than '
                            '0.')

        if not isinstance(num_orientations, int) or num_orientations <= 0:
            raise TypeError('num_orientations parameter must be an integer '
                            'greater than 0.')

        if not isinstance(pretrained, bool):
            raise TypeError('pretrained parameter must be a boolean.')

        if pretrained and num_orientations != 2:
            raise ValueError('To use the pretrained network, num_orientations '
                             'must be 2.')

        is_valid = True
        return is_valid

    def forward(
        self,
        x: torch.tensor,
        upsample_output: bool = False
    ) -> Union[List[torch.Tensor], torch.Tensor]:
        """
        Forward pass of the pyramid.

        This function returns a lit of Tensors for the subbands in each stage
        of the pyramid or, if ``upsample_output`` is ``True``, a Tensor
        containing every subband at every level that has been upsampled to be
        the same size as the input Tensor.

        Parameters
        ----------
        x : torch.Tensor
            Input to the pyramid.
        upsample_output : boolean
            If ``True`` then the every subband will be upsampled to be the same
            size as the input and then stacked to be a singular tensor.

        Raises
        ------
        TypeError:
            Input parameter ``x`` is not of dtype torch.float.

        Returns
        -------
        pyramid : Union[List[torch.Tensor], Tensor]
            List of tensors, where the first tensor is the high pass residual,
            and from thereon each entry contains the subbands at each stage of
            the pyramid. The low pass residual is the last element in the
            pyramid. If ``upsample_output`` is ``True`` then this will be one
            Tensor where each subband has been upsample to be the same
            dimensions as the input.
        """
        if x.dtype != torch.float32:
            raise TypeError('Input x must be of type torch.float32.')

        padded_x = F.pad(x,
                         pad=conv_utils.pad([x.size(2), x.size(3)], 9, 1),
                         mode='reflect')
        low_pass = F.conv2d(padded_x, self.lo0filt)
        high_pass = F.conv2d(padded_x, self.hi0filt)

        pyramid = []
        pyramid.append(high_pass)

        for h in range(0, self.stages):
            image_size = [low_pass.size(2), low_pass.size(3)]
            padded_lowpass = F.pad(low_pass,
                                   pad=conv_utils.pad(image_size, 9, 1),
                                   mode='reflect')
            subbands = F.conv2d(padded_lowpass, self.bfilts, groups=1)
            padded_lowpass = F.pad(low_pass,
                                   pad=conv_utils.pad(image_size, 17, 1),
                                   mode='reflect')
            low_pass = F.conv2d(padded_lowpass, self.lofilt, stride=[2, 2])
            pyramid.append(subbands)
        pyramid.append(low_pass)

        if upsample_output:
            original_size = [high_pass.size(2), high_pass.size(3)]
            pyr_upsample = [
                F.interpolate(stage, size=original_size) for stage in pyramid
            ]
            pyramid = torch.cat(pyr_upsample, dim=1)

        return pyramid, high_pass
