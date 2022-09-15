import sys
import matplotlib; matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

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

def get_metric_image_name(metric, image_pair):
    return metric+str(image_pair)


'''
matplotlib widget utils
'''
# Get a matplotlib canvas as a Qt Widget
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=2, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

# plot bar chart on matplotlib qt qidget
class bar_plotter:
    def __init__(self, bar_names, var_names, ax):
            self.bar_names = bar_names
            self.var_names = var_names
            self.ax = ax
            self.num_bars = len(self.bar_names)
            self.num_vars = len(self.var_names)
            self.bar_width = 1/(self.num_bars+1)
            self.bars = [np.arange(self.num_vars)]
            for i in range(1, self.num_bars):
                self.bars.append([x + self.bar_width for x in self.bars[i-1]])

    def plot(self, bar_name, var_values):
        i = self.bar_names.index(bar_name)
        self.ax.axes.bar(self.bars[i], var_values, width=self.bar_width, label=bar_name)

    def show(self):
        self.ax.axes.legend()
        self.ax.axes.set_xticks([r + self.bar_width for r in range(self.num_vars)], self.var_names)
        self.ax.draw()
