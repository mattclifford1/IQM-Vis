'''
main entry point to initialise the UI
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

import os
import time
from functools import partial
from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog
import IQM_Vis
from IQM_Vis.UI import layout, widgets, images, ProgressBar

class make_app(widgets, layout, images):
    def __init__(self, app,
                 data_stores: list,
                 transformations: dict,
                 metrics_info_format='graph', # graph or text
                 metrics_avg_graph=False,
                 metric_range_graph=True,
                 metric_params: dict={},
                 image_display_size=300,
                 default_save_dir=IQM_Vis.utils.save_utils.DEFAULT_SAVE_DIR,
                 restrict_options=None,
                 num_steps_range=11,
                 num_step_experiment=6,
                 ):
        super().__init__()
        self.app = app
        self.data_stores = data_stores
        self.transformations = transformations
        self.num_steps_range = num_steps_range
        self.num_step_experiment = num_step_experiment

        self.metrics_info_format = metrics_info_format
        self.metrics_avg_graph = metrics_avg_graph
        self.metric_range_graph = metric_range_graph
        self.metric_params = metric_params
        self.default_save_dir = default_save_dir
        self.restrict_options = restrict_options

        self.data_lims = {'fixed': 1, 'range_data': 1}
        self.plot_data_lim = 1

        self.dataset = self._single_image_or_dataset()
        self.setWindowTitle('IQM-Vis')

        self.make_status_bar()
        self.make_menu()

        self.widget_settings = {}
        self.image_display_size = image_display_size
        self.graph_size = 35
        self.rgb_brightness = 250  # max candela/m2 of rbg image
        self.display_brightness = 250  # max candela/m2 of display

        self.human_experiment_cache = {}
        self.construct_UI()

    def make_menu(self):
        self.menu_bar = self.menuBar()

        # make file menu
        self.file_menu = self.menu_bar.addMenu('File')
        save_dir_action = self.file_menu.addAction('Set Save Folder')
        load_image_action = self.file_menu.addAction('Load New Image')
        load_images_action = self.file_menu.addAction('Load New Image Folder')
        load_human_action = self.file_menu.addAction('Load Human Scores')
        load_experiment = self.file_menu.addAction('Load Experiment')
        reload_action = self.file_menu.addAction('Redo Graphs')
        quit_action = self.file_menu.addAction('Quit')

        save_dir_action.setStatusTip('Choose a folder to save project/experiments')
        save_dir_action.triggered.connect(self.change_save_folder)

        load_image_action.setStatusTip('Choose an image to load')
        load_image_action.triggered.connect(self.load_new_single_image)
        load_images_action.setStatusTip('Choose a folder of images to load')
        load_images_action.triggered.connect(self.load_new_images_folder)

        load_human_action.setStatusTip('Choose a human scores from csv file')
        load_human_action.triggered.connect(self.load_human_experiment)

        load_experiment.setStatusTip('Load experiment setup for folder')
        load_experiment.triggered.connect(self.load_experiment_from_dir)

        reload_action.setShortcut('Ctrl+R')
        reload_action.setStatusTip('')
        # reload_action.triggered.connect(self.display_images)
        reload_action.triggered.connect(partial(self.redo_plots, True))

        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip('Exit application')
        quit_action.triggered.connect(self.quit)

        self.edit_menu = self.menu_bar.addMenu('Edit')
        load_transforms = self.edit_menu.addAction('Load All Transforms')
        load_metrics = self.edit_menu.addAction('Load All Metrics')
        load_metric_images = self.edit_menu.addAction('Load All Metric Images')

        load_transforms.triggered.connect(self.load_all_transforms)
        load_metrics.triggered.connect(self.load_all_metrics)
        load_metric_images.triggered.connect(self.load_all_metric_images)

        self.get_menu_checkboxes()

    def load_all_transforms(self):
        all_trans_iqm_vis = IQM_Vis.transformations.get_all_transforms()
        for trans, data in all_trans_iqm_vis.items():
            if trans not in self.transformations:
                self.transformations[trans] = data
        self._remake_menu()
        self.construct_UI()

    def load_all_metrics(self):
        if not hasattr(self.data_stores[0], 'add_metric'):
            return
        all_metrics_iqm_vis = IQM_Vis.metrics.get_all_metrics()
        for metric, data in all_metrics_iqm_vis.items():
            self.data_stores[0].add_metric(metric, data)
        self._remake_menu()
        self.construct_UI()

    def load_all_metric_images(self):
        if not hasattr(self.data_stores[0], 'add_metric_image'):
            return
        all_metric_images_iqm_vis = IQM_Vis.metrics.get_all_metric_images()
        for metric, data in all_metric_images_iqm_vis.items():
            self.data_stores[0].add_metric_image(metric, data)
        self._remake_menu()
        self.construct_UI()

    def quit(self):
        QApplication.instance().quit()

    def __del__(self):
        # garbage collection
        self.range_worker.stop()

    def closeEvent(self, event):
        # Ask for confirmation
        answer = QMessageBox.question(self,
        "Confirm Exit...",
        "Are you sure you want to exit?\nAll unsaved data will be lost.",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.Yes)

        event.ignore()
        if answer == QMessageBox.StandardButton.Yes:
            if hasattr(self, 'range_worker'):
                self.range_worker.stop()
            event.accept()

    def get_menu_checkboxes(self):
        ''' list all trans/metrics in the menu drop downs '''
        # transformations
        self.menu_options = {'transforms': {},
                             'metrics': {},
                             'metric_images': {}}
        set_checked_menu_from_iterable(self.menu_bar,
                                       self.transformations,
                                       'Transforms',
                                       self.menu_options['transforms'],
                                       self.construct_UI,
                                       self.restrict_options['transforms'])
        set_checked_menu_from_iterable(self.menu_bar,
                                       self.data_stores[0].metric_images,
                                       'Metric Images',
                                       self.menu_options['metric_images'],
                                       self.construct_UI,
                                       self.restrict_options['metric_images'])
        set_checked_menu_from_iterable(self.menu_bar,
                                       self.data_stores[0].metrics,
                                       'Metrics',
                                       self.menu_options['metrics'],
                                       self.construct_UI,
                                       self.restrict_options['metrics'])
    
    def _remake_menu(self):
        self.menu_bar.clear()
        self.make_menu()

    def make_status_bar(self):
        self.status_bar = self.statusBar()
        self.pbar = ProgressBar(self, minimum=0, maximum=100, textVisible=False,
                        objectName="GreenProgressBar")
        self.pbar.setValue(0)
        self.status_bar.addPermanentWidget(self.pbar)

    def construct_UI(self):
        if hasattr(self, 'range_worker'):
            self.range_worker.stop() # stop any calculations on the old UI
        # if hasattr(self, 'wait_until_safe_to_change_image'):
        #     self.wait_until_safe_to_change_image()
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

        ''' update these '''
        # get any current tabs showing so we can keep them showing on a remake
        tabs_index = {}
        if hasattr(self, 'tabs'):
            tabs_index['slider'] = self.tabs['slider'].currentIndex()
            tabs_index['graph'] = self.tabs['graph'].currentIndex()
        else:
            tabs_index['slider'] = 0
            tabs_index['graph'] = 1

        # reset any range/correlation calc cache
        self.metric_range_graph_num = 0
        self.metric_correlation_graph_num = 0
        self.reset_correlation_data()

        # init the UI widgets and layouts
        self.init_style()     # layout.py
        self.init_widgets()   # widgets.py
        self.change_data(0, _redo_plots=True)   # images.py
        self.init_layout()    # layout.py
        self.tabs['slider'].setCurrentIndex(tabs_index['slider'])
        self.tabs['graph'].setCurrentIndex(tabs_index['graph'])
        # self.experiments_tab.setCurrentIndex(experi_tabs_index)
        self.reset_sliders()  # widgets.py

        # self.setMinimumSize(self.main_widget.sizeHint())
        self.resize(self.main_widget.sizeHint())

    def reset_correlation_data(self):
        self.correlation_data = {}
        for i, _ in enumerate(self.data_stores):
            self.correlation_data[i] = {}

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
    
    def change_save_folder(self):
        ''' change the save folder we are using '''
        # get the file opener for the user
        if os.path.exists(self.default_save_dir):
            start_dir = self.default_save_dir
        else:
            start_dir = os.path.expanduser("~")
        try:
            dir = QFileDialog.getExistingDirectory(self,
                                                   'Choose Save folder',
                                                   start_dir)
        except:
            return

        if dir == '':
            return
        
        self.default_save_dir = dir
        self.status_bar.showMessage(f'Changed save dir to: {self.default_save_dir}', 8000)


def set_checked_menu_from_iterable(main_menu, iterable, name, action_store, connect_func, restrict_options=None):
    _menu = main_menu.addMenu(name)
    _menu.triggered.connect(connect_func)
    for i, trans in enumerate(iterable):
        action_store[trans] = _menu.addAction(trans)
        action_store[trans].setCheckable(True)
        if isinstance(restrict_options, int):
            if i  < restrict_options:
                action_store[trans].setChecked(True)
            else:
                action_store[trans].setChecked(False)
        else:
            action_store[trans].setChecked(True)
