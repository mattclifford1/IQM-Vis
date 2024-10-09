# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

import IQM_Vis

import sys
import os
sys.path.append(os.path.abspath('..'))
from tests.QtBot_utils import BotTester

def get_UI():
    app = IQM_Vis.make_UI(test=True)
    return app


build_IQM_Vis = BotTester(get_UI=get_UI).build_IQM_Vis


def test_build_1(build_IQM_Vis):
    test_window, _ = build_IQM_Vis
    assert test_window.showing == True

