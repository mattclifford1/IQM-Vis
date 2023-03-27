'''
create experiment window
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os

import numpy as np
from PyQt6.QtWidgets import QPushButton, QLabel, QSlider, QCheckBox, QComboBox, QLineEdit, QMessageBox
from PyQt6.QtWidgets import (QWidget,
                             QMainWindow,
                             QGridLayout,
                             QHBoxLayout,
                             QVBoxLayout,
                             QStackedLayout,
                             QTabWidget,
                             QWidget,
                             QApplication)

from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt

import IQM_Vis
from IQM_Vis.UI.custom_widgets import ClickLabel
from IQM_Vis.UI import utils
from IQM_Vis.utils import gui_utils, plot_utils, image_utils


class make_experiment(QMainWindow):
    def __init__(self, checked_transformations, data_store, image_display_size):
        super().__init__()
        self.checked_transformations = checked_transformations
        self.data_store = data_store
        self.image_display_size = image_display_size
        self._init_experiment_window_widgets()
        self.experiment_layout()
        self.setCentralWidget(self.experiments_tab)

    def closeEvent(self, event):
        # Ask for confirmation
        answer = QMessageBox.question(self,
        "Confirm Exit...",
        "Are you sure you want to exit?\nAll unsaved data will be lost.",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        event.ignore()
        if answer == QMessageBox.StandardButton.Yes:
            if hasattr(self, 'range_worker'):
                self.range_worker.stop()
            event.accept()

    def quit(self):
        self.close()

    def _init_experiment_window_widgets(self):
        self.widget_experiments = {'exp': {}, 'preamble': {}}
        ''' pre experiments screen '''
        self.widget_experiments['preamble']['text'] = QLabel(self)
        self.widget_experiments['preamble']['text'].setText(''' For this experiment you will be shown a reference image and two similar images.

        You need to click on the image (A or B) which you believe to be most similar to the reference image.


        When you are ready, click the Start button to begin the experiment ''')
        self.widget_experiments['preamble']['start_button'] = QPushButton('Start', self)
        self.running_experiment = False
        self.widget_experiments['preamble']['start_button'].clicked.connect(self.toggle_experiment)

        self.widget_experiments['exp']['quit_button'] = QPushButton('Quit', self)
        self.widget_experiments['exp']['quit_button'].clicked.connect(self.quit)

        ''' images '''
        for image in ['Reference', 'A', 'B']:
            self.widget_experiments['exp'][image] = {}
            self.widget_experiments['exp'][image]['data'] = ClickLabel(image)
            self.widget_experiments['exp'][image]['data'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            # image label
            self.widget_experiments['exp'][image]['label'] = QLabel(image, self)
            self.widget_experiments['exp'][image]['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widget_experiments['exp']['A']['data'].clicked.connect(self.clicked_image)
        self.widget_experiments['exp']['B']['data'].clicked.connect(self.clicked_image)

    def toggle_experiment(self):
        if self.running_experiment:
            self.reset_experiment()
            self.experiments_tab.setTabEnabled(0, True)
            self.running_experiment = False
            self.widget_experiments['preamble']['start_button'].setText('Start')

        else:
            self.start_experiment()
            self.experiments_tab.setTabEnabled(0, False)
            self.widget_experiments['preamble']['start_button'].setText('Reset')
            self.running_experiment = True

    def reset_experiment(self):
        self.init_style('light')

    def start_experiment(self):
        self.init_style('dark')
        self.experiments_tab.setCurrentIndex(1)
        self.experiment_transforms = plot_utils.get_all_single_transform_params(self.checked_transformations)


        ''' quick proto type to display some images '''
        ref = self.data_store.get_reference_image()
        gui_utils.change_im(self.widget_experiments['exp']['Reference']['data'], ref, resize=self.image_display_size)
        self.exp_im_ind = {'A': 0, 'B': len(self.experiment_transforms)//2}
        self.change_experiment_images(A_ind=self.exp_im_ind['A'], B_ind=self.exp_im_ind['B'])

    def change_experiment_images(self, A_ind, B_ind):
        A_trans = list(self.experiment_transforms[A_ind])[0]
        A = image_utils.get_transform_image(self.data_store,
                                             {A_trans: self.checked_transformations[A_trans]},
                                             self.experiment_transforms[A_ind])
        B_trans = list(self.experiment_transforms[B_ind])[0]
        B = image_utils.get_transform_image(self.data_store,
                                             {B_trans: self.checked_transformations[B_trans]},
                                             self.experiment_transforms[B_ind])

        gui_utils.change_im(self.widget_experiments['exp']['A']['data'], A, resize=self.image_display_size)
        self.widget_experiments['exp']['A']['data'].setObjectName(f'{self.data_store.get_reference_image_name()}-{self.experiment_transforms[A_ind]}')
        gui_utils.change_im(self.widget_experiments['exp']['B']['data'], B, resize=self.image_display_size)
        self.widget_experiments['exp']['B']['data'].setObjectName(f'{self.data_store.get_reference_image_name()}-{self.experiment_transforms[B_ind]}')

    def clicked_image(self, image_name, widget_name):
        print(f'clicked {widget_name}, name: {image_name}')
        self.exp_im_ind[widget_name] += 1
        if self.exp_im_ind[widget_name] == len(self.experiment_transforms):
            self.exp_im_ind[widget_name] -= 1
        self.change_experiment_images(A_ind=self.exp_im_ind['A'], B_ind=self.exp_im_ind['B'])

    def init_style(self, style='light', css_file=None):
        if css_file == None:
            dir = os.path.dirname(os.path.abspath(__file__))
            # css_file = os.path.join(dir, 'style-light.css')
            css_file = os.path.join(dir, f'style-{style}.css')
        if os.path.isfile(css_file):
            with open(css_file, 'r') as file:
                self.setStyleSheet(file.read())
        else:
            warnings.warn('Cannot load css style sheet - file not found')

    def experiment_layout(self):

        experiment_mode_info = QVBoxLayout()
        experiment_mode_info.addWidget(self.widget_experiments['preamble']['text'])
        experiment_mode_info.addWidget(self.widget_experiments['preamble']['start_button'])

        reference = QVBoxLayout()
        for name, widget in self.widget_experiments['exp']['Reference'].items():
            reference.addWidget(widget)
        A = QVBoxLayout()
        for name, widget in self.widget_experiments['exp']['A'].items():
            A.addWidget(widget)
        B = QVBoxLayout()
        for name, widget in self.widget_experiments['exp']['B'].items():
            B.addWidget(widget)

        distorted_images = QHBoxLayout()
        distorted_images.addLayout(A)
        distorted_images.addLayout(B)

        experiment_mode_images = QVBoxLayout()
        experiment_mode_images.addLayout(reference)
        experiment_mode_images.addLayout(distorted_images)

        all_experiment = QVBoxLayout()
        all_experiment.addLayout(experiment_mode_images)
        all_experiment.addWidget(self.widget_experiments['exp']['quit_button'])


        self.experiments_tab = QTabWidget()
        for tab_layout, tab_name in zip([experiment_mode_info, all_experiment],
                                        ['info', 'run']):
            utils.add_layout_to_tab(self.experiments_tab, tab_layout, tab_name)
        # experiment_mode_layout = QVBoxLayout()
        # experiment_mode_layout.addWidget(self.experiments_tab)
        # return experiment_mode_layout
