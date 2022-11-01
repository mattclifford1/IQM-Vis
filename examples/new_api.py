import numpy as np
import sys; sys.path.append('.'); sys.path.append('..')
from IQM_VIS import api
from IQM_VIS.utils import gui_utils

import metrics, image_utils



image_path = {'X': 'examples/images/image2.jpg'}
metric = {'MAE': lambda im1, im2: np.abs(im1 - im2).mean()}
metric_im = {'MAE': lambda im1, im2: np.abs(im1 - im2)}
trans = {'brightness': {'min':-1, 'max':1, 'init_value':0, 'function':lambda im, val: np.clip(im + val, 0, 1)}}

api.make_UI(image_path,
        metric,
        metric_im,
        trans,
        metrics_info_format='text')



im = {'X': gui_utils.image_loader('examples/images/image2.jpg')}
metric = {'MAE': lambda im1, im2: np.abs(im1 - im2).mean()}
metric_im = {'MAE': lambda im1, im2: np.abs(im1 - im2)}

ui_row = {'image': im, 'metrics': metric, 'metric_images': metric_im}

transformations = {'brightness': {'min':-1, 'max':1, 'init_value':0, 'function':lambda im, val: np.clip(im + val, 0, 1)}}





# image_paths = {'X1': 'examples/images/image2.jpg',
#                'X2': 'examples/images/image3.jpg'}
#
# # metrics functions must return a single value
# metrics_dict = {'MAE': metrics.MAE,
#                 'MSE': metrics.MSE,
#                 '1-SSIM': metrics.ssim()}
#
# # metrics images return a numpy image
# metrics_image_dict = {'MSE': metrics.MSE_image,
#                       'SSIM': metrics.SSIM_image()}
#
# transformations = {
#            'rotation':{'min':-180, 'max':180, 'function':image_utils.rotation},    # normal input
#            'blur':{'min':1, 'max':41, 'normalise':'odd', 'function':image_utils.blur},  # only odd ints
#            'brightness':{'min':-1, 'max':1, 'function':image_utils.brightness},   # normal but with float
#            }
#
# # make app
# api.make_UI(image_paths, metrics_dict, metrics_image_dict, transformations, metrics_avg_graph=True)
