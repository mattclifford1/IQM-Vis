'''
Utils for PyQt6 image, text and graph widgets
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import sys
try:
    from PyQt6.QtGui import QPixmap, QImage
    import matplotlib; matplotlib.use('Qt5Agg')
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
    from matplotlib.figure import Figure
    HEADLESS = False
except ImportError:
    import warnings
    warnings.warn('Can not load PyQt6 library - running IQM_VIS package in headless mode')
    HEADLESS = True
import numpy as np
from skimage.util import img_as_ubyte
from skimage.transform import resize
import cv2
from IQM_VIS.utils.image_utils import resize_to_longest_side

'''
image helper functions
'''
# def resize_im_to(np_array, size):
#     down_im = resize(np_array, size)
#     return img_as_ubyte(down_im)

def change_im(widget, im, resize=False):
    '''
    given a numpy image, changes the given widget Frame
    '''
    # first convert to three channel
    if len(im.shape) == 2:
        im = im[..., np.newaxis]
    if im.shape[2] == 1:
        im = np.concatenate([im, im, im], axis=2)
    if resize:
        im = resize_to_longest_side(im, resize)
        im = img_as_ubyte(im)
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

def get_transformed_image_name(data_store):
    return 'T('+data_store.get_transform_image_name()+')'

def get_image_pair_name(data_store):
    return str((data_store.get_reference_image_name(), get_transformed_image_name(data_store)))


'''
matplotlib widget utils
'''
if not HEADLESS:
    # Get a matplotlib canvas as a Qt Widget
    class MplCanvas(FigureCanvasQTAgg):
        def __init__(self, parent=None, width=5, height=3, dpi=100, polar=False):
            self.figure = Figure(figsize=(width, height), dpi=dpi)
            self.axes = self.figure.add_subplot(111, polar=polar)
            super(MplCanvas, self).__init__(self.figure)
