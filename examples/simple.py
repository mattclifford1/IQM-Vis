import numpy as np
import sys; sys.path.append('.'); sys.path.append('..')
from IQM_VIS import api
from IQM_VIS.utils import gui_utils


image_path = {'X': 'examples/images/image2.jpg'}
im = {'X': gui_utils.image_loader('examples/images/image2.jpg')}
metric = {'MAE': lambda im1, im2: np.abs(im1 - im2).mean()}
metric_im = {'MAE': lambda im1, im2: np.abs(im1 - im2)}
trans = {'brightness': {'min':-1, 'max':1, 'init_value':0, 'function':lambda im, val: np.clip(im + val, 0, 1)}}

api.make_UI(im,
        metric,
        metric_im,
        trans,
        metrics_info_format='text')
