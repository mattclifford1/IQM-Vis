import os

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QInputDialog, QLineEdit, QMenu, QFileDialog, QPushButton, QGridLayout, QLabel, QSlider, QComboBox, QCheckBox
from PyQt6.QtCore import Qt

# layout class
class app_layout(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_display_size = (175, 175)

    def init_style(self, css_file=None):
        if css_file == None:
            dir = os.path.dirname(os.path.abspath(__file__))
            css_file = os.path.join(dir, 'style.css')
        with open(css_file, 'r') as file:
            self.app.setStyleSheet(file.read())

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
                metric_name = key + str(im_pair)
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
