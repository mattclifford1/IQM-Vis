'''
create experiment window JND
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
from __future__ import annotations

import os
import random
import threading
import warnings
import time
from functools import partial
import copy

import numpy as np
import pandas as pd
from PyQt6.QtWidgets import (QMainWindow,
                             QHBoxLayout,
                             QVBoxLayout,
                             QTabWidget,
                             QApplication,
                             QPushButton,
                             QLabel,
                             QMessageBox)

from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QObject, QThread
from PyQt6.QtGui import QShortcut, QKeySequence

import IQM_Vis
from IQM_Vis.UI.custom_widgets import ClickLabel
from IQM_Vis.UI import utils
from IQM_Vis.utils import gui_utils, plot_utils, image_utils, save_utils


class make_experiment_JND(QMainWindow):
    '''Window for running a Just Noticeable Difference (JND) perceptual experiment.

    Reference: https://www.verywellmind.com/what-is-the-just-noticeable-difference-2795306
    '''

    saved_experiment = pyqtSignal(str)
    reset_clicked_image = pyqtSignal(dict)

    def __init__(self,
                 checked_transformation_params: dict,
                 data_store,
                 image_display_size: int,
                 rgb_brightness: float,
                 display_brightness: float,
                 default_save_dir: str = save_utils.DEFAULT_SAVE_DIR,
                 dataset_name: str = 'dataset1',
                 image_preprocessing: str = 'None',
                 image_postprocessing: str = 'None',
                 lower_im_num: int = 1,
                 upper_im_num: int = 1,
                 checked_metrics: dict = {}) -> None:
        super().__init__()
        self.checked_transformation_params = checked_transformation_params
        if self.checked_transformation_params == {}:
            return
        elif len(self.checked_transformation_params) != 1:
            raise AttributeError(f'Just Noticable difference experiment can only use one transform/distortion')

        self.checked_metrics = checked_metrics
        self.data_store = copy.copy(data_store)
        self.image_display_size = image_display_size
        self.rgb_brightness = rgb_brightness
        self.display_brightness = display_brightness
        self.default_save_dir = os.path.join(default_save_dir, 'JND')
        self.dataset_name = dataset_name
        self.default_save_dir = os.path.join(
            self.default_save_dir, self.dataset_name)
        self.dataset_name = dataset_name
        self.curr_im_ind = 0
        self.save_im_format = '.png'
        self.lower_im_num = lower_im_num
        self.upper_im_num = upper_im_num

        self.processing = {'pre': image_preprocessing,
                           'post': image_postprocessing}

        # self.image_change_worker = reset_image_widget_to_black()
        # self.image_change_worker.completed.connect(self.click_completed)
        # self.image_worker_thread = QThread()
        # self.reset_clicked_image.connect(self.image_change_worker.change_to_solid)
        # self.image_change_worker.moveToThread(self.image_worker_thread)
        # self.image_worker_thread.start()

        self.stop_event = threading.Event()
        self.saved = False
        self.quit_experiment = False
        self._init_experiment_window_widgets()
        self.experiment_layout()
        self.setCentralWidget(self.experiments_tab)
        self.setWindowTitle('JND Experiment')
        # move to centre of the screen
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # wait for the window to show before loading images
        # self.show()
        QApplication.processEvents()
        # get all images and show them
        self.get_all_images()

        # make unique save dir name
        self.new_save_dir = self.get_unique_save_dir()

        self.show_all_images()
        self.get_metric_scores()

    def closeEvent(self, event) -> None:
        '''Prompt for confirmation before closing; stop background threads if confirmed.'''
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
            if hasattr(self, 'image_worker_thread'):
                if self.image_worker_thread.isRunning():
                    self.image_worker_thread.quit()
                    self.image_worker_thread.wait()
                self.image_change_worker.stop()
            self.stop_event.set()
            # self.clicked_event.set()
            event.accept()

    def quit(self) -> None:
        '''Close the experiment window.'''
        self.close()

    def show_all_images(self, tab: str = 'setup') -> None:
        '''Display a grid of experiment images and update the info text for *tab*.'''
        self.widget_experiments['setup']['text'].setText(f'''
        JND Experiment to be setup with the above images using the settings:
            Save folder: {self.default_save_dir}
            Image Display Size: {self.image_display_size}
            Image Calibration:
                Max RGB Brightness: {self.rgb_brightness}
                Max Display Brightness: {self.display_brightness}

            Number of Comparisons: {int(len(self.experiment_transforms))}

        Click the Setup button to setup up the experiment and hand over to the test subject.
        ''')
        self.widget_experiments[tab]['images'].axes.axis('off')
        rows = min(int(len(self.experiment_transforms)**0.5), 5)
        cols = min(int(np.ceil(len(self.experiment_transforms)/rows)), 5)
        for i, trans in enumerate(self.experiment_transforms):
            if i == rows*cols:
                break
            ax = self.widget_experiments[tab]['images'].figure.add_subplot(
                rows, cols, i+1)
            ax.imshow(image_utils.calibrate_brightness(
                trans['image'], self.rgb_brightness, self.display_brightness, ubyte=False))
            if tab == 'final':
                ax.set_ylabel('')
                ax.set_xlabel(trans['user_decision'], fontsize=6)
                ax.set_xticks([])
                ax.set_yticks([])
            else:
                ax.axis('off')
            ax.set_title(save_utils.make_name_for_trans(trans), fontsize=6)
        # self.widget_experiments[tab]['images'].figure.tight_layout()

        # time.sleep(5)
        # QApplication.processEvents()
            
    def get_all_images(self) -> None:
        '''Load all reference and transformed images for every dataset entry in range.'''
        # get all the transform values
        self.experiment_trans_params = plot_utils.get_all_single_transform_params(
            self.checked_transformation_params, num_steps='from_dict')

        # save the experiment ordering before reordering (for saving to csv col ordering)
        self.original_params_order = []
        for single_trans in self.experiment_trans_params:
            trans_name = list(single_trans.keys())[0]
            param = single_trans[trans_name]
            data = {'transform_name': trans_name,
                    'transform_value': param}
            self.original_params_order.append(
                save_utils.make_name_for_trans(data))


        # all images in the dataset
        self.all_ref_images = {}
        self.experiment_transforms = []

        for i in range(max(self.lower_im_num-1, 0), min(len(self.data_store), self.upper_im_num)):
            # load the image in dataset
            self.data_store[i]
            # REFERENCE image
            ref_image = self.data_store.get_reference_image()
            ref_name = self.data_store.get_reference_image_name()
            # save name and image
            self.all_ref_images[ref_name] = ref_image
            # if hasattr(self.data_store, 'get_reference_unprocessed'):
            #     self.ref_image_unprocessed = self.data_store.get_reference_unprocessed()
            # get all transformed images
            for single_trans in self.experiment_trans_params:
                trans_name = list(single_trans.keys())[0]
                param = single_trans[trans_name]
                img = self.get_single_transform_im(single_trans)
                data = {'transform_name': trans_name,
                        'transform_value': param,
                        'image': img,
                        'ref_name': ref_name}
                self.experiment_transforms.append(data)
        
            # add reference image to list
            data = {'transform_name': 'None',
                    'transform_value': 'None',
                    'image': ref_image,
                    'ref_name': ref_name}
            self.experiment_transforms.append(data)

            # update user
            self.widget_experiments['setup']['text'].setText(
                f'''Loading all images in the dataset {i+1}/{len(self.data_store)}''')

        # shuffle the images list
        random.shuffle(self.experiment_transforms)

    def get_metric_scores(self, calc: bool = False) -> None:
        '''Optionally compute IQM scores for every experiment image and store as a DataFrame.'''
        self.IQM_scores_df = None
        if len(self.checked_metrics) == 0:
            return
        if calc == True:
            ''' this currently doesn't work and might be a bit taxing to do for all images'''
            IQM_scores = {}
            for data in self.experiment_transforms:
                score_dict = self.data_store.get_metrics(transformed_image=data['image'],
                                                    metrics_to_use=self.checked_metrics)
                scores = []
                metrics = []
                for name, score in score_dict.items():
                    metrics.append(name)
                    scores.append(float(score))
                IQM_scores[save_utils.make_name_for_trans(data)] = scores
            IQM_scores['IQM'] = metrics
            self.IQM_scores_df = pd.DataFrame.from_dict(IQM_scores)
            self.IQM_scores_df.set_index('IQM', inplace=True)

    def _init_experiment_window_widgets(self) -> None:
        '''Create all Qt widgets used across the setup, preamble, run, and finish tabs.'''
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
        self.widget_experiments['setup']['text'].setText(f'''Loading all images in the dataset''')
        # self.widget_experiments['setup']['text'].setAlignment(
        #     Qt.AlignmentFlag.AlignCenter)

        ''' info tab '''
        self.widget_experiments['preamble']['text'] = QLabel(self)
        self.widget_experiments['preamble']['text'].setText('''
        For this experiment you will be shown a reference image a comparison image.

        You need to click SAME or DIFFERENT whether you think the comparison image is the same or different to the reference image.




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
        self.exp_info_text = 'Click same or different for the two images shown (or press the S or D key)'
        self.widget_experiments['exp']['info'] = QLabel(self.exp_info_text, self)
        for image in ['Reference', 'Comparison']:
            self.widget_experiments['exp'][image] = {}
            self.widget_experiments['exp'][image]['data'] = ClickLabel(image)
            self.widget_experiments['exp'][image]['data'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            # image label
            self.widget_experiments['exp'][image]['label'] = QLabel(image, self)
            self.widget_experiments['exp'][image]['label'].setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.widget_experiments['exp']['same_button'] = QPushButton('SAME', self)
        self.widget_experiments['exp']['same_button'].clicked.connect(partial(self.user_decision, 'same'))
        self.widget_experiments['exp']['diff_button'] = QPushButton('DIFFERENT', self)
        self.widget_experiments['exp']['diff_button'].clicked.connect(partial(self.user_decision, 'diff'))
        self.widget_experiments['exp']['quit_button'] = QPushButton('Quit', self)
        self.widget_experiments['exp']['quit_button'].clicked.connect(self.quit)
        QShortcut(QKeySequence("S"), self.widget_experiments['exp']['same_button'], partial(
            self.user_decision, 'same'))
        QShortcut(QKeySequence("D"), self.widget_experiments['exp']['same_button'], partial(
            self.user_decision, 'diff'))
        QShortcut(QKeySequence("Ctrl+Q"),
                  self.widget_experiments['exp']['quit_button'], self.quit)

        ''' finish tab '''
        self.widget_experiments['final']['order_text'] = QLabel(
            'Experiment Results:', self)
        self.widget_experiments['final']['images'] = gui_utils.MplCanvas(size=None)
        self.widget_experiments['final']['quit_button'] = QPushButton('Quit', self)
        self.widget_experiments['final']['quit_button'].clicked.connect(
            self.quit)
        QShortcut(QKeySequence("Ctrl+Q"),
                self.widget_experiments['final']['quit_button'], self.quit)
        self.widget_experiments['final']['save_label'] = QLabel('Not saved yet', self)

    def experiment_layout(self) -> None:
        '''Assemble and populate the tabbed experiment layout.'''
        ''' setup '''
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


        ''' info '''
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

        ''' experiment '''
        same_diff_button = QHBoxLayout()
        same_diff_button.addWidget(self.widget_experiments['exp']['same_button'])
        same_diff_button.addWidget(self.widget_experiments['exp']['diff_button'])
        same_diff_button.setAlignment(Qt.AlignmentFlag.AlignCenter)

        info = QVBoxLayout()
        info.addWidget(self.widget_experiments['exp']['info'])
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        quit_button = QVBoxLayout()
        quit_button.addWidget(self.widget_experiments['exp']['quit_button'])
        quit_button.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layouts = []
        for im in ['Reference', 'Comparison']:
            _layout = QVBoxLayout()
            for _, widget in self.widget_experiments['exp'][im].items():
                _layout.addWidget(widget)
            _layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            layouts.append(_layout)

        # add images to h box
        experiment_images = QHBoxLayout()
        for layout in layouts:
            experiment_images.addLayout(layout)
        experiment_images.setAlignment(Qt.AlignmentFlag.AlignTop)

        run_experiment = QVBoxLayout()
        run_experiment.addLayout(info)
        run_experiment.addLayout(same_diff_button)
        run_experiment.addLayout(experiment_images)
        run_experiment.addLayout(quit_button)
        run_experiment.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ''' finished '''
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
    def setup_experiment(self) -> None:
        '''Switch to the preamble tab and lock the setup/run tabs.'''
        self.experiments_tab.setCurrentIndex(1)
        self.experiments_tab.setTabEnabled(0, False)
        self.experiments_tab.setTabEnabled(2, False)
        self.experiments_tab.setTabEnabled(3, False)

    def toggle_experiment(self) -> None:
        '''Start or reset the experiment depending on the current running state.'''
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

    def reset_experiment(self) -> None:
        '''Return to the preamble tab and restore the light style.'''
        self.experiments_tab.setCurrentIndex(1)
        self.init_style('light')

    def start_experiment(self) -> None:
        '''Begin the JND experiment: show the run tab and display the first image pair.'''
        self.init_style('dark')
        self.experiments_tab.setCurrentIndex(2)

        # Display reference image
        gui_utils.change_im(self.widget_experiments['exp']['Reference']['data'], 
                            self.all_ref_images[self.experiment_transforms[self.curr_im_ind]['ref_name']],
                            resize=self.image_display_size, 
                            rgb_brightness=self.rgb_brightness, 
                            display_brightness=self.display_brightness)

        # exp data holder
        self.time0 = time.time()
        self.curr_im_ind = 0
        # Display comparison image
        gui_utils.change_im(self.widget_experiments['exp']['Comparison']['data'], 
                            self.experiment_transforms[self.curr_im_ind]['image'],
                            resize=self.image_display_size, 
                            rgb_brightness=self.rgb_brightness, 
                            display_brightness=self.display_brightness)

    def finish_experiment(self) -> None:
        '''Switch to the finish tab, save results, and display the final summary.'''
        self.experiments_tab.setTabEnabled(3, True)
        self.show_all_images(tab='final')
        self.init_style('light')
        self.experiments_tab.setCurrentIndex(3)
        # self.experiments_tab.setTabEnabled(2, False)

        # save experiment to file
        self.save_experiment()
        if self.saved == True:
            self.widget_experiments['final']['save_label'].setText(f'Saved to {self.default_save_dir}')
        else:
            self.widget_experiments['final']['save_label'].setText(f'Save failed to {self.default_save_dir}')

    def get_trans_funcs(self) -> dict:
        '''Return a dict mapping transform names to their callable functions.'''
        # get the current transform functions
        trans_funcs = {}
        for single_trans in self.experiment_trans_params:
            trans_name = list(single_trans.keys())[0]
            trans_funcs[trans_name] = self.checked_transformation_params[trans_name]['function']
        return trans_funcs

    def get_unique_save_dir(self) -> bool:
        '''Locate or create a unique experiment directory; return ``True`` if new.'''
        trans_funcs = self.get_trans_funcs()

        # get a unique directory (same image with diff trans need a new dir)
        i = 1
        unique_dir_found = False
        new_dir = True
        while unique_dir_found == False:
            exp_save_dir = os.path.join(self.default_save_dir, f'experiment-{i}')
            if os.path.exists(exp_save_dir):
                # get transform funcs and params
                exp_trans_params = save_utils.load_obj(
                    os.path.join(exp_save_dir, 'transforms', 'transform_params.pkl'))
                exp_trans_funcs = save_utils.load_obj(
                    os.path.join(exp_save_dir, 'transforms', 'transform_functions.pkl'))
                
                # get ref image names
                im_names = save_utils.get_JND_image_names(exp_save_dir)
                im_names.sort()
                curr_im_names = list(self.all_ref_images.keys())
                # add file extension to names
                curr_im_names = [f'{name}{self.save_im_format}' for name in curr_im_names]
                curr_im_names.sort()

                # get image processing saved params
                processing_file = save_utils.get_image_processing_file(
                    exp_save_dir)
                procesing_same = False
                if os.path.exists(processing_file):
                    processing = save_utils.load_json_dict(processing_file)
                    if processing == self.processing:
                        procesing_same = True

                # check if experiment is the same
                if ((exp_trans_params == self.original_params_order) 
                    and (trans_funcs == exp_trans_funcs) 
                    and procesing_same
                    and (im_names == curr_im_names)):
                    self.default_save_dir = exp_save_dir
                    unique_dir_found = True
                    new_dir = False
                else:
                    i += 1
            else:
                self.default_save_dir = exp_save_dir
                unique_dir_found = True

        return new_dir

    def save_experiment(self) -> None:
        '''Save all experiment images, transform metadata, and human scores to disk.'''
        # get the current transform functions
        trans_funcs = self.get_trans_funcs()

        # make all the dirs and subdirs
        os.makedirs(self.default_save_dir, exist_ok=True)
        os.makedirs(os.path.join(save_utils.get_JND_ref_image_dir(self.default_save_dir)), exist_ok=True)
        os.makedirs(os.path.join(self.default_save_dir, 'images'), exist_ok=True)
        os.makedirs(os.path.join(self.default_save_dir, 'transforms'), exist_ok=True)

        if not os.path.exists(save_utils.get_JND_ref_image_unprocessed_dir(self.default_save_dir)):
            if hasattr(self, 'ref_image_unprocessed'):
                image_utils.save_image(self.ref_image_unprocessed,
                                        save_utils.get_original_unprocessed_image_file(self.default_save_dir))
        if self.new_save_dir == True:
            # save experiment images
            for name, im in self.all_ref_images.items():
                image_utils.save_image(im,
                                       os.path.join(save_utils.get_JND_ref_image_dir(self.default_save_dir), 
                                                    f'{name}{self.save_im_format}'))
            for trans in self.experiment_transforms:
                image_utils.save_image(
                    trans['image'], 
                    os.path.join(self.default_save_dir, 
                                 'images',
                                 f"{save_utils.make_name_for_trans(trans)}-{trans['ref_name']}{self.save_im_format}",
                                 ))
            # save the transformations
            save_utils.save_obj(
                save_utils.get_transform_params_file(self.default_save_dir),
                self.original_params_order)
            save_utils.save_obj(
                save_utils.get_transform_functions_file(self.default_save_dir),
                dict(sorted(trans_funcs.items())))
            # save the image pre/post processing options
            save_utils.save_json_dict(
                save_utils.get_image_processing_file(self.default_save_dir),
                self.processing)

        # save the experiment results
        csv_file = save_utils.save_JND_experiment_results(
            self.experiment_transforms,
            self.default_save_dir,
            self.IQM_scores_df)
        self.saved = True
        self.saved_experiment.emit(csv_file)

    def user_decision(self, decision: str) -> None:
        '''Record the user's ``'same'`` or ``'diff'`` decision and advance to the next image.'''
        if decision not in ['same', 'diff']:
            raise ValueError(f'user decision for JND experiment needs to be same or diff')
        # make sure we don't go beyond the data set with acciental key presses
        if self.curr_im_ind >=  len(self.experiment_transforms):
            return
        # save time it took 

        # log decision
        self.experiment_transforms[self.curr_im_ind]['user_decision'] = decision
        self.experiment_transforms[self.curr_im_ind]['time_taken'] = time.time()-self.time0

        # move to next image
        self.curr_im_ind += 1
        if self.curr_im_ind ==  len(self.experiment_transforms):
            self.finish_experiment()
        else:
            # Display reference image
            gui_utils.change_im(self.widget_experiments['exp']['Reference']['data'],
                                self.all_ref_images[self.experiment_transforms[self.curr_im_ind]['ref_name']],
                                resize=self.image_display_size,
                                rgb_brightness=self.rgb_brightness,
                                display_brightness=self.display_brightness)
            # Comparison image
            gui_utils.change_im(self.widget_experiments['exp']['Comparison']['data'], 
                                self.experiment_transforms[self.curr_im_ind]['image'],
                                resize=self.image_display_size, 
                                rgb_brightness=self.rgb_brightness, 
                                display_brightness=self.display_brightness)
            self.widget_experiments['exp']['info'].setText(
                f'{self.exp_info_text} {self.curr_im_ind+1}/{len(self.experiment_transforms)}')

        # reset time
        self.time0 = time.time()

    def get_single_transform_im(self, single_trans_dict: dict):
        '''Apply a single transform and return the resulting image array.'''
        trans_name = list(single_trans_dict)[0]
        return image_utils.get_transform_image(self.data_store,
                                        {trans_name: self.checked_transformation_params[trans_name]},
                                        single_trans_dict)

    ''' UI '''
    def init_style(self, style: str = 'light', css_file: str | None = None) -> None:
        '''Apply a CSS stylesheet to this window.

        Args:
            style: Style name (``'light'`` or ``'dark'``). Defaults to ``'light'``.
            css_file: Explicit path to a CSS file; overrides *style* if provided.
        '''
        if css_file == None:
            dir = os.path.dirname(os.path.abspath(__file__))
            css_file = os.path.join(dir, f'style-{style}.css')
        if os.path.isfile(css_file):
            with open(css_file, 'r') as file:
                self.setStyleSheet(file.read())
        else:
            warnings.warn('Cannot load css style sheet - file not found')


class reset_image_widget_to_black(QObject):
    '''Flash a clicked image to black briefly then re-enable clicks.'''

    completed = pyqtSignal(float)

    def __init__(self, time: float = 0.1) -> None:
        super().__init__()
        self.running = True
        self.time = time
        self.black_array = np.zeros([100, 100, 3])
        # self.black_array[:, :, 1] = 1 # blue

    @pyqtSlot(dict)
    def change_to_solid(self, data: dict) -> None:
        '''Set the clicked image widget to black, wait, then signal completion.'''
        t_start = time.time()
        image_display_size = data['image_display_size']
        widget = data['widget']
        # make clicked image black to show user
        gui_utils.change_im(widget,
                            self.black_array,
                            resize=image_display_size)
        # pause for half the time needed (will use the loop below to wait for full time and also see if image has turned black yet)
        time.sleep(self.time/2)
        m = 1
        t_time = time.time() - t_start
        # wait until black image is shown
        while (not (m == 0 or m == 63.75)) and (t_time < self.time): # 63.75 is when 4th channel is all ones , rest are 0
            time.sleep(self.time/10)
            # get the image data from the widget to check if it's been made black yet
            pixmap = widget.pixmap()
            q_img = pixmap.toImage()
            ptr = q_img.bits()
            ptr = q_img.constBits()
            ptr.setsize(q_img.sizeInBytes())
            np_img = np.array(ptr, copy=False).reshape(
                q_img.height(), q_img.width(), 4)
            m = np_img.mean()
            # calc if the time is up yet
            t_time = time.time() - t_start
        # all complete so send signal 
        self.completed.emit(1.0)

    def stop(self) -> None:
        '''Stop the worker loop.'''
        self.running = False

    def __del__(self) -> None:
        # close app upon garbage collection
        self.stop()
