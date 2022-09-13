import numpy as np
import sys; sys.path.append('.'); sys.path.append('..')
import api

import metrics
import image_utils

image_paths = {'X1': 'images/image2.jpg',
               'X2': 'images/image3.jpg'}

# metrics functions must return a single value
metrics_dict = {'MAE': metrics.MAE,
                'MSE': metrics.MSE,
                'SSIM': metrics.ssim()}
                
# metrics images return a numpy image
metrics_image_dict = {'MSE': metrics.MSE_image,
                      'SSIM': metrics.SSIM_image()}

transformations = {
           'rotation':{'min':-180, 'max':180, 'init_value':0, 'function':image_utils.rotation},    # normal input
           'blur':{'min':0, 'max':40, 'init_value':0, 'normalise':'odd', 'function':image_utils.blur},  # only odd ints
           'brightness':{'min':-1, 'max':1, 'init_value':0, 'function':image_utils.brightness},   # normal but with float
           }

# make app
api.make_UI(image_paths, metrics_dict, metrics_image_dict, transformations)
