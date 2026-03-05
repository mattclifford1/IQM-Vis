'''
utils for saving experiments, images and figures
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
from __future__ import annotations

import os
import json
import pickle
from typing import Any, Optional
import pandas as pd

from IQM_Vis.utils import image_utils

DEFAULT_SAVE_DIR = os.path.join(os.path.expanduser("~"), 'IQM-Vis')

# --- getters for experiment files from save dir ---

def get_human_scores_file(dir: str) -> str:
    '''Return the path to the human scores CSV for an experiment directory.'''
    last_dir = os.path.basename(os.path.normpath(dir))
    prefix = last_dir.split('-')[0]
    return os.path.join(dir, f'{prefix}-HUMAN-scores.csv')

def get_image_name_from_human_scores(dir: str) -> str:
    '''Return the image name encoded in the human-scores filename.'''
    file_path = get_human_scores_file(dir)
    return os.path.basename(file_path)[:-len('-HUMAN-scores.csv')]

def get_human_times_file(dir: str) -> str:
    '''Return the path to the human times-taken CSV for an experiment directory.'''
    last_dir = os.path.basename(os.path.normpath(dir))
    prefix = last_dir.split('-')[0]
    return os.path.join(dir, f'{prefix}-HUMAN-times-taken.csv')

def get_IQM_file(dir: str) -> str:
    '''Return the path to the IQM scores CSV for an experiment directory.'''
    last_dir = os.path.basename(os.path.normpath(dir))
    prefix = last_dir.split('-')[0]
    return os.path.join(dir, f'{prefix}-IQM-scores.csv')

def get_original_image_file(dir: str) -> str:
    '''Return the path to the reference image file in an experiment directory.'''
    return os.path.join(dir, 'reference.png')

def get_original_unprocessed_image_file(dir: str) -> str:
    '''Return the path to the unprocessed original image in an experiment directory.'''
    last_dir = os.path.basename(os.path.normpath(dir))
    prefix = last_dir.split('-')[0]
    return os.path.join(dir, f'{prefix}.png')

def get_image_processing_file(dir: str) -> str:
    '''Return the path to the image-processing JSON in an experiment directory.'''
    return os.path.join(dir, 'transforms', 'processing.json')

def get_transform_params_file(dir: str) -> str:
    '''Return the path to the transform-parameters pickle in an experiment directory.'''
    return os.path.join(dir, 'transforms', 'transform_params.pkl')

def get_transform_functions_file(dir: str) -> str:
    '''Return the path to the transform-functions pickle in an experiment directory.'''
    return os.path.join(dir, 'transforms', 'transform_functions.pkl')

# --- other save helpers ---

def save_obj(pickle_path: str, trans: Any) -> None:
    '''Save an object to a pickle file.

    Args:
        pickle_path: Destination file path.
        trans: Object to serialise.
    '''
    with open(pickle_path, 'wb') as file:
        pickle.dump(trans, file)

def load_obj(pickle_path: str) -> Optional[Any]:
    '''Load an object from a pickle file, returning ``None`` on failure.

    Args:
        pickle_path: Path to the pickle file.

    Returns:
        The deserialised object, or ``None`` if the file does not exist or
        cannot be loaded.
    '''
    if not os.path.exists(pickle_path):
        return None
    try:
        with open(pickle_path, 'rb') as file:
            trans = pickle.load(file)
        return trans
    except:
        return None

def get_JND_image_names(dir: str) -> Optional[list]:
    '''Return the list of image filenames in the JND reference-images directory.

    Args:
        dir: Experiment save directory.

    Returns:
        A list of filenames, or ``None`` if the directory does not exist.
    '''
    images_dir = get_JND_ref_image_dir(dir)
    if not os.path.exists(images_dir):
        return None
    try:
        # get all file names in the directory
        return os.listdir(images_dir)
    except:
        return None

def get_JND_ref_image_dir(dir: str) -> str:
    '''Return the path to the JND reference-images sub-directory.'''
    return os.path.join(dir, 'reference_images')

def get_JND_ref_image_unprocessed_dir(dir: str) -> str:
    '''Return the path to the JND unprocessed reference-images sub-directory.'''
    return os.path.join(dir, 'reference_images_unprocessed')


def save_df_as_csv(df: pd.DataFrame, file: str, index: bool = False) -> None:
    '''Append *df* to an existing CSV file (or create it if absent).

    Args:
        df: DataFrame to save.
        file: Destination CSV file path.
        index: Whether to write the row index. Defaults to ``False``.
    '''
    if os.path.exists(file):
        df_saved = pd.read_csv(file)
        df = pd.concat([df_saved, df])
    df.to_csv(file, index=index)


def save_and_merge_df_as_csv(df: pd.DataFrame, file: str) -> None:
    '''Merge an indexed *df* with an existing CSV, then save.

    Args:
        df: Indexed DataFrame to merge and save.
        file: Destination CSV file path.
    '''
    if os.path.exists(file):
        df_saved = pd.read_csv(file)
        index_name = df.index.name
        df = pd.merge(df.reset_index(), df_saved, how='outer')
        df.set_index(index_name, inplace=True)
    df.to_csv(file, index=True)


def save_and_merge_rm_duplicates_df_as_csv(df: pd.DataFrame, file: str) -> None:
    '''Merge *df* with an existing CSV, remove duplicate index entries, then save.

    Args:
        df: Indexed DataFrame to merge and save.
        file: Destination CSV file path.
    '''
    if os.path.exists(file):
        df_saved = pd.read_csv(file)
        index_name = df.index.name
        df = pd.merge(df.reset_index(), df_saved, how='outer')
        df.set_index(index_name, inplace=True)
        # remove duplicates
        df = df[~df.index.duplicated(keep='last')]
    # sort columns for consistency
    cols = df.columns.tolist()
    cols.sort()
    df.to_csv(file, index=True, columns=cols)


def get_JND_user_ID(dir: str) -> int:
    '''Return the next available user ID for a JND experiment directory.

    Args:
        dir: Experiment save directory.

    Returns:
        1 if no scores file exists yet, otherwise ``max(User ID) + 1``.
    '''
    human_experiment_csv_file = get_human_scores_file(dir)
    if not os.path.exists(human_experiment_csv_file):
        return 1
    df = pd.read_csv(human_experiment_csv_file)
    # get the last user ID
    return df['User ID'].max() + 1

def save_JND_experiment_results(experiment_results: list,
                                save_dir: str,
                                IQM_scores_df: Optional[pd.DataFrame] = None) -> str:
    '''Save JND experiment results to CSV files.

    Args:
        experiment_results: List of result dicts, each containing
            ``ref_name``, ``user_decision``, ``transform_name``,
            ``transform_value``, and ``time_taken``.
        save_dir: Directory to write the output CSV files into.
        IQM_scores_df: Optional DataFrame of IQM scores to merge and save.

    Returns:
        Path to the human-scores CSV file that was written.
    '''
    # User ID
    ID = get_JND_user_ID(save_dir)
    results = {'ImageName': [],
               'UserDecision': [],
               'Transform': [],
               'TimeTaken': [],
               'User ID': []}
    for image_data in experiment_results:
        results['ImageName'].append(image_data['ref_name'])
        results['UserDecision'].append(image_data['user_decision'])
        results['Transform'].append(make_name_for_trans(image_data))
        results['TimeTaken'].append(image_data['time_taken'])
        results['User ID'].append(ID)
        # results[make_name_for_trans(image_data)] = [image_data['user_decision']]

    # make df
    df = pd.DataFrame.from_dict(results)
    # save results
    human_experiment_csv_file = get_human_scores_file(save_dir)
    save_df_as_csv(df, human_experiment_csv_file, index=False)

    # save IQM results
    if not isinstance(IQM_scores_df, type(None)) and not IQM_scores_df.empty:
        IQM_file = get_IQM_file(save_dir)
        save_and_merge_rm_duplicates_df_as_csv(IQM_scores_df, IQM_file)

    return human_experiment_csv_file

    
def save_2AFC_experiment_results(trans_names: list,
                                 results_order: list,
                                 save_dir: str,
                                 times_taken: Optional[list] = None,
                                 IQM_scores_df: Optional[pd.DataFrame] = None) -> str:
    '''Save 2-AFC experiment results to CSV files.

    Args:
        trans_names: Ordered list of transform names used in the experiment.
        results_order: List of transform names in the order chosen by the
            participant (best to worst).
        save_dir: Directory to write output CSV files into.
        times_taken: Optional list of per-comparison times (seconds).
        IQM_scores_df: Optional DataFrame of IQM scores to merge and save.

    Returns:
        Path to the human-scores CSV file that was written.
    '''
    # make HIQM scores from ordering : HIQM = pos/num_pos
    results = {}
    for i, trans_name in enumerate(results_order):
        results[str(trans_name)] = [(i+1) / len(results_order)]

    # make df
    df = pd.DataFrame.from_dict(results)
    # re order so that the trans_names are acending order as given
    df = df[trans_names]
    # save results
    human_experiment_csv_file = get_human_scores_file(save_dir)
    save_df_as_csv(df, human_experiment_csv_file, index=False)

    # save times taken
    if times_taken != None:
        times_file = get_human_times_file(save_dir)
        data = {'mean time (seconds)': [sum(times_taken)/len(times_taken)],
                'total time (seconds)': [sum(times_taken)],
                'number of comparisons': [len(times_taken)],
                'individual times (seconds)': [str(times_taken)]}
        save_df_as_csv(pd.DataFrame.from_dict(data), times_file)

    # save IQM results
    if not isinstance(IQM_scores_df, type(None)) and not IQM_scores_df.empty:
        IQM_file = get_IQM_file(save_dir)
        save_and_merge_rm_duplicates_df_as_csv(IQM_scores_df, IQM_file)

    return human_experiment_csv_file

def save_json_dict(path: str, dict_: dict) -> None:
    '''Serialise *dict_* to a JSON file at *path*.'''
    with open(path, 'w') as fp:
        json.dump(dict_, fp)

def load_json_dict(path: str) -> dict:
    '''Load and return a JSON dict from *path*.'''
    with open(path, 'r') as fp:
        return json.load(fp)

def make_name_for_trans(trans: dict) -> str:
    '''Build a canonical string key for a transform result dict.

    Args:
        trans: Dict with ``transform_name`` and ``transform_value`` keys.

    Returns:
        A string of the form ``"<name><><value>"``.
    '''
    # splitter = '-----'
    splitter = '<>'
    return f"{trans['transform_name']}{splitter}{trans['transform_value']}"
