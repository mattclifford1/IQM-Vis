'''
create experiment window
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import random
import threading
import warnings
import time

import numpy as np
from PyQt6.QtWidgets import (QMainWindow,
                             QHBoxLayout,
                             QVBoxLayout,
                             QTabWidget,
                             QApplication,
                             QPushButton,
                             QLabel,
                             QMessageBox)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence

import IQM_Vis
from IQM_Vis.UI.custom_widgets import ClickLabel
from IQM_Vis.UI import utils
from IQM_Vis.utils import gui_utils, plot_utils, image_utils


class make_experiment(QMainWindow):
    def __init__(self, 
                 checked_transformations, 
                 data_store, 
                 image_display_size,
                 rgb_brightness,
                 display_brightness,
                 default_save_dir=IQM_Vis.utils.save_utils.DEFAULT_SAVE_DIR,
                 num_trans_values=6):
        super().__init__()
        self.checked_transformations = checked_transformations
        self.data_store = data_store
        self.image_display_size = image_display_size
        self.rgb_brightness = rgb_brightness
        self.display_brightness = display_brightness
        self.default_save_dir = default_save_dir
        self.num_trans_values = num_trans_values

        self.clicked_event = threading.Event()
        self.stop_event = threading.Event()
        self.saved = False
        self.quit_experiment = False
        self._init_experiment_window_widgets()
        self.get_all_images()
        self.experiment_layout()
        self.setCentralWidget(self.experiments_tab)
        self.setWindowTitle('Experiment')
        # move to centre of the screen
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.show_all_images()

    def closeEvent(self, event):
        # Ask for confirmation if not saved
        if not self.saved:
            answer = QMessageBox.question(self,
            "Confirm Exit...",
            "Are you sure you want to exit?\nAll unsaved data will be lost.",
            QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes, 
                                          QMessageBox.StandardButton.Yes)
        else:
            answer = QMessageBox.StandardButton.Yes

        event.ignore()
        if answer == QMessageBox.StandardButton.Yes:
            self.quit_experiment = True
            if hasattr(self, 'range_worker'):
                self.range_worker.stop()
            self.stop_event.set()
            self.clicked_event.set()
            event.accept()

    def quit(self):
        self.close()

    def show_all_images(self, tab='setup'):
        self.widget_experiments[tab]['images'].axes.axis('off')
        rows = int(len(self.experiment_transforms)**0.5)
        cols = int(np.ceil(len(self.experiment_transforms)/rows))
        for i, trans in enumerate(self.experiment_transforms):
            ax = self.widget_experiments[tab]['images'].figure.add_subplot(
                rows, cols, i+1)
            ax.imshow(image_utils.calibrate_brightness(
                trans['image'], self.rgb_brightness, self.display_brightness, ubyte=False))
            ax.axis('off')
            ax.set_title(make_name_for_trans(trans), fontsize=6)
        # self.widget_experiments[tab]['images'].figure.tight_layout()

        # time.sleep(5)
        # QApplication.processEvents()
            
    def get_all_images(self):
        ''' load all transformed images and sort them via MSE '''
        self.experiment_trans_params = plot_utils.get_all_single_transform_params(
            self.checked_transformations, num_steps=self.num_trans_values)

        # remove any params with value 0 
        self.experiment_trans_params = [
            x for x in self.experiment_trans_params if not x[list(x.keys())[0]] == 0]

        # save the experiment ordering before reordering (for saving to csv col ordering)
        self.original_params_order = []
        for single_trans in self.experiment_trans_params:
            trans_name = list(single_trans.keys())[0]
            param = single_trans[trans_name]
            data = {'transform_name': trans_name,
                    'transform_value': param}
            self.original_params_order.append(make_name_for_trans(data))

        self.ref_image = self.data_store.get_reference_image()
        # get MSE for experiments to get a rough sorting
        mses = []
        mse = IQM_Vis.IQMs.MSE()
        for trans in self.experiment_trans_params:
            mses.append(
                mse(self.ref_image, self.get_single_transform_im(trans)))
        # put median MSE at the end (best for quick sort)
        self.experiment_trans_params = sort_list(
            self.experiment_trans_params, mses)  # sort array
        # take median out and get random shuffle for the rest
        median = self.experiment_trans_params.pop(
            len(self.experiment_trans_params)//2)
        random.shuffle(self.experiment_trans_params)
        self.experiment_trans_params.append(median)
        # load all images
        self.experiment_transforms = []
        # save all data
        for single_trans in self.experiment_trans_params:
            trans_name = list(single_trans.keys())[0]
            param = single_trans[trans_name]
            img = self.get_single_transform_im(single_trans)
            data = {'transform_name': trans_name,
                    'transform_value': param,
                    'image': img}
            self.experiment_transforms.append(data)
        

    def _init_experiment_window_widgets(self):
        self.widget_experiments = {'exp': {}, 'preamble': {}, 'setup': {}, 'final':{}}
        ''' setup tab '''
        self.widget_experiments['setup']['start_button'] = QPushButton(
            'Setup', self)
        self.widget_experiments['setup']['start_button'].clicked.connect(self.setup_experiment)
        self.widget_experiments['setup']['quit_button'] = QPushButton('Quit', self)
        self.widget_experiments['setup']['quit_button'].clicked.connect(self.quit)
        QShortcut(QKeySequence("Ctrl+Q"),
                  self.widget_experiments['setup']['quit_button'], self.quit)
        self.widget_experiments['setup']['images'] = gui_utils.MplCanvas(size=None)
        self.widget_experiments['setup']['text'] = QLabel(self)
        self.widget_experiments['setup']['text'].setText(f'''
        Experiment to be setup with the above images using the settings:
            Save folder: {self.default_save_dir}
            Number of steps per transform: {self.num_trans_values}
            Image Display Size: {self.image_display_size}
            Image Calibration:
                Max RGB Brightness: {self.rgb_brightness}
                Max Display Brightness: {self.display_brightness}

        Click the Setup button to setup up the experiment and hand over to the test subject.
        ''')
        # self.widget_experiments['setup']['text'].setAlignment(
        #     Qt.AlignmentFlag.AlignCenter)

        ''' info tab '''
        self.widget_experiments['preamble']['text'] = QLabel(self)
        self.widget_experiments['preamble']['text'].setText('''
        For this experiment you will be shown a reference image and two similar images.

        You need to click on the image (A or B) which you believe to be most similar to the reference image.




        When you are ready, click the Start button to begin the experiment ''')
        self.running_experiment = False
        self.widget_experiments['preamble']['start_button'] = QPushButton('Start', self)
        self.widget_experiments['preamble']['start_button'].clicked.connect(self.toggle_experiment)

        self.widget_experiments['preamble']['quit_button'] = QPushButton('Quit', self)
        self.widget_experiments['preamble']['quit_button'].clicked.connect(
            self.quit)
        QShortcut(QKeySequence("Ctrl+Q"),
                  self.widget_experiments['preamble']['quit_button'], self.quit)

        ''' experiment tab '''
        for image in ['Reference', 'A', 'B']:
            self.widget_experiments['exp'][image] = {}
            self.widget_experiments['exp'][image]['data'] = ClickLabel(image)
            self.widget_experiments['exp'][image]['data'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            # image label
            self.widget_experiments['exp'][image]['label'] = QLabel(image, self)
            self.widget_experiments['exp'][image]['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widget_experiments['exp']['A']['data'].clicked.connect(self.clicked_image)
        self.widget_experiments['exp']['B']['data'].clicked.connect(self.clicked_image)
        self.widget_experiments['exp']['quit_button'] = QPushButton('Quit', self)
        self.widget_experiments['exp']['quit_button'].clicked.connect(self.quit)
        QShortcut(QKeySequence("Ctrl+Q"),
                  self.widget_experiments['exp']['quit_button'], self.quit)

        ''' finish tab '''
        self.widget_experiments['final']['order_text'] = QLabel(
            'Experiment Sorting Order:', self)
        self.widget_experiments['final']['images'] = gui_utils.MplCanvas(size=None)
        self.widget_experiments['final']['quit_button'] = QPushButton('Quit', self)
        self.widget_experiments['final']['quit_button'].clicked.connect(
            self.quit)
        QShortcut(QKeySequence("Ctrl+Q"),
                self.widget_experiments['final']['quit_button'], self.quit)
        self.widget_experiments['final']['save_label'] = QLabel('Warning: experiment couldnt save!', self)

    def experiment_layout(self):
        # setup 
        experiment_text = QVBoxLayout()
        experiment_text.addWidget(self.widget_experiments['setup']['text'])
        experiment_setup_buttons = QHBoxLayout()
        experiment_setup_buttons.addWidget(
            self.widget_experiments['setup']['start_button'])
        experiment_setup_buttons.addWidget(
            self.widget_experiments['setup']['quit_button'])
        experiment_text.addLayout(experiment_setup_buttons)

        experiment_mode_setup = QVBoxLayout()
        experiment_mode_setup.addWidget(self.widget_experiments['setup']['images'])
        experiment_mode_setup.addLayout(experiment_text)
        experiment_mode_setup.setAlignment(Qt.AlignmentFlag.AlignCenter)
        experiment_mode_setup.addStretch()


        # info
        experiment_info_buttons = QHBoxLayout()
        experiment_info_buttons.addWidget(
            self.widget_experiments['preamble']['start_button'])
        experiment_info_buttons.addWidget(
            self.widget_experiments['preamble']['quit_button'])

        experiment_mode_info = QVBoxLayout()
        experiment_mode_info.addWidget(
            self.widget_experiments['preamble']['text'])
        experiment_mode_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        experiment_mode_info.addLayout(experiment_info_buttons)

        # experiment
        reference = QVBoxLayout()
        for name, widget in self.widget_experiments['exp']['Reference'].items():
            reference.addWidget(widget)
        reference.setAlignment(Qt.AlignmentFlag.AlignBottom)
        A = QVBoxLayout()
        for name, widget in self.widget_experiments['exp']['A'].items():
            A.addWidget(widget)
        A.setAlignment(Qt.AlignmentFlag.AlignTop)
        B = QVBoxLayout()
        for name, widget in self.widget_experiments['exp']['B'].items():
            B.addWidget(widget)
        B.setAlignment(Qt.AlignmentFlag.AlignTop)

        distorted_images = QHBoxLayout()
        distorted_images.addLayout(A)
        distorted_images.addLayout(B)
        distorted_images.setAlignment(Qt.AlignmentFlag.AlignTop)

        experiment_mode_images = QVBoxLayout()
        experiment_mode_images.addLayout(reference)
        experiment_mode_images.addLayout(distorted_images)
        experiment_mode_images.setAlignment(Qt.AlignmentFlag.AlignCenter)

        run_experiment = QVBoxLayout()
        run_experiment.addLayout(experiment_mode_images)
        run_experiment.addWidget(self.widget_experiments['exp']['quit_button'])
        run_experiment.setAlignment(Qt.AlignmentFlag.AlignCenter)

        finish_experiment = QVBoxLayout()
        finish_experiment.addWidget(self.widget_experiments['final']['order_text'])
        finish_experiment.addWidget(self.widget_experiments['final']['images'])
        finish_experiment.addWidget(self.widget_experiments['final']['save_label'])
        finish_experiment.addWidget(self.widget_experiments['final']['quit_button'])
        finish_experiment.setAlignment(Qt.AlignmentFlag.AlignCenter)
        finish_experiment.addStretch()

        self.experiments_tab = QTabWidget()
        for tab_layout, tab_name in zip([experiment_mode_setup, experiment_mode_info, run_experiment, finish_experiment],
                                        ['setup', 'info', 'run', 'finish']):
            utils.add_layout_to_tab(self.experiments_tab, tab_layout, tab_name)
        # experiment_mode_layout = QVBoxLayout()
        # experiment_mode_layout.addWidget(self.experiments_tab)
        # return experiment_mode_layout

    ''' experiment running functions'''
    def setup_experiment(self):
        self.experiments_tab.setCurrentIndex(1)
        self.experiments_tab.setTabEnabled(0, False)
        self.experiments_tab.setTabEnabled(2, False)
        self.experiments_tab.setTabEnabled(3, False)

    def toggle_experiment(self):
        if self.running_experiment:
            self.reset_experiment()
            self.experiments_tab.setTabEnabled(0, True)
            self.experiments_tab.setTabEnabled(1, True)
            self.running_experiment = False
            # self.widget_experiments['preamble']['start_button'].setText('Start')

        else:
            self.experiments_tab.setTabEnabled(2, True)
            self.start_experiment()
            self.experiments_tab.setTabEnabled(0, False)
            self.experiments_tab.setTabEnabled(1, False)
            # self.widget_experiments['preamble']['start_button'].setText('Reset')
            self.running_experiment = True

    def reset_experiment(self):
        self.experiments_tab.setCurrentIndex(1)
        self.init_style('light')

    def start_experiment(self):
        self.init_style('dark')
        self.experiments_tab.setCurrentIndex(2)

        # Display reference image
        gui_utils.change_im(self.widget_experiments['exp']['Reference']['data'], self.ref_image,
                            resize=self.image_display_size, rgb_brightness=self.rgb_brightness, display_brightness=self.display_brightness)

        # get user sorting
        self.sorting_thread = threading.Thread(target=self.quick_sort)
        self.sorting_thread.start()
        # self.quick_sort(0, len(self.experiment_transforms)-1)

    def finish_experiment(self):
        self.experiments_tab.setTabEnabled(3, True)
        self.show_all_images(tab='final')
        self.init_style('light')
        self.experiments_tab.setCurrentIndex(3)
        self.experiments_tab.setTabEnabled(2, False)
        self.save_experiment()
        if self.saved == True:
            self.widget_experiments['final']['save_label'].setText(f'Saved to {self.default_save_dir}')

    def save_experiment(self):
        # get the current transform functions
        trans_funcs = {}
        for single_trans in self.experiment_trans_params:
            trans_name = list(single_trans.keys())[0]
            trans_funcs[trans_name] = self.checked_transformations[trans_name]['function']
        # make the experiment directory
        self.default_save_dir = os.path.join(
            self.default_save_dir, self.data_store.get_reference_image_name())
        # get a unique directory (same image with diff trans need a new dir)
        i = 1
        unique_dir_found = False
        new_dir = True
        while unique_dir_found == False:
            exp_save_dir = f'{self.default_save_dir}-experiment-{i}'
            if os.path.exists(exp_save_dir):
                # check if experiment is the same
                exp_trans_params = IQM_Vis.utils.save_utils.load_obj(
                    os.path.join(exp_save_dir, 'transforms', 'transform_params.pkl'))
                exp_trans_funcs = IQM_Vis.utils.save_utils.load_obj(
                    os.path.join(exp_save_dir, 'transforms', 'transform_functions.pkl'))
                if (exp_trans_params == self.original_params_order) and (trans_funcs == exp_trans_funcs):
                    self.default_save_dir = exp_save_dir
                    unique_dir_found = True
                    new_dir = False
                else:
                    i += 1
            else:
                self.default_save_dir = exp_save_dir
                unique_dir_found = True
        # make all the dirs and subdirs
        os.makedirs(self.default_save_dir, exist_ok=True)
        os.makedirs(os.path.join(self.default_save_dir, 'images'), exist_ok=True)
        os.makedirs(os.path.join(self.default_save_dir, 'transforms'), exist_ok=True)
        if new_dir == True:
            # save experiment images
            image_utils.save_image(
                self.ref_image, os.path.join(self.default_save_dir, f'original.png'))
            for trans in self.experiment_transforms:
                image_utils.save_image(
                    trans['image'], os.path.join(self.default_save_dir, 'images', f'{make_name_for_trans(trans)}.png'))
            # save the transformations
            IQM_Vis.utils.save_utils.save_obj(
                os.path.join(self.default_save_dir, 'transforms', 'transform_params.pkl'),
                self.original_params_order)
            IQM_Vis.utils.save_utils.save_obj(
                os.path.join(self.default_save_dir, 'transforms', 'transform_functions.pkl'),
                dict(sorted(trans_funcs.items())))
        # save the experiment results
        exp_order = []
        for trans in self.experiment_transforms:
            exp_order.append(make_name_for_trans(trans))
        IQM_Vis.utils.save_utils.save_experiment_results(
            self.original_params_order,
            exp_order,
            os.path.join(self.default_save_dir, f'{self.data_store.get_reference_image_name()}-results.csv'))
        self.saved = True


    ''' sorting algorithm resource: https://www.geeksforgeeks.org/quick-sort/'''
    def quick_sort(self):
        self._quick_sort(0, len(self.experiment_transforms)-1)
        if self.quit_experiment != True:
            self.finish_experiment()
            # for trans in self.experiment_transforms:
            #     print(trans['transform_name'], trans['transform_value'])

    def _quick_sort(self, low, high):
        if low < high:
            # Find pivot elements such that element smaller than pivot are on the
            # left and elements greater than pivot are on the right
            pi = self.partition(low, high)
            if self.stop_event.is_set():
                return
            # Recursive call on the left of pivot
            self._quick_sort(low, pi - 1)
            # Recursive call on the right of pivot
            self._quick_sort(pi + 1, high)

    def partition(self, low, high):
        ''' given an unsorted partition of the array between low and high, order
            elements lower than a given pivot point to the left and higher to the right'''
        # Choose the end element as pivot
        self.high = high
        self.low = low
        self.current_comparision = low
        self.pivot = self.experiment_transforms[self.high]
        # Pointer for greater element
        self.comp_pointer = low - 1
        # Traverse through all elements and compare each element with pivot (by user clicking)
        while True:
            self.change_experiment_images(A_trans=self.experiment_transforms[self.current_comparision],
            B_trans=self.pivot)
            # wait for image to be clicked
            self.clicked_event.clear()
            self.clicked_event.wait()
            if self.stop_event.is_set():
                return
            if self.less_than_pivot == True:
            # if self.experiment_transforms[self.current_comparision]['brightness'] <= self.pivot['brightness']:
                # If element smaller than pivot is found swap it with the greater element pointed by i
                self.comp_pointer += 1
                # Swapping element at i with element at j
                self.swap_inds(self.comp_pointer, self.current_comparision)
            self.current_comparision += 1
            if self.current_comparision == self.high:
                break
        # Swap the pivot element with the greater element specified by i
        self.swap_inds(self.comp_pointer+1, self.high)
        # Return the position from where partition is done
        return self.comp_pointer + 1

    def clicked_image(self, image_name, widget_name):
        trans_str = image_name[len(self.data_store.get_reference_image_name())+1:]
        if trans_str != make_name_for_trans(self.pivot): # lower value
            # If element smaller than pivot is found swap it with the greater element pointed by i
            self.less_than_pivot = True
        else:
            self.less_than_pivot = False
        # unlock the wait
        self.clicked_event.set()

    def swap_inds(self, i, j):
        (self.experiment_transforms[i], self.experiment_transforms[j]) = (self.experiment_transforms[j], self.experiment_transforms[i])

    def get_single_transform_im(self, single_trans_dict):
        trans_name = list(single_trans_dict)[0]
        return image_utils.get_transform_image(self.data_store,
                                        {trans_name: self.checked_transformations[trans_name]},
                                        single_trans_dict)

    def change_experiment_images(self, A_trans, B_trans):
        A = A_trans['image']
        B = B_trans['image']

        gui_utils.change_im(self.widget_experiments['exp']['A']['data'], A, resize=self.image_display_size,
                            rgb_brightness=self.rgb_brightness, display_brightness=self.display_brightness)
        self.widget_experiments['exp']['A']['data'].setObjectName(f'{self.data_store.get_reference_image_name()}-{make_name_for_trans(A_trans)}')
        gui_utils.change_im(self.widget_experiments['exp']['B']['data'], B, resize=self.image_display_size,
                            rgb_brightness=self.rgb_brightness, display_brightness=self.display_brightness)
        self.widget_experiments['exp']['B']['data'].setObjectName(f'{self.data_store.get_reference_image_name()}-{make_name_for_trans(B_trans)}')

    ''' UI '''
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


def sort_list(list1, list2):
    # sort list1 based on list2
    inds = np.argsort(list2)
    sorted_list1 = []
    for i in inds:
        sorted_list1.append(list1[i])
    return sorted_list1

def make_name_for_trans(trans):
    return f"{trans['transform_name']}::{trans['transform_value']}"