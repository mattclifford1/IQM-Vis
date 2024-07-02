# tests/conftest.py

import pytest
from PyQt6.QtWidgets import QApplication
# import matplotlib

# # Use a different backend to avoid conflicts
# matplotlib.use('Agg')


@pytest.fixture(scope="session", autouse=True)
def qapp():
    """
    Ensure there's a QApplication instance running.
    This fixture is automatically used for each test session.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Properly quit the application after the tests
    app.quit()
