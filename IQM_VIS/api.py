import sys
import warnings

try:
    from PyQt6.QtWidgets import QApplication
    from IQM_VIS.UI.main import make_app
except ImportError:
    warnings.warn('Can not load PyQt6 library - running IQM_VIS package in headless mode')

class make_UI:
    def __init__(self, data_store,
                       transformations: dict,
                       metrics_info_format: str='graph',
                       metrics_avg_graph: bool=False):
        self.data_store = data_store
        self.transformations = transformations
        self.metrics_info_format = metrics_info_format
        self.metrics_avg_graph = metrics_avg_graph
        self.show()

    def show(self):
        self._check_inputs()
        app = QApplication(sys.argv)
        window = make_app(app,
                          self.data_store,
                          self.transformations,
                          metrics_info_format=self.metrics_info_format,
                          metrics_avg_graph=self.metrics_avg_graph)
        sys.exit(app.exec())

    def _check_inputs(self):
        should_be_dict = [self.transformations]
        for item in should_be_dict:
            if type(item) != dict:
                var_name = f'{item=}'.split('=')[0]
                raise TypeError('make_UI input: '+var_name+' should be a dictionary not '+str(type(item)))
            elif len(item.keys()) == 0:
                var_name = f'{item=}'.split('=')[0]
                warnings.warn('make_UI input: '+var_name+' is empty')

        #### write check for data store as list


        if type(self.metrics_info_format) != str:
            var_name = f'{self.metrics_info_format=}'.split('=')[0]
            raise TypeError('make_UI input: '+var_name+' should be a string not '+str(type(self.metrics_info_format)))
        if type(self.metrics_avg_graph) != bool:
            var_name = f'{self.metrics_info_format=}'.split('=')[0]
            raise TypeError('make_UI input: '+var_name+' should be a bool not '+str(type(self.metrics_info_format)))
