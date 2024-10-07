'''
affine (geometric) transformations
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
import numpy as np
from skimage.transform import resize, rotate


def rotation(image, angle=0):
    '''Rotate an image around its centre. Uses skimage.transform.rotate. Areas
    that are rotated beyond the image are filled in with black pixel values

    Args:
        image (np.array): image to be rotated
        angle (float): amount of rotation in degrees (Defaults to 0)

    Returns:
        image (np.array): rotated image
    '''
    if angle == 0:
        return image
    return np.clip(rotate(image, angle, order=3), 0, 1)


def x_shift(image, x_shift=0):
    '''Translate image horizontally

    Args:
        image (np.array): image to be shifted
        x_shift (float): shift proportion of the image in the range (-1, 1).
                         (Defaults to 0)

    Returns:
        image (np.array): shifted image
    '''
    if x_shift == 0:
        return image
    return _translate_image(image, x_shift, 0)


def y_shift(image, y_shift=0):
    '''Translate image vertically

    Args:
        image (np.array): image to be shifted
        y_shift (float): shift proportion of the image in the range (-1, 1).
                         (Defaults to 0)

    Returns:
        image (np.array): shifted image
    '''
    if y_shift == 0:
        return image
    return _translate_image(image, 0, y_shift)


def _translate_image(image, x_shift=0, y_shift=0):
    '''Translate image vertically

    Args:
        image (np.array): image to be shifted
        x_shift (float): shift proportion of the image in the range (-1, 1).
                         (Defaults to 0)
        y_shift (float): shift proportion of the image in the range (-1, 1).
                         (Defaults to 0)

    Returns:
        image (np.array): shifted image
    '''
    if x_shift == 0 and y_shift == 0:
        return image
    original_size = image.shape
    canvas = np.zeros(original_size, dtype=image.dtype)
    prop_x = int(original_size[1]*abs(x_shift))
    prop_y = int(original_size[0]*abs(y_shift))
    # make sure we dont go off the canvas
    if original_size[1] - prop_x < 1 or original_size[0] - prop_y < 1:
        return canvas
    if y_shift >= 0 and x_shift >= 0:
        canvas[prop_y:, prop_x:, :] = image[:original_size[0] -
                                            prop_y, :original_size[1]-prop_x, :]
    elif y_shift < 0 and x_shift >= 0:
        canvas[:original_size[0]-prop_y, prop_x:, :] = image[prop_y -
                                                             original_size[0]:, :original_size[1]-prop_x, :]
    elif y_shift >= 0 and x_shift < 0:
        canvas[prop_y:, :original_size[1]-prop_x,
               :] = image[:original_size[0]-prop_y, prop_x-original_size[1]:, :]
    elif y_shift < 0 and x_shift < 0:
        canvas[:original_size[0]-prop_y:, :original_size[1]-prop_x,
               :] = image[prop_y-original_size[0]:, prop_x-original_size[1]:, :]
    return np.clip(canvas, 0, 1)


def zoom_image(image, scale_factor=1):
    '''digital zoom of image

    Args:
        image (np.array): image to be zoomed
        scale_factor (float): the percentage to zoom in by (for square zoom only).
                              0.5  = 2x zoom out
                              1 = normal size
                              2 = 2x zoom in
                              (Defaults to 1)

    Returns:
        image (np.array): zoomed image
    '''
    if scale_factor == 1:
        return image
    original_size = image.shape
    new_size_x = int(original_size[0]/scale_factor)
    new_size_y = int(original_size[1]/scale_factor)
    if scale_factor > 1:
        start_point_x = int((original_size[0] - new_size_x)/2)
        start_point_y = int((original_size[1] - new_size_y)/2)
        image = image[start_point_x:start_point_x+new_size_x,
                      start_point_y:start_point_y+new_size_y,
                      :]
    elif scale_factor < 1:
        new_size = (new_size_x, new_size_y, original_size[2]) if len(
            original_size) == 3 else (new_size_x, new_size_y)
        start_point_x = int((new_size_x - original_size[0])/2)
        start_point_y = int((new_size_y - original_size[1])/2)
        zoomed_out = np.zeros(new_size, dtype=image.dtype)
        zoomed_out[start_point_x:start_point_x+original_size[0],
                   start_point_y:start_point_y+original_size[1],
                   :] = image
        image = zoomed_out

    return np.clip(resize(image, original_size), 0, 1)
