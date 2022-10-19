import sys
from functools import partial
import os
# import pandas as pd

import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QInputDialog, QLineEdit, QMenu, QFileDialog, QPushButton, QGridLayout, QLabel, QSlider, QComboBox, QCheckBox
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure

from IQM_VIS import gui_utils, plot_utils

class make_app(QMainWindow):
    def __init__(self, app,
                image_paths,
                metrics_dict,
                metrics_image_dict,
                transformations,
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

    def init_style(self, css_file='style.css'):
        with open(css_file, 'r') as file:
            self.app.setStyleSheet(file.read())

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

    def init_transforms(self):
            # define what sliders we are using from image transformations
        self.sliders = {}
        for key in self.transformations.keys():
            self.sliders[key] = {}
            self.sliders[key]['release'] = [self.display_images]
            self.sliders[key]['value_change'] = [partial(self.generic_value_change, key), self.display_images]
            self.sliders[key]['function'] = self.transformations[key]['function']
            if 'init_value' not in self.transformations[key].keys():
                self.transformations[key]['init_value'] = 0
            if 'values' in self.transformations[key].keys():
                self.sliders[key]['values'] = self.transformations[key]['values']
            else:
                if 'num_values' not in self.transformations[key].keys():
                    self.transformations[key]['num_values'] = 21   # make default value for steps in slider range
                self.sliders[key]['values'] = np.linspace(self.transformations[key]['min'], self.transformations[key]['max'], self.transformations[key]['num_values'])
                # see if we need to make odd numbers (for use with kernel sizes)
                if 'normalise' in self.transformations[key].keys():
                    if self.transformations[key]['normalise'] == 'odd':
                        self.sliders[key]['values'] = self.sliders[key]['values'][self.sliders[key]['values']%2 == 1]
                        self.transformations[key]['num_values'] = len(self.sliders[key]['values'])
            # get ind of the initial value to set the slider at
            self.sliders[key]['init_ind'] = np.searchsorted(self.sliders[key]['values'], self.transformations[key]['init_value'], side='left')

    def init_widgets(self):
        '''
        create all the widgets we need and init params
        '''
        # widget dictionary store
        self.widgets = {'button': {}, 'slider': {}, 'checkbox': {}, 'label': {}, 'image':{}, 'graph':{}}
        for im_pair in self.im_pair_names:
            for im_name in im_pair:
                # image widget
                self.widgets['image'][im_name] = QLabel(self)
                self.widgets['image'][im_name].setAlignment(Qt.AlignmentFlag.AlignCenter)
                # image label
                self.widgets['label'][im_name] = QLabel(self)
                self.widgets['label'][im_name].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widgets['label'][im_name].setText(im_name)
            # metrics images
            for key in self.metrics_image_dict.keys():
                metric_name = gui_utils.get_metric_image_name(key, im_pair)
                self.widgets['image'][metric_name] = QLabel(self)
                self.widgets['image'][metric_name].setAlignment(Qt.AlignmentFlag.AlignCenter)
                # image label
                self.widgets['label'][metric_name] = QLabel(self)
                self.widgets['label'][metric_name].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widgets['label'][metric_name].setText(metric_name)
            # metrics info
            self.widgets['label'][str(im_pair)+'_metrics'] = QLabel(self)
            self.widgets['label'][str(im_pair)+'_metrics'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widgets['label'][str(im_pair)+'_metrics'].setText('Metrics '+str(im_pair))
            if self.metrics_info_format == 'graph':
                self.widgets['label'][str(im_pair)+'_metrics_info'] = gui_utils.MplCanvas(self)
            else:
                self.widgets['label'][str(im_pair)+'_metrics_info'] = QLabel(self)
                self.widgets['label'][str(im_pair)+'_metrics_info'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widgets['label'][str(im_pair)+'_metrics_info'].setText('')
            # metrics graphs
            self.widgets['label'][str(im_pair)+'_metrics_graph'] = QLabel(self)
            self.widgets['label'][str(im_pair)+'_metrics_graph'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widgets['label'][str(im_pair)+'_metrics_graph'].setText('Metrics Avg. Graph')
            self.widgets['graph'][str(im_pair)+'_metrics'] = gui_utils.MplCanvas(self, polar=True)

        '''buttons'''
        # self.widgets['button']['load_dataset'] = QPushButton('Choose Dataset', self)
        # self.widgets['button']['load_dataset'].clicked.connect(self.choose_dataset)
        # self.widgets['button']['prev'] = QPushButton('<', self)
        # self.widgets['button']['prev'].clicked.connect(self.load_prev_image)
        # self.widgets['label']['filename'] = QLabel(self)
        # self.widgets['label']['filename'].setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.widgets['label']['filename'].setText('')
        # self.widgets['button']['next'] = QPushButton('>', self)
        # self.widgets['button']['next'].clicked.connect(self.load_next_image)
        self.widgets['button']['reset_sliders'] = QPushButton('Reset', self)
        self.widgets['button']['reset_sliders'].clicked.connect(self.reset_sliders)
        self.widgets['button']['force_update'] = QPushButton('Update', self)
        self.widgets['button']['force_update'].clicked.connect(self.display_images)
        self.widgets['button']['force_update'].clicked.connect(self.get_metrics_over_range)

        '''sliders'''
        self.im_trans_params = {}
        for key in self.sliders.keys():
            self.widgets['slider'][key] = QSlider(Qt.Orientation.Horizontal)
            self.widgets['slider'][key].setMinimum(0)
            self.widgets['slider'][key].setMaximum(len(self.sliders[key]['values'])-1)
            for func in self.sliders[key]['value_change']:
                self.widgets['slider'][key].valueChanged.connect(func)
            for func in self.sliders[key]['release']:
                self.widgets['slider'][key].sliderReleased.connect(func)
            self.im_trans_params[key] = self.sliders[key]['init_ind']
            self.widgets['label'][key] = QLabel(self)
            self.widgets['label'][key].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.widgets['label'][key].setText(key+':')
            self.widgets['label'][key+'_value'] = QLabel(self)
            self.widgets['label'][key+'_value'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widgets['label'][key+'_value'].setText(str(self.im_trans_params[key]))

    def init_layout(self):
        '''
        place all the widgets in the window
        '''
        # make main widget insdie the QMainWindow
        self.main_widget = QWidget()
        self.layout = QGridLayout()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        # sizes
        im_width = 15
        im_height = 15
        button = 1
        slider_width = int(im_width*2)
        check_box_width = 5
        # horizonal start values
        start_im = 1
        start_controls = 0#im_width*2+button

        # display images
        im_row = 0
        for im_pair in self.im_pair_names:
            col = 0
            self.layout.addWidget(self.widgets['label'][im_pair[0]], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
            self.layout.addWidget(self.widgets['image'][im_pair[0]], start_im+im_row*(im_height+button), (im_height+button)*col,   im_height, im_width)
            col += 1
            self.layout.addWidget(self.widgets['label'][im_pair[1]], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
            self.layout.addWidget(self.widgets['image'][im_pair[1]], start_im+im_row*(im_height+button), (im_height+button)*col, im_height, im_width)
            col += 1
            for key in self.metrics_image_dict.keys():
                metric_name = gui_utils.get_metric_image_name(key, im_pair)
                self.layout.addWidget(self.widgets['label'][metric_name], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
                self.layout.addWidget(self.widgets['image'][metric_name], start_im+im_row*(im_height+button), (im_height+button)*col, im_height, im_width)
                col += 1
            # metircs info
            self.layout.addWidget(self.widgets['label'][str(im_pair)+'_metrics'], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
            self.layout.addWidget(self.widgets['label'][str(im_pair)+'_metrics_info'], start_im+im_row*(im_height+button), (im_height+button)*col+button, im_height, im_width)
            col += 1
            self.layout.addWidget(self.widgets['label'][str(im_pair)+'_metrics_graph'], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
            self.layout.addWidget(self.widgets['graph'][str(im_pair)+'_metrics'], start_im+im_row*(im_height+button), (im_height+button)*col, im_height, im_width)
            col += 1
            im_row += 1

        # load files
        # self.layout.addWidget(self.widgets['button']['load_dataset'], im_height, 1, 1, 1)

        # image buttons (prev, copy, next, etc.)
        # self.layout.addWidget(self.widgets['button']['prev'], start_im+im_row*(im_height+button), 1, button, int(im_width*0.66))
        # self.layout.addWidget(self.widgets['label']['filename'], start_im+im_row*(im_height+button), int(im_width*0.66)+1, button, int(im_width*0.66))
        # self.layout.addWidget(self.widgets['button']['next'], start_im+im_row*(im_height+button), int(im_width*0.66)*2+1, button, int(im_width*0.66))
        # self.layout.addWidget(self.button_copy_im, 0, 1, 1, 1)

        i = (im_height+button)*im_row+button+start_im
        # checkboxes
        # self.layout.addWidget(self.widgets['checkbox']['real_im'],   button*i, start_controls+button, button, check_box_width)
        # self.layout.addWidget(self.widgets['checkbox']['run_generator'], button*i, start_controls+button+check_box_width, button, check_box_width)
        # i += 1

        # sliders
        for slider in self.sliders.keys():
            self.layout.addWidget(self.widgets['slider'][slider],   button*i, start_controls+button, button, slider_width)
            self.layout.addWidget(self.widgets['label'][slider],    button*i, start_controls,   button, button)
            self.layout.addWidget(self.widgets['label'][slider+'_value'], button*i, start_controls+button+slider_width,   button, button)
            i += 1

        # reset sliders
        self.layout.addWidget(self.widgets['button']['reset_sliders'], button*i, start_controls, button, button)
        self.layout.addWidget(self.widgets['button']['force_update'], button*i, start_controls+button, button, button)
        i += 1
        # init it!
        self.show()


    '''
    ==================== functions to bind to widgets ====================
    '''
    # buttons
    def load_prev_image(self):
        self.im_num -= 1
        if self.im_num < 0:
            self.im_num = len(self.df) - 1
        self.load_sim_image()
        self.load_real_image()
        self.display_images()

    def load_next_image(self):
        self.im_num += 1
        if self.im_num == len(self.df):
            self.im_num = 0
        self.load_sim_image()
        self.load_real_image()
        self.display_images()

    # sliders value changes
    def generic_value_change(self, key):
        index = self.widgets['slider'][key].value()
        self.im_trans_params[key] = self.sliders[key]['values'][index]
        self.display_slider_num(key) # display the new value ont UI

    def display_slider_num(self, key, disp_len=5):
        # display the updated value
        value_str = str(self.im_trans_params[key])
        value_str = gui_utils.str_to_len(value_str, disp_len, '0', plus=True)
        self.widgets['label'][key+'_value'].setText(value_str)

    def reset_sliders(self):
        for key in self.sliders.keys():
            self.widgets['slider'][key].setValue(self.sliders[key]['init_ind'])
        self.display_images()

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
        # self.get_metrics_errors()
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
        # for im_pair in self.im_pair_names:
        #     for im_name in im_pair:
        #         gui_utils.change_im(self.widgets['image'][im_name], self.image_data[im_name], resize=self.image_display_size)
            # ssim_name = 'SSIM('+str(im_pair)+')'
            # gui_utils.change_im(self.widgets['image'][ssim_name], self.image_data[ssim_name], resize=self.image_display_size)

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


    # '''
    # utils
    # '''
    # def load_dataset(self, csv_file):
    #     self.df = pd.read_csv(csv_file)
    #     self.im_num = 0   # row of csv dataset to use
    #     self.im_sim_dir = os.path.join(os.path.dirname(csv_file), 'images')
    #     self.im_real_dir = os.path.join(os.path.dirname(image_utils.get_real_csv_given_sim(csv_file)), 'images')
    #     self.load_sim_image()
    #     self.load_real_image()


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
