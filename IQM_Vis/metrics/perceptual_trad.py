# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
import warnings
import torch 

from torchmetrics import StructuralSimilarityIndexMeasure as ssim_torch
from IQM_Vis.metrics.SSIM.ssim import ms_ssim
from IQM_Vis.metrics.NLPD_torch.pyramids import LaplacianPyramid
from IQM_Vis.metrics.metric_utils import _check_shapes, _numpy_to_torch_image


class SSIM:
    '''Structural Similarity Index Measure between two images. Images must have
       the same dimensions. Score given is 1 - SSIM to give the loss/dissimilarity

    Args:
        return_image (bool): Whether to return the image (Defaults to False which
                             will return a scalar value)
    '''

    def __init__(self, return_image=False):
        self.return_image = return_image
        self.metric = ssim_torch
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.preproccess_function = _numpy_to_torch_image

    def __call__(self, im_ref, im_comp, sigma=1.5, k1=0.01, k2=0.03, ssim_kernel_size=11, **kwargs):
        '''When an instance is called

        Args:
            im_ref (np.array): Reference image
            im_comp (np.array): Comparison image
            **kwargs: Arbitrary keyword arguments

        Returns:
            score (np.array): 1-SSIM (scalar if return_image is False, image if
                             return_image is True)
        '''
        _check_shapes(im_ref, im_comp)
        im_ref = self.preproccess_function(im_ref).to(
            device=self.device, dtype=torch.float)
        im_comp = self.preproccess_function(im_comp).to(
            device=self.device, dtype=torch.float)
        ssim_kernel_size = _make_kernel_odd(ssim_kernel_size)
        # set up metric
        with warnings.catch_warnings():    # we don't care about the warnings these give
            warnings.simplefilter("ignore")
            if self.return_image:
                _metric = self.metric(
                    sigma=sigma, k1=k1, k2=k2, return_full_image=True, reduction=None, kernel_size=ssim_kernel_size)
            else:
                _metric = self.metric(sigma=sigma, k1=k1,
                                      k2=k2, kernel_size=ssim_kernel_size)
            _metric.to(self.device)
        if self.return_image:
            _, ssim_full_im = _metric(im_ref, im_comp)
            ssim_full_im = torch.squeeze(ssim_full_im, axis=0)
            ssim_full_im = ssim_full_im.permute(1, 2, 0)
            ssim_full_im = torch.clip(ssim_full_im, 0, 1)
            _score = ssim_full_im.cpu().detach().numpy()
        else:
            _score = _metric(im_ref, im_comp).cpu().detach().numpy()
        _score = 1 - _score
        _metric.reset()
        return _score


class MS_SSIM:
    '''Multi-Scale Structural Similarity Index Measure between two images.
       Images must have the same dimensions. Score given is 1 - MS_SSIM to give the
       loss/dissimilarity.
       Note that images of small size, below 180 pixels will have their kernel size
       reduced for compatability with the 4 downsizing operations.

    Args:
        return_image (bool): Whether to return the image (Defaults to False which
                             will return a scalar value)
    '''

    def __init__(self, return_image=False):
        self.return_image = return_image
        # self.metric = Mssim_torch
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.preproccess_function = _numpy_to_torch_image

    def __call__(self, im_ref, im_comp, sigma=1.5, k1=0.01, k2=0.03, mssim_kernel_size=11, ** kwargs):
        '''When an instance is called

        Args:
            im_ref (np.array): Reference image
            im_comp (np.array): Comparison image
            **kwargs: Arbitrary keyword arguments

        Returns:
            score (np.array): 1-SSIM (scalar if return_image is False, image if
                             return_image is True)
        '''
        _check_shapes(im_ref, im_comp)
        im_ref = self.preproccess_function(im_ref).to(
            device=self.device, dtype=torch.float)
        im_comp = self.preproccess_function(im_comp).to(
            device=self.device, dtype=torch.float)
        mssim_kernel_size = _make_kernel_odd(mssim_kernel_size)
        success = False
        reduced_kernel = False
        run_error = False
        while success == False and mssim_kernel_size > 0:
            # _metric = self._make_metric(sigma=sigma, k1=k1, k2=k2, kernel_size=mssim_kernel_size)
            try:
                if self.return_image:
                    # _, ssim_full_im = _metric(im_ref, im_comp)
                    ssim_full_im = ms_ssim(im_ref, im_comp,
                                           data_range=1,
                                           win_size=mssim_kernel_size,
                                           win_sigma=sigma,
                                           K=(k1, k2),
                                           return_image=True)
                    ssim_full_im = torch.squeeze(ssim_full_im, axis=0)
                    ssim_full_im = ssim_full_im.permute(1, 2, 0)
                    ssim_full_im = torch.clip(ssim_full_im, 0, 1)
                    _score = ssim_full_im.cpu().detach().numpy()
                else:
                    _score = ms_ssim(im_ref, im_comp,
                                     data_range=1,
                                     win_size=mssim_kernel_size,
                                     win_sigma=sigma,
                                     K=(k1, k2),
                                     size_average=True)
                    # _score = _metric(im_ref, im_comp).cpu().detach().numpy()
                _score = 1 - _score.cpu().detach().numpy()  # get score not similarity
                success = True
            except ValueError:
                # get an error with small images that the torchmetrics package seems to advise the wrong larger than size for
                reduced_kernel = True
                mssim_kernel_size -= 2
                _score = 0
            except AssertionError:
                # get an error with small images that the pytorch-ssim package seems to advise the wrong larger than size for
                reduced_kernel = True
                mssim_kernel_size -= 2
                _score = 0
            except RuntimeError:
                run_error = True
                success = True
                _score = 0
            # _metric.reset()
        if reduced_kernel == True:
            print(
                f'NOTE: Reduced MS_SSIM kernel size to {mssim_kernel_size} to deal with image size {im_ref.shape}')
        if run_error == True:
            print(
                f'WARNING: Image size {im_ref.shape} too small to use with MS_SSIM, returning 0')
        return _score

    def _make_metric(self, **kwargs):
        # set up metric
        with warnings.catch_warnings():    # we don't care about the warnings these give
            warnings.simplefilter("ignore")
            if self.return_image:
                _metric = self.metric(**kwargs,
                                      return_full_image=True,
                                      reduction=None)
            else:
                _metric = self.metric(**kwargs)
            _metric.to(self.device)
        return _metric


class NLPD:
    '''Normalised Laplacian pyramid
    Proposed by Valero Laparra et al. https://www.uv.es/lapeva/papers/2016_HVEI.pdf .
    NLPD is an image quality metric based on the transformations associated with the 
    early visual system: local luminance subtraction and local gain control.

    '''

    def __init__(self):
        self.initialised = False   # initialse fully on first __call__ to save load up time
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.preproccess_function = _numpy_to_torch_image
        self.nlpd_k = 1

    def __call__(self, im_ref, im_comp, nlpd_k=1, **kwargs):
        '''When an instance is called

        Args:
            im_ref (np.array): Reference image
            im_comp (np.array): Comparison image
            **kwargs: Arbitrary keyword arguments

        Returns:
            score (np.array): NLPD score
        '''
        # see if k has changed
        if self.nlpd_k != nlpd_k:
            self.nlpd_k = nlpd_k
            self.initialised = False
        # load model on first time called
        if self.initialised == False:
            with warnings.catch_warnings():    # we don't care about the warnings these give
                warnings.simplefilter("ignore")
                self.metric = LaplacianPyramid(self.nlpd_k)
            self.metric.to(self.device)
            self.initialised = True

        _check_shapes(im_ref, im_comp)
        im_ref = self.preproccess_function(im_ref).to(
            device=self.device, dtype=torch.float)
        im_comp = self.preproccess_function(im_comp).to(
            device=self.device, dtype=torch.float)
        _score = self.metric(im_ref, im_comp)
        score = _score.cpu().detach().numpy()
        return score


def _make_kernel_odd(value):
    value = int(value)
    if value % 2 == 0:
        value -= 1
    if value <= 0:
        value = 1
    return value
