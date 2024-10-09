''' KODAK dataset '''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

import IQM_Vis
from IQM_Vis.examples.KODAK_dataset import KODAK_IMAGES

def run():
    metrs = IQM_Vis.metrics.get_all_metrics()
    if '1-MS_SSIM' in metrs:
      metrs.pop('1-MS_SSIM')
    data = IQM_Vis.dataset_holder(KODAK_IMAGES,
                                  metrs,
                                #   IQM_Vis.metrics.get_all_metric_images()
                                  )


    IQM_Vis.make_UI(data,
                    IQM_Vis.transforms.get_all_transforms(),
                    restrict_options=3
                    )
    IQM_Vis.make_UI()

if __name__ == '__main__':
    run()
