'''
API to access making the PyQt6 UI for IQM-Vis
TODO: write dev_resources/docs on example usage/ what inputs etc. and what attributes that the data_store class needs
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
from __future__ import annotations

import subprocess
import platform
import sys
from typing import Any, Callable
import warnings
import types
import numpy as np

try:
    from PyQt6.QtWidgets import QApplication
    import IQM_Vis
    from IQM_Vis.utils import image_utils
    import matplotlib
    matplotlib.use("Qt5Agg")
except ImportError:
    warnings.warn('Cannot load PyQt6 library - running IQM_Vis package in headless mode')
    
from IQM_Vis.UI.main import make_app
from IQM_Vis.examples.images import DEFAULT_IMAGES


class make_UI:
    def __init__(self,
                 data_store: dataset_holder | list | None = None,
                 transformations: dict | None = None,
                 image_list: list = DEFAULT_IMAGES,
                 metrics: dict = {},
                 metric_images: dict = {},
                 metrics_info_format: str = 'graph',
                 metrics_avg_graph: bool = True,
                 metric_params: dict = {},
                 default_save_dir: str = IQM_Vis.utils.save_utils.DEFAULT_SAVE_DIR,
                 default_dataset_name: str = 'dataset1',
                 restrict_options: dict | int | None = None,
                 num_steps_range: int = 11,
                 debug: bool = False,
                 test: bool = False) -> None:
        '''Launch the IQM-Vis PyQt6 UI.

        Args:
            data_store: A :class:`dataset_holder` instance, a list of
                :class:`dataset_holder` instances, or ``None`` (in which case
                the default images and all built-in metrics are used).
            transformations: Dict mapping transform names to dicts with keys
                ``function``, ``min``, ``max``, and optionally ``init_value``
                and ``normalise``. Defaults to all built-in transforms when
                ``None``.
            image_list: List of image file paths used when *data_store* is
                ``None``.
            metrics: Dict of metric name to callable, used when *data_store*
                is ``None``.
            metric_images: Dict of metric-image name to callable, used when
                *data_store* is ``None``.
            metrics_info_format: Display format for metric results. One of
                ``'graph'``, ``'radar'``, or ``'text'``.
            metrics_avg_graph: Whether to display the average metrics graph.
            metric_params: Dict of parameter-slider definitions shared by
                metrics (e.g. SSIM kernel parameters).
            default_save_dir: Directory for saving experiment results.
            default_dataset_name: Name prefix for the saved dataset.
            restrict_options: Maximum number of transforms/metrics/metric
                images to show in the UI. Provide an ``int`` to apply the same
                limit to all three, or a ``dict`` with keys ``'transforms'``,
                ``'metrics'``, and ``'metric_images'``.
            num_steps_range: Number of steps used for the average-metrics
                range plot.
            debug: If ``True``, run extra input validation before launching
                the UI.
            test: If ``True``, do not enter the Qt event loop (used in
                automated tests).
        '''
        if data_store is None:
            data_store = IQM_Vis.dataset_holder(image_list,
                                   metrics,
                                   metric_images)
        self.data_store = data_store
        self.transformations = transformations
        self.metrics_info_format = metrics_info_format
        self.metrics_avg_graph = metrics_avg_graph
        self.metric_params = metric_params
        self.default_save_dir = default_save_dir
        self.default_dataset_name = default_dataset_name
        self.restrict_options = restrict_options
        self.num_steps_range = num_steps_range
        self.debug = debug
        self.test = test
        check_pyqt_install_deps()
        self.show()
        self.showing = True

    def show(self) -> None:
        '''Build and display the UI window, entering the Qt event loop unless
        ``test=True`` was passed to :meth:`__init__`.'''
        self._check_restrict_options()
        self._check_data_store()
        self._check_trans()
        if self.debug:
            self._check_inputs()
        self.app = QApplication(sys.argv)
        self.window = make_app(self.app,
                               self.data_store,
                               self.transformations,
                               metrics_info_format=self.metrics_info_format,
                               metrics_avg_graph=self.metrics_avg_graph,
                               metric_params=self.metric_params,
                               default_save_dir=self.default_save_dir,
                               default_dataset_name=self.default_dataset_name,
                               restrict_options=self.restrict_options,
                               num_steps_range=self.num_steps_range,
                               test=self.test)
        if self.test is False:
            sys.exit(self.app.exec())

    def _check_restrict_options(self) -> None:
        '''Normalise ``restrict_options`` to a dict keyed by component name.'''
        if self.restrict_options is None:
            trans = len(self.transformations) if self.transformations is not None else 0
            if isinstance(self.data_store, list):
                metrics = len(self.data_store[0].metrics)
                metric_images = len(self.data_store[0].metric_images)
            else:
                metrics = len(self.data_store.metrics) if self.data_store is not None else 0
                metric_images = len(self.data_store.metric_images) if self.data_store is not None else 0

            self.restrict_options = {'transforms': trans,
                                     'metrics': metrics,
                                     'metric_images': metric_images}
        if isinstance(self.restrict_options, int):
            self.restrict_options = {'transforms': self.restrict_options,
                                     'metrics': self.restrict_options,
                                     'metric_images': self.restrict_options}



    def _check_data_store(self) -> None:
        '''Ensure ``self.data_store`` is a non-empty list of data-store objects,
        falling back to the default dataset when none was supplied.'''
        if self.data_store is None:
            self.data_store = IQM_Vis.dataset_holder(IQM_Vis.examples.images.DEFAULT_IMAGES,
                IQM_Vis.metrics.get_all_metrics(),
                IQM_Vis.metrics.get_all_metric_images()
                )
            if self.metric_params == {}:
                self.metric_params = IQM_Vis.metrics.get_all_IQM_params()
        if not isinstance(self.data_store, list):
            self.data_store = [self.data_store]

    def _check_trans(self) -> None:
        '''Ensure ``self.transformations`` is set and all transform functions are
        wrapped with :class:`transform_wrapper` to clip outputs to [0, 1].'''
        if self.transformations is None:
            self.transformations = IQM_Vis.transforms.get_all_transforms()
        # make sure to wrap all transforms in clip so they don't go beyond data limits
        for trans, data in self.transformations.items():
            self.transformations[trans]['function'] = transform_wrapper(data['function'])

    def _check_inputs(self) -> None:
        '''Validate all UI inputs, raising :exc:`TypeError` on type mismatches.'''
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


def test_datastore_attributes(data_store: Any) -> None:
    '''Validate that a data-store object exposes the required IQM-Vis API.

    Checks that all mandatory attributes and methods are present with the
    correct types, and that the return types of key methods are correct.

    Args:
        data_store: Any object intended to be used as a data store with the
            IQM-Vis UI.

    Raises:
        AttributeError: If a required attribute is missing.
        TypeError: If an attribute has the wrong type or a method returns the
            wrong type.
    '''
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
    ('get_image_to_transform', np.ndarray),
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
            raise TypeError(f"{obj_name} method '{meth[0]}' needs to return type '{meth[1]}' instead of {type(ret)}")


class transform_wrapper:
    '''Wrap a transform function so its output is always clipped to [0, 1].'''

    def __init__(self, function: Callable) -> None:
        '''Args:
            function: The transform callable to wrap.
        '''
        self.function = function

    def __call__(self, *args, **kwargs) -> np.ndarray:
        '''Call the wrapped transform and clip the result to [0, 1].'''
        called = self.function(*args, **kwargs)
        return np.clip(called, 0, 1)

    def __eq__(self, other: object) -> bool:
        '''Compare equality against another wrapper or a raw callable.'''
        if isinstance(other, transform_wrapper):
            return self.function == other.function
        else:
            # unwrapped tranform function
            return self.function == other


def check_pyqt_install_deps() -> bool:
    '''Check that required system libraries for PyQt6 are installed (Linux only).

    On Debian-based Linux systems, PyQt6 may require ``libxcb-cursor0``. This
    function checks whether the package is present and prints a warning if not,
    to give a helpful message before a potential crash.

    Returns:
        ``True`` if the platform is not Linux or the package is present,
        ``False`` if the required package is missing.
    '''
    system_info = platform.system()
    if not system_info == "Linux":
        return True
    
    # if on linux try see if package installed (only for debian based)
    package_name = "libxcb-cursor0"
    installed = False
    try:
        result = subprocess.run(["dpkg", "-l", package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        installed = "ii" in result.stdout
    except subprocess.CalledProcessError:
        installed = False
    if installed == False:
        print(f"{'*'*30}\n\nWarning: not all dependencies are installed. If you get an 'Aborted (core dumped)' error below this message then please install them using:\n\n 'sudo apt install libxcb-cursor0'\n\n\n{'*'*30}\n\n")
