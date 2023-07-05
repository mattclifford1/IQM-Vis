''' KODAK dataset '''
import os
import glob
import IQM_Vis

def run():
    file_path = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(file_path,  'KODAK-dataset')
    image_list = glob.glob(os.path.join(dir, '*'))
    # remove and folders
    image_list = [f for f in image_list if os.path.isfile(f)]
    image_list.sort()

    metrs = IQM_Vis.metrics.get_all_metrics()
    metrs.pop('1-MS_SSIM')
    data = IQM_Vis.dataset_holder(image_list,
                                  metrs,
                                #   IQM_Vis.metrics.get_all_metric_images()
                                  )


    IQM_Vis.make_UI(data,
                    IQM_Vis.transformations.get_all_transforms(),
                    restrict_options=3
                    )
    IQM_Vis.make_UI()

if __name__ == '__main__':
    run()
