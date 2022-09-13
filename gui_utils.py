from PyQt6.QtGui import QPixmap, QImage
# from PyQt5.QtWidgets import qApp
from PyQt6.QtWidgets import QApplication
import numpy as np
from skimage.util import img_as_ubyte
from skimage.transform import resize
import image_utils

'''
image helper functions
'''
def resize_im_to(np_array, size):
    down_im = resize(np_array, size)
    return img_as_ubyte(down_im)

def change_im(widget, im, resize=False, return_qimage=False):
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
    QApplication.processEvents()   # force to change other UI wont respond
    if return_qimage:
        return qimage

def image_loader(im_path):
    return image_utils.load_image(im_path)


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
