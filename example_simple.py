import api
import numpy as np

image_path = {'X': 'images/image2.jpg'}
metric = {'MAE': lambda im1, im2: np.abs(im1 - im2).mean()}
metric_im = {'MAE': lambda im1, im2: np.abs(im1 - im2)}
trans = {'brightness': {'min':-1, 'max':1, 'init_value':0, 'function':lambda im, val: np.clip(im + val, 0, 1)}}

api.make_UI(image_path,
        metric,
        metric_im,
        trans)
