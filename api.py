import sys
from PyQt6.QtWidgets import QApplication
from UI import make_app

def make_UI(image_paths,
            metrics_dict,
            metrics_image_dict,
            transformations,
            metrics_info_format='graph'):
    app = QApplication(sys.argv)
    window = make_app(app,
                      image_paths,
                      metrics_dict,
                      metrics_image_dict,
                      transformations,
                      metrics_info_format=metrics_info_format)
    sys.exit(app.exec())


if __name__ == '__main__':
    import argparse
    import os
    import metrics
    import image_utils
    import numpy as np
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path1', type=str, help='image file to use', default=os.path.join('.', 'images', 'image2.jpg'))
    parser.add_argument('--image_path2', type=str, help='image file to use', default=os.path.join('.', 'images', 'image3.jpg'))
    args = parser.parse_args()

    image_paths = {'X1': args.image_path1,
                   'X2': args.image_path2}

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
               # 'x_shift':{'values':np.linspace(-0.5, 0.5, 21), 'init_value':0, 'function':image_utils.x_shift},  # explicit definition of values
               # 'y_shift':{'min':-0.5, 'max':0.5, 'init_value':0, 'function':image_utils.y_shift},
               # 'zoom':{'min':0.5, 'max':2, 'init_value':1, 'num_values': 31, 'function':image_utils.zoom},  # define number of steps
               }


    # make GUI app
    make_UI(image_paths,
            metrics_dict,
            metrics_image_dict,
            transformations)
