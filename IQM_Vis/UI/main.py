'''
main entry point to initialise the UI
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtGui import QIcon, QAction
from IQM_Vis.UI import layout, widgets, images, ProgressBar

class make_app(widgets, layout, images):
    def __init__(self, app,
                data_stores: list,
                transformations: dict,
                metrics_info_format='graph',    # graph or text
                metrics_avg_graph=False,
                metric_range_graph=True,
                metric_params: dict={},
                image_display_size=150):
        super().__init__()
        self.app = app
        self.data_stores = data_stores
        self.transformations = transformations
        self.metrics_info_format = metrics_info_format
        self.metrics_avg_graph = metrics_avg_graph
        self.metric_range_graph = metric_range_graph
        self.image_display_size = image_display_size
        self.metric_params = metric_params

        self.dataset = self._single_image_or_dataset()
        self.setWindowTitle('IQM-Vis')

        self.make_status_bar()
        self.make_menu()

        self.init_style()     # layout
        self.init_widgets()   # widgets
        self.init_layout()    # layout
        self.display_images() # images
        self.reset_sliders()  # widgets

    def make_menu(self):
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu('&File')

        quit_action = QAction(QIcon(), '&Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip('Exit application')
        quit_action.triggered.connect(QApplication.instance().quit)

        reload_action = QAction(QIcon(), '&Redo Graphs', self)
        reload_action.setShortcut('Ctrl+R')
        reload_action.setStatusTip('')
        reload_action.triggered.connect(self.display_images)
        reload_action.triggered.connect(self.redo_plots)

        self.file_menu.addAction(reload_action)
        self.file_menu.addAction(quit_action)

    def make_status_bar(self):
        self.status_bar = self.statusBar()
        self.pbar = ProgressBar(self, minimum=0, maximum=100, textVisible=False,
                        objectName="GreenProgressBar")
        self.pbar.setValue(0)
        self.status_bar.addPermanentWidget(self.pbar)

    def _single_image_or_dataset(self):
        '''set whether dataset or single image used for data_store'''
        for data_store in self.data_stores:
            try:
                data_store[1]
                dataset_found = True
                self.data_num = 0
                data_store[self.data_num]  # return to initial image
            except:
                return False

        # calc what is the last data point in all the datasets
        max_length = 0
        for data_store in self.data_stores:
            try:
                length = len(data_store)
                if length > max_length:
                    max_length = length
            except:
                obj_name = data_store.__class__.__name__
                raise AttributeError(f'{obj_name} needs to have __len__ attribute to be a dataset')
        self.max_data_ind = max_length - 1
        return dataset_found
