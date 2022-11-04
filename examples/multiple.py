import numpy as np
import sys; sys.path.append('.'); sys.path.append('..')
from IQM_VIS import api, data
from IQM_VIS.utils import gui_utils

import metrics, image_utils

# metrics functions must return a single value
metric = {'MAE': metrics.MAE,
          'MSE': metrics.MSE,
          '1-SSIM': metrics.ssim()}

# metrics images return a numpy image
metric_images = {'MSE': metrics.MSE_image,
                 'SSIM': metrics.SSIM_image()}

row_1 = data.holder(('X1', gui_utils.image_loader('examples/images/image2.jpg')),
                         metric,
                         metric_images)

row_2 = data.holder(('X2', gui_utils.image_loader('examples/images/image3.jpg')),
                         metric,
                         metric_images)

transformations = {
           'rotation':{'min':-180, 'max':180, 'function':image_utils.rotation},    # normal input
           'blur':{'min':1, 'max':41, 'normalise':'odd', 'function':image_utils.blur},  # only odd ints
           'brightness':{'min':-1, 'max':1, 'function':image_utils.brightness},   # normal but with float
           }

# make app
api.make_UI([row_1, row_2],
            transformations,
            metrics_avg_graph=True)
