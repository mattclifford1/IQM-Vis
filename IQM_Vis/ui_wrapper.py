'''
API to access making the PyQt6 UI for IQM-Vis
TODO: write docs on example usage/ what inputs etc. and what attributes that the data_store class needs
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import sys
from typing import Any
import warnings
import types
import numpy as np

try:
    from PyQt6.QtWidgets import QApplication
    import IQM_Vis
    from IQM_Vis.UI.main import make_app
    from IQM_Vis.utils import image_utils
    from IQM_Vis.examples.images import DEFAULT_IMAGES
    import matplotlib
    matplotlib.use("Qt5Agg")
except ImportError:
    warnings.warn('Cannot load PyQt6 library - running IQM_Vis package in headless mode')

class make_UI:
    def __init__(self, 
                 data_store=None,
                 transformations=None,
                 image_list: list=DEFAULT_IMAGES,
                 metrics: dict={},
                 metric_images: dict={},
                 metrics_info_format: str='graph',
                 metrics_avg_graph: bool=True,
                 metric_params: dict={},
                 default_save_dir=IQM_Vis.utils.save_utils.DEFAULT_SAVE_DIR,
                 restrict_options=None,
                 num_steps_range=11,
                 debug=False):
        if data_store == None:
            data_store = IQM_Vis.dataset_holder(image_list,
                                   metrics,
                                   metric_images)
        self.data_store = data_store
        self.transformations = transformations
        self.metrics_info_format = metrics_info_format
        self.metrics_avg_graph = metrics_avg_graph
        self.metric_params = metric_params
        self.default_save_dir = default_save_dir
        self.restrict_options = restrict_options
        self.num_steps_range = num_steps_range
        self.debug = debug
        self.show()

    def show(self):
        self._check_restrict_options()
        self._check_data_store()
        self._check_trans()
        if self.debug:
            self._check_inputs()
        app = QApplication(sys.argv)
        window = make_app(app,
                          self.data_store,
                          self.transformations,
                          metrics_info_format=self.metrics_info_format,
                          metrics_avg_graph=self.metrics_avg_graph,
                          metric_params=self.metric_params,
                          default_save_dir=self.default_save_dir,
                          restrict_options=self.restrict_options,
                          num_steps_range=self.num_steps_range)
        sys.exit(app.exec())

    def _check_restrict_options(self):
        if self.restrict_options == None:
            trans = len(self.transformations) if self.transformations != None else 0
            if isinstance(self.data_store, list):
                metrics = len(self.data_store[0].metrics)
                metric_images = len(self.data_store[0].metric_images)
            else:
                metrics = len(self.data_store.metrics) if self.data_store != None else 0
                metric_images = len(self.data_store.metric_images) if self.data_store != None else 0

            self.restrict_options = {'transforms': trans,
                                     'metrics': metrics,
                                     'metric_images': metric_images}
        if isinstance(self.restrict_options, int):
            self.restrict_options = {'transforms': self.restrict_options,
                                     'metrics': self.restrict_options,
                                     'metric_images': self.restrict_options}



    def _check_data_store(self):
        '''data store checking'''
        if self.data_store == None:
            self.data_store = IQM_Vis.dataset_holder(IQM_Vis.examples.images.DEFAULT_IMAGES,
                IQM_Vis.metrics.get_all_metrics(),
                IQM_Vis.metrics.get_all_metric_images()
                )
            if self.metric_params == {}:
                self.metric_params = IQM_Vis.metrics.get_all_IQM_params()
        if not isinstance(self.data_store, list):
            self.data_store = [self.data_store]

    def _check_trans(self):
        if self.transformations == None:
            self.transformations = IQM_Vis.transformations.get_all_transforms()
        # make sure to wrap all transforms in clip so they don't go beyond data limits
        for trans, data in self.transformations.items():
            self.transformations[trans]['function'] = transform_wrapper(data['function'])

    def _check_inputs(self):
        for item in self.data_store:
            test_datastore_attributes(item)
        '''input items that should be dictionaries'''
        should_be_dict = [self.transformations, self.metric_params]
        for item in should_be_dict:
            if not isinstance(item, dict):
                var_name = f'{item=}'.split('=')[0]
                raise TypeError('make_UI input: '+var_name+' should be a dictionary not '+str(type(item)))
            # elif len(item.keys()) == 0:
            #     var_name = f'{item=}'.split('=')[0]
            #     warnings.warn(f'make_UI input: {var_name} is empty')

        '''extra input option checks'''
        if type(self.metrics_info_format) != str:
            var_name = f'{self.metrics_info_format=}'.split('=')[0]
            raise TypeError('make_UI input: '+var_name+' should be a string not '+str(type(self.metrics_info_format)))
        if type(self.metrics_avg_graph) != bool:
            var_name = f'{self.metrics_info_format=}'.split('=')[0]
            raise TypeError('make_UI input: '+var_name+' should be a bool not '+str(type(self.metrics_info_format)))


def test_datastore_attributes(data_store):
    '''get the data handler class to make sure its properties are correct'''
    obj_name = data_store.__class__.__name__
    attributes = [
    ('get_reference_image', 'gets the input reference image', types.MethodType),
    ('get_reference_image_name', 'gets the name of the input reference image', types.MethodType),
    ('get_image_to_transform', 'gets the input image to transform', types.MethodType),
    ('get_image_to_transform_name', 'gets the name of the input image to transform', types.MethodType),
    ('metrics', 'is a dict of all metric functions', dict),
    ('metric_images','is a dict of all metric image functions', dict),
    ('get_metrics', 'is a function that returns a dict of all metrics results', types.MethodType),
    ('get_metric_images', 'is a function that returns a dict of all metric image results', types.MethodType),
    ]
    for att in attributes:
        if hasattr(data_store,  att[0]):
            attr = getattr(data_store,  att[0])
            if type(attr) != att[2]:
                raise TypeError(f"{obj_name} attribute '{att[0]}' needs to be type '{att[2]}' instead of {type(attr)}")
        else:
            raise AttributeError(f"{obj_name} needs to have attribute '{att[0]}' which {att[1]}")

    # now test returned types are correct
    method_return_types = [
    ('get_reference_image', np.ndarray),
    ('get_reference_image_name', str),
    ('get_reference_image', np.ndarray),
    ('get_image_to_transform_name', str),
    ('get_metrics', dict, image_utils.get_transform_image(data_store, {}, {})),
    ('get_metric_images', dict, image_utils.get_transform_image(data_store, {}, {})),
    ]
    for meth in method_return_types:
        method = getattr(data_store,  meth[0])
        if len(meth) < 3:
            ret = method()
        elif len(meth) == 3:
            ret = method(meth[2])
        if type(ret) != meth[1]:
            raise TypeError(f"{obj_name} method '{meth[0]}' needs to return type '{att[2]}' instead of {type(attr)}")


class transform_wrapper:
    ''' wrap transforms to make sure they return an image between [0, 1] '''
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        called = self.function(*args, **kwargs)
        return np.clip(called, 0, 1)
    
    def __eq__(self, other):
        if isinstance(other, transform_wrapper):
            return self.function == other.function
        else:
            # unwrapped tranform function
            return self.function == other