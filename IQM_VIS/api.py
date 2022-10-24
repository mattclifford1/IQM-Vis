import sys
from PyQt6.QtWidgets import QApplication
from IQM_VIS.UI.main import make_app

def make_UI(image_paths,
            metrics_dict,
            metrics_image_dict,
            transformations,
            metrics_info_format='graph'):
    app = QApplication(sys.argv)
    window = make_app(app,
                      image_paths,
                      metrics_dict,
                      metrics_image_dict,
                      transformations,
                      metrics_info_format=metrics_info_format)
    sys.exit(app.exec())
