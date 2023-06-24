import os
import numpy as np
import IQM_Vis


def run():
    # metrics functions must return a single value
    metric = {'MAE': IQM_Vis.IQMs.MAE(),
              'MSE': IQM_Vis.IQMs.MSE(),
              '1-SSIM': IQM_Vis.IQMs.SSIM()
              }

    # metrics images return a numpy image
    metric_images = {
        # 'MSE': IQM_Vis.IQMs.MSE(return_image=True),
        # 'SSIM': IQM_Vis.IQMs.SSIM(return_image=True)
                     }

    # make dataset list of images
    file_path = os.path.dirname(os.path.abspath(__file__))
    dataset = [os.path.join(file_path, 'images', 'waves1.jpeg'),
               os.path.join(file_path, 'images', 'waves2.jpeg'),
               os.path.join(file_path, 'images', 'waves3.jpeg')]
    data = IQM_Vis.dataset_holder(dataset,
                                  metric,
                                  metric_images,
                                  IQM_Vis.utils.load_image,
                                  human_exp_csv=os.path.join(file_path, 'images', 'HIQM.csv'),
                                  )

    # define the transformations
    transformations = {
               'rotation':{'min':-180, 'max':180, 'function':IQM_Vis.transforms.rotation},    # normal input
               'blur':{'min':1, 'max':41, 'normalise':'odd', 'function':IQM_Vis.transforms.blur},  # only odd ints
               'brightness':{'min':-1.0, 'max':1.0, 'function':IQM_Vis.transforms.brightness},   # normal but with float
               # 'threshold':{'min':-40, 'max':40, 'function':IQM_Vis.transforms.binary_threshold},
               'jpg comp.':{'init_value':100, 'min':1, 'max':100, 'function':IQM_Vis.transforms.jpeg_compression},
               }
    # define any parameters that the metrics need (names shared across both metrics and metric_images)
    ssim_params = {'sigma': {'min':0.25, 'max':5.25, 'init_value': 1.5},  # for the guassian kernel
                   # 'kernel_size': {'min':1, 'max':41, 'normalise':'odd', 'init_value': 11},  # ignored if guassian kernel used
                   'k1': {'min':0.01, 'max':0.21, 'init_value': 0.01},
                   'k2': {'min':0.01, 'max':0.21, 'init_value': 0.03}}

    # use the API to create the UI
    IQM_Vis.make_UI(data,
                    transformations,
                    metric_params=ssim_params,
                    )

if __name__ == '__main__':
    run()
