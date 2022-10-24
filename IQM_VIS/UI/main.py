import sys
import os
# import pandas as pd

import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QInputDialog, QLineEdit, QMenu, QFileDialog, QPushButton, QGridLayout, QLabel, QSlider, QComboBox, QCheckBox
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure

from IQM_VIS.utils import gui_utils, plot_utils
from IQM_VIS.UI.layout import app_layout
from IQM_VIS.UI.widgets import app_widgets
from IQM_VIS.UI.metrics import app_metrics
from IQM_VIS.UI.images import app_images

class make_app(app_widgets, app_layout, app_metrics, app_images):
    def __init__(self, app,
                image_paths: dict,
                metrics_dict: dict,
                metrics_image_dict: dict,
                transformations: dict,
                image_loader=gui_utils.image_loader,
                metrics_info_format='graph'    # graph or text
                ):
        super().__init__()
        self.app = app
        self.image_paths = image_paths
        self.metrics_dict = metrics_dict
        self.metrics_image_dict = metrics_image_dict
        self.transformations = transformations
        self.image_loader = image_loader
        self.metrics_info_format = metrics_info_format

        self.init_style()
        self.init_images()
        self.init_transforms()
        self.init_widgets()
        self.init_layout()

        self.display_images()
        self.reset_sliders()
        self.get_metrics_over_range()


if __name__ == '__main__':
    import argparse
    import sys
    import metrics
    import image_utils
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path1', type=str, help='image file to use', default=os.path.join(os.path.expanduser('~'),'summer-project/data/Bourne/tactip/sim/surface_3d/tap/128x128/csv_train/images/image_1.png'))
    parser.add_argument('--image_path2', type=str, help='image file to use', default=os.path.join(os.path.expanduser('~'),'summer-project/data/Bourne/tactip/sim/edge_2d/tap/128x128/csv_train/images/image_15.png'))
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
               'rotation':{'min':-180, 'max':180, 'function':image_utils.rotation},    # normal input
               'blur':{'min':1, 'max':41, 'normalise':'odd', 'function':image_utils.blur},  # only odd ints
               'brightness':{'min':-0.5, 'max':0.5, 'function':image_utils.brightness},   # normal but with float
               'zoom':{'min':0.5, 'max':2, 'init_value':1, 'num_values': 31, 'function':image_utils.zoom},  # define number of steps
               'x_shift':{'values':np.linspace(-0.5, 0.5, 21), 'function':image_utils.x_shift},  # explicit definition of values
               'y_shift':{'min':-0.5, 'max':0.5, 'function':image_utils.y_shift},
               }


    # make GUI app
    app = QApplication(sys.argv)
    window = make_app(app,
                      image_paths,
                      metrics_dict,
                      metrics_image_dict,
                      transformations)
    sys.exit(app.exec())
