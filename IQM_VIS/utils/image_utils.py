'''
image helper functions
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import cv2
import numpy as np
from skimage.transform import resize


def load_image(image_path):
    '''
    load image as RGB float
    '''
    if not os.path.isfile(image_path):
        raise ValueError(f'Image file: {image_path} does not exist')
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image.astype(np.float32) / 255.0

def load_and_resize_image(image_path, side=128):
    '''
    resize image to longest side
    '''
    im = load_image(image_path)
    shape = im.shape
    if shape[0] > shape[1]:
        scale = shape[0]/side
        size = (side, int(shape[1]/scale))
    else:
        scale = shape[1]/side
        size = (int(shape[0]/scale), side)
    im = resize(im, size)
    return im

def load_and_resize_square_image(image_path, size=128):
    '''
    resize image to longest side
    '''
    im = load_image(image_path)
    if type(size) != tuple or type(size) != list:
        size = (size, size)
    im = resize(im, size)
    return im
