'''
sample metrics to use with the examples of the UI
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import sys; sys.path.append('..'); sys.path.append('.')
import torch
import torch.nn as nn
import numpy as np
import warnings

from torchmetrics import StructuralSimilarityIndexMeasure as ssim_torch
from torchmetrics import MultiScaleStructuralSimilarityIndexMeasure as Mssim_torch
# from torchmetrics import PeakSignalNoiseRatio as PSNRs
# from torchmetrics import UniversalImageQualityIndex as UIQI
# from torchmetrics.functional import universal_image_quality_index as UIQI
# from torchmetrics import SpectralDistortionIndex as SDI
from torchmetrics.image.lpip import LearnedPerceptualImagePatchSimilarity as lpips_torch
from DISTS_pytorch import DISTS as dists_original

class MAE:
    '''Mean Absolute Error between two images. Images must have the same
       dimensions

    Args:
        return_image (bool): Whether to return the image (Defaults to False which
                             will return a scalar value)
    '''
    def __init__(self, return_image=False):
        self.return_image = return_image

    def __call__(self, im_ref, im_comp, **kwargs):
        '''When an instance is called

        Args:
            im_ref (np.array): Reference image
            im_comp (np.array): Comparison image
            **kwargs: Arbitrary keyword arguments

        Returns:
            score (np.array): MAE (scalar if return_image is False, image if
                             return_image is True)
        '''
        _check_shapes(im_ref, im_comp)
        L1 = np.abs(im_ref - im_comp)
        if self.return_image:
            return L1
        else:
            return L1.mean()

class MSE:
    '''Mean Squared Error between two images. Images must have the same
       dimensions

    Args:
        return_image (bool): Whether to return the image (Defaults to False which
                             will return a scalar value)
    '''
    def __init__(self, return_image=False):
        self.return_image = return_image

    def __call__(self, im_ref, im_comp, **kwargs):
        '''When an instance is called

        Args:
            im_ref (np.array): Reference image
            im_comp (np.array): Comparison image
            **kwargs: Arbitrary keyword arguments

        Returns:
            score (np.array): MSE (scalar if return_image is False, image if
                             return_image is True)
        '''
        _check_shapes(im_ref, im_comp)
        L2 = np.square(im_ref - im_comp)
        if self.return_image:
            return L2
        else:
            return L2.mean()

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
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.preproccess_function = _numpy_to_torch_image

    def __call__(self, im_ref, im_comp, **kwargs):
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
        im_ref = self.preproccess_function(im_ref).to(device=self.device, dtype=torch.float)
        im_comp = self.preproccess_function(im_comp).to(device=self.device, dtype=torch.float)
        # set up metric
        with warnings.catch_warnings():    # we don't care about the warnings these give
            warnings.simplefilter("ignore")
            if self.return_image:
                _metric = self.metric(return_full_image=True, reduction=None, **kwargs)
            else:
                _metric = self.metric(**kwargs)
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

class MSSIM:
    '''Multi-Scale Structural Similarity Index Measure between two images.
       Images must have the same dimensions. Score given is 1 - MSSIM to give the
       loss/dissimilarity

    Args:
        return_image (bool): Whether to return the image (Defaults to False which
                             will return a scalar value)
    '''
    def __init__(self, return_image=False):
        self.return_image = return_image
        self.metric = Mssim_torch
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.preproccess_function = _numpy_to_torch_image

    def __call__(self, im_ref, im_comp, **kwargs):
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
        im_ref = self.preproccess_function(im_ref).to(device=self.device, dtype=torch.float)
        im_comp = self.preproccess_function(im_comp).to(device=self.device, dtype=torch.float)
        # set up metric
        with warnings.catch_warnings():    # we don't care about the warnings these give
            warnings.simplefilter("ignore")
            if self.return_image:
                _metric = self.metric(return_full_image=True, reduction=None, **kwargs)
            else:
                _metric = self.metric(**kwargs)
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

class LPIPS:
    '''Learned Perceptual Image Patch Similarity between two images.
       Images must have the same dimensions.

    Args:
        network (str): Pretrained network to use. Choose between ‘alex’, ‘vgg’
                       or ‘squeeze’. (Defaults to 'alex')
        reduction (str): How to reduce over the batch dimension. Choose between
                         ‘sum’ or ‘mean’. (Defaults to 'mean')

    '''
    def __init__(self, network='alex', reduction='mean'):
        self.network = network
        self.reduction = reduction
        self.metric = lpips_torch
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.preproccess_function = _numpy_to_torch_image

    def __call__(self, im_ref, im_comp, **kwargs):
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
        im_ref = self.preproccess_function(im_ref).to(device=self.device, dtype=torch.float)
        im_comp = self.preproccess_function(im_comp).to(device=self.device, dtype=torch.float)
        # set up metric
        with warnings.catch_warnings():    # we don't care about the warnings these give
            warnings.simplefilter("ignore")
            _metric = self.metric(net_type=self.network,
                                  reduction=self.reduction,
                                  normalise=True,
                                  **kwargs)
            _metric.to(self.device)
        _score = _metric(im_ref, im_comp).cpu().detach().numpy()
        _metric.reset()
        return _score

class DISTS:
    '''Deep Image Structure and Texture Similarity (DISTS) Metric. Uses the
        code from https://github.com/dingkeyan93/DISTS. Uses the PyTorch backend.
        It is robust to texture variance (e.g., evaluating the images generated
        by GANs) and mild geometric transformations (e.g., evaluating the image
        pairs that are not strictly point-by-point aligned).

    '''
    def __init__(self):
        with warnings.catch_warnings():    # we don't care about the warnings these give
            warnings.simplefilter("ignore")
            self.metric = dists_original()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.metric.to(self.device)
        self.preproccess_function = _numpy_to_torch_image

    def __call__(self, im_ref, im_comp, **kwargs):
        '''When an instance is called

        Args:
            im_ref (np.array): Reference image
            im_comp (np.array): Comparison image
            **kwargs: Arbitrary keyword arguments

        Returns:
            score (np.array): DISTS score
        '''
        _check_shapes(im_ref, im_comp)
        im_ref = self.preproccess_function(im_ref).to(device=self.device, dtype=torch.float)
        im_comp = self.preproccess_function(im_comp).to(device=self.device, dtype=torch.float)
        _score = self.metric(im_ref, im_comp)
        score = _score.cpu().detach().numpy()
        return score


''' TO ADD TO DEMOS'''
''' simple functional format to call a metric (numpy)'''
def _MAE(im_ref, im_comp, **kwargs):
    '''Mean Absolute Error between two images. Images must have the same
       dimensions

    Args:
        im_ref (np.array): Reference image
        im_comp (np.array): Comparison image
        **kwargs: Arbitrary keyword arguments

    Returns:
        mean (np.array): scalar of MAE
    '''
    _check_shapes(im_ref, im_comp)
    L1 = np.abs(im_ref - im_comp)
    return L1.mean()

''' functional (using torch)'''
def _MSE(im_ref, im_comp, **kwargs):
    _check_shapes(im_ref, im_comp)
    metric = nn.MSELoss()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    im_ref = _numpy_to_torch_image(im_ref).to(device=device, dtype=torch.float)
    im_comp = _numpy_to_torch_image(im_comp).to(device=device, dtype=torch.float)
    _score = metric(im_ref, im_comp)
    return _score.cpu().detach().numpy()

''' can also call as a class to input default args (using torch)'''



'''Example of metric image produced to display (using numpy)'''
def _MSE_image(im_ref, im_comp, **kwargs):
    _check_shapes(im_ref, im_comp)
    L2 = (im_ref - im_comp)**2
    return L2




'''
Helper functions for metric computation
'''
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
        raise ValueError(f'Refence and transformed images need to have the same shape not: {im_ref.shape} and {im_comp.shape}')
