'''
UI create layout
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import warnings
from PyQt6.QtWidgets import (QMainWindow,
                             QGridLayout,
                             QHBoxLayout,
                             QVBoxLayout,
                             QTabWidget,
                             QWidget)
from IQM_Vis.UI import utils

# sub class used by IQM_Vis.main.make_app to initialise layout of the UI
# uses widgets from IQM_Vis.widgets.app_widgets
# class layout(QMainWindow):
class layout(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__()

    def init_layout(self):
        self.tabs = {}
        self._init_generic_layout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.show()

    def _init_generic_layout(self):
        '''
        place all the widgets in the window
        '''
        # sizes
        im_width = 10
        im_height = 4
        # save window tabs to self
        self.tabs = {}

        '''image rows displaying image, metric graphs and metric images'''
        image_layouts = QVBoxLayout()
        metric_layouts = QVBoxLayout()
        graph_layouts = QVBoxLayout()
        for i in self.widget_row:
            '''image and transformed image'''
            image_layout = QHBoxLayout()
            for image_name in self.widget_row[i]['images']:
                single_image = QVBoxLayout()
                single_image.addWidget(self.widget_row[i]['images'][image_name]['label'])
                single_image.addWidget(self.widget_row[i]['images'][image_name]['data'])
                image_layout.addLayout(single_image)
            image_layouts.addLayout(image_layout)
            image_layouts.addStretch()
            '''metric images'''
            metric_layout = QHBoxLayout()
            for metric_name in self.widget_row[i]['metric_images']:
                single_metric = QVBoxLayout()
                single_metric.addWidget(self.widget_row[i]['metric_images'][metric_name]['label'])
                single_metric.addWidget(self.widget_row[i]['metric_images'][metric_name]['data'])
                single_metric.addStretch()
                metric_layout.addLayout(single_metric)
                metric_layout.addStretch()
            metric_layouts.addLayout(metric_layout)
            metric_layouts.addStretch()

            '''graphs'''
            self.tabs['graph'] = QTabWidget()
            # '''metrics graphs'''
            metric_bar = QVBoxLayout()
            metric_bar.addWidget(self.widget_row[i]['metrics']['info']['label'])
            metric_bar.addWidget(self.widget_row[i]['metrics']['info']['data'])
            utils.add_layout_to_tab(self.tabs['graph'], metric_bar, 'Metrics')
            if 'avg' in self.widget_row[i]['metrics'].keys():
                avg_graph = QVBoxLayout()
                avg_graph.addWidget(self.widget_row[i]['metrics']['avg']['label'])
                graph = QGridLayout()
                graph.addWidget(self.widget_row[i]['metrics']['avg']['data'], 0, 0, im_height, im_width)
                avg_graph.addLayout(graph)   # need for matplotlib? - test this...   (grid)
                utils.add_layout_to_tab(self.tabs['graph'], avg_graph, 'Radar')
            if 'range' in self.widget_row[i]['metrics'].keys():
                range_graph = QVBoxLayout()
                range_graph.addWidget(self.widget_row[i]['metrics']['range']['label'])
                graph = QGridLayout()
                graph.addWidget(self.widget_row[i]['metrics']['range']['data'], 0, 0, im_height, im_width)
                range_graph.addLayout(graph)  # need for matplotlib? - test this...    (grid)
                '''graph controls''' # will add to last one since there is one widget to control all
                graph_controls = QHBoxLayout()
                graph_controls.addWidget(self.widget_controls['button']['prev_metric_graph'])
                graph_controls.addWidget(self.widget_controls['button']['next_metric_graph'])
                range_graph.addLayout(graph_controls)
                utils.add_layout_to_tab(self.tabs['graph'], range_graph, 'Range')
            if 'correlation' in self.widget_row[i]['metrics'].keys():
                correlation_graph = QVBoxLayout()
                correlation_graph.addWidget(self.widget_row[i]['metrics']['correlation']['label'])
                graph = QGridLayout()
                graph.addWidget(self.widget_row[i]['metrics']['correlation']['data'], 0, 0, im_height, im_width)
                correlation_graph.addLayout(graph)  # need for matplotlib? - test this...    (grid)
                '''graph controls''' # will add to last one since there is one widget to control all
                graph_controls = QHBoxLayout()
                graph_controls.addWidget(self.widget_controls['button']['prev_correlation_graph'])
                graph_controls.addWidget(self.widget_controls['button']['next_correlation_graph'])
                correlation_graph.addLayout(graph_controls)
                '''load experiment'''
                correlation_graph.addWidget(self.widget_controls['button']['load_exp'])
                utils.add_layout_to_tab(self.tabs['graph'], correlation_graph, 'Correlation')
            graph_layouts.addWidget(self.tabs['graph'])
            graph_layouts.addStretch()

        '''dataset controls'''
        # prev/next buttons
        dataset_layout = QHBoxLayout()
        if self.dataset:
            dataset_layout.addWidget(self.widget_controls['label']['data'])
            dataset_layout.addWidget(self.widget_controls['button']['prev_data'])
            dataset_layout.addWidget(self.widget_controls['button']['next_data'])
            dataset_layout.addWidget(self.widget_controls['label']['data_num'])

        '''transform controls'''
        image_controls = QVBoxLayout()
        # transform sliders
        for key in self.sliders['transforms']:
            tran_layout_top = QHBoxLayout()
            tran_layout_top.addWidget(self.widget_controls['slider'][key]['label'])
            tran_layout_top.addWidget(self.widget_controls['slider'][key]['value'])
            tran_layout_bottom = QHBoxLayout()
            tran_layout_bottom.addWidget(self.sliders['transforms'][key]['min_edit'])
            tran_layout_bottom.addWidget(self.widget_controls['slider'][key]['data'])
            tran_layout_bottom.addWidget(self.sliders['transforms'][key]['max_edit'])
            trans_layout = QVBoxLayout()
            trans_layout.addLayout(tran_layout_top)
            trans_layout.addLayout(tran_layout_bottom)

            image_controls.addLayout(trans_layout)
            image_controls.addStretch()
        reset_button = QHBoxLayout()
        reset_button.addWidget(self.widget_controls['button']['transforms']['reset_sliders'])
        reset_button.addStretch()
        image_controls.addLayout(reset_button)

        '''metric_param controls'''
        metric_controls = QVBoxLayout()
        for key in self.sliders['metric_params']:
            inner_metric_layout = QHBoxLayout()
            inner_metric_layout.addWidget(self.widget_controls['slider'][key]['label'])
            inner_metric_layout.addWidget(self.widget_controls['slider'][key]['data'])
            inner_metric_layout.addWidget(self.widget_controls['slider'][key]['value'])
            metric_controls.addLayout(inner_metric_layout)
        reset_button = QHBoxLayout()
        reset_button.addWidget(self.widget_controls['button']['metric_params']['reset_sliders'])
        reset_button.addStretch()

        metric_controls.addLayout(reset_button)
        metric_controls.addStretch()

        '''settings controls'''
        settings_controls = QVBoxLayout()
        for key, item in self.widget_settings.items():
            inner_layout = QHBoxLayout()
            if isinstance(item, dict):
                inner_layout.addWidget(item['label'])
                inner_layout.addWidget(item['widget'])
            else:
                inner_layout.addWidget(item)
            inner_layout.addStretch()
            settings_controls.addLayout(inner_layout)
        settings_controls.addStretch()

        ''' experiment controls'''
        experiment_controls = QVBoxLayout()
        # tranformations
        for trans_name in self.widget_experiment_params:
            experiment_trans = QHBoxLayout()
            for _, widget in self.widget_experiment_params[trans_name].items():
                experiment_trans.addWidget(widget)
                experiment_trans.addStretch()
            experiment_controls.addLayout(experiment_trans)
        experiment_controls.addStretch()
        # run experiment button
        experiment_button = QHBoxLayout()
        experiment_button.addWidget(self.widget_controls['button']['launch_exp'])
        experiment_button.addStretch()
        experiment_controls.addLayout(experiment_button)

        ''' add to parameter controls tab'''
        self.tabs['slider'] = QTabWidget()
        for tab_layout, tab_name in zip([image_controls, metric_controls, settings_controls, experiment_controls],
                                        ['transforms', 'metric params', 'image settings', 'experiment']):
            utils.add_layout_to_tab(self.tabs['slider'], tab_layout, tab_name)

        '''re calc graphs button'''
        graph_button = QVBoxLayout()
        if (self.metrics_avg_graph or self.metric_range_graph):
            graph_button.addWidget(self.widget_controls['button']['force_update'])
            graph_button.addWidget(self.widget_controls['check_box']['graph_limits'])
            graph_button.addStretch()

        ''' put the whole layout together '''
        image_left_side = QVBoxLayout()
        image_left_side.addLayout(image_layouts)
        image_left_side.addLayout(dataset_layout)
        image_middle = QVBoxLayout()
        image_middle.addLayout(metric_layouts)

        all_images = QHBoxLayout()
        all_images.addLayout(image_left_side)
        all_images.addLayout(image_middle)

        controls = QVBoxLayout()
        controls.addWidget(self.tabs['slider'])

        images_plus_controls = QVBoxLayout()
        images_plus_controls.addLayout(all_images)
        images_plus_controls.addLayout(controls)

        graph_right = QVBoxLayout()
        graph_right.addLayout(graph_layouts)
        graph_right.addLayout(graph_button)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(images_plus_controls)
        self.main_layout.addLayout(graph_right)

        # self.main_layout.setColumnStretch(1, 1)
        # self.main_layout.setSpacing(0)
        # self.main_layout.setContentsMargins(0, 0, 0, 0)

    def init_style(self, style='light', css_file=None):
        if css_file == None:
            dir = os.path.dirname(os.path.abspath(__file__))
            # css_file = os.path.join(dir, 'style-light.css')
            css_file = os.path.join(dir, f'style-{style}.css')
        if os.path.isfile(css_file):
            with open(css_file, 'r') as file:
                self.app.setStyleSheet(file.read())
        else:
            warnings.warn('Cannot load css style sheet - file not found')
