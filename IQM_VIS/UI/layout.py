'''
UI create layout
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os

from PyQt6.QtWidgets import QWidget, QMainWindow, QGridLayout

# layout class
class app_layout(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_display_size = (175, 175)

    def get_layout_defininition(self):
        '''define layout of the UI
        change in here to make the appearance of the UI widgets different
        --> widgets groups must be present in app_widgets'''
        ### tODO: make this layout work to be more generalisable!!!

        # self.layout_def = {self.im_pair_names:['label', 'label',
        #                    self.sliders.keys(): 'a'}

    def init_layout(self):
        '''
        place all the widgets in the window
        '''
        self.get_layout_defininition() # define the structure of the layout
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
                metric_name = key + str(im_pair)
                self.layout.addWidget(self.widgets['label'][metric_name], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
                self.layout.addWidget(self.widgets['image'][metric_name], start_im+im_row*(im_height+button), (im_height+button)*col, im_height, im_width)
                col += 1
            # metircs info
            self.layout.addWidget(self.widgets['label'][str(im_pair)+'_metrics'], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
            self.layout.addWidget(self.widgets['label'][str(im_pair)+'_metrics_info'], start_im+im_row*(im_height+button), (im_height+button)*col+button, im_height, im_width)
            col += 1
            if self.metrics_avg_graph:
                self.layout.addWidget(self.widgets['label'][str(im_pair)+'_metrics_graph'], start_im-1+im_row*(im_height+button), (im_height+button)*col, button, im_width)
                self.layout.addWidget(self.widgets['graph'][str(im_pair)+'_metrics'], start_im+im_row*(im_height+button), (im_height+button)*col, im_height, im_width)
                col += 1
            im_row += 1


        # sliders
        i = (im_height+button)*im_row+button+start_im
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

    def init_style(self, css_file=None):
        if css_file == None:
            dir = os.path.dirname(os.path.abspath(__file__))
            css_file = os.path.join(dir, 'style.css')
        with open(css_file, 'r') as file:
            self.app.setStyleSheet(file.read())
