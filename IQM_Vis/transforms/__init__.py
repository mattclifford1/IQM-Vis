from IQM_Vis.transforms.effects import ( 
                         blur, 
                         brightness, 
                         binary_threshold, 
                         jpeg_compression, 
                         contrast,
                         hue,
                         saturation,
                         brightness_hsv)
from IQM_Vis.transforms.affine import (rotation, x_shift, y_shift, zoom_image)
from IQM_Vis.transforms.additive_noise import (salt_and_pepper_noise, Gaussian_noise, noise_hypersphere)

def get_all_transforms():
    '''
    Get all the available transformation/distortions alongside their recommended parameter ranges

    Returns:
        - all (dict): names, min, max, init_value and function for each transform
    '''
    all = {
        'brightness':{'min':-1.0, 'max':1.0, 'function':brightness},
        'contrast': {'min': 0.5, 'max': 2.5, 'init_value': 1.0, 'function': contrast},
        'hue': {'min': -0.5, 'max': 0.5, 'function': hue},
        'saturation': {'min': -0.5, 'max': 0.5, 'function': saturation},
        # 'brightness_hsv': {'min': -1.0, 'max': 1, 'function': brightness_hsv},
        'blur': {'init_value': 1, 'min': 1, 'max': 41, 'normalise': 'odd', 'function': blur},
        'Gaussian Noise': {'init_value': 0.0, 'min': 0.0, 'max': 0.5, 'function': Gaussian_noise()},
        'noise hypersphere': {'init_value': 0.0, 'min': 0.0, 'max': 5.0, 'function': noise_hypersphere()},
        'salt pepper': {'init_value': 0.0, 'min': 0.0, 'max': 0.05, 'function': salt_and_pepper_noise},
        'jpg comp.':{'init_value':101, 'min':1, 'max':101, 'function':jpeg_compression},
        'rotation':{'min':-180, 'max':180, 'function':rotation},
        'x_shift': {'min':-0.1, 'max':0.1, 'function':x_shift, 'init_value': 0.0},
        'y_shift': {'min':-0.1, 'max':0.1, 'function':y_shift, 'init_value': 0.0},
        'zoom':    {'min': 0.8, 'max':1.2, 'function':zoom_image, 'init_value': 1.0, 'num_values':21},
        # 'threshold':{'min':-40, 'max':40, 'function':binary_threshold},
    }
    return all
