'''
main entry point to initialise the UI
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from PyQt6.QtWidgets import QLabel, QApplication, QCheckBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
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

        self.data_lims = {'fixed': 1, 'range_data': 1}
        self.plot_data_lim = 1

        self.dataset = self._single_image_or_dataset()
        self.setWindowTitle('IQM-Vis')

        self.make_status_bar()
        self.make_menu()

        self.construct_UI()

    def make_menu(self):
        self.menu_bar = self.menuBar()

        # make file menu
        self.file_menu = self.menu_bar.addMenu('File')
        reload_action = self.file_menu.addAction('Redo Graphs')
        quit_action = self.file_menu.addAction('Quit')

        reload_action.setShortcut('Ctrl+R')
        reload_action.setStatusTip('')
        reload_action.triggered.connect(self.display_images)
        reload_action.triggered.connect(self.redo_plots)

        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip('Exit application')
        quit_action.triggered.connect(QApplication.instance().quit)

        self.get_menu_checkboxes()

    def get_menu_checkboxes(self):
        ''' list all trans/metrics in the menu drop downs '''
        # transformations
        self.menu_options = {'transforms': {}, 'metrics': {}, 'metric_images': {}}
        set_checked_menu_from_iterable(self.menu_bar,
                                       self.transformations,
                                       'Transforms',
                                       self.menu_options['transforms'],
                                       self.construct_UI)
        set_checked_menu_from_iterable(self.menu_bar,
                                       self.data_stores[0].metric_images,
                                       'Metric Images',
                                       self.menu_options['metric_images'],
                                       self.construct_UI)
        set_checked_menu_from_iterable(self.menu_bar,
                                       self.data_stores[0].metrics,
                                       'Metrics',
                                       self.menu_options['metrics'],
                                       self.construct_UI)


    def make_status_bar(self):
        self.status_bar = self.statusBar()
        self.pbar = ProgressBar(self, minimum=0, maximum=100, textVisible=False,
                        objectName="GreenProgressBar")
        self.pbar.setValue(0)
        self.status_bar.addPermanentWidget(self.pbar)

    def construct_UI(self):
        # get currently selected tranformations to use
        self.checked_transformations = {}
        for trans, item in self.transformations.items():
            if self.menu_options['transforms'][trans].isChecked():
                self.checked_transformations[trans] = item
        # get currently selected metrics to use
        self.checked_metrics = []
        for metric in self.data_stores[0].metrics:
            if self.menu_options['metrics'][metric].isChecked():
                self.checked_metrics.append(metric)
        # get currently selected metric_images to use
        self.checked_metric_images = []
        for metric_image in self.data_stores[0].metric_images:
            if self.menu_options['metric_images'][metric_image].isChecked():
                self.checked_metric_images.append(metric_image)


        self.init_style()     # layout.py
        self.init_widgets()   # widgets.py
        self.init_layout()    # layout.py
        self.display_images() # images.py
        self.reset_sliders()  # widgets.py

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


def set_checked_menu_from_iterable(main_menu, iterable, name, action_store, connect_func):
    _menu = main_menu.addMenu(name)
    _menu.triggered.connect(connect_func)
    for trans in iterable:
        action_store[trans] = _menu.addAction(trans)
        action_store[trans].setCheckable(True)
        action_store[trans].setChecked(True)
