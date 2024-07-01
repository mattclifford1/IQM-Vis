# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

import pytest
from PyQt6 import QtTest, QtWidgets, QtCore
from pytestqt.plugin import QtBot, _close_widgets
import IQM_Vis
import threading


def get_UI():
    app = IQM_Vis.make_UI(test=True)
    return app


# building and closing function of UI for testing
@pytest.fixture
def build_IQM_Vis():

    test_window = get_UI()
    qtbotbis = QtBot(test_window.window)

    yield test_window, qtbotbis

    # need to handle the closing dialog
    def handle_dialog():
        messagebox = QtWidgets.QApplication.activeWindow()
        yes_button = messagebox.button(
            QtWidgets.QMessageBox.StandardButton.Yes)
        qtbotbis.mouseClick(
            yes_button, QtCore.Qt.MouseButton.LeftButton, delay=1)

    QtCore.QTimer.singleShot(100, handle_dialog)

    # test_window.window.quit()
    test_window.window.main.close()


def test_build_1(build_IQM_Vis):
    test_window, _ = build_IQM_Vis
    assert test_window.showing == True

