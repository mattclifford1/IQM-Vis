'''
generic image and metric data class constructor
both use the same image for reference and transformed
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import numpy as np

'''
store image and metric data as well as
function calls for getting metrics and metric images
'''
class data_holder:
    def __init__(self, image_reference: tuple, # (name, np data)
                       image_to_transform: tuple, # (name, np data)
                       metrics: dict,
                       metric_images: dict):
        self.image_reference = image_reference
        self.image_to_transform = image_to_transform
        self.metrics = metrics
        self.metric_images = metric_images
        self._check_inputs()

    def get_reference_image_name(self):
        return self.image_reference[0]

    def get_reference_image(self):
        return self.image_reference[1]

    def get_transform_image_name(self):
        return self.image_to_transform[0]

    def get_transform_image(self):
        return self.image_to_transform[1]

    def get_metrics(self, transformed_image):
        results = {}
        for metric in self.metrics.keys():
            results[metric] = self.metrics[metric](self.get_reference_image(), transformed_image)
        return results

    def get_metric_images(self, transformed_image):
        results = {}
        for metric in self.metric_images.keys():
            results[metric] = self.metric_images[metric](self.get_reference_image(), transformed_image)
        return results

    def _check_inputs(self):
        input_types = [(self.image_reference[0], str),
                       (self.image_reference[1], np.ndarray),
                       (self.metrics, dict),
                       (self.metric_images, dict)]
        for item in input_types:
            if type(item[0]) != item[1]:
                var_name = f'{item[0]=}'.split('=')[0]
                raise TypeError('holder input: '+var_name+' should be a '+str(item[1])+' not '+str(type(item[0])))


'''
extension of data_holder that allows to iterate through a dataset
'''
class dataset_holder:
    def __init__(self, image_list: list, # list of image file names
                       image_loader,     # function to load image files
                       metrics: dict,
                       metric_images: dict):
        self.image_list = image_list
        self.image_loader = image_loader
        self._load_image_data(0)   # load the first image
        self.metrics = metrics
        self.metric_images = metric_images
        self._check_inputs()

    def _load_image_data(self, i):
        self.current_file = self.image_list[i]
        self.image_name = os.path.splitext(os.path.basename(self.current_file))[0]
        image_data = self.image_loader(self.current_file)
        self.image_reference = (self.image_name, image_data)
        self.image_to_transform = (self.image_name, image_data)

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, i):
        self._load_image_data(i)

    def get_reference_image_name(self):
        return self.image_reference[0]

    def get_reference_image(self):
        return self.image_reference[1]

    def get_transform_image_name(self):
        return self.image_to_transform[0]

    def get_transform_image(self):
        return self.image_to_transform[1]

    def get_metrics(self, transformed_image):
        results = {}
        for metric in self.metrics.keys():
            results[metric] = self.metrics[metric](self.get_reference_image(), transformed_image)
        return results

    def get_metric_images(self, transformed_image):
        results = {}
        for metric in self.metric_images.keys():
            results[metric] = self.metric_images[metric](self.get_reference_image(), transformed_image)
        return results

    def _check_inputs(self):
        input_types = [(self.image_reference[0], str),
                       (self.image_reference[1], np.ndarray),
                       (self.metrics, dict),
                       (self.metric_images, dict)]
        for item in input_types:
            if type(item[0]) != item[1]:
                var_name = f'{item[0]=}'.split('=')[0]
                raise TypeError('holder input: '+var_name+' should be a '+str(item[1])+' not '+str(type(item[0])))
