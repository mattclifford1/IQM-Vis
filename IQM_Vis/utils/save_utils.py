'''
utils for saving experiments, images and figures
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
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
    
def save_experiment_results(trans_names, results_order, file):
    # make HIQM scores
    results = {}
    for i, trans_name in enumerate(results_order):
        results[str(trans_name)] = [(i+1) / len(results_order)]

    # make df
    df = pd.DataFrame.from_dict(results)
    # re order
    df = df[trans_names]

    # save results
    if os.path.exists(file):
        df_saved = pd.read_csv(file)
        df = pd.concat([df_saved, df])
    df.to_csv(file, index=False)
