'''
UI image functions
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

import os
import imghdr
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

    def __init__(self, **kwargs):
        self.update_images = True
        self.init_worker_thread()
        self.view_correlation_instance.connect(self.change_to_specific_trans)

    def init_worker_thread(self):
        ''' set up thread for smoother range plot calculation '''
        self.range_worker = IQM_Vis.UI.threads.get_range_results_worker()
        self.range_worker_thread = QThread()
        self.range_worker.progress.connect(self.update_progress)
        self.range_worker.current_image.connect(self.update_status_bar)
        self.range_worker.completed.connect(self.completed_range_results)
        self.range_worker.stopped.connect(self.stopped_range_worker)
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
        if self.update_images == True:
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
    def redo_plots(self, calc_range=False):
        if calc_range == True:  # add an or metrics_range val not been calculated
            if self.metrics_avg_graph or self.metric_range_graph:
                self.get_metrics_over_all_trans_with_init_values()

    '''
    change image in dataset
    '''
    def change_to_data_num(self, ind):
        # change to an exact ind in the data list - be careful that the ind exists!!!
        self.data_num = ind
        self.change_data(0)

    def change_data(self, ival, _redo_plots=True):
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
        # if hasattr(self, 'wait_until_safe_to_change_image'):
        #     self.wait_until_safe_to_change_image()
        # if ival != 0:
        for data_store in self.data_stores:
            try:
                data_store[self.data_num]
            except:
                pass # some datasets will be shorter than others - this is fine though
            self.display_images()
            self.set_image_name_text()
        if _redo_plots == True:
            self.redo_plots(calc_range=True)
        # load human experiment if any
        self.human_experiment_scores = {}
        for i, data_store in enumerate(self.data_stores):
            # first try get from UI
            # load most recent correlation plots
            name = data_store.get_reference_image_name()
            if name in self.human_experiment_cache:
                self._load_experiment(self.human_experiment_cache[name], change_image=False)
            # otherwise from the datastore scores
            elif hasattr(data_store, 'human_scores'):
                self.human_experiment_scores[i] = data_store.human_scores
        self.widget_controls['label']['data_num'].setText(f'({self.data_num+1}/{self.max_data_ind+1})')

    def load_new_single_image(self):
        ''' change the image we are using '''
        # get the file opener for the user
        try:
            start_dir = os.path.expanduser("~")
            file, _ = QFileDialog.getOpenFileName(self,
                                               "Choose Image",
                                               start_dir,
                                               "All Files (*);; PNG Files (*.png)")
        except:
            return
        if file == ('', '') or file == '':
            return
        
        if os.path.isfile(file):
            image_format = imghdr.what(file)
            if image_format == None:
                self.update_status_bar(f'Not an image file: {file}', 10000)
            else:
                self.update_datastore_image_list([file])
        else:
            self.update_status_bar(f'Cannot find file: {file}', 10000)


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
        image_list.sort()

        self.update_datastore_image_list(image_list)

    def update_datastore_image_list(self, image_list, append_dataset=False): # onyl changes the first datastore
        # make sure that we have some images
        if image_list == []:
            self.update_status_bar('No images found', 10000)
            return
        # get all images if possible and we want to append images to the current dataset
        if append_dataset == True and hasattr(self.data_stores[0], 'get_image_dataset_list'):
            image_list = self.data_stores[0].get_image_dataset_list() + image_list
            data_num_to_change_to = len(self.data_stores[0])
        else:
            data_num_to_change_to = 0
        # change image dataset
        if hasattr(self.data_stores[0], 'load_image_list') and len(image_list) != 0:
            self.data_stores[0].load_image_list(image_list)
            self.max_data_ind = len(self.data_stores[0]) - 1
            self.data_num = data_num_to_change_to
            self.construct_UI()
        else:
            self.update_status_bar('Failed to update images', 10000)

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
        self._change_human_exp(file)
        
    def _change_human_exp(self, file, change_image=True):
        # load image
        if change_image == True:
            self._load_experiment_image(os.path.dirname(file))
        # load the csv human scores file and take mean of all experiments
        self.update_status_bar(f'Loading experiment file: {file}', 10000)
        if os.path.exists(file):
            df = pd.read_csv(file)
            for i, data_store in enumerate(self.data_stores):
                self.human_experiment_scores[i] = {'mean': df.mean().to_dict(),
                                                   'std': df.std().to_dict()}
                # cache this as the last used dataset for this image
                self.human_experiment_cache[data_store.get_reference_image_name()] = os.path.dirname(file)
            self.human_scores_file = file
        else:
            self.update_status_bar(f'No experiment file: {file}', 10000)
            return
        self._load_experiment_extras(os.path.dirname(file))
        self.update_status_bar(f'Loaded experiment file: {file}', 10000)

    def _load_experiment(self, dir, change_image=True):
        file = IQM_Vis.utils.save_utils.get_human_scores_file(dir)
        self._change_human_exp(file, change_image=change_image)

    def load_experiment_from_dir(self):
        # get the file opener for the user
        try:
            start_dir = IQM_Vis.utils.save_utils.DEFAULT_SAVE_DIR
            dir = QFileDialog.getExistingDirectory(self, 
                                                   'Choose Experiment Folder',
                                                   start_dir)
        except:
            return

        if dir == '':
            return   
        self._load_experiment(dir)

    def _load_experiment_image(self, dir):
        # load image if available already
        exp_image_name = IQM_Vis.utils.save_utils.get_image_name_from_human_scores(dir)
        exp_saved_image = IQM_Vis.utils.save_utils.get_original_unprocessed_image_file(dir)
        if hasattr(self.data_stores[0], 'image_names'):
            if exp_image_name in self.data_stores[0].image_names:
                ind = self.data_stores[0].image_names.index(exp_image_name)
                self.change_to_data_num(ind)
            # else load it from the experiment
            elif os.path.exists(exp_saved_image):
                self.update_datastore_image_list([exp_saved_image], append_dataset=True)
        # else load it from the experiment
        elif os.path.exists(exp_saved_image):
            self.update_datastore_image_list([exp_saved_image], append_dataset=True)
        else:
            self.update_status_bar(f'No {exp_image_name} in dataset or file {exp_saved_image}', 10000)
        
    def _load_experiment_extras(self, dir):
        # load the image processing if available
        processing_file = IQM_Vis.utils.save_utils.get_image_processing_file(dir)
        if os.path.exists(processing_file):
            processing = IQM_Vis.utils.save_utils.load_json_dict(
                processing_file)
            updated = False
            for name, options_var, change_func in zip(['pre', 'post'], 
                                                      [self.pre_processing_options, self.post_processing_options], 
                                                      [self.change_pre_processing, self.change_post_processing]):
                if processing[name] in options_var:
                    if processing[name] != self.widget_settings[f'image_{name}_processing']['widget'].currentText():
                        self.widget_settings[f'image_{name}_processing']['widget'].setCurrentText(
                            processing[name])
                        change_func()
                        updated = True
                else:
                    self.update_status_bar(
                        f'Could not load image setting: {processing[name]}')
            if updated == True:
                self.update_image_settings()
        else:
            self.update_status_bar(f'Warning: No settings file ({processing_file}), make sure image pre/post processing settings are correct')

        # clear cache and update correlation plot
        self.reset_correlation_data()
        self.display_metric_correlation_plot()
        self.tabs['graph'].setCurrentIndex(3)

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
        self.update_status_bar('Completed Range Results', 3000)
        self.stopped_range_worker()
        # first check if we have empty results (means we cannot plot) - have changed to accept empty
        # if 'metric_over_range_results' in results:
        #     if len(results['metric_over_range_results']) == 1:
        #         if results['metric_over_range_results'][0] == {}:
        #             # dont plot
        #             return 
        # else:
        #     # incorrect data
        #     return
        
        self.metric_over_range_results = results['metric_over_range_results']
        if 'max_val' in results:
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
        if all_trans == [] or self.checked_metrics == []:
            for i, data_store in enumerate(self.data_stores):
                axes = self.widget_row[i]['metrics']['range']['data']
                message_on_plot(axes, 'No Metrics/Transforms Selected')
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
        if all_trans == [] or self.checked_metrics == []:
            for i, data_store in enumerate(self.data_stores):
                axes = self.widget_row[i]['metrics']['avg']['data']
                message_on_plot(axes, 'No Metrics/Transforms Selected')
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
            for i, data_store in enumerate(self.data_stores):
                axes = self.widget_row[i]['metrics']['correlation']['data']
                message_on_plot(axes, 'No Metrics Loaded')
            return
        metric = self.checked_metrics[self.metric_correlation_graph_num]
        # calculate the metric values at the human score test values
        for i, data_store in enumerate(self.data_stores):
            if i in self.human_experiment_scores.keys():
                # calculate metric at HIQM values (if not already cached)
                if metric not in self.correlation_data[i].keys():
                    IQM_scores = plot_utils.compute_metric_for_human_correlation(data_store,
                                            self.checked_transformations,
                                            self.params_from_sliders['metric_params'],
                                            trans_str_values = self.human_experiment_scores[i]['mean'].keys(),
                                            metric=metric)
                    # cache it
                    self.correlation_data[i][metric] = IQM_scores
                plot = plot_utils.get_correlation_plot(self.human_experiment_scores[i],
                                                self.correlation_data[i],
                                                self.widget_row[i]['metrics']['correlation']['data'],
                                                metric,
                                                self.view_correlation_instance)
                if hasattr(self, 'human_scores_file'):
                    title = plot.ax.axes.get_title()
                    title = f"{title}\n{self.human_scores_file}"
                    plot.ax.axes.set_title(title, fontsize=8)
                plot.show()
            else:
                axes = self.widget_row[i]['metrics']['correlation']['data']
                message_on_plot(axes, 'Use Load Experiment Button below\nor File->Load Human Scores for a .csv')
                

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
        # load transform if not already on the UI
        trans_found = False
        for _, slider_group in self.sliders.items():
            for key, item_sliders in slider_group.items():
                if key == trans:
                    trans_found = True
        if trans_found == False: # need to load it
            all_trans_iqm_vis = IQM_Vis.transformations.get_all_transforms()
            if trans in self.menu_options['transforms']:
                self.menu_options['transforms'][trans].setChecked(True)
                self.construct_UI()
            elif trans in all_trans_iqm_vis:
                self.transformations[trans] = all_trans_iqm_vis[trans]
                self._remake_menu()
                self.menu_options['transforms'][trans].setChecked(True)
                self.construct_UI()
            else:
                self.update_status_bar(f"Transform '{trans}' not found - please load it!")

        # show the specific tranform image
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
    def stopped_range_worker(self, signal=False):
        self.worker_working = False

def message_on_plot(widget_axes, message):
    try:
        widget_axes.axes.clear()
    except AttributeError:
        pass
    widget_axes.axes.text(
        0.5, 0.5, message, horizontalalignment='center', verticalalignment='center')
    widget_axes.draw()