'''
UI image functions
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

import os
import glob
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtCore import pyqtSignal, QThread
import IQM_Vis
from IQM_Vis.utils import gui_utils, plot_utils, image_utils

# sub class used by IQM_Vis.main.make_app to control all of the image widgets
class images:
    request_range_work = pyqtSignal(dict)
    view_correlation_instance = pyqtSignal(str)

    def __init__(self):
        self.num_steps_range = 11
        self.init_worker_thread()
        self.view_correlation_instance.connect(self.change_to_specific_trans)

    def init_worker_thread(self):
        ''' set up thread for smoother range plot calculation '''
        self.range_worker = IQM_Vis.UI.threads.get_range_results_worker()
        self.range_worker_thread = QThread()
        self.range_worker.progress.connect(self.update_progress)
        self.range_worker.current_image.connect(self.update_status_bar)
        self.range_worker.completed.connect(self.completed_range_results)
        self.range_worker.stopped.connect(self.stopped_range_results)
        self.request_range_work.connect(self.range_worker.do_work)
        # move worker to the worker thread
        self.range_worker.moveToThread(self.range_worker_thread)
        # start the thread
        self.range_worker_thread.start()
        self.worker_working = False

    '''
    image updaters
    '''
    # def transform_image(self, image):
    #     for key in self.sliders['transforms']:
    #         image = self.sliders['transforms'][key]['function'](image, self.params_from_sliders['transforms'][key])
    #     return image

    def display_images(self):
        for i, data_store in enumerate(self.data_stores):
            # reference image
            reference_image = data_store.get_reference_image()
            gui_utils.change_im(self.widget_row[i]['images']['original']['data'], reference_image, resize=self.image_display_size, rgb_brightness=self.rgb_brightness, display_brightness=self.display_brightness)
            # transform image
            trans_im = image_utils.get_transform_image(data_store, self.sliders['transforms'], self.params_from_sliders['transforms'])
            gui_utils.change_im(self.widget_row[i]['images']['transformed']['data'], trans_im, resize=self.image_display_size, rgb_brightness=self.rgb_brightness, display_brightness=self.display_brightness)
            # metrics
            metrics = data_store.get_metrics(trans_im, self.checked_metrics, **self.params_from_sliders['metric_params'])
            self.display_metrics(metrics, i)
            # metric images
            metric_images = data_store.get_metric_images(trans_im, self.checked_metric_images, **self.params_from_sliders['metric_params'])
            self.display_metric_images(metric_images, i)

            QApplication.processEvents()   # make figures become the correct size

    '''
    metric graph updaters
    '''
    def redo_plots(self, calc_range=True):
        if calc_range:  # add an or metrics_range val not been calculated
            if self.metrics_avg_graph or self.metric_range_graph:
                self.get_metrics_over_all_trans_with_init_values()

    '''
    change image in dataset
    '''
    def change_data(self, ival):
        # reset any range/correlation data stored
        if hasattr(self, 'correlation_data'):
            self.correlation_data = {}
            for i, data_store in enumerate(self.data_stores):
                self.correlation_data[i] = {}
        self.data_num += ival
        # check the num is within the data limits
        if self.data_num < 0:
            self.data_num = 0
            return
        if self.data_num > self.max_data_ind:
            self.data_num = self.max_data_ind
            return
        self.range_worker.stop() # stop any calculations on the old image
        # if ival != 0:
        for data_store in self.data_stores:
            try:
                data_store[self.data_num]
            except:
                pass # some datasets will be shorter than others - this is fine though
            self.display_images()
            self.set_image_name_text()
        self.redo_plots()
        # load human experiment if any
        self.human_experiment_scores = {}
        for i, data_store in enumerate(self.data_stores):
            if hasattr(data_store, 'human_scores'):
                self.human_experiment_scores[i] = data_store.human_scores


    def load_new_images_folder(self):
        ''' change the image dataset we are using '''
        # get the file opener for the user
        try:
            start_dir = os.path.expanduser("~")
            dir = QFileDialog.getExistingDirectory(self, 
                                                   'Choose Image folder',
                                                   start_dir)
        except:
            return

        if dir == '':
            return

        image_list = glob.glob(os.path.join(dir, '*'))
        # remove and folders
        image_list = [f for f in image_list if os.path.isfile(f)]
        # change image dataset
        if hasattr(self.data_stores[0], 'load_image_list') and len(image_list) != 0:
            self.data_stores[0].load_image_list(image_list)
            self.data_num = 0
            self.construct_UI()
            self.max_data_ind = len(image_list) - 1

    def load_human_experiment(self):
        ''' change the image dataset we are using '''
        # get the file opener for the user
        if os.path.exists(self.default_save_dir):
            start_dir = self.default_save_dir
        else:
            start_dir = os.path.expanduser("~")
        try:
            file, _ = QFileDialog.getOpenFileName(
                self,
                "Open Human Experiments File for Current Image",
                start_dir,
                "CSV Files (*.csv)",)
        except:
            return
        
        # load the csv human scores file and take mean of all experiments
        if os.path.exists(file):
            df = pd.read_csv(file)
            experiment = df.mean().to_dict()
            for i, _ in enumerate(self.data_stores):
                self.human_experiment_scores[i] = experiment
        
        # clear cache and update correlation plot
        self.reset_correlation_data()
        self.display_metric_correlation_plot()

    '''
    metric updaters
    '''
    def display_metrics(self, metrics, i):
        if self.metrics_info_format == 'graph':
            self.display_metrics_graph(metrics, i)
        else:
            self.display_metrics_text(metrics, i)

    def display_metrics_graph(self, metrics, i):
        bar_plt = plot_utils.bar_plotter(bar_names=[''],
                                        var_names=list(metrics.keys()),
                                        ax=self.widget_row[i]['metrics']['info']['data'],
                                        lim=self.plot_data_lim)
        bar_plt.plot('', list(metrics.values()))
        bar_plt.show()

    def display_metrics_text(self, metrics, i, disp_len=5):
        text = ''
        for key in metrics:
            metric = gui_utils.str_to_len(str(metrics[key]), disp_len, '0')
            text += key + ': ' + metric + '\n'
        self.widget_row[i]['metrics']['info']['data'].setText(text)

    '''
    get metric values when adjusting a single transformation value over its range
    '''
    def get_metrics_over_all_trans_with_init_values(self):
        # use the initiased/default values for all sliders
        # bundle up data needed to send to the worker
        data = {'trans': self.checked_transformations,
                'metric_params': self.params_from_sliders['metric_params'],
                'metrics_to_use': self.checked_metrics,
                'data_stores': self.data_stores,
                'num_steps': self.num_steps_range,
                }
        # start the worker working
        self.worker_working = True
        self.request_range_work.emit(data)

    def completed_range_results(self, results):
        ''' data results sent from signal from thread worker '''
        self.worker_working = False
        self.metric_over_range_results = results['metric_over_range_results']
        self.data_lims['range_data'] = results['max_val']
        if self.metrics_avg_graph:
            self.display_radar_plots()
        if self.metric_range_graph:
            self.display_metric_range_plot()
        self.display_metric_correlation_plot()

    '''
    metric range plot (line plots of range of all sliders)
    '''
    def display_metric_range_plot(self):
        all_trans = list(self.checked_transformations.keys())
        if all_trans == []:
            return
        trans_to_plot = all_trans[self.metric_range_graph_num]
        for i, data_store in enumerate(self.data_stores):
            if 'range' in self.widget_row[i]['metrics'].keys():
                axes = self.widget_row[i]['metrics']['range']['data']
                plot = plot_utils.get_transform_range_plots(self.metric_over_range_results[i], trans_to_plot, axes, self.plot_data_lim)
                plot.show()

    def change_metric_range_graph(self, add=1):
        max_graph_num = len(list(self.checked_transformations.keys()))
        self.metric_range_graph_num += add
        if self.metric_range_graph_num >= max_graph_num:
            self.metric_range_graph_num = max_graph_num - 1
        elif self.metric_range_graph_num < 0:
            self.metric_range_graph_num = 0
        self.display_metric_range_plot()

    '''
    metric averaging plots (radar plot)
    '''
    def display_radar_plots(self):
        for i, data_store in enumerate(self.data_stores):
            self.plot_radar_graph(self.metric_over_range_results[i], i)
            # uncomment below if you want to calc over the current trans values instead of init
            # results = plot_utils.compute_metrics_over_range(data_store,
            #                                                 self.checked_transformations,
            #                                                 self.params_from_sliders['transforms'],
            #                                                 self.params_from_sliders['metric_params'],
            #                                                 pbar=self.pbar)

    def plot_radar_graph(self, results, i):
        all_trans = list(self.checked_transformations.keys())
        if len(all_trans) == 0:
            return
        if 'avg'  in self.widget_row[i]['metrics'].keys():
            # get current metrics used for this data_store
            metrics_names = []
            for metric in self.data_stores[i].metrics:
                if metric in self.checked_metrics:
                    metrics_names.append(metric)

            if len(metrics_names) == 0:
                return

            transformation_names = list(self.sliders['transforms'].keys())
            axes = self.widget_row[i]['metrics']['avg']['data']
            radar_plotter = plot_utils.get_radar_plots_avg_plots(results, metrics_names, transformation_names, axes, self.plot_data_lim)
            radar_plotter.show()

    '''
    metric correlation plots
    '''
    def display_metric_correlation_plot(self):
        if self.checked_metrics == []:
            return
        metric = self.checked_metrics[self.metric_correlation_graph_num]
        # calculate the metric values at the human score test values
        for i, data_store in enumerate(self.data_stores):
            if i in self.human_experiment_scores.keys():
                # calculate metric at HIQM values (if not already cached)
                if metric not in self.correlation_data[i].keys():
                    scores = plot_utils.compute_metric_for_human_correlation(data_store,
                                            self.checked_transformations,
                                            self.params_from_sliders['metric_params'],
                                            self.human_experiment_scores[i],
                                            metric)
                    # cache it
                    self.correlation_data[i][metric] = scores
                plot = plot_utils.get_correlation_plot(self.human_experiment_scores[i],
                                                self.correlation_data[i],
                                                self.widget_row[i]['metrics']['correlation']['data'],
                                                metric,
                                                self.view_correlation_instance)
                plot.show()
            else:
                self.widget_row[i]['metrics']['correlation']['data'].axes.clear()
                self.widget_row[i]['metrics']['correlation']['data'].axes.text(
                    0.5, 0.5, 'Go to: File->Load Human Scores', horizontalalignment='center', verticalalignment='center')
                self.widget_row[i]['metrics']['correlation']['data'].draw()

    def change_metric_correlations_graph(self, add=1):
        max_graph_num = len(self.checked_metrics)
        self.metric_correlation_graph_num += add
        if self.metric_correlation_graph_num >= max_graph_num:
            self.metric_correlation_graph_num = max_graph_num - 1
        elif self.metric_correlation_graph_num < 0:
            self.metric_correlation_graph_num = 0
        self.display_metric_correlation_plot()

    def change_to_specific_trans(self, trans_str):
        trans, trans_value = gui_utils.get_trans_dict_from_str(trans_str)
        for _, slider_group in self.sliders.items():
            for key, item_sliders in slider_group.items():
                if key == trans:
                    closest_slider_val = np.argmin(np.abs(self.sliders['transforms'][key]['values']-trans_value))
                    self.widget_controls['slider'][key]['data'].setValue(closest_slider_val)
                else:
                    self.widget_controls['slider'][key]['data'].setValue(item_sliders['init_ind'])
        self.display_images()
        self.redo_plots(calc_range=False)

    '''
    metric image updaters
    '''
    def display_metric_images(self, metric_images, i):
        for key in metric_images:
            widget = self.widget_row[i]['metric_images'][key]['data']
            gui_utils.change_im(widget, metric_images[key], resize=self.image_display_size)

    '''
    thread manegment
    '''
    def stopped_range_results(self, signal):
        self.worker_working = False
