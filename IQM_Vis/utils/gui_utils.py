'''
Utils for PyQt6 image, text and graph widgets
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
try:
    from PyQt6.QtGui import QPixmap, QImage
    import matplotlib; matplotlib.use('Qt5Agg')
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
    from matplotlib.figure import Figure
    HEADLESS = False
except ImportError:
    import warnings
    warnings.warn('Can not load PyQt6 library - running IQM_Vis package in headless mode')
    HEADLESS = True
import numpy as np
from skimage.util import img_as_ubyte
from skimage.transform import resize
from IQM_Vis.utils.image_utils import resize_to_longest_side, calibrate_brightness

'''
image helper functions
'''
# def resize_im_to(np_array, size):
#     down_im = resize(np_array, size)
#     return img_as_ubyte(down_im)


def change_im(widget, im, resize=False, rgb_brightness=250, display_brightness=250):
    '''
    given a numpy image, changes the given widget Frame
    '''
    # clip image to safe bounds
    im = np.clip(im, 0, 1)
    # convert to three channel
    if len(im.shape) == 2:
        im = im[..., np.newaxis]
    if im.shape[2] == 1:
        im = np.concatenate([im, im, im], axis=2)
    if resize:
        im = resize_to_longest_side(im, resize)
        im = img_as_ubyte(im)
    im = calibrate_brightness(im, rgb_brightness, display_brightness)
    qimage = QImage(im,
                    im.shape[1],
                    im.shape[0],
                    im.shape[1]*im.shape[2],
                    QImage.Format.Format_RGB888)
    pixmap = QPixmap(qimage)
    widget.setPixmap(pixmap)

'''
text utils
'''

def str_to_len(string, length=5, append_char='0', plus=False):
    # cut string to length, or append character to make to length
    if string[0] !=  '-' and plus == True:
        string = '+' + string
    if len(string) > length:
        string = string[:length]
    elif len(string) < length:
        string = string + append_char*(length-len(string))
    return string

def get_metric_image_name(metric, data_store):
    return metric+get_image_pair_name(data_store)

def get_trans_dict_from_str(trans_str, return_dict=False):
    # determine which experiment formatting we are using
    splitter = '='
    if len(trans_str.split(splitter)) == 1:
        splitter = '-----'   # legacy code experiment format - illegible with negative numbers
    if len(trans_str.split(splitter)) == 1:
        splitter = '::'   # legacy code experiment format - didn't work with windows filesystem
    
    trans = splitter.join(trans_str.split(splitter)[:-1])
    # error with duplicated columns in csv with pandas load
    try:
        trans_value = float(trans_str.split(splitter)[-1])   # value is last part of string
    except ValueError:
        error_value = trans_str.split(splitter)[-1]
        # remove the '.1' etc appended by pandas
        value = '.'.join(error_value.split('.')[:-1])
        trans_value = float(value)
    if return_dict == True:
        return {trans: trans_value}
    else:
        return trans, trans_value

def get_transformed_image_name(data_store):
    return 'T('+data_store.get_image_to_transform_name()+')'

def get_image_pair_name(data_store):
    return str((data_store.get_reference_image_name(), get_transformed_image_name(data_store)))

def get_resolutions(data_store):
    ref = data_store.get_reference_image().shape
    trans = data_store.get_image_to_transform().shape
    return {'reference': f'{ref[0]}x{ref[1]}',
            'transform': f'{trans[0]}x{trans[1]}'}


'''
matplotlib widget utils
'''
if not HEADLESS:
    # Get a matplotlib canvas as a Qt Widget
    class MplCanvas(FigureCanvasQTAgg):
        def __init__(self, size=(3.5, 3.5), dpi=100, polar=False):
            self.figure = Figure(figsize=size)  # , dpi=dpi)
            self.axes = self.figure.add_subplot(111, polar=polar)
            super(MplCanvas, self).__init__(self.figure)
