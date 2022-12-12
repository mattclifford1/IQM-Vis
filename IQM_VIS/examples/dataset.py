import os
import numpy as np
import IQM_VIS


def run():
    file_path = os.path.dirname(os.path.abspath(__file__))

    # metrics functions must return a single value
    metric = {'MAE': IQM_VIS.metrics.MAE,
              'MSE': IQM_VIS.metrics.MSE,
              '1-SSIM': IQM_VIS.metrics.ssim()}

    # metrics images return a numpy image
    metric_images = {'MSE': IQM_VIS.metrics.MSE_image,
                     'SSIM': IQM_VIS.metrics.SSIM_image()}

    # first row of images
    dataset = [os.path.join(file_path, 'images', 'waves1.jpeg'),
               os.path.join(file_path, 'images', 'waves2.jpeg'),
               os.path.join(file_path, 'images', 'wave3.jpeg')]
    data = IQM_VIS.dataset_holder(dataset,
                                  IQM_VIS.utils.load_image,
                                  metric,
                                  metric_images)
    # second row of images
    # define the transformations
    transformations = {
               'rotation':{'min':-180, 'max':180, 'function':IQM_VIS.transforms.rotation},    # normal input
               'blur':{'min':1, 'max':41, 'normalise':'odd', 'function':IQM_VIS.transforms.blur},  # only odd ints
               'brightness':{'min':-1.0, 'max':1.0, 'function':IQM_VIS.transforms.brightness},   # normal but with float
               # 'threshold':{'min':-40, 'max':40, 'function':IQM_VIS.transforms.binary_threshold},
               'jpeg compression':{'init_value':100, 'min':1, 'max':100, 'function':IQM_VIS.transforms.jpeg_compression},
               }

    # use the API to create the UI
    IQM_VIS.make_UI(data,
                transformations,
                metrics_avg_graph=True)


if __name__ == '__main__':
    run()
