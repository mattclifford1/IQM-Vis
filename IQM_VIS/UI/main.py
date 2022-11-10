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
                metrics_avg_graph=False
                ):
        super().__init__()
        self.app = app
        self.data_stores = data_stores
        self.transformations = transformations
        self.metrics_info_format = metrics_info_format
        self.metrics_avg_graph = metrics_avg_graph

        self.init_style()     # layout
        self.init_widgets()   # widgets
        self.init_layout()    # layout
        self.display_images() # images
        self.reset_sliders()  # widgets
