from PyQt6.QtWidgets import QWidget


def add_layout_to_tab(tab, layout, name):
    _tab = QWidget()   # QTabWidget only accepts widgets not layouts so need to use this as a workaround
    _tab.setLayout(layout)
    tab.addTab(_tab, name)
