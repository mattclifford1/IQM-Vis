'''
generic image and metric data class constructor
both use the same image for reference and transformed
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import imghdr
from functools import cache
from collections import namedtuple
import numpy as np
import pandas as pd
import IQM_Vis
from IQM_Vis.data_handlers import base_dataloader, base_dataset_loader


class cache_metric_call:
    ''' cache metric fucntions that have been calculated already
     to do this we need to convert numpy arrays to a hashable object (since arrs are mutable) 
     to achieve this we convert to a bytes array (input to __call__) then load this from buffer
     '''
    def __init__(self, metric):
        self.metric = metric
    
    @cache
    def __call__(self, ref, trans, **kwargs):
        # expect a hashable bytes array tuple as input with the data type and shape
        #  N.B. we need to copy the array since from buffer gives a read only array since
        #       it is a view of a bytes array (immutable)
        ref = np.frombuffer(ref.bytes, dtype=ref.dtype).reshape(ref.shape).copy()
        trans = np.frombuffer(trans.bytes, dtype=trans.dtype).reshape(trans.shape).copy()
        return self.metric(ref, trans, **kwargs)


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
                       image_pre_processing=None,  # apply a function to the image before transformations (e.g. resize to smaller)
                       image_post_processing=None,  # apply a function to the image after transformations (e.g. zoom to help with black boarders on rotation)
                       image_list_to_transform=None, # if you want to use a different image to transform than reference
                       human_exp_csv=None    # csv for where the human experiments file is
                       ):
        self.image_storer = namedtuple('image', ['name', 'data'])
        self.bytes_arrays = namedtuple('arr', ['bytes', 'dtype', 'shape'])
        self.image_loader = image_loader
        self.image_pre_processing = image_pre_processing
        self.load_image_list(image_list)
        if image_list_to_transform != None:
            self.image_list_to_transform = image_list_to_transform
            self._load_image_data(0)   # load the first transform image
        self.metrics = metrics
        for m in self.metrics:
            self.metrics[m] = cache_metric_call(self.metrics[m])
        self.metric_images = metric_images
        self.image_post_processing = image_post_processing
        self.image_post_processing_hash = None
        if human_exp_csv is not None:
            self.human_exp_df = pd.read_csv(human_exp_csv, index_col=0)

        self._check_inputs()

    def add_metric(self, key, value):
        if not isinstance(value, cache_metric_call):
            value = cache_metric_call(value)
        self.metrics[key] = value

    def add_metric_image(self, key, value):
        self.metric_images[key] = value

    def get_image_dataset_list(self):
        # get image file list
        return self.image_list

    def load_image_list(self, image_list):
        if len(image_list) == 0:
            if not hasattr(self, 'image_list'):
                raise ValueError(f'image_list is empty')
            else:
                return
        # remove any non image file paths
        just_images = []
        for image_file in image_list:
            try:
                image_format = imghdr.what(image_file)
            except FileNotFoundError:
                image_format = None
            if image_format != None:
                just_images.append(image_file)
        self.image_list = just_images
        self.image_list_to_transform = just_images
        self.image_names = [get_image_name(file) for file in self.image_list]
        self._load_image_data(0)


    def _load_image_data(self, i):
        # reference image
        self.image_post_processing_hash = None
        self.current_file = self.image_list[i]
        image_name_ref = get_image_name(self.current_file)
        image_data_ref = self.image_loader(self.current_file)
        self.reference_unprocessed = image_data_ref
        if self.image_pre_processing is not None:
            image_data_ref = self.image_pre_processing(image_data_ref)
        self.image_reference = self.image_storer(image_name_ref, image_data_ref)
        self.ref_bytes = self.bytes_arrays(
            image_data_ref.tobytes(), image_data_ref.dtype, image_data_ref.shape)

        # image to transform
        if self.current_file == self.image_list_to_transform[i]:
            self.image_to_transform = self.image_storer(image_name_ref, image_data_ref)
        else:
            image_name_trans = get_image_name(self.image_list_to_transform[i])
            image_data_trans = self.image_loader(self.image_list_to_transform[i])
            if self.image_pre_processing is not None:
                image_data_trans = self.image_pre_processing(image_data_trans)
            self.image_reference = self.image_storer(image_name_trans, image_data_trans)

        # Human experiments
        if hasattr(self, 'human_scores'):
            del self.human_scores  # delete old scores (incase we dont have ones for new image)
        if hasattr(self, 'human_exp_df'):
            if image_name_ref in self.human_exp_df.index:
                self.human_scores = {'mean': self.human_exp_df.loc[image_name_ref].to_dict()}

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, i):
        self._load_image_data(i)

    def get_reference_image_name(self):
        return self.image_reference.name
    
    def get_reference_unprocessed(self):
        return self.reference_unprocessed

    def get_reference_image(self):
        if hash(self.image_post_processing) != self.image_post_processing_hash:
            # need to post process ref image as either first call or post processing has changed
            self.image_reference_post_processed = self.image_reference.data.copy()
            if self.image_post_processing is not None:
                self.image_reference_post_processed = self.image_post_processing(
                    self.image_reference_post_processed)
            # cache the hash so we can test if the post processing changes
            self.image_post_processing_hash = hash(self.image_post_processing)
            # save the bytes array 
            self.ref_bytes = self.bytes_arrays(
                self.image_reference_post_processed.tobytes(), 
                self.image_reference_post_processed.dtype, 
                self.image_reference_post_processed.shape)
        return self.image_reference_post_processed

    def get_image_to_transform_name(self):
        return self.image_to_transform.name

    def get_image_to_transform(self):
        return self.image_to_transform.data

    def get_metrics(self, transformed_image, metrics_to_use='all', **kwargs):
        # convert array to hashable so we can cache already calculated
        trans_bytes = self.bytes_arrays(
            transformed_image.tobytes(), transformed_image.dtype, transformed_image.shape)
        # get metrics
        results = {}
        for metric in self.metrics:
            if metric in metrics_to_use or metrics_to_use == 'all':
                if self.ref_bytes.shape != trans_bytes.shape:
                    # There has been a change in the data so need to quit this calc ASAP
                    results[metric] = 100
                else:
                    # calc as normal
                    results[metric] = self.metrics[metric](
                        self.ref_bytes, trans_bytes, **kwargs)
        return results

    def get_metric_images(self, transformed_image, metrics_to_use='all', **kwargs):
        results = {}
        for metric in self.metric_images:
            if metric in metrics_to_use or metrics_to_use == 'all':
                results[metric] = self.metric_images[metric](self.get_reference_image(), transformed_image, **kwargs)
        return results

    def _check_inputs(self):
        input_types = [(self.image_reference.name, str),
                       (self.image_reference.data, np.ndarray),
                       (self.metrics, dict),
                       (self.metric_images, dict)]
        for item in input_types:
            if type(item[0]) != item[1]:
                var_name = f'{item[0]=}'.split('=')[0]
                raise TypeError(f'holder input: {var_name} should be a {item[1]} not {type(item[0])}')


def get_image_name(file_path):
    # get name of image from filepath
    return os.path.splitext(os.path.basename(file_path))[0]