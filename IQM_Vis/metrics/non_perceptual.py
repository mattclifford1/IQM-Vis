# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
import numpy as np

# from torchmetrics import PeakSignalNoiseRatio as PSNRs
from IQM_Vis.metrics.metric_utils import _check_shapes

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


class RMSE:
    '''Root Mean Squared Error between two images. Images must have the same
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
            score (np.array): RMSE (scalar if return_image is False, image if
                             return_image is True)
        '''
        _check_shapes(im_ref, im_comp)
        L2 = np.square(im_ref - im_comp)
        if self.return_image:
            return np.sqrt(L2)
        else:
            return np.sqrt(L2.mean())


class one_over_PSNR:
    '''Peak signal to noise ratio - https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
    The score given is normalised between 0, 1 by taking 1/PSNR 

    Args:
        return_image (bool): Whether to return the image (Defaults to False which
                             will return a scalar value)
    '''

    def __init__(self):
        self.initialised = False
        # self.metric = PSNRs
        # self.device = torch.device(
        #     "cuda" if torch.cuda.is_available() else "cpu")
        # self.preproccess_function = _numpy_to_torch_image

    def __call__(self, im_ref, im_comp, **kwargs):
        '''When an instance is called

        Args:
            im_ref (np.array): Reference image
            im_comp (np.array): Comparison image
            **kwargs: Arbitrary keyword arguments

        Returns:
            score (np.array): PSNR between the images
        '''
        _check_shapes(im_ref, im_comp)
        se = np.square(im_ref - im_comp)
        mse = se.mean()
        if mse == 0:
            return 0
        psnr = 10 * np.log10(1/(mse))
        return 1/psnr

        # im_ref = self.preproccess_function(im_ref).to(
        #     device=self.device, dtype=torch.float)
        # im_comp = self.preproccess_function(im_comp).to(
        #     device=self.device, dtype=torch.float)
        # # set up metric
        # if self.initialised == False:
        #     with warnings.catch_warnings():    # we don't care about the warnings these give
        #         warnings.simplefilter("ignore")
        #         self._metric = self.metric()
        #         self._metric.to(self.device)
        # _score = self._metric(im_ref*255, im_comp*255).cpu().detach().numpy()
        # _score = 1 - _score
        # self._metric.reset()
        # return _score/255
