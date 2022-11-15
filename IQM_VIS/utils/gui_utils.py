import sys
import matplotlib; matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt6.QtGui import QPixmap, QImage
# from PyQt5.QtWidgets import qApp
# from PyQt6.QtWidgets import QApplication
import numpy as np
from skimage.util import img_as_ubyte
from skimage.transform import resize
import cv2

'''
image helper functions
'''
def resize_im_to(np_array, size):
    down_im = resize(np_array, size)
    return img_as_ubyte(down_im)

def change_im(widget, im, resize=False):
    '''
    given a numpy image, changes the given widget Frame
    '''
    if im.shape[2] == 1:
        im = np.concatenate([im, im, im], axis=2)
    if resize:
        im = resize_im_to(im, resize)
    qimage = QImage(im,
                    im.shape[1],
                    im.shape[0],
                    im.shape[1]*im.shape[2],
                    QImage.Format.Format_RGB888)
                    # QImage.Format_RGB888)  # PyQt5
    pixmap = QPixmap(qimage)
    widget.setPixmap(pixmap)
    # QApplication.processEvents()   # force to change other UI wont respond

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

def get_metric_image_name(metric, image_name):
    return metric+get_image_pair_name(image_name)

def get_transformed_image_name(image_name):
    return 'T('+image_name+')'

def get_image_pair_name(image_name):
    return str((image_name, get_transformed_image_name(image_name)))


'''
matplotlib widget utils
'''
# Get a matplotlib canvas as a Qt Widget
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=3, dpi=100, polar=False):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111, polar=polar)
        super(MplCanvas, self).__init__(self.figure)
