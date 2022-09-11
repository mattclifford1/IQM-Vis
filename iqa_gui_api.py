import sys
import argparse
from functools import partial
import os
import pandas as pd

import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QInputDialog, QLineEdit, QMenu, QFileDialog, QPushButton, QGridLayout, QLabel, QSlider, QComboBox, QCheckBox
# from PyQt6.QtGui import QImage, QColor
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QPainter, QBrush
from PyQt6.QtWidgets import QStyle, QStyleOptionSlider
from PyQt6.QtCore import QRect, QPoint, Qt

import sys; sys.path.append('..'); sys.path.append('.')
from image_utils import load_image
from gui_utils import change_im
import image_utils
# import networks
import metrics

class make_app(QMainWindow):
    def __init__(self, app,
                image_path):
        super().__init__()
        self.app = app
        self.image_path = image_path

        self.metrics = metrics.im_metrics()
        self.init_widgets()
        self.init_images()
        self.init_layout()

        self.image_display_size = (175, 175)
        self.display_images()
        self.reset_sliders()

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
        if os.path.exists(self.image_path):
            self.image_data['X'] = image_loader(self.image_path)
        else:
            print('Cannot find image file: ', self.image_path)
            self.image_data['X'] = np.zeros([128, 128, 1], dtype=np.uint8)

    def init_widgets(self):
        '''
        create all the widgets we need and init params
        '''
        # define what sliders we are using
        self.sliders = {
                   'rotation':{'min':-180, 'max':180, 'init_value':0, 'value_change':[partial(self.generic_value_change, 'rotation', normalise=None), self.display_images], 'release': [self.display_images]},
                   'blur':{'min':0, 'max':40, 'init_value':0, 'value_change':[partial(self.generic_value_change, 'blur', normalise='odd')], 'release': [self.display_images]},
                   'brightness':{'min':-255, 'max':255, 'init_value':0, 'value_change':[partial(self.generic_value_change, 'brightness', normalise=255)], 'release': [self.display_images]},
                   'zoom':{'min':10, 'max':400, 'init_value':100, 'value_change':[partial(self.generic_value_change, 'zoom', normalise=100), self.display_images], 'release': [self.display_images]},
                   'x_shift':{'min':-100, 'max':100, 'init_value':0, 'value_change':[partial(self.generic_value_change, 'x_shift', normalise=100), self.display_images], 'release': [self.display_images]},
                   'y_shift':{'min':-100, 'max':100, 'init_value':0, 'value_change':[partial(self.generic_value_change, 'y_shift', normalise=100), self.display_images], 'release': [self.display_images]},
                   }

        '''images'''
        # set up layout of images
        self.im_pair_names = [
                              # ('Xr', 'T(Xr)'),
                              ('X', 'T(X)'),
                              # ('G(Xr)', 'T(G(Xr))'),
                              # ('G(T(Xr))', 'T(G(Xr))_'),
                              ]
        # widget dictionary store
        self.widgets = {'button': {}, 'slider': {}, 'checkbox': {}, 'label': {}, 'image':{}}
        for im_pair in self.im_pair_names:
            for im_name in im_pair:
                # image widget
                self.widgets['image'][im_name] = QLabel(self)
                self.widgets['image'][im_name].setAlignment(Qt.AlignmentFlag.AlignCenter)
                # image label
                self.widgets['label'][im_name] = QLabel(self)
                self.widgets['label'][im_name].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widgets['label'][im_name].setText(im_name)
                # self.widgets['label'][im_name].setContentsMargins(0,0,0,0)
            # ssim images
            ssim_name = 'SSIM('+str(im_pair)+')'
            self.widgets['image'][ssim_name] = QLabel(self)
            self.widgets['image'][ssim_name].setAlignment(Qt.AlignmentFlag.AlignCenter)
            # image label
            self.widgets['label'][ssim_name] = QLabel(self)
            self.widgets['label'][ssim_name].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widgets['label'][ssim_name].setText(ssim_name)
            # metrics info
            self.widgets['label'][str(im_pair)+'_metrics'] = QLabel(self)
            self.widgets['label'][str(im_pair)+'_metrics'].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.widgets['label'][str(im_pair)+'_metrics'].setText('Metrics '+str(im_pair)+':')
            self.widgets['label'][str(im_pair)+'_metrics_info'] = QLabel(self)
            self.widgets['label'][str(im_pair)+'_metrics_info'].setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.widgets['label'][str(im_pair)+'_metrics_info'].setText('')
            # error info
            self.widgets['label'][str(im_pair)+'_errors'] = QLabel(self)
            self.widgets['label'][str(im_pair)+'_errors'].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.widgets['label'][str(im_pair)+'_errors'].setText('Pose Errors:')
            self.widgets['label'][str(im_pair)+'_errors_info'] = QLabel(self)
            self.widgets['label'][str(im_pair)+'_errors_info'].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.widgets['label'][str(im_pair)+'_errors_info'].setText('')

        '''buttons'''
        # self.widgets['button']['load_dataset'] = QPushButton('Choose Dataset', self)
        # self.widgets['button']['load_dataset'].clicked.connect(self.choose_dataset)
        self.widgets['button']['prev'] = QPushButton('<', self)
        self.widgets['button']['prev'].clicked.connect(self.load_prev_image)
        self.widgets['label']['filename'] = QLabel(self)
        self.widgets['label']['filename'].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widgets['label']['filename'].setText('')
        self.widgets['button']['next'] = QPushButton('>', self)
        self.widgets['button']['next'].clicked.connect(self.load_next_image)
        self.widgets['button']['reset_sliders'] = QPushButton('Reset', self)
        self.widgets['button']['reset_sliders'].clicked.connect(self.reset_sliders)
        self.widgets['button']['force_update'] = QPushButton('Update', self)
        self.widgets['button']['force_update'].clicked.connect(self.display_images)

        '''sliders'''
        self.im_trans_params = {}
        for key in self.sliders.keys():
            self.widgets['slider'][key] = QSlider(Qt.Orientation.Horizontal)
            self.widgets['slider'][key].setMinimum(self.sliders[key]['min'])
            self.widgets['slider'][key].setMaximum(self.sliders[key]['max'])
            for func in self.sliders[key]['value_change']:
                self.widgets['slider'][key].valueChanged.connect(func)
            for func in self.sliders[key]['release']:
                self.widgets['slider'][key].sliderReleased.connect(func)
            self.im_trans_params[key] = self.sliders[key]['init_value']
            self.widgets['label'][key] = QLabel(self)
            self.widgets['label'][key].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.widgets['label'][key].setText(key+':')
            self.widgets['label'][key+'_value'] = QLabel(self)
            self.widgets['label'][key+'_value'].setAlignment(Qt.AlignmentFlag.AlignRight)
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
            ssim_name = 'SSIM('+str(im_pair)+')'
            self.layout.addWidget(self.widgets['label'][ssim_name], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
            self.layout.addWidget(self.widgets['image'][ssim_name], start_im+im_row*(im_height+button), (im_height+button)*col, im_height, im_width)
            col += 1
            # metircs info
            self.layout.addWidget(self.widgets['label'][str(im_pair)+'_metrics'], start_im+im_row*(im_height+button)+1, (im_height+button)*col, button, button)
            self.layout.addWidget(self.widgets['label'][str(im_pair)+'_metrics_info'], start_im+im_row*(im_height+button)+1, (im_height+button)*col+button, im_height, button)
            col += 1
            # errors info
            self.layout.addWidget(self.widgets['label'][str(im_pair)+'_errors'], start_im+im_row*(im_height+button)+1, (im_height+button)*col+(button*2), button, button)
            self.layout.addWidget(self.widgets['label'][str(im_pair)+'_errors_info'], start_im+im_row*(im_height+button)+1, (im_height+button)*col+(button*3), im_height, button)
            im_row += 1

        # load files
        # self.layout.addWidget(self.widgets['button']['load_dataset'], im_height, 1, 1, 1)

        # image buttons (prev, copy, next, etc.)
        self.layout.addWidget(self.widgets['button']['prev'], start_im+im_row*(im_height+button), 1, button, int(im_width*0.66))
        self.layout.addWidget(self.widgets['label']['filename'], start_im+im_row*(im_height+button), int(im_width*0.66)+1, button, int(im_width*0.66))
        self.layout.addWidget(self.widgets['button']['next'], start_im+im_row*(im_height+button), int(im_width*0.66)*2+1, button, int(im_width*0.66))
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
    def generic_value_change(self, key, normalise=None):
        if normalise == 'odd':
            self.im_trans_params[key] = (int(self.widgets['slider'][key].value()/2)*2) + 1    # need to make kernel size odd
            if self.im_trans_params[key] == 1:
                self.im_trans_params[key] = 0
        else:
            self.im_trans_params[key] = self.widgets['slider'][key].value()
        if type(normalise) is int:
            self.im_trans_params[key] = self.im_trans_params[key]/normalise
        # display the updated value
        value_str = str(self.im_trans_params[key])
        disp_len = 4
        if len(value_str) > disp_len:
            value_str = value_str[:disp_len]
        elif len(value_str) < disp_len:
            value_str = ' '*(disp_len-len(value_str)) + value_str
        self.widgets['label'][key+'_value'].setText(value_str)

    def reset_sliders(self):
        for key in self.sliders.keys():
            self.widgets['slider'][key].setValue(self.sliders[key]['init_value'])
        self.display_images()

    '''
    image updaters
    '''
    def transform_image(self, image):
        return image_utils.transform_image(image, self.im_trans_params)

    def display_images(self):
        self.get_image_data()
        self.get_metrics_errors()
        self.update_image_widgets()

    def _display_images_quick(self):
        # dont calc metrics/errors - just update widgets
        self.get_image_data()
        self.update_image_widgets()

    def get_image_data(self):
        # get transformed images
        self.image_data['T(X)'] = self.transform_image(self.image_data['X'])

    def update_image_widgets(self):
        # display images
        for im_pair in self.im_pair_names:
            for im_name in im_pair:
                change_im(self.widgets['image'][im_name], self.image_data[im_name], resize=self.image_display_size)
            ssim_name = 'SSIM('+str(im_pair)+')'
            change_im(self.widgets['image'][ssim_name], self.image_data[ssim_name], resize=self.image_display_size)

    '''
    metrics/error info updaters
    '''
    def get_metrics_errors(self):
        metrics = {}
        errors = {}
        for im_pair in self.im_pair_names:
            ssim_name = 'SSIM('+str(im_pair)+')'
            metric, ssim_full_im = self.metrics.get_metrics(self.image_data[im_pair[0]], self.image_data[im_pair[1]])
            metrics[str(im_pair)] = metric
            self.image_data[ssim_name] = ssim_full_im
            # errors[str(im_pair)] = {}
            # for im_name in im_pair:
            #     # decide whether to use real or simulated space pose estimation
            #     if 'Xs' in im_name or 'G' in im_name:
            #         errors[str(im_pair)][im_name] = self.pose_esimator_sim.get_error(self.image_data[im_name], self.image_data['poses'])
            #     else:
            #         errors[str(im_pair)][im_name] = self.pose_esimator_real.get_error(self.image_data[im_name], self.image_data['poses'])

            self.display_metrics(metrics[str(im_pair)], str(im_pair))
            # self.display_errors(errors[str(im_pair)], str(im_pair))

    def display_metrics(self, metrics, label):
        text = ''
        for key in metrics.keys():
            metric = str(metrics[key][0])
            metric = metric[:min(len(metric), 5)]
            text += key + ': ' + metric + '\n'
        self.widgets['label'][label+'_metrics_info'].setText(text)

    def display_errors(self, errors_dict, label):
        text = ''
        for key in errors_dict.keys():
            text += key + ': ' + str(errors_dict[key]['MAE'][0])[:5] + '\n'
        self.widgets['label'][label+'_errors_info'].setText(text)

    '''
    utils
    '''
    def load_dataset(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.im_num = 0   # row of csv dataset to use
        self.im_sim_dir = os.path.join(os.path.dirname(csv_file), 'images')
        self.im_real_dir = os.path.join(os.path.dirname(image_utils.get_real_csv_given_sim(csv_file)), 'images')
        self.load_sim_image()
        self.load_real_image()


def image_loader(im_path):
    im = load_image(im_path)
    return image_utils.process_im(im, data_type='sim')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, help='image file to use', default=os.path.join(os.path.expanduser('~'),'summer-project/data/Bourne/tactip/sim/surface_3d/tap/128x128/csv_train/images/image_1.png'))
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = make_app(app, args.image_path)


    sys.exit(app.exec())
