'''
API to access making the PyQt6 UI for IQM-Vis
TODO: write docs on example usage/ what inputs etc. and what attributes that the data_store class needs
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import sys
import warnings
import types
import numpy as np

try:
    from PyQt6.QtWidgets import QApplication
    import IQM_Vis
    from IQM_Vis.UI.main import make_app
    from IQM_Vis.utils import image_utils
    import matplotlib
    matplotlib.use("Qt5Agg")
except ImportError:
    warnings.warn('Cannot load PyQt6 library - running IQM_Vis package in headless mode')

class make_UI:
    def __init__(self, 
                 data_store,
                 transformations: dict,
                 metrics_info_format: str='graph',
                 metrics_avg_graph: bool=True,
                 metric_params: dict={},
                 default_save_dir=IQM_Vis.utils.save_utils.DEFAULT_SAVE_DIR):
        self.data_store = data_store
        self.transformations = transformations
        self.metrics_info_format = metrics_info_format
        self.metrics_avg_graph = metrics_avg_graph
        self.metric_params = metric_params
        self.default_save_dir = default_save_dir
        self.show()

    def show(self):
        self._check_data_store()
        self._check_inputs()
        app = QApplication(sys.argv)
        window = make_app(app,
                          self.data_store,
                          self.transformations,
                          metrics_info_format=self.metrics_info_format,
                          metrics_avg_graph=self.metrics_avg_graph,
                          metric_params=self.metric_params,
                          default_save_dir=self.default_save_dir)
        sys.exit(app.exec())

    def _check_data_store(self):
        '''data store checking'''
        if type(self.data_store) != list:
            self.data_store = [self.data_store]

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
