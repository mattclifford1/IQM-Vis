# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

'''
Regression tests for dataset_holder data loading correctness.
'''
import numpy as np
import pytest
from IQM_Vis.data_handlers.data_api import dataset_holder
from IQM_Vis.examples.images import IMAGE1, IMAGE2


def test_separate_image_list_to_transform_sets_correct_names():
    """image_to_transform name should differ from reference when different images are given."""
    ds = dataset_holder([IMAGE1], image_list_to_transform=[IMAGE2])
    assert ds.get_reference_image_name() != ds.get_image_to_transform_name()


def test_separate_image_list_to_transform_sets_correct_data():
    """image data should differ when image_list_to_transform is a different image."""
    ds = dataset_holder([IMAGE1], image_list_to_transform=[IMAGE2])
    assert not np.array_equal(ds.get_reference_image(), ds.get_image_to_transform())


def test_separate_image_list_reference_unchanged():
    """Reference image should be IMAGE1 regardless of image_list_to_transform."""
    ds_same = dataset_holder([IMAGE1])
    ds_split = dataset_holder([IMAGE1], image_list_to_transform=[IMAGE2])
    assert np.array_equal(ds_same.get_reference_image(), ds_split.get_reference_image())
