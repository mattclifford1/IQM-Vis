#!/bin/python3

'''Get the current version of package locally (github repo) - N.B. needs to be run from root of repo'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import sys

def get_version():
    info = {}
    with open(os.path.join('IQM_Vis', 'version.py')) as ver_file:
        exec(ver_file.read(), info)
    return info['__version__']

if __name__ == '__main__':
    sys.stdout.flush()
    print(get_version())
