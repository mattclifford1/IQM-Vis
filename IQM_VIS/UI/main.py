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

class make_app(app_widgets, app_layout):
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

        self.image_display_size = (175, 175)
        self.init_style()
        self.init_images()
        self.init_transforms()
        self.init_widgets()
        self.init_layout()

        self.display_images()
        self.reset_sliders()
        self.get_metrics_over_range()

    def init_images(self, screen=False):
        '''
        make blank images to place on screen before actual image is chosen
        this creates the UI to be the correct size
        '''
        # make image placeholders
        self.height = int(256)
        self.width_ratio = 1
        self.width = int(self.height*self.width_ratio)

        # load images
        self.image_data = {}
        self.im_pair_names = []
        for key in self.image_paths.keys():
            if os.path.exists(self.image_paths[key]):
                self.image_data[key] = self.image_loader(self.image_paths[key])
            else:
                print('Cannot find image file: ', self.image_paths[key])
                self.image_data[key] = np.zeros([128, 128, 1], dtype=np.uint8)
            self.im_pair_names.append((key, 'T('+key+')'))

    '''
    image updaters
    '''
    def transform_image(self, image):
        for key in self.sliders.keys():
            image = self.sliders[key]['function'](image, self.im_trans_params[key])
        return image

    def display_images(self):
        self.get_image_data()
        self.compute_metrics()
        self.update_image_widgets()

    def _display_images_quick(self):
        # dont calc metrics/errors - just update widgets
        self.get_image_data()
        self.update_image_widgets()

    def get_image_data(self):
        # get transformed images
        for key in self.image_paths.keys():
            self.image_data['T('+key+')'] = self.transform_image(self.image_data[key])

    def update_image_widgets(self):
        # display images
        for key in self.image_data.keys():
            gui_utils.change_im(self.widgets['image'][key], self.image_data[key], resize=self.image_display_size)

    '''
    metrics/error info updaters
    '''
    def compute_metrics(self):
        for im_pair in self.im_pair_names:
            # compute metric scores
            metrics_values = {}
            for key in self.metrics_dict.keys():
                metrics_values[key] = self.metrics_dict[key](self.image_data[im_pair[0]], self.image_data[im_pair[1]])
            self.display_metrics(metrics_values, im_pair)
            # compute metric images
            for key in self.metrics_image_dict.keys():
                image_name = gui_utils.get_metric_image_name(key, im_pair)
                image_name = key+str(im_pair)
                self.image_data[image_name] = self.metrics_image_dict[key](self.image_data[im_pair[0]], self.image_data[im_pair[1]])

    def display_metrics(self, metrics, label):
        if self.metrics_info_format == 'graph':
            self.display_metrics_graph(metrics, label)
        else:
            self.display_metrics_text(metrics, label)

    def display_metrics_graph(self, metrics, label):
        bar_plt = plot_utils.bar_plotter(bar_names=[label[0]],
                                        var_names=list(metrics.keys()),
                                        ax=self.widgets['label'][str(label)+'_metrics_info'])
        bar_plt.plot(label[0], list(metrics.values()))
        bar_plt.show()

    def display_metrics_text(self, metrics, label, disp_len=5):
        text = ''
        for key in metrics.keys():
            metric = gui_utils.str_to_len(str(metrics[key]), disp_len, '0')
            text += key + ': ' + metric + '\n'
        self.widgets['label'][str(label)+'_metrics_info'].setText(text)

    def get_metrics_over_range(self):
        # compute all metrics over their range of params and get avg/std
        data_store = {}
        # initialise data_store
        for im_pair in self.im_pair_names:
            data_store[str(im_pair)] = {}
            for metric in self.metrics_dict.keys():
                data_store[str(im_pair)][metric] = {}
                for trans in self.sliders.keys():
                    data_store[str(im_pair)][metric][trans] = []

        # compute over all image transformations
        for im_pair in self.im_pair_names:
            for curr_trans in self.sliders.keys():
                for trans_value in self.sliders[curr_trans]['values']:
                    trans_im = self.image_data[im_pair[0]]
                    for other_trans in self.sliders.keys():
                        if other_trans != curr_trans:
                            ui_slider_value = self.im_trans_params[other_trans]
                            trans_im = self.sliders[other_trans]['function'](trans_im, ui_slider_value)
                        else:
                            trans_im = self.sliders[curr_trans]['function'](trans_im, trans_value)
                    for metric in self.metrics_dict.keys():
                        metric_score = self.metrics_dict[metric](self.image_data[im_pair[0]], trans_im)
                        data_store[str(im_pair)][metric][curr_trans].append(float(metric_score))
        self.plot_metrics_graphs(data_store)

    def plot_metrics_graphs(self, data_store):
        # plot
        for im_pair in self.im_pair_names:
            radar_plotter = plot_utils.radar_plotter(radar_names=list(self.metrics_dict.keys()),
                                            var_names=list(self.sliders.keys()),
                                            ax=self.widgets['graph'][str(im_pair)+'_metrics'])
            for metric in self.metrics_dict.keys():
                mean_value = []
                std_value = []
                transform = []
                for trans in self.sliders.keys():
                    transform.append(trans)
                    mean_value.append(np.mean(data_store[str(im_pair)][metric][trans]))
                    # std_value.append(np.std(data_store[str(im_pair)][metric][trans]))
                radar_plotter.plot(metric, mean_value)
            radar_plotter.show()


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
