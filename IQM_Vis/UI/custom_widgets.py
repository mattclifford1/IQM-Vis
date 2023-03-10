from random import randint
import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QProgressBar

StyleSheet = '''
#RedProgressBar {
    text-align: center;
}
#RedProgressBar::chunk {
    background-color: #F44336;
}
#GreenProgressBar {
    min-height: 12px;
    max-height: 12px;
    border-radius: 6px;
}
#GreenProgressBar::chunk {
    border-radius: 6px;
    background-color: #009688;
}
#BlueProgressBar {
    border: 2px solid #2196F3;
    border-radius: 5px;
    background-color: #E0E0E0;
}
#BlueProgressBar::chunk {
    background-color: #2196F3;
    width: 10px;
    margin: 0.5px;
}
'''


class ProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.setValue(0)
        self.setGeometry(100, 50, 200, 30)
        # changing the color of process bar
        self.setStyleSheet("""QProgressBar {
            min-height: 12px;
            max-height: 12px;
            border-radius: 6px;
        }
        QProgressBar::chunk {
            border-radius: 6px;
            background-color: #009688;
        }""")
