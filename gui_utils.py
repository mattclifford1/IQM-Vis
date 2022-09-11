from PyQt6.QtGui import QPixmap, QImage
# from PyQt5.QtWidgets import qApp
from PyQt6.QtWidgets import QApplication
import numpy as np
from skimage.util import img_as_ubyte
from skimage.transform import resize


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
    # qApp.processEvents()   # force to change other UI wont respond
    QApplication.processEvents()   # force to change other UI wont respond
    if return_qimage:
        return qimage
