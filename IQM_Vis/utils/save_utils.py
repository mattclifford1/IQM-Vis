'''
utils for saving experiments, images and figures
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

import os
import json
import pickle
import pandas as pd

from IQM_Vis.utils import image_utils

DEFAULT_SAVE_DIR = os.path.join(os.path.expanduser("~"), 'IQM-Vis')

''' getters for experiment files from save dir '''
def get_human_scores_file(dir):
    last_dir = os.path.basename(os.path.normpath(dir))
    prefix = last_dir.split('-')[0]
    return os.path.join(dir, f'{prefix}-HUMAN-scores.csv')

def get_image_name_from_human_scores(dir):
    file_path = get_human_scores_file(dir)
    return os.path.basename(file_path)[:-len('-HUMAN-scores.csv')]

def get_human_times_file(dir):
    last_dir = os.path.basename(os.path.normpath(dir))
    prefix = last_dir.split('-')[0]
    return os.path.join(dir, f'{prefix}-HUMAN-times-taken.csv')

def get_IQM_file(dir):
    last_dir = os.path.basename(os.path.normpath(dir))
    prefix = last_dir.split('-')[0]
    return os.path.join(dir, f'{prefix}-IQM-scores.csv')

def get_original_image_file(dir):
    return os.path.join(dir, 'reference.png')

def get_original_unprocessed_image_file(dir):
    last_dir = os.path.basename(os.path.normpath(dir))
    prefix = last_dir.split('-')[0]
    return os.path.join(dir, f'{prefix}.png')

def get_image_processing_file(dir):
    return os.path.join(dir, 'transforms', 'processing.json')

def get_transform_params_file(dir):
    return os.path.join(dir, 'transforms', 'transform_params.pkl')

def get_transform_functions_file(dir):
    return os.path.join(dir, 'transforms', 'transform_functions.pkl')

''' other save helpers '''
def save_obj(pickle_path, trans):
    ''' save transforms as pickle file '''
    with open(pickle_path, 'wb') as file:
        pickle.dump(trans, file)

def load_obj(pickle_path):
    ''' load trans dict from pkl file '''
    if not os.path.exists(pickle_path):
        return None
    try:
        with open(pickle_path, 'rb') as file:
            trans = pickle.load(file)
        return trans
    except:
        return None
    
def get_JND_image_names(dir):
    ''' load the image names from a JND experiment '''
    images_dir = get_JND_ref_image_dir(dir)
    if not os.path.exists(images_dir):
        return None
    try:
        # get all file names in the directory
        return os.listdir(images_dir)
    except:
        return None
    
def get_JND_ref_image_dir(dir):
    return  os.path.join(dir, 'reference_images')

def get_JND_ref_image_unprocessed_dir(dir):
    return  os.path.join(dir, 'reference_images_unprocessed')


def save_df_as_csv(df, file, index=False):
    if os.path.exists(file):
        df_saved = pd.read_csv(file)
        df = pd.concat([df_saved, df])
    df.to_csv(file, index=index)


def save_and_merge_df_as_csv(df, file):
    '''df need to be indexed'''
    if os.path.exists(file):
        df_saved = pd.read_csv(file)
        index_name = df.index.name
        df = pd.merge(df.reset_index(), df_saved, how='outer')
        df.set_index(index_name, inplace=True)
    df.to_csv(file, index=True)


def save_and_merge_rm_duplicates_df_as_csv(df, file):
    '''save only new IQM rows'''
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


def get_JND_user_ID(dir):
    human_experiment_csv_file = get_human_scores_file(dir)
    if not os.path.exists(human_experiment_csv_file):
        return 1
    df = pd.read_csv(human_experiment_csv_file)
    # get the last user ID
    return df['User ID'].max() + 1

def save_JND_experiment_results(experiment_results,
                                save_dir,
                                IQM_scores_df=None):

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

    
def save_2AFC_experiment_results(trans_names, 
                                results_order, 
                                save_dir, 
                                times_taken=None, 
                                IQM_scores_df=None):
    '''save all the experiment reults as csvs'''
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
        print(IQM_scores_df)
        IQM_file = get_IQM_file(save_dir)
        save_and_merge_rm_duplicates_df_as_csv(IQM_scores_df, IQM_file)

    return human_experiment_csv_file

def save_json_dict(path, dict_):
    with open(path, 'w') as fp:
        json.dump(dict_, fp)

def load_json_dict(path):
    with open(path, 'r') as fp:
        return json.load(fp)

def make_name_for_trans(trans):
    # splitter = '-----'
    splitter = '<>'
    return f"{trans['transform_name']}{splitter}{trans['transform_value']}"
