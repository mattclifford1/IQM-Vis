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
        self.im_pair_names = []
        for key in self.image_paths.keys():
            if os.path.exists(self.image_paths[key]):
                self.image_data[key] = self.image_loader(self.image_paths[key])
            else:
                print('Cannot find image file: ', self.image_paths[key])
                self.image_data[key] = np.zeros([128, 128, 1], dtype=np.uint8)
            self.im_pair_names.append((key, 'T('+key+')'))

    '''
    image updaters
    '''
    def transform_image(self, image):
        for key in self.sliders.keys():
            image = self.sliders[key]['function'](image, self.im_trans_params[key])
        return image

    def display_images(self):
        self.get_image_data()
        self.compute_metrics()
        self.update_image_widgets()

    def _display_images_quick(self):
        # dont calc metrics/errors - just update widgets
        self.get_image_data()
        self.update_image_widgets()

    def get_image_data(self):
        # get transformed images
        for key in self.image_paths.keys():
            self.image_data['T('+key+')'] = self.transform_image(self.image_data[key])

    def update_image_widgets(self):
        # display images
        for key in self.image_data.keys():
            gui_utils.change_im(self.widgets['image'][key], self.image_data[key], resize=self.image_display_size)
