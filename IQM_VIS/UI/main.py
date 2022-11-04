'''
main entry point to initialise the UI
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

import sys
import os

import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QInputDialog, QLineEdit, QMenu, QFileDialog, QPushButton, QGridLayout, QLabel, QSlider, QComboBox, QCheckBox
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure

from IQM_VIS.utils import gui_utils, plot_utils
from IQM_VIS.UI.layout import app_layout
from IQM_VIS.UI.widgets import app_widgets
from IQM_VIS.UI.metrics import app_metrics
from IQM_VIS.UI.images import app_images

class make_app(app_widgets, app_layout, app_metrics, app_images):
    def __init__(self, app,
                data_stores: list,
                transformations: dict,
                metrics_info_format='graph',    # graph or text
                metrics_avg_graph=False
                ):
        super().__init__()
        self.app = app
        self.data_stores = data_stores
        self.transformations = transformations
        self.metrics_info_format = metrics_info_format
        self.metrics_avg_graph = metrics_avg_graph

        self.init_style()                  # app_layout
        # self.init_images()               #
        self.init_widgets()                # app_widgets
        self.init_layout()                 # app_layout

        self.display_images()              # app_images
        self.reset_sliders()               # app_widgets
