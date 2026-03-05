# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

'''
Regression tests for save_utils functions.
'''
import pandas as pd
import pytest
from IQM_Vis.utils.save_utils import save_2AFC_experiment_results


def test_save_2AFC_no_stdout_print(capsys, tmp_path):
    """Bug 6 regression: save_2AFC_experiment_results must not print to stdout."""
    trans_names = ['a', 'b']
    results_order = ['a', 'b']
    IQM_df = pd.DataFrame({'a': [0.5], 'b': [0.3]})
    save_2AFC_experiment_results(
        trans_names, results_order, str(tmp_path), IQM_scores_df=IQM_df
    )
    captured = capsys.readouterr()
    assert captured.out == ''
