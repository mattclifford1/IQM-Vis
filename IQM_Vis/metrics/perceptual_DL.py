# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
import warnings
import torch

from torchmetrics.image.lpip import LearnedPerceptualImagePatchSimilarity as lpips_torch
from DISTS_pytorch import DISTS as dists_original
from IQM_Vis.metrics.metric_utils import _check_shapes, _numpy_to_torch_image


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
        self.initialised = False   # initialse fully on first __call__ to save load up time
        self.network = network
        self.reduction = reduction
        # self.metric = lpips_torch
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.preproccess_function = _numpy_to_torch_image

    def __call__(self, im_ref, im_comp, **kwargs):
        '''When an instance is called

        Args:
            im_ref (np.array): Reference image
            im_comp (np.array): Comparison image
            **kwargs: Arbitrary keyword arguments

        Returns:
            score (np.array): LPIPS score
        '''
        if self.initialised == False:
            with warnings.catch_warnings():    # we don't care about the warnings these give
                warnings.simplefilter("ignore")
                self.metric = lpips_torch(net_type=self.network,
                                          reduction=self.reduction,
                                          normalize=True)
                self.metric.to(self.device)
            self.initialised = True
        _check_shapes(im_ref, im_comp)
        im_ref = self.preproccess_function(im_ref).to(
            device=self.device, dtype=torch.float)
        im_comp = self.preproccess_function(im_comp).to(
            device=self.device, dtype=torch.float)
        with warnings.catch_warnings():    # warning because we have reset
            warnings.simplefilter("ignore")
            _score = self.metric(im_ref, im_comp)
        score = _score.cpu().detach().numpy()
        self.metric.reset()
        return score


class DISTS:
    '''Deep Image Structure and Texture Similarity (DISTS) Metric. Uses the
        code from https://github.com/dingkeyan93/DISTS. Uses the PyTorch backend.
        It is robust to texture variance (e.g., evaluating the images generated
        by GANs) and mild geometric transformations (e.g., evaluating the image
        pairs that are not strictly point-by-point aligned).

    '''

    def __init__(self):
        self.initialised = False   # initialse fully on first __call__ to save load up time
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
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
        # load model on first time called
        if self.initialised == False:
            with warnings.catch_warnings():    # we don't care about the warnings these give
                warnings.simplefilter("ignore")
                self.metric = dists_original()
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
