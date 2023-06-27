'''
utils for saving experiments, images and figures
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import json
import pickle
import pandas as pd

DEFAULT_SAVE_DIR = os.path.join(os.path.expanduser("~"), 'IQM-Vis-experiments')

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

    
def save_experiment_results(trans_names, results_order, base_file, times_taken=None, IQM_scores_df=None):
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
    human_experiment_csv_file = f"{base_file}-HUMAN-scores.csv"
    save_df_as_csv(df, human_experiment_csv_file, index=False)

    # save times taken
    if times_taken != None:
        times_file = f"{base_file}-HUMAN-times-taken.csv"
        data = {'mean time (seconds)': [sum(times_taken)/len(times_taken)],
                'total time (seconds)': [sum(times_taken)],
                'number of comparisons': [len(times_taken)],
                'individual times (seconds)': [str(times_taken)]}
        save_df_as_csv(pd.DataFrame.from_dict(data), times_file)

    # save IQM results
    if not isinstance(IQM_scores_df, type(None)):
        IQM_file = f"{base_file}-IQM-scores.csv"
        save_and_merge_df_as_csv(IQM_scores_df, IQM_file)

    return human_experiment_csv_file

def save_json_dict(path, dict_):
    with open(path, 'w') as fp:
        json.dump(dict_, fp)

def load_json_dict(path):
    with open(path, 'r') as fp:
        return json.load(fp)
