''' KODAK dataset '''
import os
import glob
import IQM_Vis

def run():
    # file_path = os.path.dirname(os.path.abspath(__file__))
    # dir = os.path.join(file_path,  'KODAK-dataset')

    dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'demo')
    image_list = glob.glob(os.path.join(dir, '*'))
    # remove and folders
    image_list = [f for f in image_list if os.path.isfile(f)]
    image_list.sort()

    metrs = IQM_Vis.metrics.get_all_metrics()
    metrs.pop('1-MS_SSIM')

    metr_ims = IQM_Vis.metrics.get_all_metric_images()
    metr_ims.pop('MSE')

    IQM_Vis.make_UI(transformations=IQM_Vis.transformations.get_all_transforms(),
                    image_list=image_list,
                    metrics=metrs,
                    metric_images=metr_ims,
                    restrict_options=3
                    )
    IQM_Vis.make_UI()

if __name__ == '__main__':
    run()