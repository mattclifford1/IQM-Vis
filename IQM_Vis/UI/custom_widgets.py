''' Custom SubClasses of PyQt6 widget to extent to the required functionality '''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QProgressBar, QLabel


class ClickLabel(QLabel):
    ''' add a click mousePressEvent event to label (so can click on images) '''
    clicked = pyqtSignal(str, str)

    def __init__(self, name='clickable label'):
        super().__init__()
        self.name = name

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName(), self.name)


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
