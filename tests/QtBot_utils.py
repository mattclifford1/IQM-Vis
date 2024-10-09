# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
import pytest
from PyQt6 import QtTest, QtWidgets, QtCore
from pytestqt.plugin import QtBot
import IQM_Vis


def default_UI():
    app = IQM_Vis.make_UI(test=True)
    return app


# building and closing function of UI for testing
class BotTester:
    def __init__(self, get_UI=default_UI, wait_time=100, final_wait=False):
        self.get_UI = get_UI
        self.wait_time = wait_time
        self.final_wait = final_wait

    @pytest.fixture(scope='function')
    def build_IQM_Vis(self):
        # Setup
        test_window = self.get_UI()
        qtbotbis = QtBot(test_window.window)

        yield test_window, qtbotbis

        # Clean up
        QtTest.QTest.qWait(1000)

        # need to handle the closing dialog
        def handle_dialog():
            messagebox = QtWidgets.QApplication.activeWindow()
            yes_button = messagebox.button(
                QtWidgets.QMessageBox.StandardButton.Yes)
            qtbotbis.mouseClick(
                yes_button, QtCore.Qt.MouseButton.LeftButton, delay=1)

        QtCore.QTimer.singleShot(100, handle_dialog)

        test_window.window.main.close()
        # if self.final_wait:
        QtTest.QTest.qWait(1000)



