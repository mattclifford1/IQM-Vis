# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
from __future__ import annotations

from PyQt6.QtWidgets import QWidget


def add_layout_to_tab(tab, layout, name: str) -> None:
    '''Add a layout as a named tab to a QTabWidget.

    Args:
        tab: The ``QTabWidget`` to add the tab to.
        layout: The layout to embed in the tab.
        name: Tab label text.
    '''
    _tab = QWidget()   # QTabWidget only accepts widgets not layouts so need to use this as a workaround
    _tab.setLayout(layout)
    tab.addTab(_tab, name)
