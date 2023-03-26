import os
import numpy as np
import IQM_Vis


def run():
    file_path = os.path.dirname(os.path.abspath(__file__))

    # metrics functions must return a single value
    metric = {'MAE': IQM_Vis.IQMs.MAE(),
              'MSE': IQM_Vis.IQMs.MSE(),
              '1-SSIM': IQM_Vis.IQMs.SSIM()}

    # metrics images return a numpy image
    metric_images = {'MSE': IQM_Vis.IQMs.MSE(return_image=True),
                     'SSIM': IQM_Vis.IQMs.SSIM(return_image=True)}

    # first row of images
    row_1 = IQM_Vis.dataset_holder([os.path.join(file_path, 'images', 'waves2.jpeg')],
                                   metric,
                                   metric_images)
    # second row of images
    row_2 = IQM_Vis.dataset_holder([os.path.join(file_path, 'images', 'waves3.jpeg')],
                                   metric,
                                   metric_images)
    # define the transformations
    transformations = {
               'rotation':{'min':-180, 'max':180, 'function':IQM_Vis.transforms.rotation},    # normal input
               'blur':{'min':1, 'max':41, 'normalise':'odd', 'function':IQM_Vis.transforms.blur},  # only odd ints
               'brightness':{'min':-1.0, 'max':1.0, 'function':IQM_Vis.transforms.brightness},   # normal but with float
               }

    # use the API to create the UI
    IQM_Vis.make_UI([row_1, row_2],
                    transformations)


if __name__ == '__main__':
    run()
