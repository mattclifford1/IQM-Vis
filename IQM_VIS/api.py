import sys
from dataclasses import dataclass
import warnings

from PyQt6.QtWidgets import QApplication

from IQM_VIS.UI.main import make_app


def make_UI(*args, metrics_info_format='graph'):
    ui = UI_wrapper(*args, metrics_info_format)
    ui.show()


@dataclass
class UI_wrapper:
    image_paths: dict
    metrics_dict: dict
    metrics_image_dict: dict
    transformations: dict
    metrics_info_format: str='graph'

    def show(self):
        self._check_inputs()
        app = QApplication(sys.argv)
        window = make_app(app,
                          self.image_paths,
                          self.metrics_dict,
                          self.metrics_image_dict,
                          self.transformations,
                          metrics_info_format=self.metrics_info_format)
        sys.exit(app.exec())

    def _check_inputs(self):
        should_be_dict = [self.image_paths, self.metrics_dict, self.metrics_image_dict]
        for item in should_be_dict:
            if type(item) != dict:
                var_name = f'{item=}'.split('=')[0]
                raise TypeError('Input: '+var_name+' should be a dictionary not '+str(type(item)))
            elif len(item.keys()) == 0:
                var_name = f'{item=}'.split('=')[0]
                warnings.warn('Input: '+var_name+' is empty')
        if type(self.metrics_info_format) != str:
            var_name = f'{self.metrics_info_format=}'.split('=')[0]
            raise TypeError('Input: '+var_name+' should be a string not '+str(type(self.metrics_info_format)))
