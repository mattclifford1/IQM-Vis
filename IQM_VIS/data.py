'''
generic image and metric data class constructor
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import numpy as np

'''
store image and metric data as well as
function calls for getting metrics and metric images
'''
class data_holder:
    def __init__(self, image: tuple,   # (name, data)
                       metrics: dict,
                       metric_images: dict):
        self.image_name = image[0]
        self.image_data = image[1]
        self.metrics = metrics
        self.metric_images = metric_images
        self._check_inputs()

    def get_metrics(self, transformed_image):
        results = {}
        for metric in self.metrics.keys():
            results[metric] = self.metrics[metric](self.image_data, transformed_image)
        return results

    def get_metric_images(self, transformed_image):
        results = {}
        for metric in self.metric_images.keys():
            results[metric] = self.metric_images[metric](self.image_data, transformed_image)
        return results

    def _check_inputs(self):
        input_types = [(self.image_name, str),
                       (self.image_data, np.ndarray),
                       (self.metrics, dict),
                       (self.metric_images, dict)]
        for item in input_types:
            if type(item[0]) != item[1]:
                var_name = f'{item[0]=}'.split('=')[0]
                raise TypeError('holder input: '+var_name+' should be a '+str(item[1])+' not '+str(type(item[0])))
