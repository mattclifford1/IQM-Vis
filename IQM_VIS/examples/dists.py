import os
import numpy as np
import torch
import IQM_VIS
from DISTS_pytorch import DISTS


'''Use DISTS metric'''
class dists_wrapper:
    def __init__(self):
        self.metric = DISTS()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.metric.to(self.device)
        self.preproccess_function = IQM_VIS.metrics.preprocess_numpy_image

    def __call__(self, im_ref, im_comp, **kwargs):
        IQM_VIS.metrics.check_shapes(im_ref, im_comp)
        im_ref = self.preproccess_function(im_ref).to(device=self.device, dtype=torch.float)
        im_comp = self.preproccess_function(im_comp).to(device=self.device, dtype=torch.float)
        _score = self.metric(im_ref, im_comp)
        score = _score.cpu().detach().numpy()
        return score


def run():
    # metrics functions must return a single value
    metric = {'DISTS': dists_wrapper(),
              'MAE': IQM_VIS.metrics.MAE,
              '1-SSIM': IQM_VIS.metrics.ssim()}

    # metrics images return a numpy image
    metric_images = {}

    # make dataset list of images
    file_path = os.path.dirname(os.path.abspath(__file__))
    dataset = [os.path.join(file_path, 'images', 'waves1.jpeg'),
               os.path.join(file_path, 'images', 'waves2.jpeg'),
               os.path.join(file_path, 'images', 'wave3.jpeg')]
    data = IQM_VIS.dataset_holder(dataset,
                                  IQM_VIS.utils.load_image,
                                  metric,
                                  metric_images)

    # define the transformations
    transformations = {
               'rotation':{'min':-180, 'max':180, 'function':IQM_VIS.transforms.rotation},    # normal input
               'blur':{'min':1, 'max':41, 'normalise':'odd', 'function':IQM_VIS.transforms.blur},  # only odd ints
               'brightness':{'min':-1.0, 'max':1.0, 'function':IQM_VIS.transforms.brightness},   # normal but with float
               # 'threshold':{'min':-40, 'max':40, 'function':IQM_VIS.transforms.binary_threshold},
               'jpeg compression':{'init_value':100, 'min':1, 'max':100, 'function':IQM_VIS.transforms.jpeg_compression},
               }
    # define any parameters that the metrics need (names shared across both metrics and metric_images)
    ssim_params = {'sigma': {'min':0.25, 'max':5.25, 'init_value': 1.5},  # for the guassian kernel
                   # 'kernel_size': {'min':1, 'max':41, 'normalise':'odd', 'init_value': 11},  # ignored if guassian kernel used
                   'k1': {'min':0.01, 'max':0.21, 'init_value': 0.01},
                   'k2': {'min':0.01, 'max':0.21, 'init_value': 0.03}}

    # use the API to create the UI
    IQM_VIS.make_UI(data,
                transformations,
                metrics_avg_graph=True,
                metric_params=ssim_params)


if __name__ == '__main__':
    run()
