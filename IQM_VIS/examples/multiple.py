import numpy as np
import IQM_VIS
from IQM_VIS.examples import metrics, image_utils, transforms
import os


def run():
    file_path = os.path.dirname(os.path.abspath(__file__))

    # metrics functions must return a single value
    metric = {'MAE': metrics.MAE,
              'MSE': metrics.MSE,
              '1-SSIM': metrics.ssim()}

    # metrics images return a numpy image
    metric_images = {'MSE': metrics.MSE_image,
                     'SSIM': metrics.SSIM_image()}

    # first row of images
    row_1 = IQM_VIS.data_holder(('X1', image_utils.image_loader(os.path.join(file_path, 'images', 'wave3.jpeg'))),
                             metric,
                             metric_images)
    # second row of images
    row_2 = IQM_VIS.data_holder(('X2', image_utils.image_loader(os.path.join(file_path, 'images', 'waves1.jpeg'))),
                             metric,
                             metric_images)
    # define the transformations
    transformations = {
               'rotation':{'min':-180, 'max':180, 'function':transforms.rotation},    # normal input
               'blur':{'min':1, 'max':41, 'normalise':'odd', 'function':transforms.blur},  # only odd ints
               'brightness':{'min':-1, 'max':1, 'function':transforms.brightness},   # normal but with float
               }

    # use the API to create the UI
    IQM_VIS.make_UI([row_1, row_2],
                transformations,
                metrics_avg_graph=True)


if __name__ == '__main__':
    run()
