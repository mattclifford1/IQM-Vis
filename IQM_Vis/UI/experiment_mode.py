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
from IQM_Vis.utils import gui_utils, plot_utils, image_utils


class make_experiment(QMainWindow):
    saved_experiment = pyqtSignal(str)
    reset_clicked_image = pyqtSignal(dict)

    def __init__(self, 
                 checked_transformation_params, 
                 data_store, 
                 image_display_size,
                 rgb_brightness,
                 display_brightness,
                 default_save_dir=IQM_Vis.utils.save_utils.DEFAULT_SAVE_DIR,
                 image_preprocessing='None',
                 image_postprocessing='None',
                 checked_metrics={}):
        super().__init__()
        self.checked_transformation_params = checked_transformation_params
        if self.checked_transformation_params == {}:
            return
        self.checked_metrics = checked_metrics
        self.data_store = data_store
        self.image_display_size = image_display_size
        self.rgb_brightness = rgb_brightness
        self.display_brightness = display_brightness
        self.default_save_dir = default_save_dir
        
        self.processing = {'pre': image_preprocessing,
                           'post': image_postprocessing}

        self.clicked_event = threading.Event()
        self.able_to_click = False

        self.image_change_worker = reset_image_widget_to_black()
        self.image_change_worker.completed.connect(self.click_completed)
        self.image_worker_thread = QThread()
        self.reset_clicked_image.connect(self.image_change_worker.change_to_solid)
        self.image_change_worker.moveToThread(self.image_worker_thread)
        self.image_worker_thread.start()

        self.stop_event = threading.Event()
        self.saved = False
        self.quit_experiment = False
        self.get_all_images()
        self._init_experiment_window_widgets()
        self.get_metric_scores()
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
            if hasattr(self, 'image_worker_thread'):
                self.image_change_worker.stop()
                self.image_worker_thread.quit()
                self.image_worker_thread.wait()
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
        ''' save image name '''
        self.image_name = self.data_store.get_reference_image_name()
        ''' load all transformed images and sort them via MSE '''
        # get all the transform values
        self.experiment_trans_params = plot_utils.get_all_single_transform_params(
            self.checked_transformation_params, num_steps='from_dict')

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

        # REFERENCE image
        self.ref_image = self.data_store.get_reference_image()
        if hasattr(self.data_store, 'get_reference_unprocessed'):
            self.ref_image_unprocessed = self.data_store.get_reference_unprocessed()
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
        for single_trans in self.experiment_trans_params:
            trans_name = list(single_trans.keys())[0]
            param = single_trans[trans_name]
            img = self.get_single_transform_im(single_trans)
            data = {'transform_name': trans_name,
                    'transform_value': param,
                    'image': img}
            self.experiment_transforms.append(data)
        self.calc_max_comparisons(num_images=len(self.experiment_transforms))
    
    def calc_max_comparisons(self, num_images):
        # calc expected number of comparisons - 
        # http://homepages.math.uic.edu/~leon/cs-mcs401-r07/handouts/quicksort-continued.pdf
        self.min_expected_comps = num_images * np.log(num_images)
        self.max_expected_comps = 1.39 * num_images * np.log(num_images)
    
    def get_metric_scores(self):
        '''get IQM scores to save alongside the experiment for plotting/analysis purposes'''
        IQM_scores = {}
        for data in self.experiment_transforms:
            score_dict = self.data_store.get_metrics(transformed_image=data['image'],
                                                 metrics_to_use=self.checked_metrics)
            scores = []
            metrics = []
            for name, score in score_dict.items():
                metrics.append(name)
                scores.append(float(score))
            IQM_scores[make_name_for_trans(data)] = scores
        IQM_scores['IQM'] = metrics
        self.IQM_scores_df = pd.DataFrame.from_dict(IQM_scores)
        self.IQM_scores_df.set_index('IQM', inplace=True)

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
            Image Display Size: {self.image_display_size}
            Image Calibration:
                Max RGB Brightness: {self.rgb_brightness}
                Max Display Brightness: {self.display_brightness}

            Expected Number of Comparisons: {int(self.min_expected_comps)}
            MAX Expected Number of Comparisons: {int(self.max_expected_comps)}

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
        self.widget_experiments['exp']['info'] = QLabel(
            'Click on which image, A or B, is most similar to the reference image', self)
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
        self.widget_experiments['final']['save_label'] = QLabel('Not saved yet', self)

    def experiment_layout(self):
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
        info = QVBoxLayout()
        info.addWidget(self.widget_experiments['exp']['info'])
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        quit = QVBoxLayout()
        quit.addWidget(self.widget_experiments['exp']['quit_button'])
        quit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layouts = []
        for im in ['A', 'Reference', 'B']:
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
        run_experiment.addLayout(experiment_images)
        run_experiment.addLayout(quit)
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
        # self.experiments_tab.setTabEnabled(2, False)
        self.save_experiment()
        if self.saved == True:
            self.widget_experiments['final']['save_label'].setText(f'Saved to {self.default_save_dir}')
        else:
            self.widget_experiments['final']['save_label'].setText(f'Save failed to {self.default_save_dir}')


    def save_experiment(self):
        # get the current transform functions
        trans_funcs = {}
        for single_trans in self.experiment_trans_params:
            trans_name = list(single_trans.keys())[0]
            trans_funcs[trans_name] = self.checked_transformation_params[trans_name]['function']
        # make the experiment directory
        self.default_save_dir = os.path.join(
            self.default_save_dir, self.image_name)
        # get a unique directory (same image with diff trans need a new dir)
        i = 1
        unique_dir_found = False
        new_dir = True
        while unique_dir_found == False:
            exp_save_dir = f'{self.default_save_dir}-experiment-{i}'
            if os.path.exists(exp_save_dir):
                # get transform funcs and params
                exp_trans_params = IQM_Vis.utils.save_utils.load_obj(
                    os.path.join(exp_save_dir, 'transforms', 'transform_params.pkl'))
                exp_trans_funcs = IQM_Vis.utils.save_utils.load_obj(
                    os.path.join(exp_save_dir, 'transforms', 'transform_functions.pkl'))
                
                # get image processing saved params
                processing_file = IQM_Vis.utils.save_utils.get_image_processing_file(exp_save_dir)
                procesing_same = False
                if os.path.exists(processing_file):
                    processing = IQM_Vis.utils.save_utils.load_json_dict(processing_file)
                    if processing == self.processing:
                        procesing_same = True

                # check if experiment is the same
                if (exp_trans_params == self.original_params_order) and (trans_funcs == exp_trans_funcs) and procesing_same:
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

        # save experiment images
        if not os.path.exists(IQM_Vis.utils.save_utils.get_original_image_file(self.default_save_dir)):
            image_utils.save_image(self.ref_image,
                                    IQM_Vis.utils.save_utils.get_original_image_file(self.default_save_dir))
        if not os.path.exists(IQM_Vis.utils.save_utils.get_original_unprocessed_image_file(self.default_save_dir)):
            if hasattr(self, 'ref_image_unprocessed'):
                image_utils.save_image(self.ref_image_unprocessed,
                                        IQM_Vis.utils.save_utils.get_original_unprocessed_image_file(self.default_save_dir))
        if new_dir == True:
            for trans in self.experiment_transforms:
                image_utils.save_image(
                    trans['image'], os.path.join(self.default_save_dir, 'images', f'{make_name_for_trans(trans)}.png'))
            # save the transformations
            IQM_Vis.utils.save_utils.save_obj(
                IQM_Vis.utils.save_utils.get_transform_params_file(self.default_save_dir),
                self.original_params_order)
            IQM_Vis.utils.save_utils.save_obj(
                IQM_Vis.utils.save_utils.get_transform_functions_file(self.default_save_dir),
                dict(sorted(trans_funcs.items())))
            # save the image pre/post processing options
            IQM_Vis.utils.save_utils.save_json_dict(
                IQM_Vis.utils.save_utils.get_image_processing_file(self.default_save_dir),
                self.processing)

        # save the experiment results
        exp_order = []
        for trans in self.experiment_transforms:
            exp_order.append(make_name_for_trans(trans))
        csv_file = IQM_Vis.utils.save_utils.save_experiment_results(
            self.original_params_order,
            exp_order,
            self.default_save_dir,
            self.times_taken,
            self.IQM_scores_df)
        self.saved = True
        self.saved_experiment.emit(csv_file)


    ''' sorting algorithm resource: https://www.geeksforgeeks.org/quick-sort/'''
    def quick_sort(self):
        self.times_taken = []
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
            time0 = time.time()
            # randomly assign to image A or B
            ims_to_display = [
                self.experiment_transforms[self.current_comparision], self.pivot]
            random.shuffle(ims_to_display)
            # display the images
            self.change_experiment_images(A_trans=ims_to_display[0],
                                          B_trans=ims_to_display[1])
            # wait for image to be clicked
            self.clicked_event.clear()
            self.able_to_click = True
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
            self.times_taken.append(time.time()-time0)
            if self.current_comparision == self.high:
                break
        # Swap the pivot element with the greater element specified by i
        self.swap_inds(self.comp_pointer+1, self.high)
        # Return the position from where partition is done
        return self.comp_pointer + 1

    def clicked_image(self, image_name, widget_name):
        if self.able_to_click == False:
            return
        self.able_to_click = False
        # get comparison to pivot
        trans_str = image_name[len(self.image_name)+1:]
        if trans_str != make_name_for_trans(self.pivot): # lower value
            # If element smaller than pivot is found swap it with the greater element pointed by i
            self.less_than_pivot = True
        else:
            self.less_than_pivot = False
        # make clicked image black to show user
        data = {'image_display_size': self.image_display_size,
                'widget': self.widget_experiments['exp'][widget_name]['data']}
        self.reset_clicked_image.emit(data)  # change to black image, after x amount of time will change to experimetn image
        
    def click_completed(self):
        # unlock the wait
        self.clicked_event.set()

    def swap_inds(self, i, j):
        (self.experiment_transforms[i], self.experiment_transforms[j]) = (self.experiment_transforms[j], self.experiment_transforms[i])

    def get_single_transform_im(self, single_trans_dict):
        trans_name = list(single_trans_dict)[0]
        return image_utils.get_transform_image(self.data_store,
                                        {trans_name: self.checked_transformation_params[trans_name]},
                                        single_trans_dict)

    def change_experiment_images(self, A_trans, B_trans):
        A = A_trans['image']
        B = B_trans['image']
        
        gui_utils.change_im(self.widget_experiments['exp']['A']['data'], A, resize=self.image_display_size,
                            rgb_brightness=self.rgb_brightness, display_brightness=self.display_brightness)
        self.widget_experiments['exp']['A']['data'].setObjectName(f'{self.image_name}-{make_name_for_trans(A_trans)}')
        gui_utils.change_im(self.widget_experiments['exp']['B']['data'], B, resize=self.image_display_size,
                            rgb_brightness=self.rgb_brightness, display_brightness=self.display_brightness)
        self.widget_experiments['exp']['B']['data'].setObjectName(f'{self.image_name}-{make_name_for_trans(B_trans)}')

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


class reset_image_widget_to_black(QObject):
    ''' change clicked image to black and pause '''
    completed = pyqtSignal(float)

    def __init__(self, time=0.1):
        super().__init__()
        self.running = True
        self.time = time
        self.black_array = np.zeros([100, 100, 3])
        # self.black_array[:, :, 1] = 1 # blue

    @pyqtSlot(dict)
    def change_to_solid(self, data):
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

    def stop(self):
        self.running = False

    def __del__(self):
        # close app upon garbage collection
        self.stop()


def sort_list(list1, list2):
    # sort list1 based on list2
    inds = np.argsort(list2)
    sorted_list1 = []
    for i in inds:
        sorted_list1.append(list1[i])
    return sorted_list1

def make_name_for_trans(trans):
    splitter = '-----'
    return f"{trans['transform_name']}{splitter}{trans['transform_value']}"
