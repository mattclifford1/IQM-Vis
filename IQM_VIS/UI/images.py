'''
UI image functions
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

import os

import numpy as np
from PyQt6.QtWidgets import QApplication

from IQM_VIS.utils import gui_utils, plot_utils

# sub class used by IQM_VIS.main.make_app to control all of the image widgets
class images:
    def __init__(self):
        self.image_display_size = (175, 175)
        # self.image_display_size = False
    '''
    image updaters
    '''
    def transform_image(self, image):
        for key in self.sliders.keys():
            image = self.sliders[key]['function'](image, self.im_trans_params[key])
        return image

    def display_images(self):
        for i, data_store in enumerate(self.data_stores):
            gui_utils.change_im(self.widget_row[i]['images'][data_store.image_name]['data'], data_store.image_data, resize=self.image_display_size)
            trans_im = self.transform_image(data_store.image_data)
            gui_utils.change_im(self.widget_row[i]['images'][gui_utils.get_transformed_image_name(data_store.image_name)]['data'], trans_im, resize=self.image_display_size)

            metrics = data_store.get_metrics(trans_im)
            self.display_metrics(metrics, i)
            metric_images = data_store.get_metric_images(trans_im)
            self.display_metric_images(metric_images, i)

            QApplication.processEvents()   # force to change other UI wont respond

    def update_image_widgets(self):
        # display images
        for i in self.widget_row.keys():
            gui_utils.change_im(self.widgets['image'][key], self.image_data[key], resize=self.image_display_size)

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
                                        ax=self.widget_row[i]['metrics']['info']['data'])
        bar_plt.plot('', list(metrics.values()))
        bar_plt.show()

    def display_metrics_text(self, metrics, i, disp_len=5):
        text = ''
        for key in metrics.keys():
            metric = gui_utils.str_to_len(str(metrics[key]), disp_len, '0')
            text += key + ': ' + metric + '\n'
        self.widget_row[i]['metrics']['info']['data'].setText(text)

    '''
    metric image updaters
    '''
    def display_metric_images(self, metric_images, i):
        for key in metric_images.keys():
            widget = self.widget_row[i]['metric_images'][key]['data']
            gui_utils.change_im(widget, metric_images[key], resize=self.image_display_size)

    '''
    metric averaging plots
    '''
    def get_metrics_over_range(self):
        # compute all metrics over their range of params and get avg/std
        results = {}
        # initialise results
        for i, data_store in enumerate(self.data_stores):
            results[i] = {}
            for metric in data_store.metrics.keys():
                results[i][metric] = {}
                for trans in self.sliders.keys():
                    results[i][metric][trans] = []

        # compute over all image transformations
        for i, data_store in enumerate(self.data_stores):
            for curr_trans in self.sliders.keys():
                for trans_value in self.sliders[curr_trans]['values']:
                    trans_im = self.transform_image(data_store.image_data)
                    for other_trans in self.sliders.keys():
                        if other_trans != curr_trans:
                            ui_slider_value = self.im_trans_params[other_trans]
                            trans_im = self.sliders[other_trans]['function'](trans_im, ui_slider_value)
                        else:
                            trans_im = self.sliders[curr_trans]['function'](trans_im, trans_value)
                    metric_scores = data_store.get_metrics(trans_im)
                    for metric in metric_scores.keys():
                        results[i][metric][curr_trans].append(float(metric_scores[metric]))
            self.plot_metrics_graphs(results, i, list(data_store.metrics.keys()))

    def plot_metrics_graphs(self, results, i, metrics_names):
        radar_plotter = plot_utils.radar_plotter(radar_names=metrics_names,
                                        var_names=list(self.sliders.keys()),
                                        ax=self.widget_row[i]['metrics']['avg']['data'])
        for metric in metrics_names:
            mean_value = []
            # std_value = []
            transform = []
            for trans in self.sliders.keys():
                transform.append(trans)
                mean_value.append(np.mean(results[i][metric][trans]))
                # std_value.append(np.std(results[i][metric][trans]))
            radar_plotter.plot(metric, mean_value)
        radar_plotter.show()
