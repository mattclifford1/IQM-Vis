import os
import glob
import numpy as np
import torch
import IQM_Vis

from PIL import Image
from PIL.TiffTags import TAGS



'''Textures calibrated image loader'''
def load_and_calibrate_image(file, max_luminance=200, size=256):
    # Calculate max luminance value in the whole dataset
    img = Image.open(file)
    meta_dict = {TAGS[key] : img.tag[key] for key in img.tag_v2}
    img = np.array(img).astype(np.float64)
    lms = correct(img, meta_dict)

    # Get each point in rgb space to visualise the colour in RGB
    # XYZ -> LMS
    Mxyzlms = np.array([ # Bradford LMS transform
        [0.8951000, 0.2664000, -0.1614000],
        [-0.7502000, 1.7135000, 0.0367000],
        [0.0389000, -0.0685000, 1.0296000]])
    # LMS -> XYZ
    Mlmsxyz = np.linalg.inv(Mxyzlms)

    # RGB -> XYZ
    Mng2xyz = np.array([[69.1661, 52.4902, 46.6052],
                        [39.0454, 115.8404, 16.3118],
                        [3.3467, 12.6700, 170.1090]])
    #XYZ -> RGB
    Mxyz2ng = np.linalg.inv(Mng2xyz)

    # Convert LMS -> XYZ and scale values for max luminance default: 200 cd/m^2
    xyz_corrected = (lms @ Mlmsxyz.T)/np.max(lms[:, 0]) * max_luminance

    # Convert XYZ -> RGB
    rgb_corrected = np.clip(xyz_corrected @ Mxyz2ng.T, 0.0, 1.0)
    rgb_small = IQM_Vis.utils.resize_to_longest_side(rgb_corrected, side=size)
    return rgb_small

''' util for calibrating images'''
# camera correction and coversation into LMS colourspace
def correct(img, meta_dict, greycale=True):
    if 'merry' in meta_dict['ImageDescription'][0]:
        T = np.array([
            [0.428443253, 0.495562896, 0.075993851],
            [0.243026144, 0.614128681, 0.142845175],
            [0.155766424, 0.132343175, 0.711890401]])
        a_R = 7.320565961
        a_G = 12.0579051
        a_B = 10.6112984
        b = 1.008634316
    elif 'pippi' in meta_dict['ImageDescription'][0]:
        T = np.array([
            [0.431088433, 0.494438389, 0.074473178],
            [0.245488691, 0.614786761, 0.139724548],
            [0.166472303, 0.124487321, 0.709040376]])
        a_R = 5.562441185
        a_G = 8.876002262
        a_B = 7.233814813
        b = 1.009696031
    II = np.zeros_like(img)
    II[:, :, 0] = a_R*(b**img[:, :, 0]-1)
    II[:, :, 1] = a_G*(b**img[:, :, 1]-1)
    II[:, :, 2] = a_B*(b**img[:, :, 2]-1)
    exposure_time = meta_dict['ImageDescription'][0].split('-')[-1]
    try:
        exposure_time = np.float64(exposure_time)
    except:
        return None
    II = II / np.float64(exposure_time)
    II = np.reshape(np.reshape(II, (np.prod(II.shape[0:2]), 3), order='F')@T.T, (II.shape), order='F')
    return II

def run():
    # metrics functions must return a single value
    metric = {'DISTS': IQM_Vis.IQMs.DISTS(),
              'MAE': IQM_Vis.IQMs.MAE(),
              '1-SSIM': IQM_Vis.IQMs.SSIM(),
              '1-MS_SSIM': IQM_Vis.IQMs.MS_SSIM(),
              'NLPD': IQM_Vis.IQMs.NLPD(),
            #   'LPIPS': IQM_Vis.IQMs.LPIPS(),
              }

    # metrics images return a numpy image - dont include any for this example
    metric_images = {}

    # make dataset list of images
    files = sorted(glob.glob('/home/matt/datasets/Textures/*'))
    data = IQM_Vis.dataset_holder(files,
                                  metric,
                                  metric_images,
                                  load_and_calibrate_image,
                                  image_post_processing=IQM_Vis.utils.image_utils.crop_centre)

    # define the transformations
    transformations = {
        'rotation':{'min':-10, 'max':10, 'function':IQM_Vis.transforms.rotation},    # normal input
        'x_shift': {'min':-0.1, 'max':0.1, 'function':IQM_Vis.transforms.x_shift, 'init_value': 0.0},
        'y_shift': {'min':-0.1, 'max':0.1, 'function':IQM_Vis.transforms.y_shift, 'init_value': 0.0},
        'zoom':    {'min': 0.8, 'max':1.2, 'function':IQM_Vis.transforms.zoom_image, 'init_value': 1.0},  # requires non standard slider params
        'brightness':{'min':-1.0, 'max':1.0, 'function':IQM_Vis.transforms.brightness},   # normal but with float
        'contrast': {'min': 0.5, 'max': 2.5, 'init_value': 1.0, 'function': IQM_Vis.transforms.contrast},
        'hue': {'min': -0.5, 'max': 0.5, 'function': IQM_Vis.transforms.hue},
        'saturation': {'min': -0.5, 'max': 0.5, 'function': IQM_Vis.transforms.saturation},
        'jpg compr':{'init_value':101, 'min':1, 'max':101, 'function':IQM_Vis.transforms.jpeg_compression},
        'blur':{'min':1, 'max':41, 'normalise':'odd', 'function':IQM_Vis.transforms.blur},  # only odd ints
        # 'threshold':{'min':-40, 'max':40, 'function':IQM_Vis.transforms.binary_threshold},
               }
    # define any parameters that the metrics need (names shared across both metrics and metric_images)
    ssim_params = {'sigma': {'min':0.25, 'max':5.25, 'init_value': 1.5},  # for the guassian kernel
                   # 'kernel_size': {'min':1, 'max':41, 'normalise':'odd', 'init_value': 11},  # ignored if guassian kernel used
                   'k1': {'min':0.01, 'max':0.21, 'init_value': 0.01},
                   'k2': {'min':0.01, 'max':0.21, 'init_value': 0.03}}

    # use the API to create the UI
    IQM_Vis.make_UI(data,
                    transformations,
                    metric_params=ssim_params)


if __name__ == '__main__':
    run()
