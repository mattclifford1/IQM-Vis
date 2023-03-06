'''
UI create layout
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import warnings
from PyQt6.QtWidgets import QWidget, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout


# sub class used by IQM_VIS.main.make_app to initialise layout of the UI
# uses widgets from IQM_VIS.widgets.app_widgets
# class layout(QMainWindow):
class layout(QWidget):
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
        for i in self.widget_row:
            '''image and transformed image'''
            image_layout = QHBoxLayout()
            for image_name in self.widget_row[i]['images']:
                single_image = QVBoxLayout()
                single_image.addWidget(self.widget_row[i]['images'][image_name]['label'])
                single_image.addWidget(self.widget_row[i]['images'][image_name]['data'])
                image_layout.addLayout(single_image)
            '''metric images'''
            metric_layout = QHBoxLayout()
            for metric_name in self.widget_row[i]['metric_images']:
                single_metric = QVBoxLayout()
                single_metric.addWidget(self.widget_row[i]['metric_images'][metric_name]['label'])
                single_metric.addWidget(self.widget_row[i]['metric_images'][metric_name]['data'])
                metric_layout.addLayout(single_metric)
            '''metrics graphs'''
            single_metric = QVBoxLayout()
            single_metric.addWidget(self.widget_row[i]['metrics']['info']['label'])
            single_metric.addWidget(self.widget_row[i]['metrics']['info']['data'])
            metric_layout.addLayout(single_metric)
            '''graphs'''
            graph_layout = QHBoxLayout()
            if self.metrics_avg_graph:
                single_graph = QVBoxLayout()
                single_graph.addWidget(self.widget_row[i]['metrics']['avg']['label'])
                graph = QGridLayout()
                graph.addWidget(self.widget_row[i]['metrics']['avg']['data'], 0, 0, im_height, im_width)
                single_graph.addLayout(graph)
                single_graph.addStretch()
                graph_layout.addLayout(single_graph)
            if self.metric_range_graph:
                single_graph = QVBoxLayout()
                single_graph.addWidget(self.widget_row[i]['metrics']['range']['label'])
                graph = QGridLayout()
                graph.addWidget(self.widget_row[i]['metrics']['range']['data'], 0, 0, im_height, im_width)
                single_graph.addLayout(graph)
                '''graph controls'''
                graph_controls = QHBoxLayout()
                graph_controls.addWidget(self.widget_controls['button']['prev_metric_graph'])
                graph_controls.addWidget(self.widget_controls['button']['next_metric_graph'])
                single_graph.addLayout(graph_controls)
                single_graph.addStretch()
                graph_layout.addLayout(single_graph)

        '''image controls'''
        image_controls = QVBoxLayout()
        # prev/next buttons
        if self.dataset:
            dataset_layout = QHBoxLayout()
            dataset_layout.addWidget(self.widget_controls['label']['data'])
            dataset_layout.addWidget(self.widget_controls['button']['prev_data'])
            dataset_layout.addWidget(self.widget_controls['button']['next_data'])
            image_controls.addLayout(dataset_layout)
        # transform sliders
        for key in self.sliders['transforms']:
            tran_layout = QHBoxLayout()
            tran_layout.addWidget(self.widget_controls['slider'][key]['label'])
            tran_layout.addWidget(self.widget_controls['slider'][key]['data'])
            tran_layout.addWidget(self.widget_controls['slider'][key]['value'])
            image_controls.addLayout(tran_layout)
        # reset sliders button
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.widget_controls['button']['reset_sliders'])
        # calculate metric avg graph
        if self.metrics_avg_graph:
            button_layout.addWidget(self.widget_controls['button']['force_update'])
        image_controls.addLayout(button_layout)
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

        # now set sub layouts to the main layout and init it!
        # outerLayout = QHBoxLayout()
        # self.setLayout(outerLayout)

        # make main widget inside the QMainWindow
        main_layout = QGridLayout()
        # self.main_widget = QWidget()
        # self.main_widget.setLayout(main_layout)
        # self.setCentralWidget(self.main_widget)

        main_layout.addLayout(image_layout,  0, 0, 1, 1)
        main_layout.addLayout(metric_layout, 0, 1, 1, 1)
        main_layout.addLayout(graph_layout,  0, 2, 2, 1)

        main_layout.addLayout(image_controls, 1, 0, 1, 1)
        main_layout.addLayout(metric_controls, 1, 1, 1, 1)

        # main_layout.setColumnStretch(1, 1)
        # main_layout.setSpacing(0)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        self.show()

    def init_style(self, css_file=None):
        if css_file == None:
            dir = os.path.dirname(os.path.abspath(__file__))
            # css_file = os.path.join(dir, 'style.css')
            css_file = os.path.join(dir, 'style.py')  # should be css but work around to include file with  pypi
        if os.path.isfile(css_file):
            with open(css_file, 'r') as file:
                self.app.setStyleSheet(file.read())
        else:
            warnings.warn('Cannot load css style sheet - file not found')
