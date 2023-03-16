'''
UI create layout
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import warnings
from PyQt6.QtWidgets import (QWidget,
                             QMainWindow,
                             QGridLayout,
                             QHBoxLayout,
                             QVBoxLayout,
                             QStackedLayout,
                             QTabWidget,
                             QWidget)


# sub class used by IQM_Vis.main.make_app to initialise layout of the UI
# uses widgets from IQM_Vis.widgets.app_widgets
# class layout(QMainWindow):
class layout(QMainWindow):
    def __init__(self):
        super().__init__()

    def init_layout(self):
        '''
        place all the widgets in the window
        '''
        # sizes
        im_width = 10
        im_height = 4
        button = 1
        slider_width = 2
        check_box_width = 1
        # horizonal start values
        start_im = button
        start_controls = 0 # im_width*2+button

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
            graph_tabs = QTabWidget()
            # '''metrics graphs'''
            metric_bar = QVBoxLayout()
            metric_bar.addWidget(self.widget_row[i]['metrics']['info']['label'])
            metric_bar.addWidget(self.widget_row[i]['metrics']['info']['data'])
            add_layout_to_tab(graph_tabs, metric_bar, 'Metrics')
            if self.metrics_avg_graph:
                avg_graph = QVBoxLayout()
                avg_graph.addWidget(self.widget_row[i]['metrics']['avg']['label'])
                graph = QGridLayout()
                graph.addWidget(self.widget_row[i]['metrics']['avg']['data'], 0, 0, im_height, im_width)
                avg_graph.addLayout(graph)   # need for matplotlib? - test this...   (grid)
                add_layout_to_tab(graph_tabs, avg_graph, 'Radar')
            if self.metric_range_graph:
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
                add_layout_to_tab(graph_tabs, range_graph, 'Range')
            graph_layouts.addWidget(graph_tabs)
            graph_layouts.addStretch()

        '''dataset controls'''
        # prev/next buttons
        dataset_layout = QHBoxLayout()
        if self.dataset:
            dataset_layout.addWidget(self.widget_controls['label']['data'])
            dataset_layout.addWidget(self.widget_controls['button']['prev_data'])
            dataset_layout.addWidget(self.widget_controls['button']['next_data'])
        '''transform controls'''
        image_controls = QVBoxLayout()
        # transform sliders
        for key in self.sliders['transforms']:
            tran_layout = QHBoxLayout()
            tran_layout.addWidget(self.widget_controls['slider'][key]['label'])
            tran_layout.addWidget(self.widget_controls['slider'][key]['data'])
            tran_layout.addWidget(self.widget_controls['slider'][key]['value'])
            image_controls.addLayout(tran_layout)
            image_controls.addStretch()

        '''metric_param controls'''
        metric_controls = QVBoxLayout()
        for key in self.sliders['metric_params']:
            inner_metric_layout = QHBoxLayout()
            inner_metric_layout.addWidget(self.widget_controls['slider'][key]['label'])
            inner_metric_layout.addWidget(self.widget_controls['slider'][key]['data'])
            inner_metric_layout.addWidget(self.widget_controls['slider'][key]['value'])
            metric_controls.addLayout(inner_metric_layout)
        metric_controls.addStretch()

        ''' parameter controls tab'''
        slider_tabs = QTabWidget()
        for tab_layout, tab_name in zip([image_controls, metric_controls], ['transforms', 'metric params']):
            add_layout_to_tab(slider_tabs, tab_layout, tab_name)

        ''' reset sliders button'''
        # reset sliders button
        reset_button = QHBoxLayout()
        reset_button.addWidget(self.widget_controls['button']['reset_sliders'])
        reset_button.addStretch()

        '''re calc graphs button'''
        graph_button = QVBoxLayout()
        if self.metrics_avg_graph or self.metric_range_graph:
            graph_button.addWidget(self.widget_controls['button']['force_update'])
            graph_button.addWidget(self.widget_controls['check_box']['graph_limits'])
            graph_button.addStretch()

        ''' put the whole layout together '''
        image_left_side = QVBoxLayout()
        image_left_side.addLayout(image_layouts)
        image_left_side.addLayout(dataset_layout)
        image_left_side.addWidget(slider_tabs)
        image_left_side.addLayout(reset_button)
        image_middle = QVBoxLayout()
        image_middle.addLayout(metric_layouts)
        graph_right = QVBoxLayout()
        graph_right.addLayout(graph_layouts)
        graph_right.addLayout(graph_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(image_left_side)
        main_layout.addLayout(image_middle)
        main_layout.addLayout(graph_right)

        # main_layout.setColumnStretch(1, 1)
        # main_layout.setSpacing(0)
        # main_layout.setContentsMargins(0, 0, 0, 0)

        # self.setLayout(main_layout)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.show()

    def init_style(self, css_file=None):
        if css_file == None:
            dir = os.path.dirname(os.path.abspath(__file__))
            # css_file = os.path.join(dir, 'style-light.css')
            css_file = os.path.join(dir, 'style-light.css')
        if os.path.isfile(css_file):
            with open(css_file, 'r') as file:
                self.app.setStyleSheet(file.read())
        else:
            warnings.warn('Cannot load css style sheet - file not found')

def add_layout_to_tab(tab, layout, name):
    _tab = QWidget()   # QTabWidget only accepts widgets not layouts so need to use this as a workaround
    _tab.setLayout(layout)
    tab.addTab(_tab, name)
