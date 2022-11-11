'''
Sample image transformations to get the user started with
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from skimage.transform import resize, rotate
import cv2
import numpy as np


def rotation(image, param):
    return rotate(image, param)

def blur(image, param):
    if param == 1:
        return image
    elif param > 0:
        blur_odd = (int(param/2)*2) + 1    # need to make kernel size odd
        image = cv2.GaussianBlur(image,(blur_odd, blur_odd), cv2.BORDER_DEFAULT)
        if len(image.shape) == 2:
            image = np.expand_dims(image, axis=2)
    return image

def zoom(image, param):
    return zoom_image(image, param)

def x_shift(image, param):
    return translate_image(image, param, 0)

def y_shift(image, param):
    return translate_image(image, 0, param)

def brightness(image, param):
    return np.clip(image + param, 0, 1)

def translate_image(image, x_shift, y_shift):
    ''' x and y shift in range (-1, 1)'''
    if x_shift == 0 and y_shift == 0:
        return image
    original_size = image.shape
    canvas = np.zeros(original_size, dtype=image.dtype)
    prop_x = int(original_size[1]*abs(x_shift))
    prop_y = int(original_size[0]*abs(y_shift))
    if y_shift >= 0 and x_shift >= 0:
        canvas[prop_y:,prop_x:,:] = image[:original_size[0]-prop_y,:original_size[1]-prop_x,:]
    elif y_shift < 0 and x_shift >= 0:
        canvas[:original_size[0]-prop_y,prop_x:,:] = image[prop_y-original_size[0]:,:original_size[1]-prop_x,:]
    elif y_shift >= 0 and x_shift < 0:
        canvas[prop_y:,:original_size[1]-prop_x,:] = image[:original_size[0]-prop_y,prop_x-original_size[1]:,:]
    elif y_shift < 0 and x_shift < 0:
        canvas[:original_size[0]-prop_y:,:original_size[1]-prop_x,:] = image[prop_y-original_size[0]:,prop_x-original_size[1]:,:]
    return canvas

def zoom_image(image, factor):
    ''' digital zoom of image: scale_factor the % to zoom in by (for square zoom only)
        0.5  = 2x zoom out
        1 = normal size
        2 = 2x zoom in'''
    original_size = image.shape
    new_size_x = int(original_size[0]/factor)
    new_size_y = int(original_size[1]/factor)
    if factor > 1:
        start_point_x = int((original_size[0] - new_size_x)/2)
        start_point_y = int((original_size[1] - new_size_y)/2)
        image = image[start_point_x:start_point_x+new_size_x,
                      start_point_y:start_point_y+new_size_y,
                      :]
    elif factor < 1:
        new_size = (new_size_x, new_size_y, original_size[2]) if len(original_size) == 3 else (new_size_x, new_size_y)
        start_point_x = int((new_size_x - original_size[0])/2)
        start_point_y = int((new_size_y - original_size[1])/2)
        zoomed_out = np.zeros(new_size, dtype=image.dtype)
        zoomed_out[start_point_x:start_point_x+original_size[0],
                   start_point_y:start_point_y+original_size[1],
                   :] = image
        image = zoomed_out

    return resize(image, original_size)
