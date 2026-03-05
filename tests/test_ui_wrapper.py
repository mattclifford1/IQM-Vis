# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

'''
Regression tests for validate_datastore_attributes validation logic.
'''
import numpy as np
import pytest
from IQM_Vis.ui_wrapper import validate_datastore_attributes
from IQM_Vis.data_handlers.data_api import dataset_holder
from IQM_Vis.examples.images import IMAGE1


class _BadTransformImage(dataset_holder):
    """Overrides get_image_to_transform to return wrong type."""
    def get_image_to_transform(self) -> str:
        return "not_an_array"


def test_validates_get_image_to_transform():
    """Bug 2 regression: get_image_to_transform must be validated, not get_reference_image twice."""
    bad_ds = _BadTransformImage([IMAGE1])
    with pytest.raises(TypeError) as exc_info:
        validate_datastore_attributes(bad_ds)
    assert "get_image_to_transform" in str(exc_info.value)


def test_error_message_contains_expected_and_actual_types():
    """Bug 3 regression: error message must name expected type (ndarray) and actual type (str)."""
    bad_ds = _BadTransformImage([IMAGE1])
    with pytest.raises(TypeError) as exc_info:
        validate_datastore_attributes(bad_ds)
    msg = str(exc_info.value)
    assert "ndarray" in msg
    assert "str" in msg
