'''
generic image and metric data class constructor
both use the same image for reference and transformed
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
from __future__ import annotations

import os
from functools import lru_cache
from collections import namedtuple
from typing import Callable, Optional
import numpy as np
import pandas as pd
import filetype
import IQM_Vis
from IQM_Vis.data_handlers import base_dataset_loader


# keep a track of all the cached functions so we can clear them easily
CACHED_FUNCTIONS = []


def cache_tracked(func: Callable) -> Callable:
    '''Decorator: wrap *func* with :func:`functools.lru_cache` and register it
    in ``CACHED_FUNCTIONS`` so the cache can be cleared later.'''
    cached_func = lru_cache(maxsize=None)(func)
    CACHED_FUNCTIONS.append(cached_func)
    return cached_func


class cache_metric_call:
    '''Cache metric function calls keyed on hashable byte-array representations
    of numpy arrays.

    Standard :func:`functools.lru_cache` cannot hash mutable numpy arrays.
    This class converts arrays to an immutable ``namedtuple`` of their raw
    bytes, dtype and shape before forwarding the call to the underlying metric.
    '''

    def __init__(self, metric: Callable) -> None:
        '''Args:
            metric: The metric callable to wrap and cache.
        '''
        self.metric = metric

    @cache_tracked
    def __call__(self, ref, trans, **kwargs) -> float:
        '''Call the metric, reconstructing numpy arrays from their byte representations.

        Args:
            ref: Hashable named-tuple with fields ``bytes``, ``dtype``, ``shape``
                representing the reference image.
            trans: Hashable named-tuple with the same fields for the transformed image.
            **kwargs: Extra keyword arguments forwarded to the metric.

        Returns:
            The metric score.
        '''
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
    def __init__(self, image_list: list,
                       metrics: dict = {},
                       metric_images: dict = {},
                       image_loader: Callable = IQM_Vis.utils.load_image,
                       image_pre_processing: Optional[Callable] = None,
                       image_post_processing: Optional[Callable] = None,
                       image_list_to_transform: Optional[list] = None,
                       human_exp_csv: Optional[str] = None) -> None:
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

    def add_metric(self, key: str, value: Callable) -> None:
        '''Add or replace a metric, wrapping it in :class:`cache_metric_call` if needed.

        Args:
            key: Name for the metric.
            value: Metric callable.
        '''
        if not isinstance(value, cache_metric_call):
            value = cache_metric_call(value)
        self.metrics[key] = value

    def add_metric_image(self, key: str, value: Callable) -> None:
        '''Add or replace a metric-image function.

        Args:
            key: Name for the metric image.
            value: Callable returning an image array.
        '''
        self.metric_images[key] = value

    def get_image_dataset_list(self) -> list:
        '''Return the list of image file paths in the dataset.'''
        return self.image_list

    def load_image_list(self, image_list: list) -> None:
        if len(image_list) == 0:
            if not hasattr(self, 'image_list'):
                raise ValueError(f'image_list is empty')
            else:
                return
        # remove any non image file paths
        just_images = []
        for image_file in image_list:
            try:
                image_guess = filetype.guess(image_file)
                image_format = image_guess.extension if image_guess else None
            except FileNotFoundError:
                image_format = None
            if image_format != None:
                just_images.append(image_file)
        self.image_list = just_images
        self.image_list_to_transform = just_images
        self.image_names = [get_image_name(file) for file in self.image_list]
        self._load_image_data(0)


    def _load_image_data(self, i: int) -> None:
        # reference image
        self.image_post_processing_hash = None
        self.current_file = self.image_list[i]
        image_name_ref = get_image_name(self.current_file)
        image_data_ref = self._cached_image_loader(self.current_file)
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
            image_data_trans = self._cached_image_loader(
                self.image_list_to_transform[i])
            if self.image_pre_processing is not None:
                image_data_trans = self.image_pre_processing(image_data_trans)
            self.image_to_transform = self.image_storer(image_name_trans, image_data_trans)

        # Human experiments
        if hasattr(self, 'human_scores'):
            del self.human_scores  # delete old scores (incase we dont have ones for new image)
        if hasattr(self, 'human_exp_df'):
            if image_name_ref in self.human_exp_df.index:
                self.human_scores = {'mean': self.human_exp_df.loc[image_name_ref].to_dict()}

    def __len__(self) -> int:
        return len(self.image_list)

    def __getitem__(self, i: int) -> None:
        self._load_image_data(i)

    @cache_tracked
    def _cached_image_loader(self, file_name: str) -> np.ndarray:
        return self.image_loader(file_name)

    def get_reference_image_by_index(self, index: int) -> np.ndarray:
        '''Return the reference image at the given dataset index.

        Args:
            index: Zero-based position in the image list.

        Returns:
            The loaded image as a float32 numpy array.

        Raises:
            IndexError: If *index* is out of range.
        '''
        if index >= len(self.image_list):
            raise IndexError('Index out of range of the length of the image list')
        file_name = self.image_list[index]
        image_data = self._cached_image_loader(file_name)
        return image_data

    def get_reference_image_name(self) -> str:
        '''Return the filename stem of the current reference image.'''
        return self.image_reference.name

    def get_reference_unprocessed(self) -> np.ndarray:
        '''Return the reference image before any pre-processing is applied.'''
        return self.reference_unprocessed

    def get_reference_image(self) -> np.ndarray:
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

    def get_image_to_transform_name(self) -> str:
        '''Return the filename stem of the current image-to-transform.'''
        return self.image_to_transform.name

    def get_image_to_transform(self) -> np.ndarray:
        '''Return the current image-to-transform as a float32 numpy array.'''
        return self.image_to_transform.data

    def get_metrics(self, transformed_image: np.ndarray, metrics_to_use: str | list = 'all', **kwargs) -> dict:
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

    def get_metric_images(self, transformed_image: np.ndarray, metrics_to_use: str | list = 'all', **kwargs) -> dict:
        results = {}
        for metric in self.metric_images:
            if metric in metrics_to_use or metrics_to_use == 'all':
                results[metric] = self.metric_images[metric](self.get_reference_image(), transformed_image, **kwargs)
        return results

    def _check_inputs(self) -> None:
        input_types = [(self.image_reference.name, str),
                       (self.image_reference.data, np.ndarray),
                       (self.metrics, dict),
                       (self.metric_images, dict)]
        for item in input_types:
            if type(item[0]) != item[1]:
                var_name = f'{item[0]=}'.split('=')[0]
                raise TypeError(f'holder input: {var_name} should be a {item[1]} not {type(item[0])}')
            
    def clear_all_cache(self) -> None:
        '''Clear all LRU caches tracked by :func:`cache_tracked`.'''
        for cached_func in CACHED_FUNCTIONS:
            cached_func.cache_clear()


def get_image_name(file_path: str) -> str:
    '''Return the filename stem (no directory, no extension) for an image path.

    Args:
        file_path: Path to the image file.

    Returns:
        The base filename without its extension.
    '''
    return os.path.splitext(os.path.basename(file_path))[0]