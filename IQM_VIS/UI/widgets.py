'''
UI create widgets
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from functools import partial

import numpy as np
from PyQt6.QtWidgets import QPushButton, QLabel, QSlider
from PyQt6.QtCore import Qt

from IQM_VIS.utils import gui_utils

# sub class used by IQM_VIS.main.make_app to initialise widgets and general UI functions for widgets
class widgets():
    def _init_transforms(self):
        ''' define what sliders we are using from image transformations '''
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
        self._init_transforms() # first setup the slider data

        self.widget_row = {}
        for i, data_store in enumerate(self.data_stores):   # create each row of the widgets
            self.widget_row[i] = {'images':{}, 'metrics':{}, 'metric_images':{}}
            '''image and transformed image'''
            for image_name in ['original', 'transformed']:
                self.widget_row[i]['images'][image_name] = {}
                # image widget
                self.widget_row[i]['images'][image_name]['data'] = QLabel(self)
                self.widget_row[i]['images'][image_name]['data'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                # image label
                self.widget_row[i]['images'][image_name]['label'] = QLabel(self)
                self.widget_row[i]['images'][image_name]['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widget_row[i]['images'][image_name]['label'].setText(image_name)

            '''metric images'''
            for key in data_store.metric_images.keys():
                self.widget_row[i]['metric_images'][key] = {}
                self.widget_row[i]['metric_images'][key]['data'] = QLabel(self)
                self.widget_row[i]['metric_images'][key]['data'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                # image label
                self.widget_row[i]['metric_images'][key]['label'] = QLabel(self)
                self.widget_row[i]['metric_images'][key]['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)

            '''metrics graphs'''
            im_pair_name = gui_utils.get_image_pair_name(data_store)
            self.widget_row[i]['metrics']['info'] = {}
            self.widget_row[i]['metrics']['info']['label'] = QLabel(self)
            self.widget_row[i]['metrics']['info']['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widget_row[i]['metrics']['info']['label'].setText('Metrics '+im_pair_name)
            if self.metrics_info_format == 'graph':
                self.widget_row[i]['metrics']['info']['data'] = gui_utils.MplCanvas(self)
            else:
                self.widget_row[i]['metrics']['info']['data'] = QLabel(self)
                self.widget_row[i]['metrics']['info']['data'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widget_row[i]['metrics']['info']['data'].setText('')
            # metrics avgerage graphs
            if self.metrics_avg_graph:
                self.widget_row[i]['metrics']['avg'] = {}
                self.widget_row[i]['metrics']['avg']['label'] = QLabel(self)
                self.widget_row[i]['metrics']['avg']['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widget_row[i]['metrics']['avg']['label'].setText('Metrics Avg. Graph')
                self.widget_row[i]['metrics']['avg']['data'] = gui_utils.MplCanvas(self, polar=True)
                self.widget_row[i]['metrics']['avg']['data'].setToolTip('Mean metric value over the range of each transform.')
            if self.metric_range_graph:
                self.widget_row[i]['metrics']['range'] = {}
                self.widget_row[i]['metrics']['range']['label'] = QLabel(self)
                self.widget_row[i]['metrics']['range']['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widget_row[i]['metrics']['range']['label'].setText('Metrics Range Graph')
                self.widget_row[i]['metrics']['range']['data'] = gui_utils.MplCanvas(self)
                self.widget_row[i]['metrics']['range']['data'].setToolTip('Single tranformation value range for all metrics.')



        '''buttons'''
        self.widget_sliders = {'button': {}, 'slider':{}, 'label':{}}
        self.widget_sliders['button']['reset_sliders'] = QPushButton('Reset', self)
        self.widget_sliders['button']['reset_sliders'].clicked.connect(self.reset_sliders)
        if self.metrics_avg_graph:
            self.widget_sliders['button']['force_update'] = QPushButton('Calc. Avg.', self)
            self.widget_sliders['button']['force_update'].setToolTip('Update metrics average plot using the current slider values.')
            self.widget_sliders['button']['force_update'].clicked.connect(self.display_images)
            self.widget_sliders['button']['force_update'].clicked.connect(self.get_metrics_over_range)
        if self.metric_range_graph:
            # buttons to control which graph to show
            self.widget_sliders['button']['next_metric_graph'] = QPushButton('->', self)
            self.widget_sliders['button']['next_metric_graph'].clicked.connect(partial(self.change_metric_range_graph, 1))
            self.widget_sliders['button']['prev_metric_graph'] = QPushButton('<-', self)
            self.widget_sliders['button']['prev_metric_graph'].clicked.connect(partial(self.change_metric_range_graph, -1))
        if self.dataset:
            # control what image is used from the dataset
            self.widget_sliders['button']['next_data'] = QPushButton('->', self)
            self.widget_sliders['button']['next_data'].clicked.connect(partial(self.change_data, 1))
            self.widget_sliders['button']['prev_data'] = QPushButton('<-', self)
            self.widget_sliders['button']['prev_data'].clicked.connect(partial(self.change_data, -1))
            self.widget_sliders['label']['data'] = QLabel(self)
            self.widget_sliders['label']['data'].setText('Dataset Scroll:')


        '''sliders'''
        self.im_trans_params = {}
        for key in self.sliders.keys():
            self.widget_sliders['slider'][key] = {}
            self.widget_sliders['slider'][key]['data'] = QSlider(Qt.Orientation.Horizontal)
            self.widget_sliders['slider'][key]['data'].setMinimum(0)
            self.widget_sliders['slider'][key]['data'].setMaximum(len(self.sliders[key]['values'])-1)
            for func in self.sliders[key]['value_change']:
                self.widget_sliders['slider'][key]['data'].valueChanged.connect(func)
            for func in self.sliders[key]['release']:
                self.widget_sliders['slider'][key]['data'].sliderReleased.connect(func)
            self.im_trans_params[key] = self.sliders[key]['init_ind']
            self.widget_sliders['slider'][key]['label'] = QLabel(self)
            self.widget_sliders['slider'][key]['label'].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.widget_sliders['slider'][key]['label'].setText(key+':')
            self.widget_sliders['slider'][key]['value'] = QLabel(self)
            self.widget_sliders['slider'][key]['value'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widget_sliders['slider'][key]['value'].setText(str(self.im_trans_params[key]))

        self.set_image_name_text()


    '''
    ==================== functions to bind to sliders/widgets ====================
    '''
    # sliders value changes
    def generic_value_change(self, key):
        index = self.widget_sliders['slider'][key]['data'].value()
        self.im_trans_params[key] = self.sliders[key]['values'][index]
        self.display_slider_num(key) # display the new value ont UI

    def display_slider_num(self, key, disp_len=5):
        # display the updated value
        value_str = str(self.im_trans_params[key])
        value_str = gui_utils.str_to_len(value_str, disp_len, '0', plus=True)
        self.widget_sliders['slider'][key]['value'].setText(value_str)

    def reset_sliders(self):
        for key in self.sliders.keys():
            self.widget_sliders['slider'][key]['data'].setValue(self.sliders[key]['init_ind'])
        self.display_images()
        self.redo_plots()

    def set_image_name_text(self):
        for i, data_store in enumerate(self.data_stores):
            self.widget_row[i]['images']['original']['label'].setText(data_store.get_reference_image_name())
            self.widget_row[i]['images']['transformed']['label'].setText(gui_utils.get_transformed_image_name(data_store))
            for key in data_store.metric_images.keys():
                metric_name = gui_utils.get_metric_image_name(key, data_store)
                if len(metric_name) > 20:
                    metric_name = key
                self.widget_row[i]['metric_images'][key]['label'].setText(metric_name)
