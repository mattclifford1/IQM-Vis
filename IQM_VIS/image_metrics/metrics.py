'''
sample metrics to use with the examples of the UI
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import sys; sys.path.append('..'); sys.path.append('.')
import torch
import torch.nn as nn
import numpy as np
import warnings

from torchmetrics import StructuralSimilarityIndexMeasure as SSIM
from torchmetrics import MultiScaleStructuralSimilarityIndexMeasure as MSSIM
from torchmetrics import PeakSignalNoiseRatio as PSNR
# from torchmetrics import UniversalImageQualityIndex as UIQI
from torchmetrics.functional import universal_image_quality_index as UIQI
from torchmetrics import SpectralDistortionIndex as SDI
from torchmetrics.image.lpip import LearnedPerceptualImagePatchSimilarity as LPIPS

from IQM_VIS.image_metrics.expert.pyramids import LaplacianPyramid

''' simple functional format to call a metric (numpy)'''
def MAE(im_ref, im_comp):
    check_shapes(im_ref, im_comp)
    L1 = np.abs(im_ref - im_comp)
    return L1.mean()

''' functional (using torch)'''
def MSE(im_ref, im_comp):
    check_shapes(im_ref, im_comp)
    metric = nn.MSELoss()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    im_ref = preprocess_numpy_image(im_ref).to(device=device, dtype=torch.float)
    im_comp = preprocess_numpy_image(im_comp).to(device=device, dtype=torch.float)
    _score = metric(im_ref, im_comp)
    return _score.cpu().detach().numpy()

''' can also call as a class to input default args (using torch)'''
class ssim:
    def __init__(self):
        with warnings.catch_warnings():    # we don't care about the warnings these give
            warnings.simplefilter("ignore")
            self.metric = SSIM()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.metric.to(self.device)
        self.preproccess_function = preprocess_numpy_image

    def __call__(self, im_ref, im_comp):
        check_shapes(im_ref, im_comp)
        im_ref = self.preproccess_function(im_ref).to(device=self.device, dtype=torch.float)
        im_comp = self.preproccess_function(im_comp).to(device=self.device, dtype=torch.float)
        _score = self.metric(im_ref, im_comp)
        score = 1 - _score.cpu().detach().numpy()
        self.metric.reset()
        return score


'''Example of metric image produced to display (using numpy)'''
def MSE_image(im_ref, im_comp):
    check_shapes(im_ref, im_comp)
    L2 = (im_ref - im_comp)**2
    return L2

'''Example of metric image produced to display (using torch metrics)'''
class SSIM_image:
    def __init__(self):
        with warnings.catch_warnings():    # we don't care about the warnings these give
            warnings.simplefilter("ignore")
            self.metric_image = SSIM(return_full_image=True, reduction=None)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.metric_image.to(self.device)
        self.preproccess_function = preprocess_numpy_image

    def __call__(self, im_ref, im_comp):
        check_shapes(im_ref, im_comp)
        im_ref = self.preproccess_function(im_ref).to(device=self.device, dtype=torch.float)
        im_comp = self.preproccess_function(im_comp).to(device=self.device, dtype=torch.float)
        _, ssim_full_im = self.metric_image(im_ref, im_comp)
        ssim_full_im = torch.squeeze(ssim_full_im, axis=0)
        ssim_full_im = ssim_full_im.permute(1, 2, 0)
        ssim_full_im = torch.clip(ssim_full_im, 0, 1)
        im = ssim_full_im.cpu().detach().numpy()
        self.metric_image.reset()   # clear mem buffer to stop overflow
        return im


'''
Helper functions for metric computation
'''
def preprocess_numpy_image(image):
    if len(image.shape) == 2:
        image = np.expand_dims(image, axis=2)
    image = image.transpose((2, 0, 1))
    image = np.expand_dims(image, axis=0)   # make into batch one 1
    image = torch.from_numpy(image)
    return image

def check_shapes(im_ref, im_comp):
    '''
    make sure both images have the same dimensions
    '''
    if im_ref.shape != im_comp.shape:
        raise ValueError(f'Refence and transformed images need to have the same shape not: {im_ref.shape} and {im_comp.shape}')
