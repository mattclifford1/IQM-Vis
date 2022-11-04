'''
UI image functions
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

import os

import numpy as np

from IQM_VIS.utils import gui_utils


class app_images:
    def init_images(self, screen=False):
        '''
        make blank images to place on screen before actual image is chosen
        this creates the UI to be the correct size
        '''
        # make image placeholders
        self.height = int(256)
        self.width_ratio = 1
        self.width = int(self.height*self.width_ratio)

        # load images
        self.image_data = {}
        # self.im_pair_names = []
        for key in self.image_paths.keys():
            self.image_data[key] = self.image_paths[key]
            self.im_pair_names.append((key, 'T('+key+')'))

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
            metric_images = data_store.get_metric_images(trans_im)
            # self.compute_metrics()
            # self.update_image_widgets()

    def update_image_widgets(self):
        # display images
        # for key in self.image_data.keys():
        for i in self.widget_row.keys():
            gui_utils.change_im(self.widgets['image'][key], self.image_data[key], resize=self.image_display_size)
