from .transforms import rotation, blur, x_shift, y_shift, brightness, zoom_image, binary_threshold, jpeg_compression

def get_all_transforms():
    all = {
        'jpg comp.':{'init_value':100, 'min':1, 'max':100, 'function':jpeg_compression},
        'blur':{'min':1, 'max':41, 'normalise':'odd', 'function':blur},
        'rotation':{'min':-180, 'max':180, 'function':rotation},
        'x_shift': {'min':-0.1, 'max':0.1, 'function':x_shift, 'init_value': 0.0},
        'y_shift': {'min':-0.1, 'max':0.1, 'function':y_shift, 'init_value': 0.0},
        'zoom':    {'min': 0.8, 'max':1.2, 'function':zoom_image, 'init_value': 1.0, 'num_values':21},
        'brightness':{'min':-1.0, 'max':1.0, 'function':brightness},
        # 'threshold':{'min':-40, 'max':40, 'function':binary_threshold},
    }
    return all
