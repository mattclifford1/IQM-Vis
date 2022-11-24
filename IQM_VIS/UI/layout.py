'''
UI create layout
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import warnings
from PyQt6.QtWidgets import QWidget, QMainWindow, QGridLayout


# sub class used by IQM_VIS.main.make_app to initialise layout of the UI
# uses widgets from IQM_VIS.widgets.app_widgets
class layout(QMainWindow):
    def __init__(self):
        super().__init__()

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
        start_controls = 0 # im_width*2+button

        '''image rows displaying image, metric graphs and metric images'''
        im_row = 0
        for i in self.widget_row.keys():
            col = 0
            '''image and transformed image'''
            for image_name in self.widget_row[i]['images'].keys():
                self.layout.addWidget(self.widget_row[i]['images'][image_name]['label'], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
                self.layout.addWidget(self.widget_row[i]['images'][image_name]['data'], start_im+im_row*(im_height+button), (im_height+button)*col,   im_height, im_width)
                col += 1
            '''metric images'''
            for metric_name in self.widget_row[i]['metric_images'].keys():
                self.layout.addWidget(self.widget_row[i]['metric_images'][metric_name]['label'], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
                self.layout.addWidget(self.widget_row[i]['metric_images'][metric_name]['data'], start_im+im_row*(im_height+button), (im_height+button)*col, im_height, im_width)
                col += 1
            '''metrics graphs'''
            self.layout.addWidget(self.widget_row[i]['metrics']['info']['label'] , start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
            self.layout.addWidget(self.widget_row[i]['metrics']['info']['data'] , start_im+im_row*(im_height+button), (im_height+button)*col+button, im_height, im_width)
            col += 1
            if self.metrics_avg_graph:
                self.layout.addWidget(self.widget_row[i]['metrics']['avg']['label'], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
                self.layout.addWidget(self.widget_row[i]['metrics']['avg']['data'], start_im+im_row*(im_height+button), (im_height+button)*col, im_height, im_width)
                col += 1
            if self.metric_range_graph:
                self.layout.addWidget(self.widget_row[i]['metrics']['range']['label'], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
                self.layout.addWidget(self.widget_row[i]['metrics']['range']['data'], start_im+im_row*(im_height+button), (im_height+button)*col, im_height, im_width)
                metrics_range_col = col
                col += 1

            im_row += 1


        '''bottom of the UI showing the image transform sliders'''
        end_of_ims_row = (im_height+button)*im_row+button+start_im
        i = end_of_ims_row
        # prev/next buttons
        if self.metric_range_graph:
            self.layout.addWidget(self.widget_sliders['button']['prev_metric_graph'], button*i, (im_height+button)*metrics_range_col,               button, (im_height/2))
            self.layout.addWidget(self.widget_sliders['button']['next_metric_graph'], button*i, (im_height+button)*metrics_range_col+(im_height/2), button, (im_height/2))
        if self.dataset:
            start = 0
            self.layout.addWidget(self.widget_sliders['label']['data'],       button*i, start,                      button, button)
            self.layout.addWidget(self.widget_sliders['button']['prev_data'], button*i, start+button,               button, button)
            self.layout.addWidget(self.widget_sliders['button']['next_data'], button*i, start+button*2, button, button)
            i += 1
        # transform sliders
        for key in self.sliders.keys():
            self.layout.addWidget(self.widget_sliders['slider'][key]['label'], button*i, start_controls,                     button, button)
            self.layout.addWidget(self.widget_sliders['slider'][key]['data'],  button*i, start_controls+button,              button, slider_width)
            self.layout.addWidget(self.widget_sliders['slider'][key]['value'], button*i, start_controls+button+slider_width, button, button)
            i += 1

        # reset sliders button
        self.layout.addWidget(self.widget_sliders['button']['reset_sliders'], button*i, start_controls, button, button)
        # calculate metric avg graph
        if self.metrics_avg_graph:
            self.layout.addWidget(self.widget_sliders['button']['force_update'], button*i, start_controls+button, button, button)

        i += 1

        # init it!
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
