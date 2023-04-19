import os
import numpy as np
import IQM_Vis


def run():
    # metrics functions must return a single value
    metric = {} #IQM_Vis.metrics.get_all_metrics()

    # metrics images return a numpy image
    metric_images = {}

    # make dataset list of images
    file_path = os.path.dirname(os.path.abspath(__file__))
    dataset = [os.path.join(file_path, 'images', 'waves1.jpeg'),
               os.path.join(file_path, 'images', 'waves2.jpeg'),
               os.path.join(file_path, 'images', 'waves3.jpeg')]
    data = IQM_Vis.dataset_holder(dataset,
                                  metric,
                                  metric_images,
                                  IQM_Vis.utils.load_image,
                                  )

    # define the transformations
    transformations = {
    'x_shift': {'min':-1.0, 'max':1.0, 'function':IQM_Vis.transforms.brightness, 'init_value': 0.0},
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
                    restrict_options=3
                    )

if __name__ == '__main__':
    run()
