'''
generic image and metric data class constructor
both use the same image for reference and transformed
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import numpy as np
import IQM_Vis
from IQM_Vis.data_handlers import base_dataloader, base_dataset_loader


class dataset_holder(base_dataset_loader):
    '''Stores images and metrics to communicate with the UI via the IQM-Vis data
       API.

       Args:
           image_list (list): list of image file paths
           metrics (dict): dictionary with keys of the metric names and values
                           of the callable metric function
           metric_images (dict): Optional dictionary with keys of the metric
                                 image names and values of the callable metric
                                 image function (Defaults to {})
           image_loader (function): Optional function which loads an image from
                                    a file path (Defaults to IQM_Vis.utils.load_image)
           image_post_processing (function): Optional function to apply after image
                 transformations. For example cropping an image after rotation.
                 (Defaults to None)
           image_list_to_transform (list): list of image file paths for images
                                to transform if they are different to the reference
                                images. If None then will use the same image as
                                the reference image. (Defaults to None)
    '''
    def __init__(self, image_list: list, # list of image file names
                       metrics: dict={},
                       metric_images: dict={},
                       image_loader=IQM_Vis.utils.load_image,     # function to load image files
                       image_post_processing=None,  # apply a function to the image after transformations (e.g. zoom to help with black boarders on rotation)
                       image_list_to_transform=None, # if you want to use a different image to transform than reference
                       ):
        self.image_list = image_list
        if image_list_to_transform == None:
            self.image_list_to_transform = image_list
        else:
            self.image_list_to_transform = image_list_to_transform
        if len(self.image_list) == 0:
            raise ValueError(f'image_list is empty')
        self.image_loader = image_loader
        self._load_image_data(0)   # load the first image
        self.metrics = metrics
        self.metric_images = metric_images
        self.image_post_processing = image_post_processing
        self._check_inputs()

    def _load_image_data(self, i):
        # reference image
        self.current_file = self.image_list[i]
        self.image_name = os.path.splitext(os.path.basename(self.current_file))[0]
        image_data = self.image_loader(self.current_file)
        self.image_reference = (self.image_name, image_data)
        # image to transform
        if self.current_file == self.image_list_to_transform[i]:
            self.image_to_transform = (self.image_name, image_data)
        else:
            image_name = os.path.splitext(os.path.basename(self.image_list_to_transform[i]))[0]
            image_data = self.image_loader(self.image_list_to_transform[i])
            self.image_reference = (self.image_name, image_data)

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, i):
        self._load_image_data(i)

    def get_reference_image_name(self):
        return self.image_reference[0]

    def get_reference_image(self):
        im = self.image_reference[1]
        if self.image_post_processing is not None:
            im = self.image_post_processing(im)
        return im

    def get_image_to_transform_name(self):
        return self.image_to_transform[0]

    def get_image_to_transform(self):
        return self.image_to_transform[1]

    def get_metrics(self, transformed_image, metrics_to_use='all', **kwargs):
        results = {}
        for metric in self.metrics:
            if metric in metrics_to_use or metrics_to_use == 'all':
                results[metric] = self.metrics[metric](self.get_reference_image(), transformed_image, **kwargs)
        return results

    def get_metric_images(self, transformed_image, metrics_to_use='all', **kwargs):
        results = {}
        for metric in self.metric_images:
            if metric in metrics_to_use or metrics_to_use == 'all':
                results[metric] = self.metric_images[metric](self.get_reference_image(), transformed_image, **kwargs)
        return results

    def _check_inputs(self):
        input_types = [(self.image_reference[0], str),
                       (self.image_reference[1], np.ndarray),
                       (self.metrics, dict),
                       (self.metric_images, dict)]
        for item in input_types:
            if type(item[0]) != item[1]:
                var_name = f'{item[0]=}'.split('=')[0]
                raise TypeError(f'holder input: {var_name} should be a {item[1]} not {type(item[0])}')
