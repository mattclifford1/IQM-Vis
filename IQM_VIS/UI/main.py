'''
main entry point to initialise the UI
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from IQM_VIS.UI import layout, widgets, images

class make_app(widgets, layout, images):
    def __init__(self, app,
                data_stores: list,
                transformations: dict,
                metrics_info_format='graph',    # graph or text
                metrics_avg_graph=False,
                metric_range_graph=True,
                image_display_size=175):
        super().__init__()
        self.app = app
        self.data_stores = data_stores
        self.transformations = transformations
        self.metrics_info_format = metrics_info_format
        self.metrics_avg_graph = metrics_avg_graph
        self.metric_range_graph = metric_range_graph
        self.image_display_size = image_display_size
        self.dataset = self._single_image_or_dataset()
        self.setWindowTitle('IQM-VIS')

        self.init_style()     # layout
        self.init_widgets()   # widgets
        self.init_layout()    # layout
        self.display_images() # images
        self.reset_sliders()  # widgets

    def _single_image_or_dataset(self):
        '''set whether dataset or single image used for data_store'''
        for data_store in self.data_stores:
            try:
                data_store[1]
                dataset_found = True
                self.data_num = 0
                data_store[self.data_num]  # return to initial image
            except:
                return False

        # calc what is the last data point in all the datasets
        max_length = 0
        for data_store in self.data_stores:
            try:
                length = len(data_store)
                if length > max_length:
                    max_length = length
            except:
                obj_name = data_store.__class__.__name__
                raise AttributeError(f'{obj_name} needs to have __len__ attribute to be a dataset')
        self.max_data_ind = max_length - 1
        return dataset_found
