import os
import numpy as np
import IQM_VIS


def run():
    file_path = os.path.dirname(os.path.abspath(__file__))
    # define simple metrics
    metric = {'MAE': lambda im1, im2: np.abs(im1 - im2).mean()}
    metric_im = {'MAE': lambda im1, im2: np.abs(im1 - im2)}
    # add numpy image and the metrics to the data handler
    data_store = IQM_VIS.data_holder(('X', IQM_VIS.utils.load_image(os.path.join(file_path, 'images', 'wave3.jpeg'))),
                             ('X', IQM_VIS.utils.load_image(os.path.join(file_path, 'images', 'wave3.jpeg'))),
                             metric,
                             metric_im)
    # define the transformations
    trans = {'brightness': {'min':-1.0, 'max':1.0, 'init_value':0, 'function':lambda im, val: np.clip(im + val, 0, 1)}}
    # use the API to create the UI
    IQM_VIS.make_UI([data_store],
                trans,
                metrics_info_format='text')


if __name__ == '__main__':
    run()
