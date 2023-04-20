'''
UI create widgets
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from functools import partial

import numpy as np
from PyQt6.QtWidgets import QPushButton, QLabel, QSlider, QCheckBox, QComboBox, QLineEdit
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt

import IQM_Vis
from IQM_Vis.UI.custom_widgets import ClickLabel
from IQM_Vis.utils import gui_utils, plot_utils, image_utils

# sub class used by IQM_Vis.main.make_app to initialise widgets and general UI functions for widgets
class widgets():
    def init_widgets(self):
        '''
        create all the widgets we need and init params
        '''
        self._init_widgets()
        self.set_image_name_text()
        self._init_image_settings()

    def _init_widgets(self):
        '''
        create all the widgets we need and init params
        '''
        # first setup the slider data
        self.sliders = {'transforms': {}, 'metric_params': {}}
        self._init_sliders(self.sliders['transforms'], self.checked_transformations,  param_group='transforms')
        self._init_sliders(self.sliders['metric_params'], self.metric_params, param_group='metric_params')

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
            for metric_image in data_store.metric_images:
                if metric_image in self.checked_metric_images:
                    self.widget_row[i]['metric_images'][metric_image] = {}
                    self.widget_row[i]['metric_images'][metric_image]['data'] = QLabel(self)
                    self.widget_row[i]['metric_images'][metric_image]['data'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                    # image label
                    self.widget_row[i]['metric_images'][metric_image]['label'] = QLabel(self)
                    self.widget_row[i]['metric_images'][metric_image]['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)

            '''metrics graphs'''
            im_pair_name = gui_utils.get_image_pair_name(data_store)
            self.widget_row[i]['metrics']['info'] = {}
            self.widget_row[i]['metrics']['info']['label'] = QLabel(self)
            self.widget_row[i]['metrics']['info']['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widget_row[i]['metrics']['info']['label'].setText('Metrics '+im_pair_name)
            if self.metrics_info_format == 'graph':
                self.widget_row[i]['metrics']['info']['data'] = gui_utils.MplCanvas(size=(self.graph_size/10, self.graph_size/10))
            else:
                self.widget_row[i]['metrics']['info']['data'] = QLabel(self)
                self.widget_row[i]['metrics']['info']['data'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widget_row[i]['metrics']['info']['data'].setText('')
            # metrics avgerage graphs
            if self.metrics_avg_graph:
                self.widget_row[i]['metrics']['avg'] = {}
                self.widget_row[i]['metrics']['avg']['label'] = QLabel(self)
                self.widget_row[i]['metrics']['avg']['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widget_row[i]['metrics']['avg']['label'].setText('IQM Averages')
                self.widget_row[i]['metrics']['avg']['data'] = gui_utils.MplCanvas(size=(self.graph_size/10, self.graph_size/10), polar=True)
                self.widget_row[i]['metrics']['avg']['data'].setToolTip('Mean metric value over the range of each transform.')
            if self.metric_range_graph:
                self.widget_row[i]['metrics']['range'] = {}
                self.widget_row[i]['metrics']['range']['label'] = QLabel(self)
                self.widget_row[i]['metrics']['range']['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widget_row[i]['metrics']['range']['label'].setText('Response Profiles')
                self.widget_row[i]['metrics']['range']['data'] = gui_utils.MplCanvas(size=(self.graph_size/10, self.graph_size/10))
                self.widget_row[i]['metrics']['range']['data'].setToolTip('Single tranformation value range for all metrics.')
            self.widget_row[i]['metrics']['correlation'] = {}
            self.widget_row[i]['metrics']['correlation']['label'] = QLabel(self)
            self.widget_row[i]['metrics']['correlation']['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widget_row[i]['metrics']['correlation']['label'].setText('Human Correlation')
            self.widget_row[i]['metrics']['correlation']['data'] = gui_utils.MplCanvas(size=(self.graph_size/10, self.graph_size/10))
            self.widget_row[i]['metrics']['correlation']['label'].setToolTip('Human scores versus IQMs.')


        '''buttons'''
        self.widget_controls = {'button': {}, 'slider': {}, 'label': {}, 'check_box': {}}
        
        if (self.metrics_avg_graph or self.metric_range_graph):
            # Update graphs
            self.widget_controls['button']['force_update'] = QPushButton('Update Graphs', self)
            self.widget_controls['button']['force_update'].setToolTip('Update graphs using all the current slider values.')
            self.widget_controls['button']['force_update'].clicked.connect(self.display_images)
            self.widget_controls['button']['force_update'].clicked.connect(partial(self.redo_plots, True))
            # Change plot limits
            self.widget_controls['check_box']['graph_limits'] = QCheckBox('Squeeze plots')
            self.widget_controls['check_box']['graph_limits'].setToolTip('Set the scale of the plots to the metric data range.')
            self.widget_controls['check_box']['graph_limits'].setCheckState(Qt.CheckState.Unchecked)
            self.widget_controls['check_box']['graph_limits'].stateChanged.connect(self.change_plot_lims)

        if self.metric_range_graph:
            # buttons to control which metric range graph to show
            self.widget_controls['button']['next_metric_graph'] = QPushButton('->', self)
            self.widget_controls['button']['next_metric_graph'].clicked.connect(partial(self.change_metric_range_graph, 1))
            self.widget_controls['button']['prev_metric_graph'] = QPushButton('<-', self)
            self.widget_controls['button']['prev_metric_graph'].clicked.connect(partial(self.change_metric_range_graph, -1))
        # buttons to control which correlation graph to show
        self.widget_controls['button']['next_correlation_graph'] = QPushButton('->', self)
        self.widget_controls['button']['next_correlation_graph'].clicked.connect(partial(self.change_metric_correlations_graph, 1))
        self.widget_controls['button']['prev_correlation_graph'] = QPushButton('<-', self)
        self.widget_controls['button']['prev_correlation_graph'].clicked.connect(partial(self.change_metric_correlations_graph, -1))

        if self.dataset:
            # control what image is used from the dataset
            self.widget_controls['button']['next_data'] = QPushButton('->', self)
            self.widget_controls['button']['next_data'].clicked.connect(partial(self.change_data, 1))
            self.widget_controls['button']['prev_data'] = QPushButton('<-', self)
            self.widget_controls['button']['prev_data'].clicked.connect(partial(self.change_data, -1))
            self.widget_controls['label']['data'] = QLabel(self)
            self.widget_controls['label']['data'].setText('Change Image:')

        # launch experiment button
        self.widget_controls['button']['launch_exp'] = QPushButton('Run Experiment', self)
        self.widget_controls['button']['launch_exp'].clicked.connect(self.launch_experiment)


        '''sliders'''
        self.params_from_sliders = {}
        for param_group, slider_group in self.sliders.items():
            self.params_from_sliders[param_group] = {}
            self.widget_controls['button'][param_group] = {}
            self.widget_controls['button'][param_group]['reset_sliders'] = QPushButton('Reset', self)
            if param_group == 'metric_params':
                redo_graphs = True
            else:
                redo_graphs = False
            self.widget_controls['button'][param_group]['reset_sliders'].clicked.connect(
                partial(self.reset_slider_group, param_group, redo_graphs))

            for key, item_sliders in slider_group.items():
                self.widget_controls['slider'][key] = {}
                self.widget_controls['slider'][key]['data'] = QSlider(Qt.Orientation.Horizontal)
                self.widget_controls['slider'][key]['data'].setMinimum(0)
                self.widget_controls['slider'][key]['data'].setMaximum(len(item_sliders['values'])-1)
                for func in item_sliders['value_change']:
                    self.widget_controls['slider'][key]['data'].valueChanged.connect(func)
                for func in item_sliders['release']:
                    self.widget_controls['slider'][key]['data'].sliderReleased.connect(func)
                self.params_from_sliders['transforms'][key] = item_sliders['init_ind']
                self.widget_controls['slider'][key]['label'] = QLabel(self)
                self.widget_controls['slider'][key]['label'].setAlignment(Qt.AlignmentFlag.AlignRight)
                self.widget_controls['slider'][key]['label'].setText(f"{key}:")
                self.widget_controls['slider'][key]['value'] = QLabel(self)
                self.widget_controls['slider'][key]['value'].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widget_controls['slider'][key]['value'].setText(str(self.params_from_sliders['transforms'][key]))

    '''
    setup/helper functions
    '''
    def _init_sliders(self, sliders_dict, info_dict, param_group):
        '''
        generic initialiser of sliders (will change the dicts input rather than returning - like C++ pointers &)
            sliders_dict: holds the slider widgets
            info_dict: info to initialise the sliders
        '''
        for key, info_item in info_dict.items():
            sliders_dict[key] = {}
            sliders_dict[key]['release'] = [self.display_images]
            sliders_dict[key]['value_change'] = [partial(self.generic_value_change, key, param_group), self.display_images]
            if 'function' in info_item.keys():
                sliders_dict[key]['function'] = info_item['function']
            if 'init_value' not in info_item.keys():
                info_item['init_value'] = 0
            if 'values' in info_item.keys():
                sliders_dict[key]['values'] = info_item['values']
            else:
                if 'num_values' not in info_item.keys():
                    info_item['num_values'] = 21   # make default value for steps in slider range
                sliders_dict[key]['values'] = np.linspace(info_item['min'], info_item['max'], info_item['num_values'])
                # see if we need to make odd numbers (for use with kernel sizes)
                if 'normalise' in info_item.keys():
                    if info_item['normalise'] == 'odd':
                        sliders_dict[key]['values'] = sliders_dict[key]['values'][sliders_dict[key]['values']%2 == 1]
                        info_item['num_values'] = len(sliders_dict[key]['values'])
            # get ind of the initial value to set the slider at
            sliders_dict[key]['init_ind'] = np.searchsorted(sliders_dict[key]['values'], info_item['init_value'], side='left')

    def _init_image_settings(self):
        self.widget_settings = {}

        # pre processing
        self.pre_processing_options = {'None': None,
                                       'Resize 64': partial(IQM_Vis.utils.image_utils.resize_to_longest_side, side=64),
                                       'Resize 128': partial(IQM_Vis.utils.image_utils.resize_to_longest_side, side=128),
                                       'Resize 256': partial(IQM_Vis.utils.image_utils.resize_to_longest_side, side=256),
                                       'Resize 512': partial(IQM_Vis.utils.image_utils.resize_to_longest_side, side=512)}
        if not hasattr(self, 'pre_processing_option'):
            self.pre_processing_option = 'Resize 128'  # init_val

        for i, data_store in enumerate(self.data_stores):
            if hasattr(data_store, 'image_pre_processing'):
                if str(data_store.image_pre_processing) not in [str(f) for f in self.pre_processing_options.values()]:
                    name = f"Custom {i}"
                    self.pre_processing_options[name] = data_store.image_pre_processing
                    init_val = name
        combobox_pre = QComboBox()
        combobox_pre.addItems(list(self.pre_processing_options.keys()))
        combobox_pre.setCurrentText(self.pre_processing_option)
        combobox_pre.activated.connect(self.change_pre_processing)
        self.widget_settings['image_pre_processing'] = {'widget': combobox_pre, 'label': QLabel('Image Pre Processing:')}
        self.change_pre_processing()   # apply default

        # post processing
        self.post_processing_options = {'None': None,
                                        'Crop Centre': IQM_Vis.utils.image_utils.crop_centre}
        if not hasattr(self, 'post_processing_option'):
            self.post_processing_option = 'None'  # init_val
        for i, data_store in enumerate(self.data_stores):
            if hasattr(data_store, 'image_post_processing'):
                if data_store.image_post_processing not in list(self.post_processing_options.values()):
                    name = f"Custom {i}"
                    self.post_processing_options[name] = data_store.image_post_processing
                    init_val = name
        combobox_post = QComboBox()
        combobox_post.addItems(list(self.post_processing_options.keys()))
        combobox_post.setCurrentText(self.post_processing_option)
        combobox_post.activated.connect(self.change_post_processing)
        self.widget_settings['image_post_processing'] = {'widget': combobox_post, 'label': QLabel('Image Post Processing:')}
        self.change_post_processing()    # apply default

        # image display size
        line_edit_display = QLineEdit()
        line_edit_display.setValidator(QIntValidator())
        line_edit_display.setMaxLength(3)
        line_edit_display.setText(str(self.image_display_size))
        line_edit_display.textChanged.connect(self.change_display_im_size)
        self.widget_settings['image_display_size'] = {'widget': line_edit_display, 'label': QLabel('Image Display Size:')}

        # graph display size
        line_edit_graph = QLineEdit()
        line_edit_graph.setValidator(QIntValidator())
        line_edit_graph.setMaxLength(2)
        line_edit_graph.setText(str(self.graph_size))
        line_edit_graph.textChanged.connect(self.change_graph_size)
        self.widget_settings['graph_display_size'] = {'widget': line_edit_graph, 'label': QLabel('Graph Display Size:')}

        # graph/experiment number of steps in the range
        line_edit_num_steps = QLineEdit()
        line_edit_num_steps.setValidator(QIntValidator())
        line_edit_num_steps.setMaxLength(4)
        line_edit_num_steps.setText(str(self.num_steps_range))
        line_edit_num_steps.textChanged.connect(self.change_num_steps)
        self.widget_settings['graph_num_steps'] = {'widget': line_edit_num_steps, 'label': QLabel('Graph/Experiment Step Size:')}

        # image screen calibration
        line_edit_rgb = QLineEdit()
        line_edit_rgb.setValidator(QIntValidator())
        line_edit_rgb.setMaxLength(4)
        line_edit_rgb.setText(str(self.rgb_brightness))
        line_edit_rgb.textChanged.connect(self.change_display_im_rgb_brightness)
        self.widget_settings['image_display_rgb_brightness'] = {
            'widget': line_edit_rgb, 'label': QLabel('RGB Max Brightness:')}

        line_edit_display = QLineEdit()
        line_edit_display.setValidator(QIntValidator())
        line_edit_display.setMaxLength(4)
        line_edit_display.setText(str(self.display_brightness))
        line_edit_display.textChanged.connect(self.change_display_im_display_brightness)
        self.widget_settings['image_display_display_brightness'] = {
            'widget': line_edit_display, 'label': QLabel('Display Max Brightness:')}

        # update settings button
        self.widget_settings['update_button'] = QPushButton('Apply Settings', self)
        self.widget_settings['update_button'].clicked.connect(self.update_image_settings)

    '''
    ==================== functions to bind to sliders/widgets ====================
    '''
    # sliders value changes
    def generic_value_change(self, key, param_group):
        index = self.widget_controls['slider'][key]['data'].value()
        self.params_from_sliders[param_group][key] = self.sliders[param_group][key]['values'][index]
        self.display_slider_num(key, param_group) # display the new value ont UI

    def display_slider_num(self, key, param_group, disp_len=5):
        # display the updated value
        value_str = str(self.params_from_sliders[param_group][key])
        value_str = gui_utils.str_to_len(value_str, disp_len, '0', plus=True)
        self.widget_controls['slider'][key]['value'].setText(value_str)

    def reset_slider_group(self, param_group, redo_plots=False, display_images=True):
        for key, item_sliders in self.sliders[param_group].items():
            self.widget_controls['slider'][key]['data'].setValue(item_sliders['init_ind'])
        if display_images == True:
            self.display_images()
        if redo_plots == True:
            self.redo_plots()

    def reset_sliders(self):
        for param_group in self.sliders:
            self.reset_slider_group(param_group, False, False)
        self.display_images()
        self.redo_plots()

    def set_image_name_text(self):
        for i, data_store in enumerate(self.data_stores):
            self.widget_row[i]['images']['original']['label'].setText(data_store.get_reference_image_name())
            self.widget_row[i]['images']['transformed']['label'].setText(gui_utils.get_transformed_image_name(data_store))
            for metric_image in data_store.metric_images:
                if metric_image in self.checked_metric_images:
                    metric_name = gui_utils.get_metric_image_name(metric_image, data_store)
                    if len(metric_name) > 20:
                        metric_name = metric_image
                    self.widget_row[i]['metric_images'][metric_image]['label'].setText(metric_name)

    def change_plot_lims(self, state):
        if state == 2:  # 2 is the checked value
            self.plot_data_lim = self.data_lims['range_data']
        else:
            self.plot_data_lim = self.data_lims['fixed']
        self.redo_plots(calc_range=False)

    def change_pre_processing(self, *args):
        self.pre_processing_option = self.widget_settings['image_pre_processing']['widget'].currentText()
        for data_store in self.data_stores:
            if hasattr(data_store, 'image_pre_processing'):
                data_store.image_pre_processing = self.pre_processing_options[self.pre_processing_option]
        self.image_settings_update_plots = True

    def change_post_processing(self, *args):
        self.post_processing_option = self.widget_settings['image_post_processing']['widget'].currentText()
        for data_store in self.data_stores:
            if hasattr(data_store, 'image_post_processing'):
                data_store.image_post_processing = self.post_processing_options[self.post_processing_option]
        self.image_settings_update_plots = True
        # self.display_images()
        # self.redo_plots()

    def update_image_settings(self):
        ''' button to apply new image settings '''
        self.change_data(0)  # update the image data settings
        self.display_images()
        if hasattr(self, 'update_UI'):
            if self.update_UI == True:
                self.construct_UI()
        elif hasattr(self, 'image_settings_update_plots'):
            if self.image_settings_update_plots == True:
                # only redo the graphs if nessesary
                self.redo_plots()
        self.image_settings_update_plots = False
        self.update_UI = False

    def change_display_im_size(self, txt):
        if txt == '':
            txt = 1
        old_size = self.image_display_size
        self.image_display_size = max(1, int(txt))
        self.update_UI = True
        # self.construct_UI()
        # self.display_images()
        # if old_size > self.image_display_size:
        #     self.setMaximumSize(self.main_widget.sizeHint())
        # if old_size < self.image_display_size:
        #     self.setMinimumSize(self.main_widget.sizeHint())

    def change_graph_size(self, txt):
        if txt == '':
            txt = 1
        self.graph_size = max(1, int(txt))
        self.update_UI = True

    def change_num_steps(self, txt):
        if txt == '':
            txt = 1
        self.num_steps_range = max(2, int(txt))
        self.update_UI = True
    
    def change_display_im_rgb_brightness(self, txt):
        if txt == '':
            txt = 1
        self.rgb_brightness = max(1, int(txt))
    
    def change_display_im_display_brightness(self, txt):
        if txt == '':
            txt = 1
        self.display_brightness = max(1, int(txt))

    def update_progress(self, v):
        self.pbar.setValue(v)
        if v == 0:
            self.status_bar.showMessage('Done', 3000)

    def update_status_bar(self, v):
        self.status_bar.showMessage(v)

    def launch_experiment(self):
        self.experiment = IQM_Vis.UI.make_experiment(self.checked_transformations,
                                                     self.data_stores[0],
                                                     self.image_display_size,
                                                     self.rgb_brightness,
                                                     self.display_brightness,
                                                     self.default_save_dir,
                                                     self.num_steps_range)
        self.experiment.show()
        self.experiment.showFullScreen()
