'''
UI create widgets
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>


from functools import partial

import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QInputDialog, QLineEdit, QMenu, QFileDialog, QPushButton, QGridLayout, QLabel, QSlider, QComboBox, QCheckBox
from PyQt6.QtCore import Qt

from IQM_VIS.utils import gui_utils

# base sub class to initialise QMainWindow and general UI functions for widgets
class app_widgets():
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
        self.widgets = {'button': {}, 'slider': {}, 'label': {}, 'image':{}, 'graph':{}}
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
        self.widgets['button']['reset_sliders'] = QPushButton('Reset', self)
        self.widgets['button']['reset_sliders'].clicked.connect(self.reset_sliders)
        self.widgets['button']['force_update'] = QPushButton('Update', self)
        self.widgets['button']['force_update'].clicked.connect(self.display_images)
        if self.metrics_avg_graph:
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


    '''
    ==================== functions to bind to sliders/widgets ====================
    '''
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
